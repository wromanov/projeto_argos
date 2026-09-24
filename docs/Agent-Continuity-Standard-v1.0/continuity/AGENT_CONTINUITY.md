# ARGOS — Agent Continuity

STATUS = ACTIVE
DOCUMENT_TYPE = PROJECT_SPECIFIC_CONTINUITY_INSTANCE
CONTINUITY_STANDARD = Agent Continuity Standard v1.0
CONTINUITY_PROTOCOL_PACKAGE = Protocolo Continuidade Projeto Em Andamento Com Novo Agente 2.0
CONTINUITY_ADOPTION_MODE = RETROFIT_REQUIRED
CONTINUITY_RETROFIT_GATE = PASS
USER_PROTOCOL_ACTIVATION = APPROVED
PROJECT = ARGOS
LANGUAGE = pt-BR

## 1. Finalidade

Este documento materializa, para o Projeto ARGOS, o protocolo universal de
continuidade entre chats, agentes, máquinas e sessões.

Ele NÃO substitui:
- `AGENTS.md`;
- authorities específicas do projeto;
- políticas transversais canônicas;
- ADRs e roadmap canônicos;
- segurança e gates próprios do ARGOS.

Regra de precedência operacional:

1. instrução explícita atual do usuário;
2. authorities/contratos canônicos específicos do ARGOS;
3. segurança, operação e limites de authority;
4. políticas transversais canônicas aplicáveis;
5. este documento de continuidade;
6. convenções auxiliares.

CAPABILITY != AUTHORITY
DELEGATION != AUTHORITY_TRANSFER
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
CONTINUITY_RECOVERY_GATE = PASS != IMPLEMENTATION_PREFLIGHT = PASS

## 2. Identidade e repositório

PROJECT_ID = ARGOS
PROJECT_PURPOSE = inventário e monitoramento técnico de câmeras
PRIMARY_REPOSITORY = https://github.com/wromanov/projeto_argos.git

LAST_VERIFIED_LOCAL_ROOT = C:\Users\walacedelgado\PycharmProjects\projeto_argos
LAST_VERIFIED_BRANCH = master
CURRENT_CANONICAL_GIT_BASELINE = 202e4f353551e7ab05667d86f9216cc102f351cc
CURRENT_BASELINE_BEFORE_DOCUMENTARY_COMMIT = 202e4f353551e7ab05667d86f9216cc102f351cc
LAST_VERIFIED_HEAD = 202e4f353551e7ab05667d86f9216cc102f351cc
LAST_VERIFIED_ORIGIN_MASTER = 202e4f353551e7ab05667d86f9216cc102f351cc
LAST_VERIFIED_DIVERGENCE = HEAD ahead 0 / behind 0
LAST_VERIFIED_WORKTREE = CLEAN (baseline antes deste commit documental)
LAST_VERIFIED_STAGING = EMPTY

Observação:
os facts acima são o snapshot da baseline técnica imediatamente anterior ao
commit documental; revalidar Git antes de usá-los como estado atual.

## 3. Governança transversal ativa

As políticas operacionais atuais são:

- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.4.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Independencia-Analitica-Agente-v1.md`

Regras de version hygiene:
- R2.4 substitui operacionalmente R2.3;
- AGENTS R2.1 usa a baseline anterior somente como histórico;
- Skills/Plugins v1.1 substitui v1.0;
- versões superseded não são authorities ativas.

## 4. Continuidade do estado técnico

LAST_COMPLETED_PUBLISHED_ACTIVITY = MON-09 — fechamento técnico publicado em 850efd2
LAST_PUBLISHED_BASELINE = 850efd2
CURRENT_ACTIVITY_COMPLETED = UI-DS — CANONICAL DOCUMENTATION AND CONTINUITY RECONCILIATION
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
NEXT_REQUIRED_ACTIVITY = UI-0 — READ-ONLY PREFLIGHT (UI-DS; após adjudicação humana e autorização)
NEXT_PROJECT_ACTIVITY = FASE C — Captura manual e gestão de imagens
NEXT_PROJECT_ACTIVITY_STATUS = PLANEJADA
NEXT_REQUIRED_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED
MON08C6_STATUS = COMPLETE / FINAL ADJUDICATION COMPLETE
MON08C6_IMPLEMENTATION_AUTHORIZATION = NOT_APPLICABLE
CHECKPOINT_STAGE_COMMIT_AUTHORIZATION = NO
PUSH = NOT_AUTHORIZED

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
MON08C6 = PASS / FINAL ADJUDICATION COMPLETE
MON08C_DISCOVERY = PASS
MON08C1 = PASS
MON08C2 = PASS
MON08C3 = PASS
MON08C4 = PASS
MON08C5 = PASS
MON08C_FINAL_VERDICT = PASS_WITH_FINDINGS
MON08C_COMPLETE = YES
MON08_TECHNICAL_VERDICT = PASS_WITH_FINDINGS
MON08_TECHNICALLY_COMPLETE = YES
NEXT_TECHNICAL_MON08_ACTIVITY = NONE
MON08_BLOCKERS = NONE
MON08_MAJOR = NONE
MON08_MINOR = NONE

Evidência factual aprovada da MON-08C-H2:
- FAST_TEST_COUNT = 1; SCALE_TEST_COUNT = 4;
- FAST_DATASET_SIZE = 3; SCALE_DATASET_SIZE = 2300;
- DATASET_2300_CREATION_COUNT = 6 → 4;
- COMPLETION_CALLS_APPROX = 39101 → 27607;
- STRUCTURAL_REDUCTION_APPROX = 29.4%;
- MASS_FAILURE_RECOVERY_CONSOLIDATED = YES;
- FAST_TESTS = PASS — aproximadamente 0.067 s;
- REPRESENTATIVE_SCALE_TEST = PASS — 2300 ativos — aproximadamente 270.869 s;
- FULL_MON08C_RERUN = NOT_REQUIRED; GLOBAL_SUITE_RUN = NO;
- PRODUCTION_SOURCE_CHANGED = NO; CI_CHANGED = NO; SCHEMA_CHANGED = NO;
- CI_SCALE_OPT_IN = DEFERRED / NON-BLOCKING;
- BLOCKERS = 0; MAJOR = 0; MINOR = 0.

## 5. Gates de segurança e operação preservados

SECURITY_GATE_LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS
SECURITY_GATE_HOMOLOGATION = BLOCKED
SECURITY_GATE_DEPLOYMENT = BLOCKED
SECURITY_GATE_PRODUCTION = BLOCKED

LIVE / produção / homologação não são autorizados por este documento.

## 5.1 Histórico: fechamento documental da MON-08 (supersedido como estado atual)

NEW_MATERIAL_VALIDATION_REQUIRED_FOR_MON08_CLOSURE = NO
FUTURE_MATERIAL_VALIDATION_REQUIRED = YES
FUTURE_VALIDATION_SCOPE = production capacity; PostgreSQL; multi-instance / multi-worker; real network / firewall / VLAN; real cameras / credentials; formal resource/performance budgets
CONFIRMATION_MEMORY_STABLE_RELOAD = PROVEN
CONFIRMATION_MEMORY_PENDING_STREAK_RESTART = NOT_VALIDATED / HARDENING CANDIDATE
QUERY_VOLUME = PERFORMANCE_OBSERVATION / HARDENING CANDIDATE
CI_SCALE_OPT_IN = BACKLOG / NON-BLOCKING

VALIDATED_ENVELOPE = Django ORM; SQLite local; single instance; resultados de probe sintéticos/determinísticos; aproximadamente 2300 ativos; concorrência configurada e observada de 20; persistência integrada local; transições; indisponibilidades; restart/idempotência; stale generation/CAS; confirmation memory nos estados exercitados
NOT_VALIDATED_BOUNDARIES = PostgreSQL real; multi-instance; multi-worker; distributed lease; real network; real firewall/VLAN; real cameras; real credentials; production performance; production capacity

MON08_HOMOLOGATION_AUTHORIZED = NO
MON08_DEPLOYMENT_AUTHORIZED = NO
MON08_PRODUCTION_AUTHORIZED = NO

## 6. Decisões técnicas importantes preservadas

- Monitoramento técnico é separado da situação operacional da câmera.
- Browser/UI nunca executa probes.
- Probes pertencem a execução dedicada/independente do request/response.
- Concorrência deve ser bounded.
- UNKNOWN / ONLINE / OFFLINE são estados estáveis.
- SUSPECT é efêmero e não deve virar quarto estado persistido.
- Stale/freshness é qualificador separado; stale preserva last stable state, mas
  o estado efetivo de leitura é UNKNOWN(stale).
- Monitoramento e captura são desacoplados.
- Credenciais não pertencem a URLs, logs ou documentos de continuidade.
- Exportação CSV/PDF de inventário permanece DEFERRED para sprint final.
- HARDENING_TRANSITION_REAL permanece DEFERRED / NON-BLOCKING.
- HARDENING_SCOPE_BATCH_NPLUS1 permanece DEFERRED / NON-BLOCKING.

## 7. Primeiro comportamento em novo chat/agente

FIRST_RESPONSE_MODE = READ_ONLY_CONTINUITY_REVALIDATION
CONTINUITY_RECOVERY_GATE_SCOPE = EACH_NEW_CHAT
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

O novo agente deve:
1. ler `AGENTS.md`;
2. ler `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`;
3. ler `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`;
4. ler `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`;
5. ler as policies canônicas relevantes em `docs/Agent-Continuity-Standard-v1.0/policies/`;
6. revalidar Git;
7. apresentar divergências e itens UNVERIFIED;
8. aguardar validação humana.

## 8. Estado atual e próxima atividade

MON-09A = COMPLETE / PASS; MON-09B = COMPLETE / PASS_WITH_SCOPE_DEVIATION; MON-09C = COMPLETE / PASS_WITH_FINDINGS; MON-09D = COMPLETE; MON-09E = COMPLETE / PASS.

MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_PROJECT_ACTIVITY = FASE C — Captura manual e gestão de imagens
NEXT_PROJECT_ACTIVITY_STATUS = PLANEJADA
NEXT_REQUIRED_ACTIVITY = UI-0 — READ-ONLY PREFLIGHT (UI-DS; após adjudicação humana e autorização)
NEXT_REQUIRED_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED
UI_DS_CANONICAL_SPEC = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
UI_DS_CANONICAL_SPRINT_MAP = docs/projeto/SPRINTS_ARGOS_V5.md
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = PENDING
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
UI_DS = UI-0, UI-1, UI-2, UI-3, UI-4
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED

A frente de monitoramento está encerrada tecnicamente; não retomar MON-09 nem criar outra atividade MON. Limites futuros continuam: PostgreSQL real, multi-processo de produção, rede/câmeras/credenciais reais, capacidade produtiva e budgets formais de CPU, memória e conexões. Potencial volume de logs INFO é HARDENING / NON-BLOCKING. A próxima macrofase é a Fase C planejada, conforme roadmap. Implementação futura exige autorização própria. O baseline Git acima descreve a validação imediatamente anterior a este commit documental; revalidar Git ao iniciar nova sessão.

## 9. Retrofit gate

Este pacote foi gerado para materialização no repositório, mas o gate só pode
mudar para PASS após confirmação factual de que os arquivos estão presentes,
coerentes e legíveis no checkout oficial.

Critérios:

AGENTS_MD_PRESENT = REQUIRED
AGENT_CONTINUITY_PRESENT = REQUIRED
PROJECT_STATE_PRESENT = REQUIRED
NEW_CHAT_BOOTSTRAP_PRESENT = REQUIRED
ACTIVE_DOCUMENT_MAP_PRESENT = REQUIRED
KNOWN_BLOCKERS_RECORDED = YES
KNOWN_DIVERGENCES_RECORDED = YES
NEXT_REQUIRED_ACTIVITY_RECORDED = YES

Verificação factual concluída:
CONTINUITY_RETROFIT_GATE = PASS


### Fechamento técnico MON-09 — estado vigente

LAST_RELEVANT_CHECKPOINT = 850efd2381d7f5b7df27e528dc3374ea58e507b3 (850efd2)
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_PROJECT_ACTIVITY = FASE C — Captura manual e gestão de imagens
NEXT_PROJECT_ACTIVITY_STATUS = PLANEJADA
VALIDATED_ENVELOPE = UNKNOWN / ONLINE / OFFLINE como estados estáveis; SUSPECT efêmero; STALE como freshness; confirmation memory persistente; pending failure streak sobrevive restart; thresholds respeitados; restart sem transição/outage falsa; falha de banco não equivale a câmera offline; CANCELLED neutro; timeout/rede conforme semântica canônica; sem histórico funcional falso em falha operacional e com recovery possível; ownership por câmera, owner persistente e epoch monotônico; lease define elegibilidade operacional de takeover; epoch é fencing token; config_generation é independente; completion de owner obsoleto sem side effects de domínio; owner antigo não libera owner novo; completion válida libera ownership atomicamente; renovação de lease não implementada; MonitoringConfig integrado à configuração ARGOS, config inválida fail-fast; status, backlog/in-flight, falhas operacionais e ownership diagnosticáveis; observabilidade sem histórico funcional e logs sem secrets
FUTURE_VALIDATIONS = PostgreSQL real; multi-processo real em produção; rede real; câmeras reais; credenciais reais; capacidade produtiva; budgets formais de CPU, memória e conexões
SECURITY_GATES = LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS; HOMOLOGATION = BLOCKED; DEPLOYMENT = BLOCKED; PRODUCTION = BLOCKED
IMPLEMENTATION_FUTURE = requer autorização própria

## 10. UI-DS e continuidade de produto

Existe uma specification canônica para a integração seletiva do
`camera-inventory-design-system-v1.0.1`:

`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`

O mapa canônico de sprints/slices é:

`docs/projeto/SPRINTS_ARGOS_V5.md`

O pacote de referência foi localizado em:

`C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip`

Ele não foi copiado para o repositório; `REFERENCE_PACKAGE_REPOSITORY_COPY =
PENDING`. A frente UI-DS registra retrofit visual seletivo, adoção seletiva de
interações, preservação da composição atual do ARGOS, adoção do
`CameraQuickDetailPanel`, dependência explícita da Fase C para
`LATEST_CAMERA_CAPTURE`, distinção de `PRIMARY_IMAGE`, preservação da
proveniência `UPLOAD_MANUAL`, ausência de captura automática na abertura,
proibição de integração big-bang e `INTEGRATION_GATE` obrigatório quando
aplicável.

`UI-0` é a próxima atividade preparatória recomendada: read-only, encerra com
relatório e exige adjudicação/autorização humana antes de qualquer
implementação visual.
