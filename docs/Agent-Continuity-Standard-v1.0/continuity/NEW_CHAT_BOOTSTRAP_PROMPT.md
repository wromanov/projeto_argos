# ARGOS — New Chat Bootstrap Prompt

STATUS = ACTIVE
PROJECT = ARGOS
LANGUAGE = pt-BR
FIRST_RESPONSE_MODE = READ_ONLY_CONTINUITY_REVALIDATION

Responda sempre em português do Brasil. Em nova conversa, primeiro leia
`AGENTS.md`, os quatro documentos de continuidade listados no mapa ativo, o
roadmap vigente, `docs/projeto/SPRINTS_ARGOS_V5.md`,
`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` e as authorities
aplicáveis; valide Git diretamente. Reconcilie os fatos atuais antes de qualquer
ação. Implementação ou outra ação Git consequencial futura exige autorização
própria.

## Recovery boundary

CONTINUITY_RECOVERY_GATE = NOT_PASSED
USER_CONTINUITY_VALIDATION = PENDING
READY_TO_RESUME_PROJECT = NO
IMPLEMENTATION = PROHIBITED UNTIL AUTHORIZED
EDIT = PROHIBITED UNTIL AUTHORIZED
STAGE = PROHIBITED UNTIL AUTHORIZED
COMMIT = PROHIBITED UNTIL AUTHORIZED
PUSH = PROHIBITED UNTIL AUTHORIZED
DEPLOY = PROHIBITED
PHASE_ADVANCEMENT = PROHIBITED UNTIL AUTHORIZED

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

A capacidade validada inclui estados estáveis UNKNOWN / ONLINE / OFFLINE; SUSPECT efêmero; STALE como dimensão de freshness; memória de confirmação persistente e streak pendente após restart; thresholds respeitados; restart sem transition/outage falsa; falha de banco distinta de câmera OFFLINE; CANCELLED neutro; timeouts e rede conforme semântica canônica; falhas operacionais sem histórico funcional falso e com recovery; ownership persistente por câmera, epoch monotônico, lease de takeover e fencing; config_generation independente; completion obsoleta sem side effects; observabilidade/configuração e logs sem secrets.

LEASE_EXPIRY_ALONE_INVALIDATES_COMPLETION = NO
NEWER_OWNERSHIP_EPOCH_INVALIDATES_COMPLETION = YES
ATTEMPT_MAX_DURATION_REQUIRED_FOR_CORRECTNESS = NO
LEASE_DURATION = janela operacional configurável de takeover
LEASE_RENEWAL_IMPLEMENTED = NO

## Roadmap e limites

NEXT_PROJECT_ACTIVITY = FASE C — Captura manual e gestão de imagens
NEXT_PROJECT_ACTIVITY_STATUS = PLANEJADA
NEXT_REQUIRED_ACTIVITY = UI-0 — READ-ONLY PREFLIGHT (UI-DS; após adjudicação humana e autorização)
NEXT_REQUIRED_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED

UI_DS = UI-0, UI-1, UI-2, UI-3, UI-4
UI_0 = read-only; relatório; stop após discovery
UI_1 = token/component adapter foundation
UI_2 = inventory visual retrofit
UI_3 = CameraQuickDetailPanel integrado ao fluxo canônico
UI_4 = QA visual/funcional/acessibilidade/interação

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
`HEAD = origin/master = 202e4f353551e7ab05667d86f9216cc102f351cc`, divergence
`0/0`, worktree clean e staging empty. O checkpoint técnico MON-09 em
`850efd2381d7f5b7df27e528dc3374ea58e507b3` é histórico; valide o estado atual e
o commit documental mais recente diretamente no Git antes de qualquer
conclusão. Não execute push sem autorização humana separada.

A Fase C permanece apenas planejada. `UI-0` é apenas a próxima atividade
preparatória recomendada e read-only; não inicia implementação visual. Qualquer
implementação futura exige escopo e autorização próprios. A conclusão MON-09
não altera gates ambientais nem declara homologation, deployment ou production
ready.
