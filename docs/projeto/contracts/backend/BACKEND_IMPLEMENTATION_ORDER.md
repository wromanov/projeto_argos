# BC-02 — Ordem de implementação dos contratos backend

```text
STATUS = ACTIVE / BC-02 CONTRACT READINESS
BASE_SHA = 2ab1c8a05bdc3e541c34e15a7c2931eb1137459f
DEFAULT_IMPLEMENTER = LUNA
IMPLEMENTATION_AUTHORIZED_BY_THIS_DOCUMENT = NO
REAL_CAMERA_ACCESS = NO
HOMOLOGATION = NO
PRODUCTION = NO
```

Este documento fecha a ordem **técnica** para implementação local. Cada slice
precisa de autorização de execução própria. `IMPLEMENTATION_READY` significa
que Luna pode implementar o contrato sem projetar arquitetura; não significa
que a validação em equipamento, rede ou PostgreSQL ocorreu. Os critérios de
aceite normativos ficam no contrato de cada slice.

## 1. Fronteiras e precedência

Instrução humana vigente prevalece sobre o baseline BC-00. Os quatro perfis e
os fluxos RTSP/health adjudicados no BC-02 são vinculantes. ADR-019 preserva
separação web/worker/captura; ADR-020 preserva UNKNOWN/ONLINE/OFFLINE,
anti-flapping e histórico; ADR-021 preserva destino IPv4 autorizado, segredo
separado, allowlist e egress. A URI RTSP é **configuração persistida por
Técnico/Administrador**, não alvo fornecido no momento do probe. Seu host deve
ser exatamente o IPv4 canônico de `Camera.ip`; userinfo, hostname/DNS, fragmento
e query secreta são rejeitados. O path é override privilegiado permitido pelo
perfil, sujeito à mesma validação de destino/porta. Se o path contiver segredo,
ele não é aceito como URI pública; o equipamento requer contrato de credencial
adequado antes da integração. A URI exibida ao Operador não contém credencial.

O teste manual A→B→C→D é diagnóstico isolado: não grava `EstadoMonitoramento`,
streak, `TransicaoEstadoMonitoramento` ou `Indisponibilidade`. Somente uma
tentativa automática contratada que chegue a **D PASS, com frame/mídia válida**,
pode produzir `ProbeResult.SUCCESS` para o reducer. Falha A/B/C/D isolada
continua sujeita à classificação/confirmacão de ADR-020; erro de auth,
configuração, policy, codec ou decoder é neutro, nunca OFFLINE direto.

## 2. DAG de slices

```text
BC-AUTH -> CAM-INT-01
BC-AUTH + CAM-INT-01 -> CAM-INT-02 -> CAM-INT-02-R1
CAM-INT-01 -> CAM-INT-06
CAM-INT-01 + CAM-INT-02 + CAM-INT-02-R1 + CAM-INT-06 + CAM-INT-07
    ├-> CAM-INT-03 -> CAM-INT-05 -> CAM-HEALTH
    └-> CAM-INT-04
BC-AUTH + CAM-INT-03 + CAM-INT-04 + CAM-INT-06 -> IMG-CAP
MON-OBS + CAM-INT-05 + CAM-HEALTH + core MON -> MON-WORKER
BC-AUTH / backend contracts -> UI P5 integration contracts
```

Dependências fortes: CAM-INT-03 e 04 exigem perfil, credencial e policy de
destino fechados; CAM-INT-05 integra os resultados em estágios; IMG-CAP exige
fontes de captura validadas e permissão; MON-WORKER usa o core de monitoramento
existente, observabilidade e o adapter contratado. CAM-INT-06 é framework de
compatibilidade; dados reais permanecem validação externa. Em runtime,
capability ausente/UNVERIFIED impede monitoramento automático e captura, mas
Técnico/Admin pode executar teste manual controlado para colher evidência, com
allowlist e autorização. O teste não declara suporte nem muda health.

Adjacência normativa do DAG local (`[]` = nenhum predecessor novo; os cinco
contratos MON de core já estão implementados):

```text
BC-AUTH       <- []
MON-OBS       <- []
CAM-INT-07    <- []
CAM-INT-01    <- [BC-AUTH]
CAM-INT-02    <- [BC-AUTH, CAM-INT-01]
CAM-INT-02-R1 <- [CAM-INT-02]
CAM-INT-06    <- [CAM-INT-01]
CAM-INT-03    <- [CAM-INT-01, CAM-INT-02, CAM-INT-02-R1, CAM-INT-06, CAM-INT-07]
CAM-INT-04    <- [CAM-INT-01, CAM-INT-02, CAM-INT-02-R1, CAM-INT-06, CAM-INT-07]
CAM-INT-05    <- [CAM-INT-03]
CAM-HEALTH    <- [CAM-INT-05]
IMG-CAP       <- [BC-AUTH, CAM-INT-03, CAM-INT-04, CAM-INT-06]
MON-WORKER    <- [MON-OBS, CAM-INT-05, CAM-HEALTH]
```

CAM-INT-07 está na wave 2 por conveniência de integração com o schema da
configuração; seu núcleo de policy é independente e pode começar antes em
worktree próprio. CAM-INT-02 e CAM-INT-06 são serializados por colisão de
`cameras/models.py`/migrations, embora o DAG lógico não imponha essa ordem.

### 2.1. CAM-INT-02-R1 — reconciliação do gap operacional (2026-10-02)

CAM-INT-02 publicou custódia/lifecycle/reveal, sem API pública de execução.
Adicionar a sub-slice `CAM-INT-02-R1 — Runtime Credential Resolution Boundary`,
cujo [contrato](camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md)
fecha o serviço interno, value object, falhas, autorização, testes e aceite.
Não transferir crypto aos adapters. A dependência HTTP é factual: Basic/Digest
já está contratado. CAM-INT-06 e CAM-INT-07 permanecem predecessores
independentes dos adapters, sem arco novo vindo de R1.

```text
CAM-INT-02 -> CAM-INT-02-R1 -> CAM-INT-03
                          -> CAM-INT-04
CAM_INT_02_R1_STATUS = IMPLEMENTATION_READY / NOT_IMPLEMENTED
CAM_INT_02_R1_READY_NOW = YES / CAM-INT-02 published; separate authorization required
CAM_INT_03_STATUS = PAUSED_ARCHITECTURAL_DEPENDENCY
CAM_INT_03_READY_NOW = NO / CAM-INT-02-R1 not published
CAM_INT_04_READY_NOW = NO / CAM-INT-02-R1 not published
CAM_INT_04_EXECUTION_STATUS = LOCAL_CHANGES_OBSERVED / not adjudicated as paused or complete
```

Readiness técnica imediata de CAM-INT-03/04 descrita nos checkpoints anteriores
à descoberta do gap é histórica e supersedida por este gate. Antes de retomada
ou integração dos consumers, R1 precisa estar implementada, integrada,
validada e publicada; autorização existente de cada consumer deve ser
revalidada na retomada. Lanes existentes e sua baseline são preservadas.

## 3. Waves e ownership

| Wave | Slices | Paralelo | Predecessores | Arquivos compartilhados / regra |
|---|---|---|---|---|
| 1 | BC-AUTH | Não | Core Django existente | Dono exclusivo de `usuarios/management/commands/configurar_perfis_argos.py`, `usuarios/admin_security.py` e alteração de permissões em `cameras/models.py`; migration de permissions se necessária |
| 2 | CAM-INT-01, CAM-INT-07, MON-OBS | Sim, em worktrees distintos | Wave 1 para CAM-INT-01; nenhum para policy e observability | CAM-INT-01 possui `cameras/models.py` e sua migration; CAM-INT-07 possui `cameras/integracao/target_policy.py`; MON-OBS possui `cameras/monitoramento/observability.py`. `PROJECT_STATE`, mapa, roadmap e sprints não são propriedade de slices |
| 3 | CAM-INT-02, CAM-INT-06 | **Não simultaneamente**: subordem CAM-INT-02 → CAM-INT-06 | Wave 2 | Ambos exigem schema em `cameras/models.py` e migration; executar em sequência na mesma linha de integração |
| 3-R1 | CAM-INT-02-R1 | Execução isolada antes dos consumers | CAM-INT-02 publicada | Possui `cameras/integracao/credentials.py` e novo `cameras/test_camera_credential_resolution.py`; models/provider/configuration são referências read-only; sem migration |
| 4 | CAM-INT-03 e CAM-INT-04 | Sim, em worktrees distintos, após R1 publicada | Waves 2–3 e 3-R1 | RTSP possui `cameras/integracao/rtsp/`; HTTP possui `cameras/integracao/http_snapshot/`; não editar credentials/crypto/provider, o mesmo service, model ou migration. Integração de configuração comum pertence à etapa de reconciliação posterior |
| 5 | CAM-INT-05/CAM-HEALTH | Não | Wave 4 | Diagnóstico cria `CameraHealthSnapshot` em `cameras/models.py` e migration própria; leitura health integra depois do schema |
| 6 | IMG-CAP e MON-WORKER | Sim, em worktrees distintos | Wave 5; MON-OBS e core MON | Captura possui `cameras/models.py`, migration, `cameras/imagens/` e command de captura; worker possui `cameras/monitoramento/` e command de monitoramento. Views/URLs comuns só na integração sequencial |
| 7 | Validação integrada local | Não | Waves 1–6 | Revisar permissões, fake/real boundary, migrations, migrations inversas, regressões focais e ausência de side effects de teste manual |
| 8 | PROD-PERSIST, PROD-TOPO, PROD-CAP | Não é implementação local desta fila | Decisões/infraestrutura de produção e gate próprio | PostgreSQL, rede, câmeras, egress, storage, restore, carga e homologação reais |

As waves descrevem precedência técnica, não autorização para criar branch,
worktree, executar ou integrar. Cada worktree paralelo parte do SHA integrado
mais recente após predecessores, com branch `codex/bc02-<id>` ou nome aprovado
na atividade de implementação. Não usar o `BASE_SHA` acima se `master` tiver
avançado. Um único integrador reconcilia migrations, arquivos comuns e
continuidade depois das slices; nenhuma slice paralela altera
`PROJECT_STATE.md`, `ACTIVE_DOCUMENT_MAP.md`, `ROADMAP_ARGOS_V5.md` ou
`SPRINTS_ARGOS_V5.md`.

## 4. Primeira slice Luna

```text
FIRST_LUNA_SLICE = BC-AUTH
CONTRACT = 01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md
WHY_FIRST = quatro perfis e matriz funcional estão decididos pelo usuário;
            independe de câmera, rede, segredo e banco de produção; tem
            aceitação local objetiva; fundamenta as rotas posteriores
BLOCKING_DEPENDENCIES = NONE for local implementation
EXPECTED_PRIMARY_FILES = usuarios/management/commands/configurar_perfis_argos.py;
                         usuarios/admin_security.py; cameras/models.py (Meta.permissions)
EXPECTED_NEW_FILES = cameras/integracao/authorization.py (ou módulo equivalente)
EXPECTED_TEST_FILES = usuarios/test_perfil.py; usuarios/test_admin_sec_r02c.py;
                      cameras/test_governanca_views.py; testes focais novos de negação
MIGRATION_EXPECTED = YES, AlterModelOptions para custom permissions de Camera
SOL_ESCALATION_TRIGGER = requisito novo de produto, conflito com ADR/contrato,
                         mudança de escopo de usuário protegido ou permissão
                         que exija decisão além da matriz publicada
```

## 5. Plano consolidado de schema

Nenhuma migration é criada no BC-02. O identificador numérico exato deve ser
obtido do grafo real no checkout da slice. Migrations de mesma app são
sequenciais; não gerar nós paralelos com o mesmo predecessor.

| Slice | MODEL_CHANGE / EXPECTED_MODELS | RELATIONSHIPS | CONSTRAINTS / INDEXES | DATA_MIGRATION | ROLLBACK_CONSIDERATION |
|---|---|---|---|---|---|
| BC-AUTH | `Camera.Meta.permissions` e reconciliação de grupos | Permission ↔ Group já existentes | codename estável; sem coluna de domínio | Comando de perfis idempotente; não atribuir Técnico por inferência a usuários antigos | Remover permission só após revogar grants; preservar contas/grupos preexistentes |
| CAM-INT-01 | `CameraCapabilityProfile`, `CameraConnectionConfig` | Profile 1:N Config; Camera 1:1 Config | `(profile_key, version)` único; configuração válida/ativa por câmera; índices de ativo e perfil | Seed idempotente `RTSP_DISCOVERY_V1` sem vendor SUPPORTED; configs antigas ausentes/inativas | Desativar vínculo antes de remover perfil; não apagar dados operacionais |
| CAM-INT-02 | `CameraCredential`, `CameraCredentialVersion` e FK nullable em `CameraConnectionConfig` | Camera 1:1 Credential; Credential 1:N Version; versão ativa FK vinculada; Config N:1 Credential opcional | `(credential_id, version)` único; no máximo uma versão ACTIVE por credential; coerência de referência ativa validada em service transacional | Nenhum segredo legado importado; binding inicial ausente | Reverter sem expor plaintext; preservar ciphertext/backups e plano de chave |
| CAM-INT-02-R1 | Nenhuma mudança de model/migration; API/value object no serviço existente | Reutiliza Config -> Credential -> active_version, mesma câmera e owner | Integridade/lifecycle e releitura transacional no serviço | Não | Retirar boundary/consumer sob gate, preservando custódia; nunca exportar plaintext |
| CAM-INT-06 | `Camera.firmware_version` e `CameraCapabilityEvidence` | Profile 1:N Evidence; câmera opcional para evidência por unidade | índice `(profile, vendor, model, firmware, status)` e fonte/version obrigatórias | Não gerar `SUPPORTED` a partir de cadastro livre | Preservar evidência de auditoria antes de remover schema |
| CAM-INT-03/04/07 | Sem nova tabela além de Config/Profile/Credential/Evidence | Reutilizar relações anteriores | Não aplicável | Não | Não aplicável |
| CAM-INT-05 | `CameraHealthSnapshot` | Camera 1:1 Snapshot | coerência A-D e generation; índice observed_at | Não inferir A-D de status antigo | Snapshot é derivado; preservar histórico de monitoramento |
| MON-WORKER/MON-OBS | Sem schema local novo; usam `EstadoMonitoramento`/lease existentes | Não aplicável | Não aplicável | Não | Não aplicável |
| IMG-CAP | `CameraCaptureJob`; reutilizar `CameraImageRecord` | Camera/User 1:N Job; Job 0..1:1 ImageRecord | unique(camera,requestor,idempotency_key); índice (status,created_at) | Não | Drenar jobs, preservar imagens; compensar objeto/linha conforme contrato |
| PROD-* | Nenhuma migration BC-02; validação na engine futura | Conforme decisão de produção | Revalidar constraints/índices reais | Plano separado | Backup/restore testado antes de reversão produtiva |

## 6. Regras de parada, ambiente e UI

Luna implementa o contrato, sem decidir produto ou ampliar trust boundary.
Parar e escalar a Sol somente se a implementação exigir estado/transição não
contratado, schema diferente do plano acima, contradizer ADR/contrato, demandar
protocolo/biblioteca inviável na stack ou tornar um critério de aceite
impossível. Configuração de CIDR real, credenciais reais, câmera e rede reais,
PostgreSQL, supervisão e budgets são validações posteriores e não bloqueiam
framework/adapters/fakes locais. Erro mecânico comum permanece com Luna.

P5 consome autorização BC-AUTH, URI RTSP sem segredo para Operador, edição por
Técnico/Admin, workflow de credencial/reveal, teste manual e health A/B/C/D.
P5-0 não depende de backend implementado para iniciar o trabalho visual que
não consome essas capacidades. Nenhuma UI é implementada neste checkpoint.
`SECURITY_REMEDIATION = DEFERRED_TO_FINAL_SECURITY_GATE`; os invariantes de
segredo, autorização, allowlist e egress continuam obrigatórios.
