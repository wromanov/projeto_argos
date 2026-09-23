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

O snapshot local pré-stage verificado em 2026-09-23 está alinhado ao remoto:

HEAD = 14a1c40e8d431ff6f253f6d306677dc5e0eb7970
ORIGIN_MASTER = 14a1c40e8d431ff6f253f6d306677dc5e0eb7970
DIVERGENCE = ahead 0 / behind 0
WORKTREE = two expected MON-08B files untracked + four continuity documents modified for formal closure
STAGING = EMPTY
SNAPSHOT = PRE-STAGE; revalidate after the controlled Git checkpoint

MON-08A = PASS.
MON-08B = COMPLETE / TECHNICALLY_APPROVED.
MON-08B_IMPLEMENTATION = COMPLETE
MON-08B_SELF_VALIDATION_GATE = PASS
MON-08B_FINAL_INDEPENDENT_REVIEW = PASS
MON-08B_REV_001 = RESOLVED
MON-08B_REV_002 = RESOLVED

Uma implementação anterior da MON-08B foi perdida quando o computador foi
formatado antes de qualquer stage/commit/push. Esse fato e a evidência daquela
versão são históricos; a implementação atual foi reconstruída e aprovada com
evidência própria:

MON-08B_PREVIOUS_EVIDENCE = HISTORICAL_REFERENCE_ONLY
CANONICAL_RUNTIME = Python 3.14.7
TESTS_MON08B = PASS — 10/10
FOCUSED_TESTS = PASS — 188/188
GLOBAL_TESTS = PASS — 705/705
DJANGO_CHECK = PASS
MIGRATION_CHECK = PASS
COMPILEALL = PASS
GIT_DIFF_CHECK = PASS
UNTRACKED_WHITESPACE_CHECK = PASS
RUNTIME_AND_NETWORK = SYNTHETIC_ONLY; REAL_DB_CAPACITY_VALIDATED = NO

Os arquivos atuais da implementação permanecem untracked até o futuro checkpoint
Git controlado. Não confunda o gate por-chat abaixo com o status técnico da MON-08B.

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
CURRENT_ACTIVITY =
LAST_COMPLETED_ACTIVITY =
COMPLETED_STATE =
PENDING_STATE =
BLOCKERS =
IMPORTANT_ACTIVE_DECISIONS =
CURRENT_GATES =
NEXT_REQUIRED_ACTIVITY =
REPOSITORY_ROOT =
CURRENT_BRANCH =
CURRENT_HEAD =
UPSTREAM =
WORKTREE_STATE =
STAGING_STATE =
UNVERIFIED_ITEMS =
CONTRADICTIONS_FOUND =
MISSING_CONTEXT =
CONTINUITY_RECOVERY_GATE = NOT_PASSED
USER_CONTINUITY_VALIDATION = PENDING
READY_TO_RESUME_PROJECT = NO

Aguarde confirmação explícita do usuário para validar a continuidade desta nova
conversa; essa validação não altera o estado técnico aprovado da MON-08B.

Somente após:
USER_CONTINUITY_VALIDATION = PASS
CONTINUITY_RECOVERY_GATE = PASS

o agente pode sair do modo de revalidação desta conversa. A próxima atividade do
projeto continua exigindo scope e autorização próprios.

## Next required activity

MON-08B CONTROLLED GIT CHECKPOINT

CHECKPOINT_AUTHORIZED = NO
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
