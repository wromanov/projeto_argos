# ARGOS — New Chat Bootstrap Prompt

STATUS = ACTIVE
PROJECT = ARGOS
FIRST_RESPONSE_MODE = READ_ONLY_RECOVERY

Você continuará o Projeto ARGOS. Antes de qualquer implementação, edição,
stage, commit, push, deploy ou avanço de fase:

1. leia `AGENTS.md`;
2. leia `AGENT_CONTINUITY.md`;
3. leia `PROJECT_STATE.md`;
4. leia `continuity/ACTIVE_DOCUMENT_MAP.md`;
5. resolva e leia as authorities canônicas aplicáveis no repositório;
6. aplique as políticas transversais vigentes;
7. valide Git diretamente.

Políticas transversais ativas:
- `Politica-Prompts-Agente-v1.7-R2.4.md`;
- `AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`;
- `Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`;
- `Independencia-Analitica-Agente-v1.md`.

Não use versões superseded como authority operacional.

## Recovery boundary

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

O clone atual possuía, na última evidência conhecida, um commit local adicional:

92023b2
(docs): atualização arquivos agentes codex

MON-08A = PASS.

Uma implementação local da MON-08B existiu anteriormente, mas foi perdida quando
o computador foi formatado antes de qualquer commit/push. Portanto:

MON-08B_PREVIOUS_EVIDENCE = HISTORICAL_REFERENCE_ONLY
MON-08B_CURRENT_IMPLEMENTATION = NOT_PRESENT
MON-08B_CURRENT_GATE = RECOVERY_REQUIRED

Não promova o PASS histórico da MON-08B para o checkout atual.

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

Se qualquer fact divergir de `PROJECT_STATE.md`, o Git atual prevalece para
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

Aguarde confirmação explícita do usuário.

Somente após:
USER_CONTINUITY_VALIDATION = PASS
CONTINUITY_RECOVERY_GATE = PASS

o projeto pode sair da recuperação. Mesmo assim, a próxima atividade exige
preflight, scope e autorização próprios.

## Next required activity after recovery

MON-08B RECOVERY — READ-ONLY CODE/GIT PREFLIGHT AND RECONSTRUCTION PLAN

Isso NÃO é autorização de implementação.
