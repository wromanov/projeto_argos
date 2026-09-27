# ARGOS — New Chat Bootstrap Prompt

STATUS = ACTIVE
PROJECT = ARGOS
LANGUAGE = pt-BR
FIRST_RESPONSE_MODE = READ_ONLY_CONTINUITY_REVALIDATION

Responda sempre em português do Brasil. Em nova conversa, siga esta ordem:

1. valide repo root, branch, HEAD, `origin/master`, divergência, worktree e staging;
2. leia `ACTIVE_DOCUMENT_MAP.md`;
3. leia `PROJECT_STATE.md`;
4. leia `AGENT_CONTINUITY.md`;
5. leia `ROADMAP_ARGOS_V5.md` e `SPRINTS_ARGOS_V5.md` no nível necessário;
6. leia a authority especializada da atividade atual ou planejada;
7. compare as fontes e só então proponha ou execute ações autorizadas.

Leia também `AGENTS.md`, este bootstrap e as policies transversais ativas
indicadas no mapa. A authority específica de continuidade é
`docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`. Git é a fonte factual
para estado do repositório. `DO_NOT_RESUME_FROM_CHAT_MEMORY_ONLY = YES`.

## Recovery boundary

AGENT_HANDOFF_GATE_RESULT = consult PROJECT_STATE.md; current checkpoint = PASS
CONTINUITY_RECOVERY_GATE = REVALIDATE_GIT_AND_AUTHORITIES_EACH_NEW_CHAT
USER_CONTINUITY_VALIDATION = NOT_REQUIRED_FOR_STATE_DISCOVERY
READY_TO_RESUME_PROJECT = YES_AFTER_READ_ONLY_REVALIDATION
RESUME_SCOPE = dentro das autorizações explícitas vigentes
IMPLEMENTATION = PROHIBITED UNTIL AUTHORIZED
EDIT = PROHIBITED UNTIL AUTHORIZED
STAGE = PROHIBITED UNTIL AUTHORIZED
COMMIT = PROHIBITED UNTIL AUTHORIZED
PUSH = PROHIBITED UNTIL AUTHORIZED
DEPLOY = PROHIBITED
PHASE_ADVANCEMENT = PROHIBITED UNTIL AUTHORIZED
DO_NOT_ASSUME_IMPLEMENTATION_AUTHORIZATION = YES
DO_NOT_RESUME_FROM_CHAT_MEMORY_ONLY = YES
PUSH = NOT_AUTHORIZED

Leia as políticas transversais ativas indicadas em `AGENT_CONTINUITY.md`; não use versões superseded como authority.

## Estado técnico histórico — referência anterior a IMG-02 + UI-1

LAST_RELEVANT_CHECKPOINT = 850efd2381d7f5b7df27e528dc3374ea58e507b3 (850efd2)
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
MON-09A = COMPLETE / PASS
MON-09B = COMPLETE / PASS_WITH_SCOPE_DEVIATION
MON-09C = COMPLETE / PASS_WITH_FINDINGS
MON-09D = COMPLETE
MON-09E = COMPLETE / PASS
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
DO_NOT_RESUME_OR_EXTEND_MON09 = YES
UI_DS_CANONICAL_SPEC = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
UI_DS_CANONICAL_SPRINT_MAP = docs/projeto/SPRINTS_ARGOS_V5.md
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
CAMERA_QUICK_DETAIL_PANEL = USER_APPROVED / canonical details in docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md section 7.3
CAMERA_QUICK_DETAIL_PANEL_VMS = DO_NOT_ADOPT; LOCATION_REPLACES_VMS
ARGOS_CURRENT_PAGE_COMPOSITION = PRESERVE
LATEST_CAMERA_CAPTURE_FEEDS_PANEL = YES_WHEN_CANONICAL_CONTRACT_AVAILABLE
PRIMARY_IMAGE_DISTINCTION = RECORDED
MANUAL_UPLOAD_PROVENANCE = PRESERVED
NO_AUTO_CAPTURE_ON_PANEL_OPEN = RECORDED
FASE_C_DEPENDENCY = EXPLICIT
ARGOS_INCREMENTAL_INTEGRATION_RULE = RECORDED
INTEGRATION_GATE = REQUIRED_WHEN_APPLICABLE
BIG_BANG_INTEGRATION = PROHIBITED
IMG01_STATUS = COMPLETE / DOCUMENTAL
CANONICAL_IMAGE_CONTRACT = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
LATEST_CAMERA_CAPTURE = captured_at DESC, recorded_at DESC, immutable_id DESC; avaliar validade/integridade/disponibilidade após selecionar registro
NO_SILENT_FALLBACK_TO_OLDER_CAPTURE = YES
PROVENANCES = CAPTURA_CAMERA, UPLOAD_MANUAL
PRIMARY_IMAGE = DEFERRED_TO_IMG07
CAMERA_QUICK_DETAIL_PANEL = consome LATEST_CAMERA_CAPTURE; não captura ao abrir; UPLOAD_MANUAL não é fallback implícito
MONITORING_SEPARATION = CAMERA_AVAILABILITY != IMAGE_CAPTURE_SUCCESS; falha de captura não altera ONLINE/OFFLINE
OPEN_DECISION_COUNT = 7; detalhes e momentos de fechamento no contrato canônico
IMG02_IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_DOCUMENT

A capacidade validada inclui estados estáveis UNKNOWN / ONLINE / OFFLINE; SUSPECT efêmero; STALE como dimensão de freshness; memória de confirmação persistente e streak pendente após restart; thresholds respeitados; restart sem transition/outage falsa; falha de banco distinta de câmera OFFLINE; CANCELLED neutro; timeouts e rede conforme semântica canônica; falhas operacionais sem histórico funcional falso e com recovery; ownership persistente por câmera, epoch monotônico, lease de takeover e fencing; config_generation independente; completion obsoleta sem side effects; observabilidade/configuração e logs sem secrets.

LEASE_EXPIRY_ALONE_INVALIDATES_COMPLETION = NO
NEWER_OWNERSHIP_EPOCH_INVALIDATES_COMPLETION = YES
ATTEMPT_MAX_DURATION_REQUIRED_FOR_CORRECTNESS = NO
LEASE_DURATION = janela operacional configurável de takeover
LEASE_RENEWAL_IMPLEMENTED = NO

## Contexto histórico de roadmap e limites — checkpoint pré-UI-3

NEXT_ACTIVITY_CANDIDATES = IMG-03 — Upload manual; UI-2 — Inventory Visual Retrofit
NEXT_ACTIVITY_STATUS = NOT_AUTHORIZED; não iniciar por inferência
NEXT_REQUIRED_ACTIVITY_AUTHORIZED = NONE

UI_DS = UI-0, UI-1, UI-2, UI-3, UI-4
UI_0 = COMPLETE / PASS_WITH_FINDINGS; read-only; não autoriza implementação
UI_1 = COMPLETE / INTEGRATED; commit c5928e8
UI_2 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI_3 = CameraQuickDetailPanel integrado ao fluxo canônico
UI_4 = QA visual/funcional/acessibilidade/interação
ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE; consultar resultado e critérios no PROJECT_STATE.md
UI_0_FINDINGS_DETAIL = docs/projeto/ARGOS_UI_DS_UI0_PREFLIGHT_FINDINGS_V1.md; findings não bloqueantes; UI_0_FINDINGS_DISCOVERABLE = YES

Este é o nível macro indicado pelo roadmap; não decomponha nem inicie a fase por inferência. Security gates vigentes:

LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS
HOMOLOGATION = BLOCKED
DEPLOYMENT = BLOCKED
PRODUCTION = BLOCKED

FUTURE_VALIDATIONS = PostgreSQL real; multi-processo real em produção; rede real; câmeras reais; credenciais reais; capacidade produtiva; budgets formais de CPU, memória e conexões. Esses limites não são falhas da MON-09 e não permitem alegar readiness produtiva. Preservar o estado factual de SEC-001...SEC-010; não reabrir SEC-007...SEC-010 nem mover SEC-001...SEC-006 para MON-09.

LOG_VOLUME_HARDENING_STATUS = HARDENING / NON-BLOCKING — potencial volume elevado de logs INFO por ciclo/attempt
MON09B_C_ACCIDENTAL_SCALE_EXECUTIONS = observação processual, não blocker técnico

## Git e ação

O snapshot histórico da baseline técnica antes da atividade documental anterior foi
`HEAD = origin/master = f4e88146c1146cdf04d657eb6e3cefa560639b61`, divergence
`0/0`, worktree clean e staging empty. O checkpoint técnico MON-09 em
`850efd2381d7f5b7df27e528dc3374ea58e507b3` é histórico; valide o estado atual e
o commit documental mais recente diretamente no Git antes de qualquer
conclusão. Não execute push sem autorização humana separada.

Esse bloco registra o contexto pré-integração e é supersedido pelo checkpoint
vigente abaixo. IMG-01 permanece concluída como checkpoint documental; o contrato
canônico mantém sete decisões abertas e suas slices de fechamento. A conclusão
MON-09 não altera gates ambientais nem declara homologation, deployment ou
production ready.


## Checkpoint histórico — integração IMG-02 + UI-1 (2026-09-25)

Para detalhes do contrato funcional e das decisões deferred, consulte
docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md. Este checkpoint registra status,
commits, gates e autorização; não duplica os detalhes técnicos.

IMG-02 = COMPLETE / INTEGRATED
IMG-02_COMMIT = ceda8f6
UI-1 = COMPLETE / INTEGRATED
UI-1_COMMIT = c5928e8
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; cameras.test_imagens_read_service 13/13 PASS
IMG-03 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-2 = NEXT_CANDIDATE / NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
PRODUCTION_STORAGE_BACKEND = DEFERRED; IMG-02 exige contrato persistente de storage e abstração configurável antes da migration
GIT_BASELINE = master; HEAD d5f1f54bea518496d7e8c8b64487cfea459372f6; origin/master 05b710a57137f9d0cdefd256c037e4d86fe0e3bb; ahead 3 / behind 0
GIT_WORKTREE = documentação deste checkpoint modificada e unstaged; staging vazio
IMPLEMENTATION_AUTHORIZED = nenhuma autorização atual; a autorização de IMG-02 foi consumida
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED
ACTIVITY_COMPLETION_PERCENT = 100%
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS

## Checkpoint histórico — integração IMG-03 + UI-2 (2026-09-25)

Leia o checkpoint mais recente em `PROJECT_STATE.md` e `AGENT_CONTINUITY.md`
antes de qualquer ação. Ele supersede os status de IMG-03/UI-2 deste bootstrap
que estejam marcados como históricos.

IMG-03 = COMPLETE / INTEGRATED; COMMIT = f6e08b6; INTEGRATION_COMMIT = 0708797
UI-2 = COMPLETE / INTEGRATED; COMMIT = b57f959; INTEGRATION_COMMIT = c79fa06
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; makemigrations --check --dry-run PASS; cameras.test_imagens_read_service + cameras.test_imagens_upload = 20/20 PASS
PILLOW = dependência técnica de upload; versão 12.3.0 disponível no venv integrado

INVENTORY_CAMERA_THUMBNAIL = APPROVED; SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = DEFERRED
THUMBNAIL_CURRENT_STATE = somente placeholder neutro; não há thumbnail real nem completude funcional
NO_MANUAL_UPLOAD_FALLBACK = YES
NO_PRIMARY_IMAGE_FALLBACK = YES
NO_SILENT_OLDER_CAPTURE_FALLBACK = YES

SECURE_IMAGE_PREVIEW_DELIVERY = REQUIRED / NOT_YET_AUTHORIZED
SECURE_IMAGE_PREVIEW_DELIVERY_STATUS = NEXT_CANDIDATE / NOT_AUTHORIZED
SECURE_IMAGE_PREVIEW_DELIVERY_CONSUMERS = Inventory thumbnail; CameraQuickDetailPanel
DELIVERY_ARCHITECTURE = ONE SECURE DELIVERY CONTRACT → MULTIPLE AUTHORIZED CONSUMERS
IMG-04 = NOT_AUTHORIZED
UI-3 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE

STORAGE_BACKEND_DEFINITIVE = DEFERRED
IMAGE_FORMAT_POLICY_DEFINITIVE = DEFERRED
UPLOAD_SIZE_LIMIT_POLICY_DEFINITIVE = DEFERRED
IMAGE_DIMENSION_LIMIT_POLICY_DEFINITIVE = DEFERRED
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED / FUTURE HARDENING
DETAILS = docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md and docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md

GIT_BASELINE = master; HEAD c79fa06775ccb707b6753f2a8ed0e988e8a9c86d; origin/master 547678de9c70ee9eda2fc30599417d217c878006; ahead 4 / behind 0 at activity start
GIT_WORKTREE_AFTER_DOCUMENTARY_RECONCILIATION = seis documentos permitidos modificados e unstaged; staging vazio
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS

Nesta reconciliação, os gates foram aceitos como evidência fornecida e não
reexecutados. Valide Git diretamente ao iniciar nova sessão; esta atividade
documental não autoriza implementação, staging, commit ou push.

## Checkpoint histórico — Secure Image Preview Delivery (2026-09-25)

Leia o checkpoint vigente completo em PROJECT_STATE.md; ele registra fatos
de segurança, decisões deferred, baseline Git e evidências. Os detalhes
técnicos HTTP permanecem em ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md.

SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED
TECHNICAL_COMMIT = e3f2d40
INTEGRATION_COMMIT = 7ca5f7c
INTEGRATION_GATE = PASS
INVENTORY_CAMERA_THUMBNAIL = APPROVED; SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
PREVIEW_VARIANTS = THUMB; PANEL; dimensões na authority de imagens, seção 24
UI-3 = NEXT_CANDIDATE / NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE

Naquele checkpoint, UI-3 ainda era candidata e deveria reutilizar a entrega
segura na variante PANEL. Esse estado foi supersedido pelo checkpoint vigente
abaixo.

ON_DEMAND_PREVIEW_COST_LOAD_BENCHMARK = DEFERRED / NOT BENCHMARKED
PERSISTENT_DERIVED_PREVIEW_CACHE_OR_CDN = NOT IMPLEMENTED / DEFERRED
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED
DEFINITIVE_STORAGE_BACKEND = DEFERRED
DEFINITIVE_MIME_SIZE_DIMENSION_POLICY = DEFERRED
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED
IMPLEMENTATION_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
ACTIVITY_COMPLETION_PERCENT = 100%
COMPLETION_BASIS = baseline validado; seis documentos reconciliados; git diff --check PASS; alterações unstaged prontas para adjudicação; sem commit, push ou publicação

## Checkpoint vigente — UI-3 pós-integração e aceitação visual pendente (2026-09-25)

Consulte `PROJECT_STATE.md` para baseline Git, evidências, invariantes, decisões
deferred, gates de segurança e estado completo do handoff. A authority UI-DS
define o gate obrigatório de aceitação visual; a authority de imagens preserva
o contrato técnico de preview e as decisões do domínio.

```text
BASELINE = master; HEAD 1015a8f0d7b6165ab057d81afb22007c3ae5e91b; origin/master 20be98d48ccfc19d458e393189168d9ecc93f309; ahead 2 / behind 0
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
UI-3_TECHNICAL_IMPLEMENTATION = COMPLETE; TECHNICAL_COMMIT = bcc7e7d
UI-3_INTEGRATION = COMPLETE; INTEGRATION_COMMIT = 1015a8f; INTEGRATION_GATE = PASS
UI-3_FUNCTIONAL_VALIDATION = PASS
UI-3_VISUAL_ACCEPTANCE = PENDING
UI-3_PRODUCT_ACCEPTANCE = PENDING
UI-3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PENDING
IMG-04 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-4 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
ON_DEMAND_PREVIEW_COST_LOAD_BENCHMARK = DEFERRED / NOT BENCHMARKED
PERSISTENT_DERIVED_PREVIEW_CACHE_OR_CDN = DEFERRED
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED
DEFINITIVE_STORAGE_BACKEND = DEFERRED
DEFINITIVE_MIME_SIZE_DIMENSION_POLICY = DEFERRED
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED / future hardening IMG-08
IMPLEMENTATION_AUTHORIZED = NO for further UI-3/IMG-04/UI-4 work
VISUAL_REPAIR_STARTED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
ACTIVITY_COMPLETION_PERCENT = 100%
COMPLETION_BASIS = sete documentos reconciliados; validação documental PASS; sem alteração de código/runtime, reexecução de testes, reparo visual, commit, push ou publicação
```

## Checkpoint atual — ARGOS UI V2 (2026-09-27)

Antes de qualquer ação, revalidar Git e ler `PROJECT_STATE.md`, seção 23;
`AGENT_CONTINUITY.md`, seção 19; e `ACTIVE_DOCUMENT_MAP.md`, seção 14. A nova
authority operacional é `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md`.

```text
UI_V2_TRACK_STATUS = DOCUMENTED / PARALLEL_TO_BACKEND
NEXT_UI_ACTIVITY = UI-V2-P0 — SCREEN CENSUS
NEXT_UI_ACTIVITY_STATUS = PLANNED / NOT_STARTED / NOT_AUTHORIZED_BY_THIS_DOCUMENT
IMPLEMENTATION_AUTHORIZED = NO
P0_EXECUTED_IN_PREVIOUS_ACTIVITY = NO
PHASE0_AND_BATCH_A = CLOSED / PRESERVED
BATCH_B_VISUAL_SCOPES = RETAINED / FLOW_THROUGH_APPROVED_PROTOTYPES
QUICK_DETAIL_VISUAL_BASELINE = APPROVED / PROTECTED
QUICK_DETAIL_REDRAW_WITHOUT_NEW_EXPLICIT_AUTHORIZATION = PROHIBITED
UI-3_PRODUCT_ACCEPTANCE = PENDING
```

Use `docs/projeto/ROADMAP_ARGOS_V5.md` para direção macro e
`docs/projeto/SPRINTS_ARGOS_V5.md` para a ordem. A auditoria e a diretriz CSS
continuam como evidência/guardrails, subordinadas ao master plan para o processo
de aprovação visual. As fases A2/A3/A4 permanecem; os resultados visuais seguem
P0–P7.

Git factual foi verificado antes da atividade documental: repository
`C:\Users\walac\desenvolvimento\projeto_argos`, branch `master`, baseline HEAD
`323bfb0856a0bedc2b1b17cb07cb60dbcdd7c816`, upstream
`origin/master` em `47c6965f3a60c0026117584dae21ca8a280986a5`, divergence `16/0`,
worktree limpo e staging vazio no preflight. A atividade deixou alterações
somente nos documentos identificados em `PROJECT_STATE.md`; staging permanece
vazio. Revalidar Git antes de qualquer operação consequencial.

`IMG-04` segue como candidata backend/imagens não autorizada registrada no mapa
de sprints. `MON-AVAIL-01` bloqueada por lacuna histórica e `MON-AVAIL-02`
recomendada foram informadas na instrução atual, não localizadas nos documentos
do checkout; a sequência backend permanece aberta e métricas não foram
fabricadas.

A reconciliação é documental. Não iniciar P0, protótipos ou implementação sem
instrução e autorização próprias.
