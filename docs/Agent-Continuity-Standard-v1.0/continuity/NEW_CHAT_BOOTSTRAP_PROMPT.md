# ARGOS — New Chat Bootstrap Prompt

STATUS = ACTIVE
PROJECT = ARGOS
FIRST_RESPONSE_MODE = READ_ONLY_CONTINUITY_REVALIDATION

Você continuará o Projeto ARGOS. Antes de qualquer implementação, edição,
stage, commit, push, deploy ou avanço de fase:

1. leia `AGENTS.md`;
2. leia `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`;
3. leia `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`;
4. leia `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`;
5. resolva e leia as authorities canônicas aplicáveis no repositório;
6. aplique as políticas transversais vigentes;
7. valide Git diretamente.

Políticas transversais ativas:
- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.4.md`;
- `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`;
- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`;
- `docs/Agent-Continuity-Standard-v1.0/policies/Independencia-Analitica-Agente-v1.md`.

Não use versões superseded como authority operacional.

## Recovery boundary

BOOTSTRAP_SESSION_GATE_SCOPE = EACH_NEW_CHAT
CONTINUITY_RECOVERY_GATE = NOT_PASSED
USER_CONTINUITY_VALIDATION = PENDING
READY_TO_RESUME_PROJECT = NO

IMPLEMENTATION = PROHIBITED
EDIT = PROHIBITED
STAGE = PROHIBITED
COMMIT = PROHIBITED
PUSH = PROHIBITED
DEPLOY = PROHIBITED
PHASE_ADVANCEMENT = PROHIBITED

READ_FILES = YES
READ_GIT = YES
INSPECT_STATE = YES
VERIFY_FACTS = YES
COMPARE_AUTHORITIES = YES

## Known continuity point

O último baseline publicado conhecido é:

079baee
docs(monitoramento): encerrar mon-07 e direcionar mon-08

O baseline local pré-checkpoint verificado em 2026-09-23 está alinhado ao remoto:

CURRENT_BASELINE_BEFORE_CHECKPOINT = 40c77c4c988c960000773d3830d8e1915bbcbc59
HEAD = 40c77c4c988c960000773d3830d8e1915bbcbc59
ORIGIN_MASTER = 40c77c4c988c960000773d3830d8e1915bbcbc59
DIVERGENCE = ahead 0 / behind 0
WORKTREE = one expected MON-08C harness untracked + four continuity documents modified for this checkpoint
STAGING = EMPTY
SNAPSHOT = PRE-COMMIT; revalidate post-commit directly from Git

MON-08A = PASS.
MON-08B = COMPLETE / TECHNICALLY_APPROVED (HISTORICAL).
MON08C_DISCOVERY_PREFLIGHT = PASS.
MON08C1_NORMAL_PERSISTENCE = PASS.
MON08C2_MASS_FAILURE = PASS.
MON08C3_MASS_RECOVERY = PASS.
MON08C4_RESTART_IDEMPOTENCY = PASS.
MON08C5_STALE_GENERATION_CAS = PASS.
MON08C_H1_HARNESS_DISCOVERY = PASS.
MON08C_H2_HARNESS_REFACTOR = PASS.

FAST_TEST_COUNT = 1; SCALE_TEST_COUNT = 4.
FAST_DATASET_SIZE = 3; SCALE_DATASET_SIZE = 2300.
DATASET_2300_CREATION_COUNT = 6 → 4.
COMPLETION_CALLS_APPROX = 39101 → 27607.
STRUCTURAL_REDUCTION_APPROX = 29.4%.
MASS_FAILURE_RECOVERY_CONSOLIDATED = YES.
FAST_TESTS = PASS — aproximadamente 0.067 s.
REPRESENTATIVE_SCALE_TEST = PASS — 2300 ativos — aproximadamente 270.869 s.
FULL_MON08C_RERUN = NOT_REQUIRED.
GLOBAL_SUITE_RUN = NO.
PRODUCTION_SOURCE_CHANGED = NO; CI_CHANGED = NO; SCHEMA_CHANGED = NO.
CI_SCALE_OPT_IN = DEFERRED / NON-BLOCKING.
BLOCKERS = 0; MAJOR = 0; MINOR = 0.

O harness MON-08C está incluído neste checkpoint. Nenhum código produtivo foi
alterado pela H2 e nenhum novo teste pesado é requerido por ritual.

## Git verification

Verifique, no mínimo:

- repository root;
- current branch;
- HEAD;
- upstream/origin;
- divergence;
- worktree;
- staging;
- últimos commits;
- presença/ausência dos artifacts MON-08B.

Se qualquer fact divergir de `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, o Git atual prevalece para
estado do repositório e a divergência deve ser reportada.

## First response contract

Explique em linguagem humana:
- estado recuperado;
- último ponto confiável;
- pendências;
- blockers;
- divergências;
- itens UNVERIFIED;
- próximo passo.

Depois apresente:

AGENT_IDENTITY_RECOVERED =
GOVERNANCE_RECOVERED =
PROJECT_STATE_RECOVERED =
HANDOFF_PREPARATION_GATE =
CONTINUITY_ADOPTION_MODE =
CONTINUITY_RETROFIT_GATE =
CURRENT_PHASE =
CURRENT_ACTIVITY = MON-08C-H2 — PASS
LAST_COMPLETED_ACTIVITY = MON-08C-H2 — harness refactor and approved validation
COMPLETED_STATE =
PENDING_STATE =
BLOCKERS =
IMPORTANT_ACTIVE_DECISIONS =
CURRENT_GATES =
NEXT_REQUIRED_ACTIVITY =
MON-08C-6 — CONSOLIDATED MEASUREMENT / FINAL ADJUDICATION
REPOSITORY_ROOT =
CURRENT_BRANCH =
CURRENT_HEAD = baseline pré-checkpoint 40c77c4c988c960000773d3830d8e1915bbcbc59; pós-commit consultar Git
UPSTREAM =
WORKTREE_STATE =
STAGING_STATE =
UNVERIFIED_ITEMS =
CONTRADICTIONS_FOUND =
MISSING_CONTEXT =
CONTINUITY_RECOVERY_GATE = NOT_PASSED
USER_CONTINUITY_VALIDATION = PENDING
READY_TO_RESUME_PROJECT = NO

Aguarde a validação do checkpoint/continuidade diretamente no Git antes de iniciar
a MON-08C-6; essa validação não autoriza implementação da MON-08C-6.

Somente após:
USER_CONTINUITY_VALIDATION = PASS
CONTINUITY_RECOVERY_GATE = PASS

o agente pode sair do modo de revalidação desta conversa. A próxima atividade do
projeto continua exigindo scope e autorização próprios.

## Next required activity

MON-08C-6 — CONSOLIDATED MEASUREMENT / FINAL ADJUDICATION

MON08C6_STATUS = NOT_STARTED
MON08C6_IMPLEMENTATION_AUTHORIZATION = NO
CHECKPOINT_STAGE_COMMIT_AUTHORIZED = YES
PUSH = NOT_AUTHORIZED
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
