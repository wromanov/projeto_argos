# ARGOS — New Chat Bootstrap Prompt

STATUS = ACTIVE
PROJECT = ARGOS
LANGUAGE = pt-BR
FIRST_RESPONSE_MODE = READ_ONLY_CONTINUITY_REVALIDATION

Responda sempre em português do Brasil. Em nova conversa, primeiro leia `AGENTS.md`, os quatro documentos de continuidade listados no mapa ativo, o roadmap vigente e as authorities aplicáveis; valide Git diretamente. Reconcilie os fatos atuais antes de qualquer ação. Implementação ou outra ação Git consequencial futura exige autorização própria.

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

A capacidade validada inclui estados estáveis UNKNOWN / ONLINE / OFFLINE; SUSPECT efêmero; STALE como dimensão de freshness; memória de confirmação persistente e streak pendente após restart; thresholds respeitados; restart sem transition/outage falsa; falha de banco distinta de câmera OFFLINE; CANCELLED neutro; timeouts e rede conforme semântica canônica; falhas operacionais sem histórico funcional falso e com recovery; ownership persistente por câmera, epoch monotônico, lease de takeover e fencing; config_generation independente; completion obsoleta sem side effects; observabilidade/configuração e logs sem secrets.

LEASE_EXPIRY_ALONE_INVALIDATES_COMPLETION = NO
NEWER_OWNERSHIP_EPOCH_INVALIDATES_COMPLETION = YES
ATTEMPT_MAX_DURATION_REQUIRED_FOR_CORRECTNESS = NO
LEASE_DURATION = janela operacional configurável de takeover
LEASE_RENEWAL_IMPLEMENTED = NO

## Roadmap e limites

NEXT_PROJECT_ACTIVITY = FASE C — Captura manual e gestão de imagens
NEXT_PROJECT_ACTIVITY_STATUS = PLANEJADA

Este é o nível macro indicado pelo roadmap; não decomponha nem inicie a fase por inferência. Security gates vigentes:

LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS
HOMOLOGATION = BLOCKED
DEPLOYMENT = BLOCKED
PRODUCTION = BLOCKED

FUTURE_VALIDATIONS = PostgreSQL real; multi-processo real em produção; rede real; câmeras reais; credenciais reais; capacidade produtiva; budgets formais de CPU, memória e conexões. Esses limites não são falhas da MON-09 e não permitem alegar readiness produtiva. Preservar o estado factual de SEC-001...SEC-010; não reabrir SEC-007...SEC-010 nem mover SEC-001...SEC-006 para MON-09.

LOG_VOLUME_HARDENING_STATUS = HARDENING / NON-BLOCKING — potencial volume elevado de logs INFO por ciclo/attempt
MON09B_C_ACCIDENTAL_SCALE_EXECUTIONS = observação processual, não blocker técnico

## Git e ação

O snapshot da baseline técnica anterior ao commit documental foi `HEAD = origin/master = 850efd2381d7f5b7df27e528dc3374ea58e507b3`, divergence `0/0`, worktree clean e staging empty. Esse snapshot é histórico; valide o estado atual e o commit documental mais recente diretamente no Git antes de qualquer conclusão. Não execute push sem autorização humana separada.

A Fase C permanece apenas planejada. Qualquer implementação futura exige escopo e autorização próprios. A conclusão MON-09 não altera gates ambientais nem declara homologation, deployment ou production ready.
