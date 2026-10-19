# ARGOS E3 — Plano de recuperação primária RTSP

ACTIVITY_ID = ARGOS-E3-RTSP-DOC-01
STATUS = DOCUMENTATION_ONLY / HUMAN_DOCUMENT_APPROVAL_PENDING
BASELINE_REFERENCE = codex/hom-v1-integration @ d44e4e6f (informado para HML; não verificado como HEAD local)
LOCAL_PREFLIGHT = branch codex/hom-v1-integration; HEAD 5c798bb37285d8cf7f42b9197dfc81057f472e09; worktree possui WIP preexistente

## 1. Direção aprovada e limites

Por decisão explícita registrada no pedido desta atividade, `RTSP_FRAME` é o método principal e `HTTP_SNAPSHOT` é método secundário independente. RTSP convencional usa `rtsp://`, porta 554 por padrão (configurável sob policy), credencial já cadastrada, decodificação de vídeo e extração de um frame JPEG. RTSPS e certificado HTTPS não são requisitos para RTSP convencional. Não haverá fallback silencioso. Ambos os métodos convergem para validação, persistência privada, metadados, auditoria e galeria E4; o domínio existente de `CameraImageRecord` será reutilizado.

Esta direção entra como decisão de produto/arquitetura fornecida pelo usuário, mas os conflitos com contratos canônicos vigentes ficam sujeitos ao amendment/supersession humano em `ARGOS_E3_RTSP_PRIMARY_RECOVERY_AMENDMENTS.md`. Este documento não altera retroativamente contratos, não autoriza implementação, câmera real, VM, worker recorrente ou publicação.

## 2. Evidência e estado HML

Fatos HML recebidos no payload (não reexecutados nesta atividade): release `d44e4e6f` em `codex/hom-v1-integration`; Gunicorn, Django, Nginx e smoke HTTP/funcional aprovados; migrations 0020/0021 aplicadas; rollback local preparado; nenhum worker permanente iniciado. Câmera RF0420, Hikvision DS-2CD2143G2-IS, banco ID 4, IPv4 10.143.108.79, porta candidata 554, endpoint candidato `/Streaming/Channels/101` ainda sem captura real.

Problemas confirmados no payload: worker E3 rejeita `RTSP_FRAME`; adapter RTSP detecta frame mas não entrega bytes; câmera sem `CameraConnectionConfig`; `RTSP_DISCOVERY_V1` não é perfil operacional; integração admin de perfis/conexões incompleta; Target Policy ausente/inválida e chaves de criptografia ausentes na HML examinada; câmera em `CONFIGURATION_INCOMPLETE`; nenhuma captura real nem galeria validada. Permissão de captura de `qa-operacional-hom03` foi corrigida conforme evidência fornecida. Certificado HTTPS inválido da câmera pertence ao método HTTP Snapshot e não bloqueia RTSP convencional.

Pendências F02 (recovery de jobs QUEUED/RUNNING, DRAFT) e F03 (semântica `error_code`/`CANCELLED`, aberta) permanecem com os mesmos identificadores. Não habilitar worker recorrente até resolver formalmente recovery/idempotência, cancelamento/erro, claim/retry, configuração e segredos HML, autorização e observabilidade operacional.

## 3. Diagnóstico arquitetural

Conectividade/diagnóstico RTSP mede etapas de rede, negociação e descrição de mídia. Receber um frame confirma entrega de mídia. Extrair amostra decodificada e codificar JPEG produz bytes persistíveis. Um job durável representa solicitação e estado; storage privado guarda o objeto; `CameraImageRecord` é o registro canônico; a galeria E4 lê e apresenta esse registro pelas regras de imagem aprovadas. Nenhuma etapa implica automaticamente a seguinte.

A lacuna está entre CAM-INT-03 e E3: o protocolo atual `RtspAdapter.receive_one_frame(session) -> bool` confirma resultado, sem bytes de imagem; `GStreamerRtspAdapter` mantém o resultado de entrega em estado efêmero e o consome. O worker E3 precisa receber um artefato de frame limitado e validável, não o booleano diagnóstico. `probe()`/`describe()` não constituem captura persistente.

## 4. Componentes e reaproveitamento

| Componente | Responsabilidade / situação | Reuso ou lacuna |
|---|---|---|
| `Camera` | Identidade e cadastro | Reusar; vínculo operacional/config ainda incompleto na HML |
| `CameraCapabilityProfile` | Scheme, portas, auth e limites técnicos | Reusar; `RTSP_DISCOVERY_V1` não declara suporte de captura |
| `CameraCapabilityEvidence` | Evidências de capacidade | Reusar; exigir evidência adequada para `SUPPORTED` |
| `CameraConnectionConfig` | Endpoint/perfil por câmera | Reusar; ausência confirmada para RF0420 |
| `CameraCredential` / `CameraCredentialVersion` | Segredo cifrado e versões | Reusar via API pública CAM-INT-02; configuração de chave HML ausente |
| `CameraCaptureJob` | Job durável | Contratado em IMG-CAP, não existe no checkout atual |
| `CameraImageRecord` | Registro canônico de imagens | Reusar; não duplicar tabela/domínio |
| `EventoAuditoria` | Auditoria de ação e resultado | Reusar; nunca registrar segredo, URI com userinfo ou bytes |
| GStreamer RTSP adapter | Probe A–D, SDP/codec e detecção de entrega | Reusar base bounded; evoluir para obter amostra/bytes e encerrar pipeline |
| `capture_service.py` | Orquestração/persistência de captura | Previsto em contrato, ausente no checkout |
| `run_capture_worker` | Consumo separado de jobs | Comando de captura ainda ausente; não confundir com worker MON |
| E4 read/display/preview services | Leitura, seleção e entrega privada | Reusar sem alterar Quick Detail nem suas regras aprovadas |

## 5. Arquitetura-alvo

Django web autentica/autoriza a ação explícita, valida elegibilidade e cria job + auditoria; não abre stream na requisição de UI. Serviço de aplicação resolve perfil, configuração, Target Policy e credencial efêmera através das APIs contratadas. Adaptadores `RTSP_FRAME` e `HTTP_SNAPSHOT` entregam conteúdo limitado ao pipeline compartilhado. Worker de captura isolado de monitoramento reivindica job com concorrência/timeout bounded, valida e decodifica, re-encoda JPEG, persiste via storage privado e cria `CameraImageRecord`; transação/compensação mantém job e imagem coerentes. PostgreSQL guarda configuração, jobs, auditoria e metadados; storage privado guarda imagem. E4 lê imagem por serviços/rotas existentes. Sem fallback automático entre métodos.

## 6. Plano P1–P8

| Etapa | Entrega e dependências | Critério de aceite |
|---|---|---|
| P1 — RTSP Frame Extraction Foundation | Diagnóstico dirigido do adapter/runtime GStreamer; contrato de frame; appsink/sample, decode H.264/H.265, JPEG, limites e runtime Linux/Python | Testes sintéticos provam frame bytes bounded, JPEG válido, cancelamento/timeout/limpeza; sem câmera real |
| P2 — Integração dos dados, perfis técnicos e configurações | Perfil, evidência, conexão, fabricante/modelo/firmware/canal/path/porta | Config válida e associação auditável; `SUPPORTED` só com evidência; default 554 conforme policy |
| P3 — Credenciais e preparação operacional | Resolver CAM-INT-02, chaves HML, Target Policy e autorização | Secrets injetados e validados; sem segredo em URI/log; preflight de destino bloqueia fechado |
| P4 — Worker RTSP no pipeline E3 | Job, claim, serviço, adapter de frame, pipeline comum e persistência | RTSP e HTTP convergem; idempotência/falhas coerentes; sem alteração de health/monitoramento |
| P5 — Admin e UI/UX | Gestão de perfil/conexão/credencial e ação/estado de captura conforme autorização | Ação explícita, permissionada e sem captura automática; Quick Detail preservado |
| P6 — Testes e regressão | Unitário/sintético, integração fake, segurança, resiliência, regressões E3/E4 | Gates técnicos e F02/F03 resolvidos antes de recorrência |
| P7 — Homologação real | Autorização operacional específica para RF0420 e janela/rede aprovadas | `RTSP → FRAME → JPEG → CAMERA_IMAGE_RECORD → GALERIA E4` validado com imagem real |
| P8 — Reconciliação e encerramento | Evidência, roadmap, contratos, estado e aceite humano | Estado HML reconciliado; nenhuma alegação acima da evidência; encerramento humano |

Dependências globais: amendment dos contratos conflitantes; P1 antes de integrar frame; P2/P3 antes de sessão operacional; P4 antes da UI operacional; gates e autoridade separados para P7. Rodada 1 é somente P1 e não inicia neste documento.

## 7. Compatibilidade

Compatibilidade é relação explícita entre fabricante, modelo, firmware e capability profile; canal/path, transporte, porta, método de autenticação e limites ficam associados à configuração validada. Canal/path candidato da RF0420 não é ainda validado. Evidência sintética prova parsing/pipeline, não compatibilidade de câmera. Estado `SUPPORTED` exige evidência apropriada e aprovada conforme CAM-INT-01/06; ausência vira `UNVERIFIED`/incompleto e bloqueia captura. Porta 554 é default, não autorização de destino; Target Policy continua obrigatória.

## 8. Critério final e status

Conclusão operacional requer validação real autorizada do marco `RTSP → FRAME → JPEG → CAMERA_IMAGE_RECORD → GALERIA E4` na câmera Hikvision de homologação. Hoje: captura real não feita; galeria com captura real não validada; worker recorrente não iniciado.

```text
RTSP_PRIMARY_DECISION = RECORDED_FROM_EXPLICIT_USER_INPUT
ROADMAP_SPRINTS_ALIGNMENT = VERIFIED / Roadmap §26 and Sprints §23; no implementation status promoted
HML_CURRENT_STATE = RECONCILED_FROM_SUPPLIED_EVIDENCE_ONLY
ROUND_1_IMPLEMENTATION_PLAN = READY / SEPARATE DOCUMENT
CODE_CHANGES = NONE
VM_CHANGES = NONE
ROUND_1_EXECUTION = NOT_STARTED
HUMAN_DOCUMENT_APPROVAL = PENDING
REMOTE_BASE_VERIFIED = origin/codex/hom-v1-integration @ d44e4e6f5556cef8b9db00637c40fbd08259f2f3
ORIGINAL_LOCAL_HEAD = 5c798bb37285d8cf7f42b9197dfc81057f472e09 / preserved with preexisting WIP
```
