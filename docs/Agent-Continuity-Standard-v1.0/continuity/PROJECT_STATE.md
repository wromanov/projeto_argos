# ARGOS — Project State

STATUS = CURRENT_SNAPSHOT
SNAPSHOT_DATE = 2026-09-27
PROJECT = ARGOS
STATE_SOURCE = verified Git checkpoint + UI-AUD-01 report + frontend remediation directive v1 + Phase 0 canonical closure + Batch A technical validation
PROJECT_STATE_UPDATE = PASS
SNAPSHOT_SCOPE = ARGOS UI REMEDIATION Batch A Phases 1–3 technically complete and visually accepted on a dedicated worktree; earlier checkpoints remain historical

## 1. Executive status

CURRENT_PHASE = FASE C — imagens e UI; ARGOS UI REMEDIATION Batch A = PASS / CANONICAL_INTEGRATION_PENDING
CURRENT_ACTIVITY = ARGOS UI REMEDIATION — FAST TRACK BATCH A / USER VISUAL ACCEPTANCE / PASS
LAST_COMPLETED_ACTIVITY = ARGOS UI REMEDIATION — PHASE 0 / CLOSED / canonical merge 9bdea6a; post-integration user visual acceptance PASS
LATEST_TECHNICAL_UI_ACTIVITY = UI-4A / TECHNICAL_IMPLEMENTATION_COMPLETE / VISUAL_ACCEPTANCE_PENDING
LAST_COMPLETED_PUBLISHED_ACTIVITY = MON-09 technical completion
LAST_PUBLISHED_BASELINE = 850efd2
CURRENT_CANONICAL_GIT_BASELINE = master @ be1adfb523c958d754e97f2dbf002aac65700b13; origin/master 47c6965f3a60c0026117584dae21ca8a280986a5; ahead 9 / behind 0 at Batch A start; canonical master unchanged by Batch A; revalidate Git on resume
NEXT_PROJECT_ACTIVITY = ARGOS UI REMEDIATION — FAST TRACK BATCH A / CANONICAL INTEGRATION; UI-3/UI-4A acceptance and IMG-04 authorization retain their separately recorded status
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
CURRENT_BASELINE_BEFORE_IMG02 = 05b710a57137f9d0cdefd256c037e4d86fe0e3bb

PROJECT_PROGRESS_LAST_VALID_PUBLISHED_ESTIMATE = 78% (HISTORICAL; NOT CURRENT)
MON08_PROGRESS_LAST_VALID_PUBLISHED_ESTIMATE = 15% (HISTORICAL; NOT CURRENT)
PROJECT_PROGRESS_UPDATE = NOT_RECALCULATED; percentual global continua sem fórmula aprovada
PROGRESS_BASIS = Percentuais históricos preservados sem interpretação como estado atual; não há fórmula/authority suficiente para recalcular.

## 2. Git baseline snapshot — before MON-09 documentary commit

REPOSITORY_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
BRANCH = master
HEAD = 850efd2381d7f5b7df27e528dc3374ea58e507b3
ORIGIN_MASTER = 850efd2381d7f5b7df27e528dc3374ea58e507b3
DIVERGENCE = ahead 0 / behind 0
WORKTREE_STATE = CLEAN
WORKTREE_CONTENTS = NONE
STAGING_STATE = EMPTY
SNAPSHOT_VALIDITY = TECHNICAL BASELINE BEFORE DOCUMENTARY COMMIT
REVALIDATE_AFTER_DOCUMENTARY_COMMIT = REQUIRED; Git posterior é a fonte de verdade

## 2.1 Git baseline snapshot — before current continuity/handoff documentary checkpoint

REPOSITORY_ROOT = C:\Users\walacedelgado\PycharmProjects\projeto_argos
BRANCH = master
HEAD = f4e88146c1146cdf04d657eb6e3cefa560639b61
ORIGIN_MASTER = f4e88146c1146cdf04d657eb6e3cefa560639b61
DIVERGENCE = ahead 0 / behind 0
WORKTREE_STATE = CLEAN
WORKTREE_CONTENTS = NONE
STAGING_STATE = EMPTY
SNAPSHOT_VALIDITY = BASELINE BEFORE CURRENT DOCUMENTARY ACTIVITY
REVALIDATE_AFTER_DOCUMENTARY_COMMIT = REQUIRED; Git posterior é a fonte de verdade

UI_DS_CANONICAL_SPEC = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
UI_DS_CANONICAL_SPRINT_MAP = docs/projeto/SPRINTS_ARGOS_V5.md
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES

## 3. Completed state

MON-07 = COMPLETE / PUBLISHED
Historical continuity snapshot after MON-08; superseded for current status by section 10 below.

MON-08A = PASS
MON-08B = PASS / PUBLISHED
MON08C_DISCOVERY_PREFLIGHT = PASS
MON08C1_NORMAL_PERSISTENCE = PASS
MON08C2_MASS_FAILURE = PASS
MON08C3_MASS_RECOVERY = PASS
MON08C4_RESTART_IDEMPOTENCY = PASS
MON08C5_STALE_GENERATION_CAS = PASS
MON08C_H1_HARNESS_DISCOVERY = PASS
MON08C_H2_HARNESS_REFACTOR = PASS

FAST_TEST_COUNT = 1
SCALE_TEST_COUNT = 4
FAST_DATASET_SIZE = 3
SCALE_DATASET_SIZE = 2300
DATASET_2300_CREATION_COUNT = 6 → 4
COMPLETION_CALLS_APPROX = 39101 → 27607
STRUCTURAL_REDUCTION_APPROX = 29.4%
MASS_FAILURE_RECOVERY_CONSOLIDATED = YES
FAST_TESTS = PASS — aproximadamente 0.067 s
REPRESENTATIVE_SCALE_TEST = PASS — 2300 ativos — aproximadamente 270.869 s
FULL_MON08C_RERUN = NOT_REQUIRED
GLOBAL_SUITE_RUN = NO
PRODUCTION_SOURCE_CHANGED = NO
CI_CHANGED = NO
SCHEMA_CHANGED = NO
CI_SCALE_OPT_IN = DEFERRED / NON-BLOCKING

MON08A_RESULT = PASS
MON08B_RESULT = PASS / PUBLISHED
MON08C_DISCOVERY = PASS
MON08C1 = PASS
MON08C2 = PASS
MON08C3 = PASS
MON08C4 = PASS
MON08C5 = PASS
MON08C_H1 = PASS
MON08C_H2 = PASS
MON08C6 = PASS / FINAL ADJUDICATION COMPLETE
MON08C_FINAL_VERDICT = PASS_WITH_FINDINGS
MON08C_COMPLETE = YES
MON08_TECHNICAL_VERDICT = PASS_WITH_FINDINGS
MON08_TECHNICALLY_COMPLETE = YES
NEXT_TECHNICAL_MON08_ACTIVITY = NONE
MON08_BLOCKERS = NONE
MON08_MAJOR = NONE
MON08_MINOR = NONE
NEW_MATERIAL_VALIDATION_REQUIRED_FOR_MON08_CLOSURE = NO
FUTURE_MATERIAL_VALIDATION_REQUIRED = YES
FUTURE_VALIDATION_SCOPE = production capacity; PostgreSQL; multi-instance / multi-worker; real network / firewall / VLAN; real cameras / credentials; formal resource/performance budgets

MON-07 published commits:
- 9bc5608 feat(monitoramento): criar camada canonica de leitura
- 766b35a feat(monitoramento): integrar leitura canonica na interface
- 079baee docs(monitoramento): encerrar mon-07 e direcionar mon-08

MON-07 final global suite = 695 PASS

MON-08C fast test = PASS — aproximadamente 0.067 s
MON-08C representative scale test = PASS — 2300 ativos — aproximadamente 270.869 s
MON-08C full rerun = NOT_REQUIRED
MON-08C global suite = NO
MON-08C diff check = PASS
MON-08C harness whitespace check = PASS
MON-08C Ruff = NOT_AVAILABLE; not installed

## 4. Historical MON-08 snapshot (superseded by section 10)

MON-08A = PASS
MON-08B = PASS / PUBLISHED
MON-08C = COMPLETE / PASS_WITH_FINDINGS
MON-08 = TECHNICALLY COMPLETE / PASS_WITH_FINDINGS

CONFIGURED_CONCURRENCY = 20
OBSERVED_MAX_IN_FLIGHT = 20
BOUNDED_CONCURRENCY = PASS
ASSET_COUNT = 2300
NORMAL_SCENARIO = PASS
MASS_FAILURE_SCENARIO = PASS
MASS_FAILURE_ROUNDS = 2
MASS_FAILURE_TOTAL_REQUESTS = 4600
MASS_FAILURE_TOTAL_RESULTS = 4600
MASS_FAILURE_TOTAL_MISSING = 0
MASS_FAILURE_TOTAL_DUPLICATES = 0
MASS_FAILURE_ROUND_1_OFFLINE = 0
MASS_FAILURE_ROUND_2_OFFLINE = 2300
MASS_RECOVERY_SCENARIO = PASS
MASS_RECOVERY_REQUESTS = 2300
MASS_RECOVERY_RESULTS = 2300
MASS_RECOVERY_ONLINE = 2300

REAL_NETWORK_USED = NO
ORM_USED = YES
REAL_DB_CAPACITY_VALIDATED = NO
MIGRATIONS = NONE
DEPENDENCIES = NONE

NEXT_PROJECT_ACTIVITY = MON-09 — Hardening operacional
NEXT_PROJECT_ACTIVITY_STATUS = NOT_STARTED
MON08C6_STATUS = COMPLETE / FINAL ADJUDICATION COMPLETE
MON08C6_IMPLEMENTATION_AUTHORIZATION = NOT_APPLICABLE
CHECKPOINT_STAGE_COMMIT_AUTHORIZATION = NO
PUSH = NOT_AUTHORIZED
BLOCKERS = 0
MAJOR = 0
MINOR = 0

CONFIRMATION_MEMORY_STABLE_RELOAD = PROVEN
CONFIRMATION_MEMORY_PENDING_STREAK_RESTART = NOT_VALIDATED / HARDENING_CANDIDATE
QUERY_VOLUME = PERFORMANCE_OBSERVATION / HARDENING_CANDIDATE
QUERY_VOLUME_OBSERVATION = aproximadamente 90.280 queries em aproximadamente 60.897 s para 2300 normal completions
QUERY_VOLUME_IS_MON08_FAILURE = NO
CI_SCALE_OPT_IN_ADJUDICATION = BACKLOG / NON-BLOCKING

VALIDATED_ENVELOPE = Django ORM; SQLite local; single instance; resultados de probe sintéticos/determinísticos; aproximadamente 2300 ativos; concorrência configurada e observada de 20; persistência integrada local; transições; indisponibilidades; restart/idempotência; stale generation/CAS; confirmation memory nos estados exercitados

NOT_VALIDATED_BOUNDARIES = PostgreSQL real; multi-instance; multi-worker; distributed lease; real network; real firewall/VLAN; real cameras; real credentials; production performance; production capacity

## 5. Historical recovery context

HISTORICAL_LOSS = the pre-formatting local MON-08B implementation was lost before stage/commit/push.
HISTORICAL_LOSS_SCOPE = prior implementation and its evidence only; it does not describe the current reconstructed files.
HISTORICAL_EVIDENCE = reference only; current PASS is based on the reconstructed implementation's validation and final independent review.

O harness MON-08C permanece untracked até o checkpoint controlado. Nenhum código
produtivo foi alterado pela H2; nenhum novo teste pesado é requerido por ritual.

## 6. Current project blockers and active decisions

PROJECT_BLOCKERS =
1. Homologation, deployment and production security gates remain blocked.
2. Real runtime/adapter/network execution remains unauthorized outside the validated local envelope.

DIVERGENCES = NONE_CURRENT
HISTORICAL_DIVERGENCE_D-01 = the earlier recovery snapshot reflected the lost local implementation; resolved by reconstructing, validating and independently reviewing the current implementation.

- DIRECT is the default; MULTIAGENT only with material demonstrable gain.
- Prompt generation follows Card A + Card B separation.
- Native-first for Skills/Plugins; NONE is valid.
- Plugin actual use requires user awareness/confirmation according to active policy.
- No automatic Git stage/commit/push.
- No real runtime, network, homologation, deployment or production execution is authorized by MON-08 technical completion.
- MON-08 technical completion does not authorize homologation, deployment or production.
- Hardening candidates and future boundaries do not block MON-08 closure.
- The lab reuses canonical contracts and does not alter production execution or persistence.

## 7. Current gates

CONTINUITY_PROTOCOL = ACTIVE
CONTINUITY_ADOPTION_MODE = RETROFIT_REQUIRED
CONTINUITY_RETROFIT_GATE = PASS
HANDOFF_PREPARATION_GATE = PASS

SECURITY_GATE_LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS
SECURITY_GATE_HOMOLOGATION = BLOCKED
SECURITY_GATE_DEPLOYMENT = BLOCKED
SECURITY_GATE_PRODUCTION = BLOCKED

MON08_EXECUTION_SCOPE = LOCAL_SYNTHETIC_LAB_ONLY
MON08_REAL_RUNTIME_AUTHORIZATION = NO
MON08_HOMOLOGATION_AUTHORIZED = NO
MON08_DEPLOYMENT_AUTHORIZED = NO
MON08_PRODUCTION_AUTHORIZED = NO

## 8. Atividade seguinte registrada no checkpoint histórico MON-08

NEXT_REQUIRED_ACTIVITY = MON-09 — Hardening operacional
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
CHECKPOINT_AUTHORIZED = NO

MON-08 está encerrada tecnicamente e não deve ser reaberta. A próxima atividade
deve aguardar escopo e autorização humana próprios.

## 9. Unverified items

UNVERIFIED_ITEMS =
- real database capacity and production SLA thresholds;
- current eligibility for future homologation/deployment/production security gates;
- future validation of PostgreSQL, multi-instance / multi-worker, real network / firewall / VLAN, real cameras / credentials and formal resource/performance budgets;
- post-checkpoint Git result, inclusive o novo HEAD, a ser obtido diretamente do Git;
- concrete scope and authorization for MON-09.

## 10. Deferred items

- CSV/PDF inventory export = DEFERRED
- HARDENING_TRANSITION_REAL = DEFERRED / NON-BLOCKING
- HARDENING_SCOPE_BATCH_NPLUS1 = DEFERRED / NON-BLOCKING
- SEC-R03 = FUTURE


## 10. Snapshot histórico após baseline técnica MON-09 — substituído pelos checkpoints das seções 12 e 13

Os status desta seção preservam o registro histórico daquele checkpoint. Para o
estado corrente, prevalecem o resumo executivo e os checkpoints IMG-01 e de
continuidade nas seções 12 e 13; fatos Git atuais devem ser revalidados no Git.

LAST_RELEVANT_CHECKPOINT = 850efd2381d7f5b7df27e528dc3374ea58e507b3 completo (850efd2)
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
MON-09A = COMPLETE / PASS
MON-09B = COMPLETE / PASS_WITH_SCOPE_DEVIATION
MON-09C = COMPLETE / PASS_WITH_FINDINGS
MON-09D = COMPLETE
MON-09E = COMPLETE / PASS
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_PROJECT_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED

BASELINE_GIT_SNAPSHOT_BEFORE_DOCUMENTARY_COMMIT: branch master; HEAD = 850efd2381d7f5b7df27e528dc3374ea58e507b3; origin/master = 850efd2381d7f5b7df27e528dc3374ea58e507b3; divergence = 0/0; worktree = CLEAN; staging = EMPTY. Este é o estado factual da baseline técnica antes do novo commit documental; o commit documental posterior será informado no relatório e revalidado diretamente no Git.

VALIDATED_ENVELOPE = UNKNOWN / ONLINE / OFFLINE como estados estáveis; SUSPECT efêmero; STALE como freshness; confirmation memory persistente; pending failure streak sobrevive restart; thresholds respeitados; restart sem transição/outage falsa; falha de banco não equivale a câmera offline; CANCELLED neutro; timeout/rede conforme semântica canônica; sem histórico funcional falso em falha operacional e com recovery possível; ownership por câmera, owner persistente e epoch monotônico; lease define elegibilidade operacional de takeover; epoch é fencing token; config_generation é independente; completion de owner obsoleto sem side effects de domínio; owner antigo não libera owner novo; completion válida libera ownership atomicamente; renovação de lease não implementada; MonitoringConfig integrado à configuração ARGOS, config inválida fail-fast; status, backlog/in-flight, falhas operacionais e ownership diagnosticáveis; observabilidade sem histórico funcional e logs sem secrets
LEASE_EXPIRY_ALONE_INVALIDATES_COMPLETION = NO
NEWER_OWNERSHIP_EPOCH_INVALIDATES_COMPLETION = YES
ATTEMPT_MAX_DURATION_REQUIRED_FOR_CORRECTNESS = NO
LEASE_DURATION = janela operacional configurável de takeover; não garante duração máxima do attempt
LEASE_RENEWAL_IMPLEMENTED = NO

FUTURE_VALIDATIONS = PostgreSQL real; multi-processo real em produção; rede real; câmeras reais; credenciais reais; capacidade produtiva; budgets formais de CPU, memória e conexões
LOG_VOLUME_HARDENING_STATUS = HARDENING / NON-BLOCKING — potencial volume elevado de logs INFO por ciclo/attempt
MON09B_C_ACCIDENTAL_SCALE_EXECUTIONS = OBSERVAÇÃO PROCESSUAL; NON-BLOCKING
SECURITY_GATES = LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS; HOMOLOGATION = BLOCKED; DEPLOYMENT = BLOCKED; PRODUCTION = BLOCKED
SECURITY_FINDINGS = preservar estados já documentados; não reabrir SEC-007 a SEC-010 nem mover SEC-001 a SEC-006 para MON-09
PRODUCTION_READINESS = NOT_ESTABLISHED

MON-09 está encerrada tecnicamente. Não criar/retomar atividade MON subsequente. Fase C é a próxima macrofase planejada no roadmap; qualquer implementação futura exige autorização própria.

## 11. Estado histórico da integração UI-DS no checkpoint IMG-02 + UI-1

UI_DS_STATUS = UI-1 COMPLETE / INTEGRATED; próximas slices permanecem sujeitas a autorização própria
UI_0 = COMPLETE / PASS_WITH_FINDINGS; READ_ONLY; NOT_IMPLEMENTATION_AUTHORIZATION
UI_1 = COMPLETE / INTEGRATED
UI_1_COMMIT = c5928e8
UI_2 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI_3 = PENDING; depende dos contratos e slices canônicas aplicáveis
UI_4 = PENDING; QA após integração aplicável
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS

A authority de UI-DS é docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md;
a ordem e os marcos estão em docs/projeto/SPRINTS_ARGOS_V5.md.
Os detalhes funcionais e visuais permanecem exclusivamente nessas authorities.

## 12. Estado histórico da Fase C no checkpoint IMG-02 + UI-1

IMG01_STATUS = COMPLETE / DOCUMENTAL
IMG02_STATUS = COMPLETE / INTEGRATED
IMG02_ACTIVITY_CLOSED = YES; limitada à slice aprovada e integrada
IMG02_IMPLEMENTATION_AUTHORIZATION = GRANTED_FOR_THIS_SLICE_ONLY; CONSUMED
IMG02_COMMIT = ceda8f6
LATEST_INTEGRATION_COMMIT = d5f1f54
CANONICAL_IMAGE_CONTRACT = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
STORAGE_REQUIREMENT = contrato persistente e abstração configurável antes da migration
PRODUCTION_STORAGE_BACKEND = DEFERRED
OPEN_DECISION_COUNT = 7; detalhes e fechamento permanecem no contrato canônico
FASE_C_COMPLETE = NO

## 13. Evidência de integração e candidatas no checkpoint IMG-02 + UI-1

UI1_STATUS = COMPLETE / INTEGRATED
UI1_COMMIT = c5928e8
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; cameras.test_imagens_read_service 13/13 PASS
IMG03_STATUS = NEXT_CANDIDATE / NOT_AUTHORIZED
UI2_STATUS = NEXT_CANDIDATE / NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
FEATURE_DETAILS_AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md and docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
SPRINT_ORDER_AUTHORITY = docs/projeto/SPRINTS_ARGOS_V5.md

## 14. Estado Git, handoff e autorização no checkpoint IMG-02 + UI-1

ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE
CONTINUITY_AUTHORITY = docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md
PROJECT_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
BASELINE_VERIFIED_AT = 2026-09-25
BRANCH = master
HEAD = d5f1f54bea518496d7e8c8b64487cfea459372f6
ORIGIN_MASTER = 05b710a57137f9d0cdefd256c037e4d86fe0e3bb
DIVERGENCE = ahead 3 / behind 0
WORKTREE = documentação deste checkpoint modificada e unstaged; staging vazio
CURRENT_ACTIVITY = reconciliação documental IMG-02 + UI-1 concluída; sem implementação ativa
ACTIVITY_COMPLETION_PERCENT = 100%
IMPLEMENTATION_AUTHORIZED = nenhuma autorização atual; autorização anterior IMG-02 consumida
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
SECURITY_GATES = LOCAL_DEVELOPMENT: RELEASED_WITH_CONTROLS; HOMOLOGATION: BLOCKED; DEPLOYMENT: BLOCKED; PRODUCTION: BLOCKED
BLOCKERS = nenhum blocker técnico na integração; IMG-03 e UI-2 requerem autorização independente
DEFERRED_ITEMS = backend definitivo de produção; demais decisões abertas do contrato de imagem; IMG-03; UI-2; UI-3; UI-4; validações futuras de ambiente/segurança
CURRENT_STATE_DISCOVERABLE = YES
CURRENT_BASELINE_DISCOVERABLE = YES
LAST_COMPLETED_ACTIVITY_DISCOVERABLE = YES
NEXT_ACTIVITY_DISCOVERABLE = YES; candidatas explicitadas como NOT_AUTHORIZED
CANONICAL_AUTHORITIES_DISCOVERABLE = YES
OPEN_DECISIONS_DISCOVERABLE = YES
IMPLEMENTATION_AUTHORIZATION_STATE_DISCOVERABLE = YES
SECURITY_OR_ENVIRONMENT_GATES_DISCOVERABLE = YES
NEW_AGENT_CAN_RESUME_WITHOUT_CHAT_HISTORY = YES
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS

## 15. Checkpoint histórico — integração IMG-03 + UI-2 (2026-09-25)

Este checkpoint supersede os resumos anteriores que apontam IMG-03 ou UI-2
como candidatas ainda não integradas. Git foi validado no início desta
reconciliação; o estado pós-edição é listado abaixo. Os gates técnicos abaixo
foram fornecidos como evidência para esta atividade e não foram reexecutados.

PROJECT_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
BASELINE_VERIFIED_AT = 2026-09-25
BRANCH = master
HEAD = c79fa06775ccb707b6753f2a8ed0e988e8a9c86d
ORIGIN_MASTER = 547678de9c70ee9eda2fc30599417d217c878006
DIVERGENCE = ahead 4 / behind 0
BASELINE_WORKTREE = CLEAN
BASELINE_STAGING = EMPTY
CURRENT_WORKTREE = somente os seis documentos desta reconciliação modificados e unstaged
CURRENT_STAGING = EMPTY

IMG-03 = COMPLETE / INTEGRATED
IMG-03_COMMIT = f6e08b60d289d4eecb54995daaa63979b123181f
IMG-03_INTEGRATION_COMMIT = 070879762017fafe196d585b92a4a05531144d27
IMG-03_FUNCTIONALITY = upload manual seguro integrado ao fluxo canônico
UI-2 = COMPLETE / INTEGRATED
UI-2_COMMIT = b57f959036ca085804063934a3b90a5b1a805cc9
UI-2_INTEGRATION_COMMIT = c79fa06775ccb707b6753f2a8ed0e988e8a9c86d
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; makemigrations --check --dry-run PASS (No changes detected); cameras.test_imagens_read_service + cameras.test_imagens_upload = 20/20 PASS
PILLOW = dependência técnica de upload; versão 12.3.0 disponível no venv integrado
MERGE_CONFLICTS_IMG03 = NONE
MERGE_CONFLICTS_UI2 = NONE

INVENTORY_CAMERA_THUMBNAIL = APPROVED
INVENTORY_THUMBNAIL_SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = DEFERRED
SECURE_THUMBNAIL_SOURCE_AVAILABLE_AT_UI2_INTEGRATION = NO
BLOCKING_DEPENDENCY = SECURE_IMAGE_PREVIEW_DELIVERY
INVENTORY_THUMBNAIL_CURRENT_STATE = apenas placeholder neutro; não há thumbnail real nem completude funcional
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
PLANNED != AUTHORIZED
DOCUMENTED != AUTHORIZED
NEXT_CANDIDATE != AUTHORIZED

STORAGE_BACKEND_DEFINITIVE = DEFERRED
IMAGE_FORMAT_POLICY_DEFINITIVE = DEFERRED
UPLOAD_SIZE_LIMIT_POLICY_DEFINITIVE = DEFERRED
IMAGE_DIMENSION_LIMIT_POLICY_DEFINITIVE = DEFERRED
CURRENT_REVERSIBLE_UPLOAD_DEFAULTS = 10 MiB; 20 milhões de pixels; JPEG; PNG; WebP estático
CURRENT_UPLOAD_DEFAULTS_ARE_PRODUCT_CONTRACT = NO
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED / não coberto no caminho atual; futuro hardening IMG-08
UPLOAD_REJECTION_AUDIT_EVIDENCE = evento registrado após upload aceito; rejeição atual retorna mensagem sem evento de auditoria
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED / FUTURE HARDENING
OPEN_IMAGE_DECISIONS = consultar docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md

CANONICAL_IMAGE_AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
CANONICAL_UI_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
SPRINT_ORDER_AUTHORITY = docs/projeto/SPRINTS_ARGOS_V5.md
CONTINUITY_AUTHORITY = docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md
SECURITY_GATES = LOCAL_DEVELOPMENT: RELEASED_WITH_CONTROLS; HOMOLOGATION: BLOCKED; DEPLOYMENT: BLOCKED; PRODUCTION: BLOCKED
DOCUMENTARY_RECONCILIATION_AUTHORIZED = YES
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
BLOCKERS_FOR_DOCUMENTARY_ACTIVITY = NONE
BLOCKERS_DISCOVERABLE = YES
PRODUCT_DEPENDENCY = secure preview delivery blocks real-data thumbnail wiring
NONBLOCKING_FINDING = audit de upload rejeitado permanece deferred para hardening
MAJOR_FINDINGS = NONE_CLASSIFIED
MAJOR_FINDINGS_DISCOVERABLE = YES
ACTIVITY_COMPLETION_PERCENT = 100%
RECOMMENDATION = PASS_WITH_FINDINGS
GIT_DIFF_CHECK = PASS
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS
CURRENT_STATE_DISCOVERABLE = YES
CURRENT_BASELINE_DISCOVERABLE = YES
LAST_COMPLETED_ACTIVITY_DISCOVERABLE = YES
NEXT_ACTIVITY_DISCOVERABLE = YES
CANONICAL_AUTHORITIES_DISCOVERABLE = YES
OPEN_DECISIONS_DISCOVERABLE = YES
BLOCKERS_AND_DEFERRED_ITEMS_DISCOVERABLE = YES
DEFERRED_ITEMS_DISCOVERABLE = YES
IMPLEMENTATION_AUTHORIZATION_STATE_DISCOVERABLE = YES
SECURITY_OR_ENVIRONMENT_GATES_DISCOVERABLE = YES
NEW_AGENT_CAN_RESUME_WITHOUT_CHAT_HISTORY = YES

## 16. Checkpoint histórico — Secure Image Preview Delivery (2026-09-25)

Este snapshot reconcilia o estado integrado em 7ca5f7c. O gate técnico
abaixo foi fornecido como evidência validada da integração e não foi
reexecutado nesta atividade documental.

```text
BASELINE_VALIDATED = YES
PROJECT_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
BRANCH = master
HEAD = 7ca5f7c9c7dda8d66754406be4d351071612aa92
ORIGIN_MASTER = c32ccc2836313fcb58a31f096f71aa9502cbc7f9
DIVERGENCE = ahead 2 / behind 0
BASELINE_WORKTREE = CLEAN
BASELINE_STAGING = EMPTY
CURRENT_WORKTREE = seis documentos compartilhados permitidos, modificados e unstaged
CURRENT_STAGING = EMPTY
SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED
TECHNICAL_COMMIT = e3f2d40
INTEGRATION_COMMIT = 7ca5f7c
INTEGRATION_GATE = PASS
MERGE_CONFLICTS = NONE
INTEGRATION_VALIDATION = manage.py check PASS; makemigrations --check --dry-run PASS / no changes; cameras.test_imagens_read_service + cameras.test_imagens_upload + cameras.test_imagens_preview = 28/28 PASS
VALIDATION_EVIDENCE = fornecida para esta reconciliação; gates não reexecutados
INVENTORY_CAMERA_THUMBNAIL = APPROVED
INVENTORY_THUMBNAIL_SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
PREVIEW_VARIANTS = THUMB; PANEL; dimensões e contrato técnico em ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md, seção 24
PREVIEW_DELIVERY_AUTHENTICATION_AUTHORIZATION = REQUIRED; permission atual = cameras.view_camera
STORAGE_KEY_OR_PATH_EXPOSED_TO_CLIENT = NO
PRIVATE_MEDIA_MADE_PUBLIC = NO
LATEST_PREVIEW_PROVENANCE = CAPTURA_CAMERA only
FALLBACK_TO_UPLOAD_MANUAL_PRIMARY_IMAGE_OR_OLDER_CAPTURE = NO
CAPTURE_SIDE_EFFECT = NONE
INVENTORY_HTML_READS_IMAGE_BYTES_OR_STORAGE = NO
INVENTORY_PREVIEW_FETCH = browser lazy request
CACHE_CONTROL = no-store
CAMERA_QUICK_DETAIL_PANEL = USER_APPROVED; UI-3 deve reutilizar a entrega segura existente com PANEL; layout aprovado e detalhes em ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md, seção 7.3
UI-3 = NEXT_CANDIDATE / NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
IMPLEMENTATION_AUTHORIZED = NO
ON_DEMAND_PREVIEW_COST_LOAD_BENCHMARK = DEFERRED / NOT BENCHMARKED
PERSISTENT_DERIVED_PREVIEW_CACHE_OR_CDN = NOT IMPLEMENTED / DEFERRED
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED
DEFINITIVE_STORAGE_BACKEND = DEFERRED
DEFINITIVE_MIME_SIZE_DIMENSION_POLICY = DEFERRED
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED / future hardening IMG-08
DETAIL_ONCE_REFERENCE_MANY = YES; detalhes técnicos HTTP e limites operacionais ficam na authority de imagens
DEFERRED_ITEMS = custo on-demand não benchmarked; cache persistente/CDN; matriz final de permissões; backend definitivo; políticas definitivas de MIME/tamanho/dimensões; hardening de auditoria de rejeições de upload
BLOCKERS = NONE
RECOMMENDATION = PASS_WITH_FINDINGS
SECURITY_GATES = LOCAL_DEVELOPMENT: RELEASED_WITH_CONTROLS; HOMOLOGATION: BLOCKED; DEPLOYMENT: BLOCKED; PRODUCTION: BLOCKED
DOCUMENTARY_RECONCILIATION_AUTHORIZED = YES
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
ACTIVITY_COMPLETION_PERCENT = 100%
COMPLETION_BASIS = baseline validado; seis documentos reconciliados; git diff --check PASS; alterações unstaged prontas para adjudicação; sem commit, push ou publicação
GIT_DIFF_CHECK = PASS
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS
CONTINUITY_DISCOVERABILITY = YES; status, commits, fatos de segurança, decisões deferred, authorities e autorização recuperáveis sem histórico de chat
```

## 17. Checkpoint histórico — UI-3 pós-integração e aceitação visual pendente (2026-09-25)

Este snapshot registra a integração técnica da UI-3 e distingue validação
funcional de aceitação visual/produto. A evidência de integração abaixo foi
fornecida para esta reconciliação documental; os testes não foram reexecutados.

```text
BASELINE_VALIDATED = YES
PROJECT_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
BRANCH = master
HEAD = 1015a8f0d7b6165ab057d81afb22007c3ae5e91b
ORIGIN_MASTER = 20be98d48ccfc19d458e393189168d9ecc93f309
DIVERGENCE = ahead 2 / behind 0
BASELINE_WORKTREE = CLEAN
BASELINE_STAGING = EMPTY
CURRENT_WORKTREE = sete documentos autorizados modificados e unstaged
CURRENT_STAGING = EMPTY
FILES_CHANGED = ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md; ROADMAP_ARGOS_V5.md; SPRINTS_ARGOS_V5.md; PROJECT_STATE.md; AGENT_CONTINUITY.md; ACTIVE_DOCUMENT_MAP.md; NEW_CHAT_BOOTSTRAP_PROMPT.md
CODE_OR_RUNTIME_CHANGED = NO
UI-3_TECHNICAL_IMPLEMENTATION = COMPLETE
UI-3_TECHNICAL_COMMIT = bcc7e7d03b14d233499e1d5fcb97a8e6a9e2a8ea
UI-3_INTEGRATION = COMPLETE
UI-3_INTEGRATION_COMMIT = 1015a8f0d7b6165ab057d81afb22007c3ae5e91b
INTEGRATION_GATE = PASS
MERGE_CONFLICTS = NONE (evidence supplied)
INTEGRATION_VALIDATION = manage.py check PASS; makemigrations --check --dry-run PASS / no changes; 32/32 tests PASS across cameras.test_quick_detail, cameras.test_imagens_read_service, cameras.test_imagens_upload, cameras.test_imagens_preview; evidence supplied, not re-executed
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
UI-3_FUNCTIONAL_VALIDATION = PASS
UI-3_VISUAL_QA_EVIDENCE = 390, 1293, 1920, 2560 px; no horizontal overflow; no relevant JavaScript console errors (evidence supplied)
UI-3_VISUAL_ACCEPTANCE = PENDING / explicit user approval not recorded
UI-3_PRODUCT_ACCEPTANCE = PENDING
UI-3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PENDING
CAMERA_QUICK_DETAIL_PANEL = operational; canonical details in ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
PANEL_PREVIEW = Secure Image Preview Delivery / PANEL 640x448 / LATEST_CAMERA_CAPTURE
LATEST_CAMERA_CAPTURE = no fallback to UPLOAD_MANUAL, PRIMARY_IMAGE or older capture
PANEL_OPEN_SIDE_EFFECTS = no new capture; no monitoring mutation
MONITORING_INTEGRATION = MonitoringReadService reused; camera availability remains separate from image capture success
ACCESSIBILITY_INTERACTION = accessible row control; native dialog focus containment; initial focus managed; Escape closes; focus restored to trigger; formal UI-4 QA not authorized
ASYNC_RACE_PROTECTION = AbortController + request identity fencing
PERFORMANCE_FINDING = 6 queries in measured case; test limit 7; on-demand load benchmark deferred
IMG-04 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-4 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
ON_DEMAND_PREVIEW_COST_LOAD_BENCHMARK = DEFERRED / NOT BENCHMARKED
PERSISTENT_DERIVED_PREVIEW_CACHE_OR_CDN = DEFERRED
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED
DEFINITIVE_STORAGE_BACKEND = DEFERRED
DEFINITIVE_MIME_SIZE_DIMENSION_POLICY = DEFERRED
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED / future hardening IMG-08
OPEN_IMAGE_DECISIONS = 7; details in ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
DETAIL_ONCE_REFERENCE_MANY = YES; implementation/UI details in UI-DS authority; preview details and image decisions in image contract
VISUAL_REPAIR_STARTED = NO
DOCUMENTARY_RECONCILIATION_AUTHORIZED = YES
IMPLEMENTATION_AUTHORIZED = NO for further UI-3/IMG-04/UI-4 work
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
BLOCKERS = UI-3 visual/product acceptance pending; no blocker to this documentary reconciliation
RECOMMENDATION = PASS_WITH_FINDINGS
SECURITY_GATES = LOCAL_DEVELOPMENT: RELEASED_WITH_CONTROLS; HOMOLOGATION: BLOCKED; DEPLOYMENT: BLOCKED; PRODUCTION: BLOCKED
ACTIVITY_COMPLETION_PERCENT = 100%
COMPLETION_BASIS = seven authorized documents reconciled; git diff --check PASS; changes unstaged; no code/runtime changes, tests re-executed, visual repair, commit, push or publication
GIT_DIFF_CHECK = PASS
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS
CONTINUITY_DISCOVERABILITY = YES; baseline, statuses, commits, acceptance gate, deferred decisions, next candidate, authorities and authorization recoverable without chat history
```

## 18. Checkpoint histórico — UI-4A Desktop Shell Density Foundation (2026-09-26)

Este checkpoint autoriza e registra somente a base geométrica global do shell.
A aceitação visual do usuário continua pendente; a seção 17 permanece como
histórico e seus bloqueios de UI-4 foram supersedidos apenas para UI-4A.

```text
PROJECT_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
BRANCH = master
HEAD = cad076099258e96b13f9e5ef11b301fc68891c4d
ORIGIN_MASTER = 47c6965f3a60c0026117584dae21ca8a280986a5
DIVERGENCE = ahead 3 / behind 0
UI-4A_USER_AUTHORIZED = YES
UI-4A_SCOPE = shell geometry: content max-width/centering, sidebar, topbar, shell gutters
UI-4A_TECHNICAL_IMPLEMENTATION = COMPLETE
UI-4A_VISUAL_ACCEPTANCE = PENDING_USER
BASELINE_VIEWPORT = 2552x866 px; browser zoom 100%
MAIN_CONTENT_MAX_WIDTH = 2304px -> 1400px
MAIN_CONTENT_RENDERED_WIDTH = 2224px -> 1400px at 2552x866
SIDEBAR_WIDTH = 248px -> 164px
TOPBAR_HEIGHT = 60px baseline -> 40px token / 42px rendered
PAGE_TOP_SPACING = 40px -> 32px at wide viewport
PAGE_BOTTOM_SPACING = 48px -> 40px
CONTENT_CENTERED = YES; main and topbar share the centered 1400px width
EXCESSIVE_HORIZONTAL_STRETCH = NO
SIDEBAR_BRAND_CLIPPED = NO; ARGOS and Central operacional fit
DASHBOARD_LAYOUT_REGRESSION = NO; grids and existing card geometry unchanged
DASHBOARD_LAYOUT_AT_2552 = inventory 5 columns; monitoring 3 columns with the fourth card in row 2; quality 3 columns; activity 2 columns
INVENTORY_FILTER_LAYOUT_AFTER_SHELL_CHANGE = ONE_ROW at 2552x866; labels may wrap
INVENTORY_FILTER_LAYOUT_AT_SMALLER_VIEWPORTS = TWO_ROWS at 1366x768; responsive reflow retained at 900x768 and 390x844
INVENTORY_LAYOUT_REGRESSION = YES finding: table-region has a 2px local horizontal scroll at 2552x866 and 7px at 1366x768; baseline attribution is unverified
HORIZONTAL_OVERFLOW = YES only inside table-region; document/root has no horizontal overflow at tested sizes
BREAKPOINT_REGRESSION_FOUND = NO; existing 64rem, 56rem, 44rem and 30rem rules retained; mobile nav remains internally scrollable
QUICK_DETAIL_MODIFIED_BY_UI4A = NO; pre-existing UI-3 diff in static/css/inventario.css preserved byte-for-byte during UI-4A
FILES_MODIFIED_BY_UI4A = static/css/argos.css; static/css/design-system.css (shell tokens only)
PREEXISTING_WORKTREE_DIFF = static/css/inventario.css (UI-3 Drawer); unchanged by UI-4A
RESPONSIVE_VISUAL_QA = 2552x866; 1366x768; 900x768; 390x844 at 100%
DJANGO_CHECK = PASS; System check identified no issues
GIT_DIFF_CHECK = PASS
BROWSER_CONSOLE_ERRORS = NONE observed
CURRENT_WORKTREE = static/css/argos.css; static/css/design-system.css; static/css/inventario.css; continuity checkpoint files; all unstaged
CURRENT_STAGING = EMPTY
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
READY_FOR_USER_VISUAL_REVIEW = YES
ACTIVITY_COMPLETION_PERCENT = 95%
ACTIVITY_COMPLETE = NO; UI-4A visual acceptance pending
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
UI-4B / UI-4C / UI-4D / UI-4E = NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
IMPLEMENTATION_AUTHORIZED = NO after the UI-4A shell slice
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
PROJECT_STATE_UPDATE = PASS
CONTINUITY_DISCOVERABILITY = YES
FINAL_VERDICT = TECHNICAL IMPLEMENTATION COMPLETE WITH LOCAL TABLE-SCROLL FINDING; READY FOR USER VISUAL REVIEW
```

A folga de 4px no max-width foi testada e revertida: a diferença de 2px entre
`.table-region` e a tabela acompanhou a largura do shell. Corrigir a barra
exigiria alterar a tabela ou um override específico, ambos fora deste slice.
A barra local permanece registrada para UI-4D; não há overflow horizontal no
root da página. Nenhum filtro, tabela, card, controle, tipografia, spacing
primitivo ou Quick Detail foi editado nesta atividade.

## 19. Frente documental UI-AUD-01 e remediação estrutural (2026-09-27)

O relatório `docs/frontend/ARGOS_FRONTEND_AUDIT_REPORT.md` concluiu
`STRUCTURAL_REFACTOR_RECOMMENDED`, sem implementação pela auditoria. A diretriz
`docs/frontend/ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md` foi recebida como
orientação técnica da frente de UI, subordinada às authorities do projeto e às
decisões do usuário. Preservar Django SSR, Templates, HTML semântico, CSS
customizado, JavaScript Vanilla, progressive enhancement, `<dialog>` nativo e o
Design System próprio. `NEW_VISUAL_PATCHES = FROZEN UNTIL REMEDIATION PHASES`.

O checkout principal `master` tinha exatamente cinco arquivos modificados e
nada staged/untracked antes do checkpoint: `AGENT_CONTINUITY.md`,
`PROJECT_STATE.md`, `argos.css`, `design-system.css`, `inventario.css`. O delta
incluía UI-4A no shell, densidade de controles e a compactação recente do
Quick Detail em `@media(max-height:800px)`, com `:has()` afetando o shell. Os
cinco arquivos foram preservados sem descarte no commit local `768844d`; esse
commit é checkpoint, não aceitação visual. Nenhum push foi feito.

```text
UI-AUD-01 = COMPLETE / STRUCTURAL_REFACTOR_RECOMMENDED
FRONTEND_REMEDIATION_DIRECTIVE_V1 = RECEIVED / TECHNICAL_GUIDANCE
STRUCTURAL_FRONTEND_REMEDIATION = NOT_STARTED
SEQUENCE = Phase 0 dead/defeated CSS; Phase 1 ownership; Phase 2 shell;
           Phase 3 shared density; Phase 4 inventory; Phase 5 dashboard;
           Phase 6 Quick Detail; final cross-viewport regression
NEXT_ACTIVITY = Phase 0 / PLANNED / NOT_STARTED
PHASE_0_GATE = COMPUTED_STYLE_DELTA NONE; VISUAL_DELTA NONE;
               FUNCTIONAL_DELTA NONE; CSS_COMPLEXITY_REDUCED YES
QUICK_DETAIL = UI-3 INTEGRATED / VISUAL_AND_PRODUCT_ACCEPTANCE_PENDING
QUICK_DETAIL_COMPACT_HEIGHT_CSS = CHECKPOINTED / NOT_VISUALLY_ACCEPTED
IMG-DISPLAY-01 = INTEGRATED / merge cad0760; fallback contract in
                 docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md section 25
UI_UX_FRONTEND_CONTINUITY = USER_WILL_CONTINUE_WITH_THIS_AGENT
IMPLEMENTATION_AUTHORIZED_FOR_PHASE_0 = NO; documentary opening only
PUSH_AUTHORIZED = NO
PROJECT_STATE_UPDATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS
```

No Quick Detail, o usuário preserva três cards full width em coluna, quatro
informações em cada card, inclusive Ambiente, sem remover conteúdo. O alvo de
2048×741 sem scroll interno continua requisito de avaliação, não aceite
comprovado. A auditoria atribuiu o scroll a fatores locais e compartilhados,
predominantemente locais. A limpeza do drawer pertence à Phase 6. O
IMG-DISPLAY-01 já está integrado no código; este registro não equivale a nova
validação funcional ou visual nesta frente. Antes da Phase 0, estabelecer
baseline no mesmo checkout e medir computed styles, overflow e screenshots.

Correção factual ao checkpoint histórico UI-4A: ele cita sidebar de 164 px;
o token CSS no checkout e a medição da UI-AUD-01 apontam 192 px. Para a
remediação, usar 192 px como baseline atual e medir novamente no runtime.

## 20. Phase 0 — dead CSS / defeated rules cleanup (2026-09-27)

A execução foi autorizada pelo usuário no baseline limpo `master @ c210fe6` e
realizada no worktree dedicado abaixo, sem reutilizar ou alterar o worktree
`codex/ui-03-visual-completion`. A implementação técnica foi registrada no commit `7b938a33b3c6192b8294da98decd7b245c27d8db`; o estado Git abaixo é o checkpoint anterior a esta reconciliação documental.

```text
CANONICAL_WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos
PHASE0_WORKTREE = C:\Users\walac\.codex\worktrees\argos-ui-remediation-phase-0\projeto_argos
BRANCH = codex/ui-remediation-phase-0
HEAD = 7b938a33b3c6192b8294da98decd7b245c27d8db (pré-reconciliação documental)
UPSTREAM = NONE
DJANGO_BASE_DIR = C:\Users\walac\.codex\worktrees\argos-ui-remediation-phase-0\projeto_argos
RUNTIME_SOURCE = PHASE0_WORKTREE / http://127.0.0.1:8010
RUNTIME_PROVENANCE = PASS; SHA-256 do inventario.css servido coincidiu com o arquivo do worktree em todos os viewports
BROWSER = Microsoft Edge headless; zoom/deviceScaleFactor 100%/1
VIEWPORTS = 2552x866; 2048x914; 1920x1080; 1366x768; 900x768; 390x844
```

### Finding P0-001 — larguras históricas por nth-child

```text
SYMPTOM = oito regras antigas distribuíam largura entre até nove colunas, enquanto a tabela atual usa sete colunas e colgroup semântico
ROOT_CAUSE = camada histórica anterior à composição atual da camera-table
EVIDENCE = os seletores posteriores .camera-table.data-table th/td anulavam width e o colgroup atual definia as larguras vencedoras; computed styles e screenshots permaneceram idênticos após remoção
WINNING_RULE = .camera-table.data-table th/td e .camera-table__col--*
CONFLICTING_RULES = .camera-table th/td:nth-child(1..9)
OWNER_CURRENT = inventario.css
OWNER_EXPECTED = inventario.css / camera-table colgroup
AFFECTED_COMPONENTS = tabela do Inventário
SEVERITY = LOW
FIX_CLASS = REMOVE
FILES_EXPECTED = static/css/inventario.css
REGRESSION_RISK = LOW
VALIDATION_GATE = PASS em seis viewports
```

### Finding P0-002 — sequência de min-width 62rem para 64rem

```text
SYMPTOM = dois mínimos de 62rem permaneciam antes do mínimo canônico posterior de 64rem
ROOT_CAUSE = evolução incremental da tabela sem remoção das versões anteriores
EVIDENCE = a regra posterior idêntica de 64rem vence no desktop; abaixo de 75rem a composição posterior aplica min-width:0; 62rem nunca venceu na matriz
WINNING_RULE = .camera-table.data-table { min-width:64rem } ou @media(max-width:75rem) { min-width:0 }
CONFLICTING_RULES = min-width:62rem base e dentro de @media(max-width:56rem)
OWNER_CURRENT = inventario.css
OWNER_EXPECTED = inventario.css / composição responsiva da camera-table
AFFECTED_COMPONENTS = tabela do Inventário
SEVERITY = LOW
FIX_CLASS = REMOVE
FILES_EXPECTED = static/css/inventario.css
REGRESSION_RISK = LOW
VALIDATION_GATE = PASS em seis viewports
```

### Finding P0-003 — padding, tipografia e layout anteriores da tabela

```text
SYMPTOM = declarações antigas de padding, sizing, overflow, tipografia e hover continuavam antes das regras Visual 2A/UI posteriores
ROOT_CAUSE = camadas de estilo preservadas após reescrita do componente
EVIDENCE = seletores posteriores de mesma ou maior especificidade definiam os mesmos computed styles; comparação não encontrou qualquer diferença de estilo ou geometria
WINNING_RULE = blocos .camera-table.data-table posteriores e tratamento visual final da tabela
CONFLICTING_RULES = blocos iniciais .camera-table, th, td, caption e tr:hover
OWNER_CURRENT = inventario.css
OWNER_EXPECTED = inventario.css / bloco atual da camera-table
AFFECTED_COMPONENTS = tabela do Inventário
SEVERITY = LOW
FIX_CLASS = REMOVE
FILES_EXPECTED = static/css/inventario.css
REGRESSION_RISK = LOW
VALIDATION_GATE = PASS em seis viewports
```

### Finding P0-004 — larguras de colunas substituídas

```text
SYMPTOM = sete regras antigas de .camera-table__col--* precediam outra definição completa das mesmas classes
ROOT_CAUSE = versão anterior do dimensionamento preservada na cascata
EVIDENCE = regras posteriores com os mesmos seletores venciam por ordem; larguras computadas e overflow permaneceram idênticos
WINNING_RULE = segundo conjunto .camera-table__col--status/camera/location/network/equipment/governance/actions
CONFLICTING_RULES = primeiro conjunto das mesmas classes
OWNER_CURRENT = inventario.css
OWNER_EXPECTED = inventario.css / único conjunto de colunas
AFFECTED_COMPONENTS = tabela do Inventário
SEVERITY = LOW
FIX_CLASS = REMOVE
FILES_EXPECTED = static/css/inventario.css
REGRESSION_RISK = LOW
VALIDATION_GATE = PASS em seis viewports
```

### Finding P0-005 — overflow duplicado do inventory panel

```text
SYMPTOM = regra isolada repetia overflow:hidden já definido no bloco canônico anterior
ROOT_CAUSE = duplicação histórica exata
EVIDENCE = mesmo seletor e mesmo valor; remoção não alterou computed style
WINNING_RULE = bloco inicial .inventory-panel
CONFLICTING_RULES = segundo bloco isolado .inventory-panel
OWNER_CURRENT = inventario.css
OWNER_EXPECTED = inventario.css / bloco base do painel
AFFECTED_COMPONENTS = painel de resultados do Inventário
SEVERITY = LOW
FIX_CLASS = CONSOLIDATE
FILES_EXPECTED = static/css/inventario.css
REGRESSION_RISK = LOW
VALIDATION_GATE = PASS em seis viewports
```

### Finding P0-006 — mínimo antigo do summary

```text
SYMPTOM = min-height:2.75rem precedia a definição posterior baseada em --control-height-default
ROOT_CAUSE = migração incompleta para o contrato de controle atual
EVIDENCE = a mesma classe posterior vence por ordem; computed min-height permaneceu 36px no desktop e 44px no mobile
WINNING_RULE = .filter-multiselect__summary { min-height:var(--control-height-default) } e contrato touch de maior especificidade
CONFLICTING_RULES = .filter-multiselect__summary { min-height:2.75rem }
OWNER_CURRENT = argos.css
OWNER_EXPECTED = contrato atual do multiselect
AFFECTED_COMPONENTS = summaries dos filtros
SEVERITY = LOW
FIX_CLASS = REMOVE
FILES_EXPECTED = static/css/argos.css
REGRESSION_RISK = LOW
VALIDATION_GATE = PASS em seis viewports
```

### Finding P0-007 — preview antigo e regra duplicada do loading frame

```text
SYMPTOM = preview/imagem antigos eram integralmente substituídos pela seção UI-3; o loading frame aparecia em duas regras consecutivas
ROOT_CAUSE = reescrita visual adicionada sem retirada da versão anterior e fragmentação do mesmo seletor
EVIDENCE = seção UI-3 posterior definiu min-height, alinhamento, fundo e imagem; as duas regras de loading foram unidas sem mudar valores; computed styles e screenshots do drawer ficaram idênticos
WINNING_RULE = seção UI-3 .camera-quick-detail__preview e .camera-quick-detail__image-frame
CONFLICTING_RULES = três regras antigas do preview/img e duas regras consecutivas do loading frame
OWNER_CURRENT = inventario.css
OWNER_EXPECTED = inventario.css / seção delimitada do Quick Detail
AFFECTED_COMPONENTS = Quick Detail preview
SEVERITY = LOW
FIX_CLASS = REMOVE / CONSOLIDATE
FILES_EXPECTED = static/css/inventario.css
REGRESSION_RISK = LOW
VALIDATION_GATE = PASS em seis viewports
```

### Candidatos analisados e adiados

```text
P0-D01 = @media(min-width:144rem) com 11 colunas; ainda altera layout; DEFERRED_TO_PHASE_4
P0-D02 = !important da identidade do Quick Detail; ainda participa da cascata; DEFERRED_TO_PHASE_6
P0-D03 = @media(max-height:800px) e :has() do drawer/shell; comportamento ativo; DEFERRED_TO_PHASE_6
```

```text
PHASE0_TECHNICAL_IMPLEMENTATION = PASS
PHASE0_USER_VISUAL_REVIEW = PASS
PHASE0_LOCAL_CHECKPOINT = PASS
PHASE0_DOCUMENTATION_RECONCILIATION = PASS
BASELINE_HEAD = c210fe62f49ec2ba259b0d3a64a1f6ea1e6fdf83
IMPLEMENTATION_COMMIT = 7b938a33b3c6192b8294da98decd7b245c27d8db
REVIEW_RECONCILIATION_COMMIT = baa51c61a942a1387990f73fea98b367568167c1
CANONICAL_MERGE_COMMIT = 9bdea6a9f39a908a2f19b33b8132102631868066
PHASE0_CANONICAL_CODE_INTEGRATION = PASS
POST_INTEGRATION_VISUAL_GATE = PASS
USER_POST_INTEGRATION_ACCEPTANCE = PASS
PHASE0_CANONICAL_CLOSURE = PASS
PHASE0_STATUS = CLOSED
PHASE1 = READY_NOT_STARTED
NEXT_ACTIVITY = ARGOS UI REMEDIATION — PHASE 1 / CSS OWNERSHIP CONSOLIDATION
ACTIVITY_COMPLETION_PERCENT = 100%
FILES_MODIFIED = static/css/argos.css; static/css/inventario.css; docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md
CSS_RULE_COUNT_BEFORE = 1060
CSS_RULE_COUNT_AFTER = 1035
RULES_REMOVED = 24
RULES_CONSOLIDATED = 1
AUTHORED_DECLARATIONS_REMOVED_NET = 46
CSSOM_DECLARATION_ENTRIES_BEFORE = 8081
CSSOM_DECLARATION_ENTRIES_AFTER = 7999
SELECTORS_REMOVED = 35
COMPUTED_STYLE_DELTA = NONE
GEOMETRY_DELTA = NONE
VISUAL_DELTA = NONE; 12/12 screenshots finais byte a byte idênticas às baselines
FUNCTIONAL_DELTA = NONE; abertura, foco inicial, Escape e retorno de foco PASS nos seis viewports
DJANGO_CHECK = PASS; System check identified no issues
GIT_DIFF_CHECK = PASS
STAGING = EMPTY
TECHNICAL_COMMIT = 7b938a33b3c6192b8294da98decd7b245c27d8db
PUSH = NOT_PERFORMED
PROJECT_STATE_UPDATE = PASS
FINAL_VERDICT = ARGOS UI REMEDIATION PHASE 0 CLOSED; CANONICAL INTEGRATION AND POST-INTEGRATION USER VISUAL ACCEPTANCE PASS; PHASE 1 READY_NOT_STARTED
```

## 21. ARGOS UI REMEDIATION — Fast Track Batch A (2026-09-27)

Este é o checkpoint vigente da remediação UI. Os registros anteriores deste
documento são históricos quando apontam a Phase 1 como ainda não iniciada.
O usuário autorizou execução direta das Phases 1, 2 e 3, commits locais por
fase e commit documental, sem push, merge ou início do Batch B.

```text
BASELINE_HEAD = be1adfb523c958d754e97f2dbf002aac65700b13
CANONICAL_WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos
CANONICAL_BRANCH = master
CANONICAL_HEAD_AT_START = be1adfb523c958d754e97f2dbf002aac65700b13
BATCH_A_WORKTREE = C:\Users\walac\.codex\worktrees\argos-ui-remediation-batch-a\projeto_argos
BATCH_A_BRANCH = codex/ui-remediation-batch-a
BATCH_A_START_HEAD = be1adfb523c958d754e97f2dbf002aac65700b13
PHASE1_TECHNICAL = PASS
PHASE1_COMMIT = c64525c
PHASE2_TECHNICAL = PASS
PHASE2_COMMIT = 9365a07
PHASE3_TECHNICAL = PASS
PHASE3_COMMIT = 5fdf371
BATCH_A_TECHNICAL = PASS
BATCH_A_TECHNICAL_IMPLEMENTATION = PASS
BATCH_A_USER_VISUAL_ACCEPTANCE = PASS
BATCH_A_STATUS = PASS
BATCH_A_LOCAL_CHECKPOINT = PASS
BATCH_A_CANONICAL_INTEGRATION = PENDING
ACTIVITY_COMPLETION_PERCENT = 100%
ACTIVITY_COMPLETE = YES
PHASE4 = NOT_STARTED
PHASE5 = NOT_STARTED
PHASE6 = NOT_STARTED
PROJECT_STATE_UPDATE = PASS
PUSH_EXECUTED = NO
MERGE_EXECUTED = NO
NEXT_ACTIVITY = ARGOS UI REMEDIATION — FAST TRACK BATCH A / CANONICAL INTEGRATION
```

### Ownership e deltas técnicos

- `design-system.css` concentra tokens, tipografia, botão base, inputs e native
  selects, cards, badges, tabela genérica, `table-region`, page header,
  multiselect, foco e alturas compartilhadas. O bloco de multiselect e o page
  header saíram de `argos.css`. O foco da `table-region` saiu de `inventario.css`.
- `argos.css` concentra sidebar, topbar, main, navegação e page container. A
  regra do shell condicionada ao Quick Detail aberto saiu de `inventario.css`
  sem mudança computada observada. O breakpoint de 64rem que repetia valores
  do shell base foi removido.
- `inventario.css` preserva composição da lista, tabela de câmeras, ações locais
  e Quick Detail. As regras antes globais de botão foram limitadas ao main; o
  `metric-card` local foi limitado a `inventory-result-count`.
- `portal.css` permanece owner da composição do Dashboard;
  `governanca.css`, da composição de Governança. Os três campos de filtro do
  histórico de substituições passaram a consumir o primitive `.field` do
  Design System, eliminando o controle local de 42px.
- O summary do multiselect agora usa o mesmo contrato de altura mínima e
  padding vertical dos demais controles. Medidas finais: desktop 36px,
  compacto 32px, mobile/touch 44px. Não houve alteração funcional intencional.

### Validação e proveniência

```text
DJANGO_BASE_DIR = C:\Users\walac\.codex\worktrees\argos-ui-remediation-batch-a\projeto_argos
RUNTIME_SOURCE = Django source, templates, static assets and SQLite QA database from the Batch A worktree; HTML/JSON snapshots generated via Django test client from that same worktree and served on loopback for browser inspection
RUNTIME_BRANCH = codex/ui-remediation-batch-a
RUNTIME_HEAD_AT_FINAL_TECHNICAL_VALIDATION = 5fdf371
RUNTIME_VALIDATION = PASS_FOR_RENDERED_UI_AND_SHARED_COMPONENTS; authenticated live request flow was not exercised by the snapshot server
DJANGO_CHECK = PASS after each phase
FRONTEND_TESTS = 18/18 PASS after Phase 1 and Phase 3
GIT_DIFF_CHECK = PASS after each phase
BROWSER_ZOOM = 100%
VIEWPORTS_VALIDATED = 2552x866; 2048x914; 1920x1080; 1366x768; 900x768; 390x844
NO_PAGE_HORIZONTAL_OVERFLOW = YES in Dashboard and Inventory at all six viewports; Governance at 1366x768 and 390x844
SHELL_BASELINE = sidebar 192px desktop; page max-width 1400px; topbar computed approximately 43px; shell top/bottom spacing preserved
DASHBOARD_REGRESSION = NONE observed; all six viewports checked for document overflow, sidebar and main geometry
INVENTORY_REGRESSION = NONE observed for shared components; Phase 1 computed styles and geometry matched baseline at all six viewports
GOVERNANCE_REGRESSION = NONE observed in filtered history view at desktop/mobile
QUICK_DETAIL_REGRESSION = NONE observed in shared primitives/shell at 900x768; full synthetic detail content loaded, Escape closed and focus returned
ACCESSIBILITY_REGRESSION = NONE observed in tested keyboard/focus flows; no WCAG-complete claim
```

O navegador recebeu HTML e a resposta JSON do Quick Detail gerados pelas
views do worktree com um usuário e uma câmera sintéticos no SQLite local
ignorado pelo Git. CSS e JS foram servidos pelo `manage.py runserver` do
worktree. Esse método comprova a origem do código renderizado, mas não valida
login real nem as chamadas autenticadas contra o servidor Django ao vivo.
As medições do Quick Detail pertencem à regressão de shell e primitives; a
reconstrução local do drawer continua reservada à Phase 6.

### Findings preservados para o Batch B

```text
PHASE4 = grid de filtros baseado no viewport; label wrap; tabela/coluna Ações e conteúdo longo; comportamento 900/896px; card mode mobile
PHASE5 = densidade e composição dos metric cards do Dashboard; quarto card de Monitoramento; min-height/grid-template-rows/gaps
PHASE6 = scroll e composição local do Quick Detail; max-height:800px; identidade !important; navegação local de 32px; simplificação das regras compensatórias
BLOCKERS = NONE for Batch A technical implementation
READY_FOR_USER_REVIEW = YES
FINAL_VERDICT = BATCH A TECHNICAL PASS; USER VISUAL ACCEPTANCE PENDING; NO PUSH OR MERGE
```
