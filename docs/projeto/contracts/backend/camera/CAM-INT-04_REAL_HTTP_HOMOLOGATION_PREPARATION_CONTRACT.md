# CAM-INT-04 — Contrato de preparação da homologação HTTP real

```text
PROJECT = ARGOS
ACTIVITY = CAM-INT-04-REAL-HTTP-HOMOLOGATION-PREPARATION
DATE = 2026-10-08 / America/Sao_Paulo
MODE = CONTRACT_PREPARATION
STATUS = PREPARATION_COMPLETE / EXECUTION_PENDING_OPERATOR
BRANCH = codex/cam-int-04-implementation
HEAD = 8e6fa230a9d137c8b1aedd502e0ac9cdf6ef2ecf
MASTER_BASELINE = 5bd22b06891a9cfa3886aa2dd2fbe0bf97e125c9
EXECUTION_MODE = DIRECT
RUNTIME_MODEL / RUNTIME_EFFORT = UNKNOWN / no reconfiguration
SUBAGENTS = 0
SKILL = activity-progress-reporting / explicit user instruction
PLUGIN = NONE
HTTP_SNAPSHOT_CONTRACT_STATUS = CLOSED_FOR_PREPARATION / REAL_VALIDATION_PENDING
IMG_CAP_CONTRACT_STATUS = CLOSED_FOR_PREPARATION / REAL_VALIDATION_PENDING
HOMOLOGATION_CONTRACT_READY = YES / procedure, not execution readiness
REAL_EXECUTION_READY = NO
TARGET_STATUS = REQUIRES_OPERATOR_INPUT
HTTP_ENDPOINT_STATUS = UNCONFIRMED
```

## 1. Autoridade e evidência

Esta preparação autoriza somente documentação na worktree CAM-INT-04.
São proibidos código/testes, câmera/rede HTTP real, credenciais reais, banco
operacional, migrations operacionais, alteração de master/UI e publicação Git.
A próxima atividade exige autorização própria. Gate aprovado não substitui
instrução explícita de execução.

FATO: Git confirmou a worktree
`C:/Users/walacedelgado/PycharmProjects/projeto_argos_cam_int_04`, branch/HEAD
acima, limpa e staging vazio antes das edições. HEAD igual à referência local
origin/codex/cam-int-04-implementation, divergência 0/0. Sem fetch nesta
preparação; isto não confirma estado novo do servidor remoto. Master local
permanece no baseline acima.

PROJECT_STATE §68 registra publicação da implementação `43a08a5`, validação
histórica 141/141 e homologação real pendente. Testes não foram reexecutados
nesta preparação. O HEAD esperado incorpora continuidade posterior.
DIVERGÊNCIA: IMG-CAP contém parágrafo histórico de testes não executados e
migration não aplicada; início do contrato e PROJECT_STATE §§67–68 registram
validação posterior em DB de teste destruído. Tratar o parágrafo como snapshot
anterior, preservado; nenhuma migration operacional foi executada aqui.

## 2. Fontes e rastreabilidade

Paths relativos à worktree, APIs/símbolos existentes:

| Fonte | Responsabilidade |
|---|---|
| `docs/projeto/contracts/backend/camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md` | BC-02, HTTP/R1 e bounds |
| `docs/projeto/contracts/backend/images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` | IMG-CAP e proveniência |
| `docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md` | resolução ativa e lifetime |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md` | configuração ambiental |
| `cameras/integracao/target_policy.py` | TargetPolicy.from_environment/validate, sem rede |
| `cameras/integracao/http_snapshot/adapter.py` | HttpSnapshotAdapter.capture, SnapshotRequest/Image/Error |
| `cameras/integracao/configuration.py` | save_connection_config, resolve_connection_config |
| `cameras/integracao/capabilities.py`, `compatibility.py` | SUPPORTED baseado em evidência |
| `cameras/integracao/credentials.py`, `key_provider.py` | replace, R1, provider ambiental |
| `cameras/authorization.py` | require_camera_permission |
| `cameras/imagens/capture_service.py` | request_camera_capture, run_next_capture e persistência |
| `cameras/management/commands/run_capture_worker.py` | entrypoint --once |
| `cameras/models.py`, `cameras/auditoria.py` | CameraCaptureJob, CameraImageRecord e auditoria |
| `cameras/test_camera_http_snapshot.py` | client, auth, imagem, bounds, timeout/cancelamento com fakes |
| `cameras/test_imagens_capture_service.py`, `test_imagens_capture_worker.py` | serviço, policy/R1, idempotência e comando |
| `config/settings.py`, `requirements.txt`, `.venv/pyvenv.cfg` | defaults e ambiente |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` §68 | checkpoint anterior |

Inspeção focal não encontrou testes específicos de todas as falhas de storage/
DB e recovery por interrupção. Não afirmar validação dessas situações.

## 3. Ficha do operador e requisitos de alvo

Todos os dados abaixo estão FALTANTES/UNCONFIRMED. Não consultar DB operacional
ou segredos históricos para preenchê-los; não varrer endpoints.

| Dado necessário | Critério |
|---|---|
| CAMERA_ID e identidade física | mapear explicitamente ID do Argos ao ID do DB isolado |
| fabricante/modelo/firmware | corresponder à evidência exata HTTP SUPPORTED |
| host | IPv4 canônico em Camera.ip; sem DNS/IPv6 |
| scheme/porta | scheme efetivo e porta exata aprovados no profile/policy |
| endpoint Snapshot | path relativo confirmado pelo operador/manual/equipamento; sem query/fragmento/userinfo/token |
| método auth | NONE, BASIC ou DIGEST realmente suportado; autenticado exige HTTPS |
| TLS | certificado válido para IPv4 e cadeia confiável ao client padrão |
| profile | key/version ativo HTTP_SNAPSHOT, source_ref, evidence SUPPORTED |
| operador | autorização sobre câmera física e identidade Django com permissões reais |
| policy | CIDRs/exclusões, portas por scheme, farm quando aplicável, path alternativo exato |
| janela/budget | horário, timeout T, quantidade de aquisições e efeitos autorizados |
| isolamento/retenção | RUN_ROOT absoluto exclusivo, DB/storage privados e prazo das evidências |

RTSP homologado não comprova HTTP. Sem HTTP SUPPORTED, parar e exigir
qualificação de capability sob authority própria; não forjar evidence/profile.
Se requer DNS, redirect, query, auth não suportada ou TLS bypass, registrar
incompatibilidade e parar. Nenhum endpoint ou câmera universal é presumido.
Não solicitar senha/chave no chat. A ficha pede somente dados não secretos.

## 4. Configuração, policy e autorização

Usar TargetPolicy.from_environment(os.environ) real, sem policy permissiva
injetada. Variáveis canônicas:

- ARGOS_CAMERA_ALLOWED_CIDRS: CSV de CIDRs IPv4 canônicos; preferir /32 aprovado.
- ARGOS_CAMERA_DENIED_CIDRS: exclusões, com precedência sobre allow.
- ARGOS_CAMERA_ALLOWED_PORTS: scheme:porta[,porta];... restrito ao alvo.
- ARGOS_CAMERA_ALLOWED_FARMS: CSV opcional coerente com Camera.farm.
- ARGOS_CAMERA_ALLOWED_PATHS: scheme:/path[,/path];... para alternativo exato.

Default path é autorizado pelo profile. Alternativo exige allowlist independente
confiável; não derivá-la do override do usuário. Ausência, lista malformada,
revogação ou incompatibilidade scheme/porta falha antes de R1/rede. Sem wildcard.

Camera elegível, não DESATIVADA; CameraConnectionConfig enabled, profile ativo
HTTP_SNAPSHOT e compatibility SUPPORTED. Resolver config com
resolve_connection_config(camera_id=..., environment_allowed_ports=...,
automatic=False). Porta default exige profile com uma única porta; override
só nos campos permitidos pelo profile. Usar save_connection_config para
alteração aprovada, não update direto para contornar validação.

Permissões: cameras.capture_camera_image para A/B;
cameras.change_camera_connection para configurar;
cameras.change_camera_credential para cadastrar credencial;
cameras.manage_camera_capability para eventual gestão aprovada de profile/
evidence. Guards são por modelo Django, sem escopo de objeto no baseline;
a autorização física permanece exigência externa. Não usar superuser fictício.

## 5. Credencial segura, no mesmo processo

Futura sessão: processo local interativo, entrada oculta getpass para username/
password, sem transcript/histórico de segredo/debug HTTP. Nenhum input real
nesta preparação. Gerar chave Fernet efêmera em memória para DB descartável;
definir no próprio processo ARGOS_CAMERA_CREDENTIAL_KEYS (mapa JSON versão→
chave) e ARGOS_CAMERA_CREDENTIAL_ACTIVE_KEY_VERSION. Não persistir chave em
.env, DB, Git ou arquivo; não usar chave histórica nem depender de outro terminal.
Preferir processo sem chaves herdadas, sem children; restaurar valores ambientais
alterados em finally sem imprimir conteúdo.

No DB isolado, cadastrar via replace_camera_credential(actor=..., camera_id=...,
username=..., password=...) com permissão real. Cria ciphertext e auditoria.
Execução resolve somente por resolve_active_credential_for_execution(config=...)
após permissão/config/policy. Não usar decrypt privado, provider direto no
consumer, reveal, credential_metadata, segredo hardcoded, URI autenticada,
cache ou fallback de versão. B faz sua própria resolução canônica.

Basic/Digest exigem HTTPS no código atual. NONE só se explicitamente permitido,
credential_required=False e sem credential vinculada. Não retirar vínculo para
contornar auth. HTTPX usa verify=True, trust_env=False e redirects off; não
usar verify=False, proxy, CA bypass ou monkeypatch. Certificado incompatível
com acesso por IPv4 bloqueia sessão. Liberar referências ao terminar e encerrar
processo; zeroização de strings Python não é garantida. DB/ciphertext isolado
não é evidência a preservar.

## 6. Runtime e persistência isolados

FATO por metadados, sem Django setup/DB: Python 3.13.1 em
`C:/Users/walacedelgado/PycharmProjects/projeto_argos_cam_int_04/.venv/Scripts/python.exe`;
Django 5.2.16, HTTPX 0.28.1, Pillow 12.3.0, cryptography 46.0.7. Nenhuma
instalação feita. Revalidar imports/versões no preflight futuro.

Defaults config.settings usam BASE_DIR/db.sqlite3 e BASE_DIR/private_media.
Não executar worker com defaults. Não há variável de DB demonstrada nesse
settings; não inventar ARGOS_DATABASE_URL/MEDIA_ROOT ambiental.
Harness futuro cria módulo de settings temporário fora dos arquivos versionados,
herdando config.settings e sobrescrevendo antes de django.setup:
DATABASES.default SQLite NAME=<RUN_ROOT>/homologation.sqlite3;
MEDIA_ROOT=<RUN_ROOT>/images; STORAGES.default FileSystemStorage privado nessa
raiz; DEBUG=False. Sem mudar config/settings.py. Resolver paths e rejeitar DB/
media operacional, master/UI e paths fora de RUN_ROOT antes de conexão.

RUN_ROOT exclusivo com ID aleatório/acesso restrito. Migrations para bootstrap
somente nesse DB descartável requerem aprovação posterior de isolamento;
nenhuma DB/migration nesta preparação. Criar apenas fixtures mínimas aprovadas
(ator/permissões, câmera, profile/evidence qualificada, config e credencial
nova), sem copiar DB produtivo/password de operador. Baseline após setup
separa efeitos de configuração e auditoria de A/B.

Um processo, um worker, um job QUEUED por vez; sem servidor/monitoramento/worker
contínuo. T explícito, finito, 0<T≤30 s. ARGOS_CAMERA_CAPTURE_TIMEOUT_SECONDS
é setting Django, não variável lida automaticamente; defini-lo no módulo
isolado. T limita aquisição async, não bootstrap/DB/storage/decode síncrono/
cleanup; medir duração total à parte. Watchdog externo exige budget aprovado;
kill pode deixar RUNNING/objeto órfão, não fingir recovery.

## 7. Gate A — HTTP Snapshot real

Não cria job/CameraImageRecord. Não existe comando público específico A
confirmado. Harness futuro é apenas orquestração das APIs públicas, sem HTTP,
crypto, decode, retry, fallback, storage ou correção de defeito produtivo.
Não está implementado/executado nesta preparação; revisar antes da sessão.

Procedimento após aprovação:

1. Revalidar branch/HEAD, isolamento, alvo e autorização física. Exigir
   require_camera_permission(actor=..., permission_codename='capture_camera_image', camera_id=...).
2. Carregar config persistida; resolve_connection_config público e compatibility
   SUPPORTED. Confirmar elegibilidade, profile HTTP ativo e scheme/porta/path
   da ficha iguais aos efetivos produtivos (HTTPS prioritário, sem fallback).
3. Policy pelo ambiente confiável. validate(Camera.ip, URI construída somente
   do IPv4/scheme/porta/path confirmados, allowed_schemes=(scheme,),
   allowed_ports=tuple(profile.allowed_ports), default_port=porta, farm=Camera.farm,
   allowed_paths=(profile.default_path,) se path=default, senão None).
   Exigir AUTHORIZED_TARGET/request; nunca fabricar TargetValidation.
4. Para Basic/Digest confirmar HTTPS/vínculo ativo, revalidar permissão e usar
   R1. Para NONE aplicar seção 5. Relê config/profile e compara IP, vínculo,
   versões e parâmetros; revalida destino antes do adapter. Mudança aborta.
5. SnapshotRequest(target=validação real, auth_method=profile.auth_method,
   credential_required=profile.credential_required,
   allowed_content_types=SUPPORTED_CONTENT_TYPES, timeout_seconds=T).
   Chamar HttpSnapshotAdapter().capture(request, credential=...) via async,
   client/transport padrão, no mesmo processo.
6. Registrar retorno SnapshotImage ou código SnapshotCaptureError; medir
   duração, formato/dimensões, len(data)>0 e SHA-256 dos bytes sanitizados;
   verificar decode desses bytes. Sem salvar imagem A por default. Conferir
   ausência de escritas de captura; liberar client/objeto/credencial.

| Critério | Aceitação e evidência |
|---|---|
| HTTP_SUCCESS | candidata 200 sem redirect; retorno canônico implica 200 pelo código inspecionado, inferência explícita, sem dump HTTP |
| VALID_IMAGE_RECEIVED | retorno validado, bytes positivos, JPEG/PNG/WEBP estático, MIME coerente, decode completo, ≤10 MiB, ≤20 milhões de pixels; tamanho/formato/dimensões/digest |
| auth | método aprovado funciona no endpoint confirmado; NONE só explicitamente permitido |
| timeout | T finito positivo ≤30; CONNECT_TIMEOUT/READ_TIMEOUT e duração no cenário exercitado |
| auth negada | 401/403→AUTH_FAILURE, sem fallback, via fixture controlada por default |
| endpoint indisponível | CONNECT_ERROR/CONNECT_TIMEOUT/HTTP_TRANSPORT_ERROR ou HTTP_STATUS_ERROR conforme cenário, sem declarar OFFLINE |
| conteúdo inválido | CONTENT_TYPE_INVALID/BODY_TOO_LARGE/IMAGE_INVALID, sem imagem aceita; HTML, MIME falso, vazio/truncado/oversize em cenário controlado |
| TLS/redirect | TLS_ERROR ou HTTP_STATUS_ERROR; sem bypass ou hop |
| path fora da lista | policy não autorizada, zero R1 e zero adapter/rede, prova controlada com contador de port |
| sanitização | nenhum segredo, chave, URI completa, header ou body nos outputs |

HTTP 200 sozinho nunca é PASS. Adapter não retorna status/body bruto; não
inventar instrumentação disponível. Bytes são pós-reencode, hash pode diferir
do payload original. A=PASS real requer aquisição válida no alvo aprovado e
matriz obrigatória com evidência identificada. Cenário sem prova fica
NOT_VALIDATED. Provas controladas não são provas de rede/câmera real.
Timeout/auth failure reais exigem autorização específica de cenário/budget,
inclusive risco de lockout; não provocar falha na câmera por default.

## 8. Gate B — IMG-CAP end-to-end

Entrypoint fiel: no mesmo processo, request_camera_capture(actor=...,
camera_id=..., idempotency_key=<token aleatório 16–128 caracteres>,
source_preference='HTTP_SNAPSHOT'), sem policy/allowed_ports/adapter injetados;
depois django.core.management.call_command('run_capture_worker', once=True).
Usa o comando produtivo --once sem segundo processo com segredo ausente.
Não inserir job direto por ORM nem supor endpoint web de captura existente.

1. Baseline após setup: contagens jobs/imagens/auditoria, inventário storage,
   estado/geração/streak/transições/indisponibilidades. Fila vazia e nenhum
   outro consumidor.
2. Enqueue deve criar exatamente um QUEUED HTTP_SNAPSHOT, ator/câmera e versões
   corretos; evento imagem.captura.solicitada. Mesma key devolve mesmo job.
3. Worker faz claim condicional QUEUED→RUNNING/started_at, revalida permissão/
   config/capability/policy, R1, relê config e usa adapter real. Sem retry,
   câmera alternativa, RTSP ou fallback de scheme.
4. SUCCEEDED exige finished_at, error_code vazio, exatamente um image_record
   ligado à mesma câmera, CAPTURA_CAMERA, captured_by_system='IMG-CAP',
   captured_at/recorded_at timezone-aware do servidor, storage key gerada e
   objeto no storage isolado.
5. Ler objeto por default_storage; comparar len, SHA-256, MIME/formato,
   dimensões e decode com registro. Não comparar hashes A/B (capturas distintas).
   latest segue contrato canônico sem promover captura antiga.
6. Exigir imagem.captura.concluida e invariantes de monitoramento iguais ao
   baseline. 'Processed 1' não comprova sucesso/integridade; consultar job/DB.
7. Repetir enqueue mesma key depois do sucesso: sem job/imagem/auditoria extra.
   Worker não reprocessa SUCCEEDED. Nova key/captura só com budget autorizado.
8. Complementar negativos controlados: FAILED+finished_at+error allowlisted,
   FK image_record ausente, zero imagem nova/órfão conhecido e evento
   imagem.captura.falhou. Negação no enqueue não cria job.

| Falha | Expectativa | Evidência atual / limite |
|---|---|---|
| permissão revogada | AUTHORIZATION_DENIED, antes de R1/HTTP | teste focal existente |
| policy/config alterada | TARGET_DENIED/CONFIG_INVALID, sem execução | testes focais existentes |
| R1 indisponível | CREDENTIAL_UNAVAILABLE, sem adapter | teste focal existente |
| HTTP/auth/timeout/decode | código allowlisted, FAILED, sem imagem | negativos integrados devem ser complementados controladamente |
| storage.save | STORAGE_ERROR, sem linha imagem | código inspecionado; teste específico não encontrado |
| DB/auditoria após storage | normalmente INTERNAL_ERROR e tentativa de compensação | prova controlada futura; delete pode falhar |
| DB no claim/finalização | pode não haver terminal, RUNNING possível | não prometer FAILED garantido |
| processo interrompido | RUNNING e/ou órfão possíveis | sem lease/requeue/recovery automático visível |

B=PASS exige fluxo integrado e negativos obrigatórios com origem de prova,
cleanup verificado e ausência de defeito mascarado. Registrar sucesso do fluxo
feliz separado de B global NOT_VALIDATED se faltarem negativos. Nenhum teste
controlado pode ser apresentado como câmera real. Se recovery automático ou
zero órfãos sob kill/delete falho forem exigidos, gate fica FAIL/BLOCKED e
hardening requer atividade própria. Harness não pode implementar recovery
produtivo para fabricar PASS.

## 9. Efeitos e cleanup

| Classe | Efeitos da futura sessão isolada |
|---|---|
| DATABASE_WRITES | schema/fixtures; config, credencial/versão; EstadoMonitoramento/geração por save_connection_config; job/claim/terminal; imagem e auditorias |
| FILESYSTEM_WRITES | SQLite e journals/WAL/SHM quando gerados; imagens; settings/harness temporários; manifesto sanitizado; caches Python quando gerados |
| IMAGE_ARTIFACTS | A em memória; B em camera-images/<camera-id>/<uuid>.<ext> no media isolado; nenhuma imagem no Git |
| AUDIT_EVENTS | setup aprovado; imagem.captura.solicitada/concluida/falhou; nenhum reveal |

Auditoria congela identidade do ator; DB isolado continua privado. Eventos são
imutáveis: não excluir linhas individualmente; descarte inteiro só conforme
isolamento aprovado.

Manifesto: run ID, Git/interpreter/versões, alias privado do alvo, gate/cenário,
origem REAL_TARGET ou CONTROLLED, início/fim UTC, T/duração, decisão policy,
job/status/error, formato/dimensões/tamanho/digest, contagens/auditorias,
integridade, invariantes, cleanup e limites. Mapeamento real do alvo fica
privado fora do Git. Sem IP/path real, username, ciphertext, imagem, headers,
response body, chave, dumps de ambiente ou traceback bruto em documento
versionado. Desabilitar debug HTTPX/httpcore/transcript. Exceção desconhecida
vira evidência genérica sanitizada, não repr arbitrário.

Cleanup em finally, seguido de confirmação independente:

1. Parar consumidores, confirmar nenhum processo ativo, fechar DB/client/
   handles. Inventariar QUEUED/RUNNING e objetos antes de descartar.
2. Comparar arquivos/storage_keys enquanto DB existe. _persist_success tenta
   delete ao falhar, mas suprime falha de delete: verificar storage.exists e
   órfãos. Rollback SQL não remove arquivos.
3. Preservar só manifesto sanitizado aprovado. Imagem requer decisão de prazo/
   acesso privado fora do Git. Não preservar DB/ciphertext/chave.
4. Restaurar ambiente temporário e encerrar processo com segredo. Isolamento
   violado: suspender descarte, reportar e não intervir no DB operacional.
5. Resolver RUN_ROOT absoluto, verificar ownership/run marker e ausência de
   reparse points/symlinks externos; confirmar que não é repo/master/UI.
   Excluir somente essa raiz aprovada, handles fechados, operação nativa no
   mesmo shell. Sem git clean/reset/restore ou paths calculados não verificados.
6. Confirmar ausência DB/journals/imagens/settings/harness e chave persistida;
   HEAD/master/UI preservados, staging vazio e delta documental apenas.
   Cleanup incompleto=FAIL, com pendência explícita.

Não recolocar RUNNING na fila por update manual para fazer cenário passar; preservar
manifesto e descartar run seguro/autorizado. Estratégia é descarte de ambiente
isolado, não recuperação produtiva. Erro de cleanup é evidência de falha.

## 10. Aprovação e decisões do operador

Antes de bootstrap, input de segredo ou rede real, todos os gates requerem
YES com responsável, origem e data, e autorização explícita posterior:

```text
TARGET_CONFIRMED = NO
OPERATOR_AUTHORIZED = NO
ENDPOINT_CONFIRMED = NO
CREDENTIAL_FLOW_APPROVED = NO
POLICY_CONFIRMED = NO
PERSISTENCE_ISOLATION_APPROVED = NO
ACCEPTANCE_CRITERIA_CLOSED = YES / criteria only, no test result implied
REAL_HTTP_EXECUTION_AUTHORIZED = NO
```

OPERATOR_INPUT_REQUIRED: ficha §3, permissões de setup e target, evidência HTTP
SUPPORTED, TLS compatível por IPv4, credencial efêmera, policy e RUN_ROOT.
UNRESOLVED_DECISIONS: autorizar schema isolado e settings/harness; T/janela/
watchdog; orçamento de duas aquisições A/B sem retry automático (Digest pode
ter challenge); retenção/cleanup; negativos reais ou controlados. Default dos
negativos é CONTROLLED sem câmera. Auth failure real requer risco de lockout/
número de tentativas aprovados. Sem ampliar endpoint/policy para gerar falha.

Próxima atividade: CAM-INT-04-REAL-HTTP-HOMOLOGATION, começando pelo preflight e
revisão do harness temporário. Se HTTP SUPPORTED faltar, qualificação prévia
requer authority própria. Contrato pronto não concede execução automática.

```text
REAL_CAMERA_ACCESSED = NO
REAL_CREDENTIALS_ACCESSED = NO
PRODUCTION_CODE_CHANGED = NO
TEST_CODE_CHANGED = NO
MASTER_UNCHANGED = YES
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
HOMOLOGATION_CONTRACT_READY = YES
NEXT_RECOMMENDED_ACTIVITY = CAM-INT-04-REAL-HTTP-HOMOLOGATION
```
