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

## Estado técnico atual

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
CAMERA_QUICK_DETAIL_PANEL = ADOPT
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

## Roadmap e limites

NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_PROJECT_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
NEXT_REQUIRED_ACTIVITY = IMG-02 — Modelo, storage e proveniência (após adjudicação humana e autorização)
NEXT_REQUIRED_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION

UI_DS = UI-0, UI-1, UI-2, UI-3, UI-4
UI_0 = COMPLETE / PASS_WITH_FINDINGS; read-only; não autoriza implementação
UI_1 = token/component adapter foundation
UI_2 = inventory visual retrofit
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

O snapshot da baseline técnica antes desta atividade documental foi
`HEAD = origin/master = f4e88146c1146cdf04d657eb6e3cefa560639b61`, divergence
`0/0`, worktree clean e staging empty. O checkpoint técnico MON-09 em
`850efd2381d7f5b7df27e528dc3374ea58e507b3` é histórico; valide o estado atual e
o commit documental mais recente diretamente no Git antes de qualquer
conclusão. Não execute push sem autorização humana separada.

IMG-01 está concluída como checkpoint documental. A próxima atividade de
projeto é IMG-02 — Modelo, storage e proveniência, após adjudicação humana e
autorização própria; o contrato canônico enumera sete decisões abertas e
indica quando cada uma deve ser fechada. `UI-0` foi registrada como completa
com findings, em modo read-only, e não substitui IMG-02. Nenhuma dessas
indicações autoriza implementação automaticamente. A conclusão MON-09 não
altera gates ambientais nem declara homologation, deployment ou production
ready.
