# ARGOS — Active Document Map

STATUS = CURRENT
DOCUMENT_TYPE = PROJECT_SPECIFIC_AUTHORITY_MAP
PROJECT = ARGOS
ACTIVE_DOCUMENT_MAP_READY = YES

## 1. Project continuity authorities

| Path | Role | Status |
|---|---|---|
| `AGENTS.md` | Project entrypoint / agent authority map | PRESENT / CURRENT CHECKOUT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Project-specific continuity instance | PRESENT / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Current operational snapshot | PRESENT / CURRENT_SNAPSHOT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Active authority/document map | PRESENT / CURRENT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md` | New-chat recovery contract | PRESENT / ACTIVE |

## 2. Known project canonical documents

| Path / identity | Role | Status |
|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md` | Project roadmap / workstream direction | PRESENT / CANONICAL; verify current content |
| `docs/projeto/ADR-019_monitoramento_disponibilidade_gestao_imagens.md` | Monitoring architecture/behavior authority | PRESENT; verify current content |
| `docs/projeto/ADR-020_contrato_estado_tecnico_monitoramento.md` | Monitoring state/read semantics authority | PRESENT; verify current content |
| `docs/projeto/ADR-021_seguranca_capacidade_monitoramento.md` | Monitoring security/capability authority | PRESENT / CANONICAL; verify current content |

## 3. Transversal policy set

CURRENT / ACTIVE:

- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.4.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Independencia-Analitica-Agente-v1.md`

SUPERSEDED / HISTORICAL ONLY:

- `Politica-Prompts-Agente-v1.7-R2.3.md`
- prior AGENTS baseline v1.7-R2
- `Politica-de-Uso-de-Skills-Codex-Work-v1.0.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Prompt para internalização de politicas para Agentes.txt` — auxiliary historical prompt; it references R2.3 and is not an active authority

Rules:
- historical references are allowed as evidence;
- superseded versions are not operational authorities;
- project-specific authorities and explicit user instructions have precedence;
- capability never expands authority.

## 4. Current technical source of truth

Git controls factual repository state.

Last verified snapshot:

- repository: `C:\Users\walac\desenvolvimento\projeto_argos`
- branch: `master`
- HEAD: `40c77c4c988c960000773d3830d8e1915bbcbc59` (baseline pré-checkpoint)
- origin/master: `40c77c4c988c960000773d3830d8e1915bbcbc59`
- divergence: ahead 0 / behind 0
- worktree: um harness MON-08C esperado untracked; quatro documentos de continuidade modificados neste checkpoint
- staging: empty
- snapshot: pre-commit; Git pós-commit deve ser revalidado diretamente

A future agent must reverify these values before relying on them.

## 5. Monitoring workstream continuity

MON-07 = COMPLETE / PUBLISHED
MON-08A = PASS
MON-08B = COMPLETE / TECHNICALLY_APPROVED (HISTORICAL)
MON-08C-H1 = PASS
MON-08C-H2 = PASS
MON-08C-1 = PASS
MON-08C-2 = PASS
MON-08C-3 = PASS
MON-08C-4 = PASS
MON-08C-5 = PASS
MON-08C = H2 COMPLETE / TECHNICALLY APPROVED; MON-08C-6 NOT_STARTED
MON-08D = BLOCKED_BY_ENVIRONMENT_AND_SECURITY_GATES
MON-08E = NOT_STARTED

FAST_TEST_COUNT = 1
SCALE_TEST_COUNT = 4
FAST_DATASET_SIZE = 3
SCALE_DATASET_SIZE = 2300
DATASET_2300_CREATION_COUNT = 6 → 4
COMPLETION_CALLS_APPROX = 39101 → 27607
STRUCTURAL_REDUCTION_APPROX = 29.4%
CI_SCALE_OPT_IN = DEFERRED / NON-BLOCKING
PRODUCTION_SOURCE_CHANGED = NO
CI_CHANGED = NO
SCHEMA_CHANGED = NO
MON-08 = IN_PROGRESS; H2 não inicia MON-08C-6.
NEXT_REQUIRED_ACTIVITY = MON-08C-6 — CONSOLIDATED MEASUREMENT / FINAL ADJUDICATION
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
MON08C6_STATUS = NOT_STARTED
MON08C6_IMPLEMENTATION_AUTHORIZATION = NO
PUSH = NOT_AUTHORIZED
