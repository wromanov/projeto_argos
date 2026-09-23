# ARGOS — Active Document Map

STATUS = CURRENT
DOCUMENT_TYPE = PROJECT_SPECIFIC_AUTHORITY_MAP
PROJECT = ARGOS

## 1. Project continuity authorities

| Path | Role | Status |
|---|---|---|
| `AGENTS.md` | Project entrypoint / agent authority map | PRESENT in commit 92023b2; content must be inspected by executor |
| `AGENT_CONTINUITY.md` | Project-specific continuity instance | TO_MATERIALIZE |
| `PROJECT_STATE.md` | Current operational snapshot | TO_MATERIALIZE |
| `continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md` | New-chat recovery contract | TO_MATERIALIZE |
| `continuity/ACTIVE_DOCUMENT_MAP.md` | Active authority/document map | TO_MATERIALIZE |

## 2. Known project canonical documents

| Path / identity | Role | Status |
|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md` | Project roadmap / workstream direction | KNOWN_CANONICAL; verify current content |
| `docs/projeto/ADR-021_seguranca_capacidade_monitoramento.md` | Monitoring security/capability ADR | KNOWN_CANONICAL; verify current content |
| ADR-019 | Monitoring architecture/behavior authority | EXACT_PATH_UNVERIFIED |
| ADR-020 | Monitoring state/read semantics authority | EXACT_PATH_UNVERIFIED |

Do not invent exact paths for ADR-019/ADR-020. Resolve them from the repository
during read-only recovery.

## 3. Transversal policy set

CURRENT / ACTIVE:

- `Politica-Prompts-Agente-v1.7-R2.4.md`
- `AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`
- `Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`
- `Independencia-Analitica-Agente-v1.md`

SUPERSEDED / HISTORICAL ONLY:

- `Politica-Prompts-Agente-v1.7-R2.3.md`
- prior AGENTS baseline v1.7-R2
- `Politica-de-Uso-de-Skills-Codex-Work-v1.0.md`

Rules:
- historical references are allowed as evidence;
- superseded versions are not operational authorities;
- project-specific authorities and explicit user instructions have precedence;
- capability never expands authority.

## 4. Current technical source of truth

Git controls factual repository state.

Last verified:
- repository: `C:\Users\walac\desenvolvimento\projeto_argos`
- branch: `master`
- HEAD: `92023b2`
- origin/master: `079baee`
- divergence: ahead 1 / behind 0
- worktree: clean
- staging: clean

A future agent must reverify these values before relying on them.

## 5. Monitoring workstream continuity

MON-07 = COMPLETE / PUBLISHED
MON-08A = PASS
MON-08B = RECOVERY_REQUIRED
MON-08C = NOT_STARTED
MON-08D = BLOCKED
MON-08E = NOT_STARTED

Historical MON-08B implementation evidence is not a current source-code authority.
