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

RETOMADA ATUAL HOM-01-WORK-PC-QA-BOOTSTRAP-CLOSURE (2026-10-13): consultar
`PROJECT_STATE.md` §107 e `ACTIVE_DOCUMENT_MAP.md` §71 para o fechamento da
recuperação QA no computador do trabalho. O ambiente está preparado para
continuar HOM-01; `DASHBOARD_V7_VISUAL_QA=PENDING`, `HOM01_STATUS=IN_PROGRESS`
e `HOM02_START=BLOCKED`. A seção 106 contém o checkpoint publicado anterior.
Para contexto de produto, consultar o follow-up §14 de
`docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md` e o relatório
`docs/projeto/ARGOS_HOM_01_SIDEBAR_ACTIVE_STATE_RECOVERY.md`. Repositório
`https://github.com/wromanov/projeto_argos.git`, branch
`codex/hom-v1-integration`. HEAD inicial deste checkpoint:
`b122ece404c3b67afdbd1acf9087e340d1c07d2c`; o commit V7 foi preservado. Os
commits de implementação são `7c4fac3a81ba6311ecaf9bad2e080240759cfd0c`
(sidebar e evidências) e `d0b4c2f5bef8d4533834898a67e4d2f03b0e2d1e`
(monitoramento/A–D, Inventário e Quick Detail). O registro documental deste
checkpoint identifica o HEAD final como o próprio commit que o contém; use
`git rev-parse HEAD` para resolver seu SHA. O push normal para a branch remota
e a igualdade exata dos SHAs foram verificados após a publicação.

`manage.py check` passou pelo Python do `.venv`; 105 testes direcionados
passaram com `scripts.localqa.test_settings`, banco SQLite temporário e
sintético; `git diff --check` passou. A suíte global de 937 testes não foi
executada nesta atividade. O Dashboard V7 tem aceite humano limitado à
composição registrada em `PROJECT_STATE.md` §105; a sidebar tem aprovação
desktop das cinco páginas em §101; A–D tem aprovação limitada aos rótulos e à
omissão da linha para UNKNOWN em §99. Esses aceites não encerram HOM-01. O
finding do cabeçalho MONITORAMENTO em 1366px segue aberto; responsividade da
sidebar e aceite da composição completa da Camera Detail não foram inferidos.

Para continuar em outro computador, primeiro confirme `git status --branch`,
`git status --porcelain=v1 -uall`, `git rev-parse HEAD` e a URL de `origin`.
Preserve e reconcilie qualquer alteração local antes de trocar de branch ou
atualizar. Só com worktree limpa, execute `git fetch origin
codex/hom-v1-integration`; confirme a relação de ancestralidade e então faça
checkout/fast-forward conforme §106. Nunca use reset, clean, stash ou force
push como recuperação. Para QA, recrie `.venv` e `.local/qa` localmente; não
copie bancos, venv, `.env`, sessão ou credenciais entre máquinas. O launcher
`INICIAR_ARGOS_QA.cmd` prepara um SQLite sintético isolado e inicia Django em
`http://127.0.0.1:8765/`; confira Dashboard em `/dashboard/`. HOM-01 segue
`IN_PROGRESS`, HOM-02 segue `BLOCKED`, e esta autorização de push se limitou
ao checkpoint concluído.

## UI-V2-P1 — seleção visual e fechamento (2026-09-27)

O usuário selecionou C — ARGOS HYBRID como direção visual do ARGOS UI V2.
A/B permanecem alternativas históricas, não selecionadas. Os artefatos e as
capturas A/B/C estão em `docs/prototype/ui-v2/style-lab/` no worktree
`codex/ui-v2-p1-style-lab`. O estado atual consta em `PROJECT_STATE.md` e no
registro de execução do `ARGOS_UI_V2_MASTER_PLAN.md`; registros abaixo que
apontam P1 pendente são snapshots históricos.

```text
USER_SELECTION = C — ARGOS HYBRID
USER_VISUAL_SELECTION_GATE = PASS
DIRECTION_A_STATUS = HISTORICAL_ALTERNATIVE / NOT_SELECTED
DIRECTION_B_STATUS = HISTORICAL_ALTERNATIVE / NOT_SELECTED
DIRECTION_C_STATUS = SELECTED / VISUAL_DIRECTION_AUTHORITY
P1_STATUS = CLOSED / PASS
P1_FORMAL_CLOSURE = PASS
P2_STARTED = NO
NEXT_ACTIVITY = UI-V2-P2 — VISUAL FOUNDATION
QUICK_DETAIL = APPROVED / PROTECTED
ADMIN_UI_V2_SCOPE = TRACKED_AS_INHERITED
ADMIN_CUSTOM_REDESIGN = NO_BY_DEFAULT
PROTOTYPE_STACK_COMPATIBILITY = REQUIRED_GATE
PRODUCTION_FILES_CHANGED = NO
PUSH_AUTHORIZED = NO
```

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

ARGOS_CONTINUITY_AUTHORITY = docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md
ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE

## 2. Identidade e repositório

PROJECT_ID = ARGOS
PROJECT_PURPOSE = inventário e monitoramento técnico de câmeras
PRIMARY_REPOSITORY = https://github.com/wromanov/projeto_argos.git

LAST_VERIFIED_LOCAL_ROOT = C:\Users\walacedelgado\PycharmProjects\projeto_argos
LAST_VERIFIED_BRANCH = master
CURRENT_CANONICAL_GIT_BASELINE = ae8199e019c8f1c9331da919e7807d23d7f7210f
CURRENT_BASELINE_BEFORE_DOCUMENTARY_COMMIT = ae8199e019c8f1c9331da919e7807d23d7f7210f
LAST_VERIFIED_HEAD = ae8199e019c8f1c9331da919e7807d23d7f7210f
LAST_VERIFIED_ORIGIN_MASTER = ae8199e019c8f1c9331da919e7807d23d7f7210f
LAST_VERIFIED_DIVERGENCE = HEAD ahead 0 / behind 0
LAST_VERIFIED_WORKTREE = CLEAN (baseline antes deste checkpoint documental)
LAST_VERIFIED_STAGING = EMPTY

Observação:
os facts acima são o snapshot da baseline técnica imediatamente anterior ao
commit documental; revalidar Git antes de usá-los como estado atual.

## 3. Governança transversal ativa

As políticas operacionais atuais são:

- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.6.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.3-Roteamento-Economico.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.2.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Independencia-Analitica-Agente-v1.md`

Regras de version hygiene:
- Prompt R2.6 substitui operacionalmente R2.5;
- AGENTS R2.3 substitui operacionalmente R2.2;
- Skills/Plugins v1.2 substitui v1.1;
- versões superseded não são authorities ativas.

## 4. Contexto histórico do estado técnico (status vigente na seção 20.19 e em PROJECT_STATE.md, seção 52)

LAST_COMPLETED_PUBLISHED_ACTIVITY = MON-09 — fechamento técnico publicado em 850efd2
LAST_PUBLISHED_BASELINE = 850efd2
CURRENT_ACTIVITY_COMPLETED = IMG-01 — CANONICAL IMAGE CONTRACT CHECKPOINT
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
NEXT_REQUIRED_ACTIVITY = IMG-02 — Modelo, storage e proveniência (após adjudicação humana e autorização)
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_PROJECT_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
NEXT_REQUIRED_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
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
CONTINUITY_RECOVERY_GATE = REVALIDATE_GIT_AND_AUTHORITIES
USER_CONTINUITY_VALIDATION = NOT_REQUIRED_FOR_STATE_DISCOVERY
READY_TO_RESUME_PROJECT = YES_AFTER_READ_ONLY_REVALIDATION
RESUME_SCOPE = dentro das autorizações explícitas vigentes

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
1. validar repo root, branch, HEAD, `origin/master`, divergência, worktree e staging;
2. ler `ACTIVE_DOCUMENT_MAP.md`;
3. ler `PROJECT_STATE.md`;
4. ler `AGENT_CONTINUITY.md`;
5. ler `NEW_CHAT_BOOTSTRAP_PROMPT.md`;
6. ler `docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`;
7. ler roadmap, sprints, authority especializada e policies canônicas aplicáveis;
8. apresentar divergências e itens UNVERIFIED; não iniciar implementação por inferência.

## 8. Estado e próxima atividade no checkpoint anterior à integração UI-3 (histórico)

MON-09A = COMPLETE / PASS; MON-09B = COMPLETE / PASS_WITH_SCOPE_DEVIATION; MON-09C = COMPLETE / PASS_WITH_FINDINGS; MON-09D = COMPLETE; MON-09E = COMPLETE / PASS.

MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_PROJECT_ACTIVITY = UI-3 — CameraQuickDetailPanel
NEXT_PROJECT_ACTIVITY_STATUS = NEXT_CANDIDATE / NOT_AUTHORIZED
NEXT_REQUIRED_ACTIVITY = UI-3 — CameraQuickDetailPanel (sujeita a autorização explícita)
NEXT_REQUIRED_ACTIVITY_STATUS = NEXT_CANDIDATE / NOT_AUTHORIZED
UI_DS_CANONICAL_SPEC = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
UI_DS_CANONICAL_SPRINT_MAP = docs/projeto/SPRINTS_ARGOS_V5.md
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
CAMERA_QUICK_DETAIL_PANEL = USER_APPROVED / details in docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md section 7.3
CAMERA_QUICK_DETAIL_PANEL_VMS = DO_NOT_ADOPT; VMS_REPLACEMENT = LOCATION
ARGOS_CURRENT_PAGE_COMPOSITION = PRESERVE
LATEST_CAMERA_CAPTURE_FEEDS_PANEL = SECURE PREVIEW AVAILABLE; UI-3 MUST REUSE PANEL VARIANT
PRIMARY_IMAGE_DISTINCTION = RECORDED
MANUAL_UPLOAD_PROVENANCE = PRESERVED
NO_AUTO_CAPTURE_ON_PANEL_OPEN = RECORDED
FASE_C_DEPENDENCY = EXPLICIT
ARGOS_INCREMENTAL_INTEGRATION_RULE = RECORDED
INTEGRATION_GATE = REQUIRED_WHEN_APPLICABLE
BIG_BANG_INTEGRATION = PROHIBITED
UI_DS = UI-0, UI-1, UI-2, UI-3, UI-4
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED
SECURITY_FINDINGS_AUTHORITY = docs/security_audit/auditoria_segurança_001.md; ver matriz vigente antes de reclassificar SEC-001...SEC-010
LOG_VOLUME_HARDENING_STATUS = HARDENING / NON-BLOCKING — potential high INFO log volume per cycle/attempt

No checkpoint desta seção, UI-3 era a próxima candidata e ainda não estava autorizada. Esse estado foi supersedido pela integração UI-3 e pelo checkpoint vigente da seção 15. A frente de monitoramento continua encerrada tecnicamente; não retomar MON-09 nem criar outra atividade MON. Revalidar Git ao iniciar nova sessão.

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


### Fechamento técnico MON-09 — registro histórico do checkpoint

O retrato desta seção pertence ao fechamento MON-09. O estado atual do projeto
após IMG-01 e do handoff está registrado nas seções 8 e 11.

LAST_RELEVANT_TECHNICAL_CHECKPOINT = 850efd2381d7f5b7df27e528dc3374ea58e507b3 (850efd2)
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_PROJECT_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
VALIDATED_ENVELOPE = UNKNOWN / ONLINE / OFFLINE como estados estáveis; SUSPECT efêmero; STALE como freshness; confirmation memory persistente; pending failure streak sobrevive restart; thresholds respeitados; restart sem transição/outage falsa; falha de banco não equivale a câmera offline; CANCELLED neutro; timeout/rede conforme semântica canônica; sem histórico funcional falso em falha operacional e com recovery possível; ownership por câmera, owner persistente e epoch monotônico; lease define elegibilidade operacional de takeover; epoch é fencing token; config_generation é independente; completion de owner obsoleto sem side effects de domínio; owner antigo não libera owner novo; completion válida libera ownership atomicamente; renovação de lease não implementada; MonitoringConfig integrado à configuração ARGOS, config inválida fail-fast; status, backlog/in-flight, falhas operacionais e ownership diagnosticáveis; observabilidade sem histórico funcional e logs sem secrets
FUTURE_VALIDATIONS = PostgreSQL real; multi-processo real em produção; rede real; câmeras reais; credenciais reais; capacidade produtiva; budgets formais de CPU, memória e conexões
SECURITY_GATES = LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS; HOMOLOGATION = BLOCKED; DEPLOYMENT = BLOCKED; PRODUCTION = BLOCKED
IMPLEMENTATION_FUTURE = requer autorização própria

## 10. UI-DS e continuidade de produto — contexto histórico (status atual na seção 15)

Existe uma specification canônica para a integração seletiva do
`camera-inventory-design-system-v1.0.1`:

`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`

O mapa canônico de sprints/slices é:

`docs/projeto/SPRINTS_ARGOS_V5.md`

O pacote de referência recebido foi localizado em:

`C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip`

Sua cópia canônica está em
`docs/projeto/camera-inventory-design-system-v1.0.1.zip`; o título interno foi
alinhado para `v1.0.1`, e o ZIP original em Downloads foi preservado sem
alteração. A frente UI-DS registra retrofit visual seletivo, adoção seletiva de
interações, preservação da composição atual do ARGOS, adoção do
`CameraQuickDetailPanel`, dependência explícita da Fase C para
`LATEST_CAMERA_CAPTURE`, distinção de `PRIMARY_IMAGE`, preservação da
proveniência `UPLOAD_MANUAL`, ausência de captura automática na abertura,
proibição de integração big-bang e `INTEGRATION_GATE` obrigatório quando
aplicável.

`IMG-01` está concluída como checkpoint documental; a authority canônica é
`docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`. A seleção de
`LATEST_CAMERA_CAPTURE_RECORD` ocorre antes da avaliação de disponibilidade ou
integridade, portanto não há fallback silencioso para captura antiga. As
proveniências iniciais são somente `CAPTURA_CAMERA` e `UPLOAD_MANUAL`;
`CameraQuickDetailPanel` consome `LATEST_CAMERA_CAPTURE`, sem captura na
abertura. Monitoramento e captura permanecem separados.

`IMG-02` é a próxima atividade de projeto, mas requer adjudicação humana e
autorização própria antes de implementação. Backend de storage, limites de
arquivo, fallback visual de `UPLOAD_MANUAL`, retenção/expurgo, política
temporal `STALE`, credencial/perfil para captura e semântica de
`PRIMARY_IMAGE` são sete decisões abertas; o contrato canônico especifica o
fechamento de cada uma. `UI-0`
está registrada como `COMPLETE / PASS_WITH_FINDINGS`, read-only, sem autorizar
implementação visual.

## 11. Handoff ARGOS — checkpoint histórico (supersedido pela seção 15)

Authority normativa específica: `docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`.
O `PROJECT_STATE.md` é o snapshot operacional; este documento preserva somente
os invariantes, riscos, limites, decisões abertas e referências necessários à
retomada. O `ACTIVE_DOCUMENT_MAP.md` identifica escopo e vigência de cada
authority, e o bootstrap define a sequência de recuperação.

```text
ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE
LAST_COMPLETED_PROJECT_ACTIVITY = IMG-01 — Contrato funcional de imagem
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
OPEN_DECISION_COUNT = 7; consultar ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
UI_DS_STATUS = UI-0 COMPLETE / PASS_WITH_FINDINGS; UI-1...UI-4 PENDING
UI_0_FINDINGS_DETAILS = docs/projeto/ARGOS_UI_DS_UI0_PREFLIGHT_FINDINGS_V1.md; UI_0_FINDINGS_DISCOVERABLE = YES; PASS_WITH_FINDINGS não bloqueante
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED
BIG_BANG_INTEGRATION = PROHIBITED
INTEGRATION_GATE = REQUIRED_WHEN_APPLICABLE
```

Os findings recuperados do UI-0 estão em
`docs/projeto/ARGOS_UI_DS_UI0_PREFLIGHT_FINDINGS_V1.md`; o relatório preserva
os itens sem ampliá-los e sem convertê-los em blockers. O handoff gate deste
checkpoint passa após a reconciliação documental. Nenhuma próxima atividade ou
prontidão técnica amplia autorização.


## 12. Registro histórico — integração IMG-02 + UI-1 (2026-09-25)

Este checkpoint supersede as referências anteriores que apontam IMG-02 como
próxima, aguardando adjudicação ou ainda não integrada. O estado Git, os
commits, as candidatas sem autorização e as authorities técnicas são
recuperáveis neste repositório, sem histórico de chat.

IMG-02 = COMPLETE / INTEGRATED
IMG-02_COMMIT = ceda8f6
UI-1 = COMPLETE / INTEGRATED
UI-1_COMMIT = c5928e8
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; cameras.test_imagens_read_service 13/13 PASS
IMG-03 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-2 = NEXT_CANDIDATE / NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
PRODUCTION_STORAGE_BACKEND = DEFERRED; IMG-02 requer contrato persistente de storage e abstração configurável, conforme ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
OPEN_DECISIONS = consultar o contrato canônico de imagem
SPRINT_ORDER_AUTHORITY = docs/projeto/SPRINTS_ARGOS_V5.md
PROJECT_STATE = docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md
BASELINE = master; HEAD d5f1f54bea518496d7e8c8b64487cfea459372f6; origin/master 05b710a57137f9d0cdefd256c037e4d86fe0e3bb; ahead 3 / behind 0
WORKTREE = documentação deste checkpoint modificada e unstaged; staging vazio
IMPLEMENTATION_AUTHORIZED = nenhuma autorização atual; autorização anterior IMG-02 consumida
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED
ACTIVITY_COMPLETION_PERCENT = 100%
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS

## 13. Registro histórico — integração IMG-03 + UI-2 (2026-09-25)

Este checkpoint supersede o estado anterior IMG-02 + UI-1. O snapshot Git
completo, evidências dos gates, defaults locais e lista de decisões deferred
estão em `PROJECT_STATE.md`; os detalhes continuam nas authorities
especializadas.

IMG-03 = COMPLETE / INTEGRATED
IMG-03_COMMIT = f6e08b6
IMG-03_INTEGRATION_COMMIT = 0708797
IMG-03_UPLOAD_MANUAL_FUNCTIONAL = YES
UI-2 = COMPLETE / INTEGRATED
UI-2_COMMIT = b57f959
UI-2_INTEGRATION_COMMIT = c79fa06
INTEGRATION_GATE = PASS

INVENTORY_CAMERA_THUMBNAIL = APPROVED; SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = DEFERRED
THUMBNAIL_CURRENT_RENDERING = placeholder neutro; não há thumbnail real nem completude funcional
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

STORAGE_BACKEND_DEFINITIVE = DEFERRED
IMAGE_FORMAT_POLICY_DEFINITIVE = DEFERRED
UPLOAD_SIZE_LIMIT_POLICY_DEFINITIVE = DEFERRED
IMAGE_DIMENSION_LIMIT_POLICY_DEFINITIVE = DEFERRED
PILLOW = dependência técnica de upload; versão 12.3.0 disponível no venv integrado
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED / FUTURE HARDENING

CANONICAL_IMAGE_AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
CANONICAL_UI_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
SPRINT_ORDER_AUTHORITY = docs/projeto/SPRINTS_ARGOS_V5.md
GIT_BASELINE = master; HEAD c79fa06775ccb707b6753f2a8ed0e988e8a9c86d; origin/master 547678de9c70ee9eda2fc30599417d217c878006; ahead 4 / behind 0
GIT_WORKTREE = seis documentos desta reconciliação modificados e unstaged; staging vazio
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED
PROJECT_STATE_UPDATE = PASS
DOCUMENT_RECONCILIATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS
NEW_AGENT_CAN_RESUME_WITHOUT_CHAT_HISTORY = YES

## 14. Checkpoint histórico — Secure Image Preview Delivery (2026-09-25)

```text
SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED
TECHNICAL_COMMIT = e3f2d40
INTEGRATION_COMMIT = 7ca5f7c
INTEGRATION_GATE = PASS
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
PREVIEW_VARIANTS = THUMB; PANEL; dimensões na authority de imagens, seção 24
UI-3 = NEXT_CANDIDATE / NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
IMPLEMENTATION_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
```

No checkpoint, UI-3 era a próxima candidata e deveria reutilizar a variante
PANEL existente. Esse estado foi supersedido pela integração da UI-3 registrada
na seção 15. Os detalhes do contrato de preview continuam em
ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md.

## 15. Checkpoint histórico — UI-3 integrada, aceitação visual pendente (2026-09-25)

```text
UI-3_TECHNICAL_IMPLEMENTATION = COMPLETE
UI-3_TECHNICAL_COMMIT = bcc7e7d
UI-3_INTEGRATION = COMPLETE
UI-3_INTEGRATION_COMMIT = 1015a8f
INTEGRATION_GATE = PASS
UI-3_FUNCTIONAL_VALIDATION = PASS
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
UI-3_VISUAL_ACCEPTANCE = PENDING
UI-3_PRODUCT_ACCEPTANCE = PENDING
UI-3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PENDING
IMG-04 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-4 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
IMPLEMENTATION_AUTHORIZED = NO for further UI-3/IMG-04/UI-4 work
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED
OPEN_IMAGE_DECISIONS = 7; details in ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
ON_DEMAND_PREVIEW_COST_LOAD_BENCHMARK = DEFERRED / NOT BENCHMARKED
PERSISTENT_DERIVED_PREVIEW_CACHE_OR_CDN = DEFERRED
FINAL_IMAGE_PERMISSION_MATRIX = DEFERRED
DEFINITIVE_STORAGE_BACKEND = DEFERRED
DEFINITIVE_MIME_SIZE_DIMENSION_POLICY = DEFERRED
UPLOAD_REJECTION_AUDIT_HARDENING = DEFERRED / future hardening IMG-08
```

UI-3 usa a variante `PANEL` da entrega segura para `LATEST_CAMERA_CAPTURE`, sem
fallback para upload manual, imagem principal ou captura anterior; abrir o
painel não captura imagem nem altera monitoramento. Os detalhes funcionais e
técnicos, o registro de evidências e a regra de aceitação visual ficam na
authority UI-DS e em `PROJECT_STATE.md`; o contrato do preview e as decisões de
imagem ficam em `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`. Evidência funcional e QA
visual foram fornecidas para esta reconciliação; os testes não foram
reexecutados. Nenhuma rodada de reparo visual foi iniciada.

## 16. Checkpoint histórico — UI-4A Desktop Shell Density Foundation (2026-09-26)

```text
UI-4A_USER_AUTHORIZED = YES
UI-4A_SCOPE = shell global: largura e centralização do conteúdo, sidebar, topbar e gutters
UI-4A_TECHNICAL_IMPLEMENTATION = COMPLETE
UI-4A_VISUAL_ACCEPTANCE = PENDING_USER
MAIN_CONTENT_MAX_WIDTH = 2304px -> 1400px
MAIN_CONTENT_RENDERED_WIDTH = 2224px -> 1400px at 2552x866 / 100%
SIDEBAR_WIDTH = 248px -> 164px; brand fits without clipping
TOPBAR_HEIGHT = 60px -> 40px token / 42px rendered
PAGE_TOP_SPACING = 40px -> 32px; PAGE_BOTTOM_SPACING = 48px -> 40px
CONTENT_CENTERED = YES; EXCESSIVE_HORIZONTAL_STRETCH = NO
DASHBOARD_LAYOUT_REGRESSION = NO; existing grids/card geometry preserved
INVENTORY_FILTER_LAYOUT_AFTER_SHELL_CHANGE = ONE_ROW at 2552x866; TWO_ROWS at 1366x768
INVENTORY_LAYOUT_REGRESSION = YES finding: local table-region horizontal bar (2px wide viewport; 7px at 1366); baseline attribution unverified
HORIZONTAL_ROOT_OVERFLOW = NO; table-region remains locally scrollable
BREAKPOINT_REGRESSION_FOUND = NO at 2552x866, 1366x768, 900x768, 390x844; zoom 100%
QUICK_DETAIL_MODIFIED_BY_UI4A = NO; pre-existing UI-3 diff preserved
FILES_CHANGED_BY_UI4A = static/css/argos.css; static/css/design-system.css
PREEXISTING_DIFF = static/css/inventario.css (UI-3 Drawer), unchanged
DJANGO_CHECK = PASS
GIT_DIFF_CHECK = PASS
BROWSER_CONSOLE_ERRORS = NONE observed
GIT = master; HEAD cad0760; origin/master 47c6965; ahead 3 / behind 0; changes unstaged; staging empty
READY_FOR_USER_VISUAL_REVIEW = YES
ACTIVITY_COMPLETION_PERCENT = 95%; activity is not complete until user visual acceptance
UI-4B / UI-4C / UI-4D / UI-4E = NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
IMPLEMENTATION_AUTHORIZED = NO after this UI-4A slice
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
PROJECT_STATE_UPDATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS
```

A checagem visual confirmou o shell centralizado e responsivo. A tabela mantém
uma barra horizontal local de 2px no viewport alvo; uma tentativa de aumentar
o max-width em 4px não removeu a diferença e foi revertida. Não foram alterados
a tabela, os filtros, os cards do Dashboard, os controles ou o Quick Detail.
A aceitação final da aparência pertence ao usuário; as fatias seguintes de
UI-4 continuam sem autorização.

## 17. Handoff histórico — frente de remediação de UI (2026-09-27)

O usuário continuará a melhoria de UI/UX e front-end do ARGOS com este agente.
Ler `docs/frontend/ARGOS_FRONTEND_AUDIT_REPORT.md` como evidência de UI-AUD-01
e `docs/frontend/ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md` como diretriz
técnica. A auditoria recomenda refatoração estrutural do CSS existente; não
propõe migração de stack. Novos patches visuais estão congelados até as fases
de remediação. O detalhamento Phase 0..6 fica na diretriz e a ordem executiva
em `docs/projeto/SPRINTS_ARGOS_V5.md`.

O checkpoint local `768844d` preservou os cinco arquivos previamente sujos
do `master`. O delta recente do Quick Detail em `inventario.css` é trabalho
preservado, não aceito visualmente. UI-3/Quick Detail segue integrada com
aceitação visual/produto pendente; três cards full width empilhados, quatro
campos por card e Ambiente preservado. O ajuste para 2048×741 sem scroll
interno permanece não comprovado. A Phase 6 tratará o drawer após as fases
anteriores; Phase 0 ainda não começou.

IMG-DISPLAY-01 está integrado pelo merge `cad0760`, usando a política
DISPLAY_IMAGE do contrato de imagem, seção 25. A imagem exibida no Inventário
e no Quick Detail pode usar upload manual somente em
`NO_CAPTURE_AVAILABLE`; não muda a semântica de LATEST_CAMERA_CAPTURE. Revalidar Git,
runtime e aceitação antes de declarar gates de implementação. Nenhum push foi
autorizado por esta frente documental.

## 18. Continuidade — fechamento da Phase 0 (2026-09-27)

A seção 17 preserva o handoff anterior à execução da remediação. O estado
vigente após integração canônica e aceitação visual pós-integração está em
`docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 20,
e `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 15.

```text
CANONICAL_BRANCH = master
CANONICAL_HEAD_AT_PHASE0_MERGE = 9bdea6a9f39a908a2f19b33b8132102631868066
ARGOS_UI_REMEDIATION_PHASE0 = CLOSED
PHASE0_CANONICAL_CODE_INTEGRATION = PASS
POST_INTEGRATION_VISUAL_GATE = PASS
PHASE0_CANONICAL_CLOSURE = PASS
PHASE1 = READY_NOT_STARTED
NEXT_ACTIVITY = ARGOS UI REMEDIATION — PHASE 1 / CSS OWNERSHIP CONSOLIDATION
IMPLEMENTATION_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
```

Phase 1 não foi iniciada nem autorizada por este registro.

## 19. UI V2 — continuidade vigente (2026-09-27)

O checkpoint atual e os fatos Git validados estão na seção 29 de
PROJECT_STATE.md. A authority operacional da trilha é
docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md; o inventário factual e a authority do
census estão em docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md; a direção macro e a
ordem executiva estão, respectivamente, em docs/projeto/ROADMAP_ARGOS_V5.md e
docs/projeto/SPRINTS_ARGOS_V5.md.

```
UI_V2_TRACK_STATUS = DOCUMENTED / P0_CLOSED_PASS / P1_CLOSED_PASS / PARALLEL_TO_BACKEND
UI-V2-P0 = CLOSED_PASS / ACTIVITY_COMPLETE = YES
UI-V2-P1 = CLOSED / PASS / ACTIVITY_COMPLETE = YES
USER_SELECTION = C — ARGOS HYBRID
USER_VISUAL_SELECTION_GATE = PASS
DIRECTION_A_STATUS = HISTORICAL_ALTERNATIVE / NOT_SELECTED
DIRECTION_B_STATUS = HISTORICAL_ALTERNATIVE / NOT_SELECTED
DIRECTION_C_STATUS = SELECTED / VISUAL_DIRECTION_AUTHORITY
SCREEN_CENSUS_AUTHORITY = docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md
SCREEN_CENSUS = 35_SURFACES / 15_FAMILIES / 24_YES / 11_INHERITED / 0_NO
NEXT_UI_ACTIVITY = UI-V2-P2 — VISUAL FOUNDATION
NEXT_UI_ACTIVITY_STATUS = NOT_STARTED / REQUIRES_SEPARATE_AUTHORIZATION
P2_STARTED = NO
QUICK_DETAIL = APPROVED / PROTECTED
ADMIN_UI_V2_SCOPE = TRACKED_AS_INHERITED / NO_CUSTOM_REDESIGN_BY_DEFAULT
PROTOTYPE_STACK_COMPATIBILITY = REQUIRED_GATE
CANONICAL_STACK = Django SSR + Django Templates + semantic HTML + custom CSS + Vanilla JS + progressive enhancement
PROTOTYPE_VISUAL_ACCEPTANCE_GATE = REQUIRED
POST_IMPLEMENTATION_VISUAL_ACCEPTANCE_GATE = REQUIRED
QUICK_DETAIL_VISUAL_BASELINE = APPROVED / PROTECTED
QUICK_DETAIL_REDRAW_WITHOUT_NEW_EXPLICIT_AUTHORIZATION = PROHIBITED
BATCH_B_POST_INTEGRATION_VISUAL_GATE = PENDING_USER_REVIEW
PHASE0_AND_BATCH_A = CLOSED / PRESERVED
BATCH_B_STATUS = TECHNICALLY_INTEGRATED_ON_MASTER / SOURCE_VISUAL_ACCEPTANCE_PASS / INTEGRATED_VISUAL_REVIEW_PENDING
```
UI-3_VISUAL_ACCEPTANCE = PASS para a baseline atual do Quick Detail,
aprovada explicitamente pelo usuário; UI-3_PRODUCT_ACCEPTANCE segue PENDING. O
Admin permanece contado no census como superfícies herdadas; a decisão padrão
de planejamento não inclui redesenho customizado, salvo autorização explícita
posterior. A recomendação backend MON-AVAIL-02 e o bloqueio informado para
MON-AVAIL-01 foram fornecidos na instrução atual, mas não foram encontrados
como registros locais; IMG-04 permanece candidata não autorizada no mapa de
sprints. O sequenciamento backend entre essas frentes continua aberto, sem
métricas fabricadas.

P0 é documentalmente encerrado. Não iniciar P1, protótipos ou implementação sem
autorização explícita própria.

## 20. UI-V2-P2 — continuidade do início da execução (checkpoint histórico supersedido, 2026-09-28)

Este checkpoint registra a execução antes da aprovação visual e é mantido para rastreabilidade. Seus estados e instruções operacionais foram supersedidos pelo checkpoint vigente na seção 20.3, por PROJECT_STATE.md seção 33 e pelo master plan seção 12.3. Consultar esses registros mais recentes para o status e próximos gates. A aprovação humana e a autorização de fechamento agora estão registradas nesses checkpoints atuais.

CURRENT_ACTIVITY = UI-V2-P2 — VISUAL FOUNDATION
CURRENT_STATUS = PASS / READY_FOR_USER_FOUNDATION_REVIEW
DESIGN_STRATEGY = CODE_FIRST / STACK_NATIVE / PROTOTYPE_DRIVEN
VISUAL_DIRECTION = C — ARGOS HYBRID / NOT_REOPENED
CANONICAL_CSS = static/css/ui-v2/{tokens.css,base.css,components.css,patterns.css}
DESIGN_SYSTEM_VERSION = 2.0.0-rc.1 / APPROVAL_PENDING
FIGMA = PARTIAL_REFERENCE / OPTIONAL / NON-CANONICAL / BLOCKS_P2=NO
PRODUCTION_RUNTIME_BEHAVIOR_CHANGED = NO
PRODUCTION_TEMPLATES_CHANGED = NO
PRODUCTION_UI_V2_INTEGRATION_STARTED = NO
UI_V2_CSS_REFERENCED_BY_PRODUCTION = NO
P3_STARTED = NO
QUICK_DETAIL = APPROVED / PROTECTED / NO_TOKEN_MIGRATION
ADMIN = INHERITED / NO_CUSTOM_REDESIGN
DESIGN_QA = PASS / SCREENSHOT_EVIDENCE_PERSISTED
COMMIT = NOT_CREATED / REVIEW_HANDOFF_READY

Preservar os contratos visuais em docs/prototype/ui-v2/contracts/ e a foundation em docs/prototype/ui-v2/foundation/. O checkpoint 20.1 supersede a pendência de screenshots e gates de interação: ambos passaram, com evidências persistidas. A próxima ação é a revisão visual humana. Não aprovar em nome do usuário, não promover 2.0.0, não iniciar P3 e não alterar templates ou runtime de produção.



### 20.1. UI-V2-P2 — QA técnico antes do aceite humano (snapshot histórico supersedido, 2026-09-28)

O checkpoint 31 de PROJECT_STATE.md supersede os campos de validação pendente acima quanto ao QA. A revisão técnica passou; falta a decisão visual do usuário.

CURRENT_STATUS = PASS / READY_FOR_USER_FOUNDATION_REVIEW
ACTIVITY_COMPLETION_PERCENT = 98%
DESIGN_QA = PASS / SCREENSHOT_EVIDENCE_PERSISTED
VIEWPORTS = 1440x900; 1366x768; 1920x1080; 900x768; 768x900; 390x844
ROUTE_VIEWPORT_SWEEP = PASS / 48 of 48
KPI_LAYOUT = 260x78.3 at 1366/1440 / 3 columns; 2+1 at 900/768; single column at 390
PROJECT_STATE_UPDATE = PASS
USER_FOUNDATION_APPROVAL = PENDING
UI_FOUNDATION_VISUAL_ACCEPTANCE = PENDING_USER
DESIGN_SYSTEM_VERSION_PINNED = NO
P3_STARTED = NO
COMMIT = NOT_CREATED / review handoff

As capturas ficam em docs/prototype/ui-v2/foundation/screenshots/; o relatório integral fica em design-qa.md. Não declarar ACTIVITY_COMPLETE até a aprovação visual humana.



### 20.2. UI-V2-P2 — composição dos KPI tiles antes do aceite final (snapshot histórico supersedido, 2026-09-28)

O checkpoint 32 de PROJECT_STATE.md supersede a composição KPI registrada em 20.1. Direção C preservada; esta atualização aplica a instrução visual explícita mais recente.

CURRENT_STATUS = PASS / READY_FOR_USER_FOUNDATION_REVIEW
ACTIVITY_COMPLETION_PERCENT = 98%
KPI_GROUP_CENTERED = YES
KPI_CONTENT_CENTERED = YES
KPI_CARD_WIDTH = 220px
KPI_CARD_HEIGHT = 77.3px / natural
KPI_GROUP_WIDTH = 692px at desktop / centered
KPI_GAP = 16px
KPI_INTERNAL = padding 14x16; value-label gap 4px; value and label centers aligned
KPI_RESPONSIVE = 3 desktop; 2+1 tablet with centered final tile; 1 mobile
GENERIC_CARD_ALIGNMENT_CHANGED = NO
RESPONSIVE_REGRESSION = NO
UI_VISUAL_ACCEPTANCE = PENDING_USER
PROJECT_STATE_UPDATE = PASS
ACTIVITY_COMPLETE = NO
P3_STARTED = NO
COMMIT = NOT_CREATED / review handoff

As capturas atuais e a comparação ficam em docs/prototype/ui-v2/foundation/screenshots/. O aceite final continua pendente do usuário.



### 20.3. UI-V2-P2 — aprovação e fechamento (2026-09-28)

Este checkpoint supersede os estados históricos pendentes das seções 20–20.2. A aprovação humana foi concedida explicitamente no adendo de fechamento.

CURRENT_ACTIVITY = UI-V2-P2 — VISUAL FOUNDATION + CANONICAL INTEGRATION
P2_STATUS = CLOSED / PASS
USER_VISUAL_ACCEPTANCE = PASS
USER_FOUNDATION_APPROVAL = PASS
DESIGN_SYSTEM_VERSION = 2.0.0
DESIGN_SYSTEM_VERSION_PINNED = YES
P2_GATES = PASS / tokens, components, density, responsive, interaction, domain-status language, desktop/mobile, accessibility interaction, long content
P2_CLOSURE_COMMIT = PENDING_LOCAL_COMMIT
CANONICAL_MERGE = AUTHORIZED / pending
POST_MERGE_DJANGO_CHECK = PENDING
PUSH_AUTHORIZED = YES / pending gates
PUSH_PERFORMED = NO
REMOTE_SYNC = PENDING
PRODUCTION_RUNTIME_BEHAVIOR_CHANGED = NO
PRODUCTION_TEMPLATES_CHANGED = NO
PRODUCTION_UI_V2_INTEGRATION_STARTED = NO
UI_V2_CSS_REFERENCED_BY_PRODUCTION = NO
P3_STARTED = NO
NEXT_ACTIVITY = UI-V2-P3 — NAVIGABLE SCREEN PROTOTYPES / NOT STARTED
PROJECT_STATE_UPDATE = PASS
ACTIVITY_COMPLETE = NO / canonical integration pending

O fechamento de P2 não inicia P3. A conclusão da atividade ampliada exige merge, Django check, push e sincronização remota.

### 20.4. UI-V2-P2 — merge canônico e validação Django (2026-09-28)

Checkpoint vigente de integração antes do push. Os estados de P2 e aprovação permanecem os da seção 20.3; esta seção registra o merge e gates posteriores.

P2_CLOSURE_COMMIT = 7277f16f3f6470c975d2e9624309c1dd04e78eb1
MASTER_BEFORE = 6de91063526ab9e323114ad69f0967cc2849145a
MERGE_COMMIT = 7da532ffd93311a4d8d7ea86ec668fb7ec7d0165 / NO_FF
INTEGRATION_GATE = PASS
POST_MERGE_DJANGO_CHECK = PASS / System check identified no issues
PUSH_AUTHORIZED = YES
PUSH_PERFORMED = NO / pending
REMOTE_SYNC = PENDING
PROJECT_STATE_UPDATE = PASS
ACTIVITY_COMPLETE = NO / push and remote sync pending
P3_STARTED = NO
PRODUCTION_RUNTIME_BEHAVIOR_CHANGED = NO
PRODUCTION_TEMPLATES_CHANGED = NO
### 20.5. UI-V2-P2 — atividade concluída e remota sincronizada (2026-09-28)

Fechamento final após envio da atualização de estado e verificação pós-push.

P2_STATUS = CLOSED / PASS
USER_VISUAL_ACCEPTANCE = PASS
DESIGN_SYSTEM_VERSION = 2.0.0 / PINNED
P2_CLOSURE_COMMIT = 7277f16f3f6470c975d2e9624309c1dd04e78eb1
MERGE_COMMIT = 7da532ffd93311a4d8d7ea86ec668fb7ec7d0165 / NO_FF
POST_MERGE_DJANGO_CHECK = PASS
PUSH_PERFORMED = YES / origin master
REMOTE_SYNC = PASS / HEAD local = origin/master; divergence 0/0
PROJECT_STATE_UPDATE = PASS / final checkpoint published
ACTIVITY_COMPLETE = YES
P3_STARTED = NO
PRODUCTION_RUNTIME_BEHAVIOR_CHANGED = NO
PRODUCTION_TEMPLATES_CHANGED = NO
### 20.6. UI-V2-P3-0 — harness em revisão técnica (2026-09-28)

CURRENT_ACTIVITY = UI-V2-P3-0 / PROTOTYPE HARNESS & COMPOSITION CONTRACT
CURRENT_STATUS = COMPLETE / PASS / PUBLISHED / FAN-OUT READY
ACTIVITY_COMPLETION_PERCENT = 100%
CANONICAL_REPOSITORY_ROOT = C:\Users\walacedelgado\PycharmProjects\projeto_argos
P3_0_BASELINE_HEAD = 7702b4c14cac6f7338625ccd08730e8d89fb9495
BRANCH = codex/ui-v2-p3-0-prototype-harness
DESIGN_SYSTEM_VERSION = 2.0.0 / PINNED / UNMODIFIED
PRODUCT_DESIGN_GET_CONTEXT = PASS
PRODUCT_DESIGN_DESIGN_QA = PASS / shared shell only
SCREEN_OWNERSHIP = 35 IDs / no conflicts
FAMILY_PARTITION = P3-A/B/C/D / 24 eligible / 11 inherited or protected
P3_FAMILY_IMPLEMENTATION_STARTED = NO
PRODUCTION_CHANGED = NO
P3_0_WORK_COMMIT = 7bf33de0456fbaaaf46943d73f44f82abb3e3a84
USER_P3_0_APPROVAL = PASS
CANONICAL_INTEGRATION = PASS / merged --no-ff and published
MERGE_COMMIT = 02d1c03c8df784f82ae1d3d838a17d49a0db6eae
POST_INTEGRATION_VALIDATION = PASS / Django check + HTTP_LOCAL prototype checks
REMOTE_SYNC_AFTER_P3_0 = PASS / HEAD == origin/master; divergence 0/0
FAN_OUT_BASE_COMMIT = CURRENT PUBLISHED MASTER HEAD / EXACT SHA IN GATE REPORT
FAN_OUT_READY = YES
PROJECT_STATE_UPDATE = PASS
CONTINUITY_RECONCILIATION = PASS / Card B is activity-specific authority; older roadmap snapshots retained
ACTIVITY_COMPLETE = YES / technical harness, user review, integration, validation and publication complete
PUSH_PERFORMED = YES / origin/master; divergence 0/0
MERGE_PERFORMED = YES / --no-ff

O harness, índice, shell, fixture, quatro capturas e contratos estão em `docs/prototype/ui-v2/`. O master `SCREEN_COVERAGE.md` permanece root-owned; as famílias continuam sem artefatos. P3-0 foi aprovado, integrado, validado e publicado; fan-out liberado a partir do `FAN_OUT_BASE_COMMIT` indicado no relatório final. P3-A/B/C/D não foram iniciadas.

### 20.7. UI-V2 ROOT — sincronização e patch semântico do Design System (2026-09-28)

CURRENT_ACTIVITY = UI-V2 ROOT — HOME SYNCHRONIZATION + DSCR-UIV2-001-HIDDEN-SEMANTICS
CURRENT_STATUS = COMPLETE / PASS / PUBLISHED
ACTIVITY_COMPLETION_PERCENT = 100%
CANONICAL_REPOSITORY_ROOT = C:\Users\walac\desenvolvimento\projeto_argos
MASTER_SYNC = PASS / FF_ONLY to 9943e20d9b1e04159e067c72aa4dd70eab2bdb36
ROOT_PATCH_BRANCH = codex/ui-v2-ds-2.0.1-hidden-semantics
DESIGN_SYSTEM_VERSION = 2.0.1
DS_PATCH_WORK_COMMIT = 8121ed38cc15e1ff6e72cb46bbb2ca865100bce0
DS_PATCH_INTEGRATION_COMMIT = 70e996f5e25d9c9b5d0f4ec0a256c44efcec6274 / NO_FF
REMOTE_SYNC_AFTER_PATCH_PUSH = PASS / HEAD == origin/master at 70e996f; divergence 0/0
REMOTE_HANDOFFS = 4/4 MATCH
P3_A = 2ca597826af7b32c884f4efd91cc49381ee646a5
P3_B = b57ad0044722a838e761f987eeb0aa556c6646b0
P3_C = ed7e2e5567b312b52c190484e2c174b26912415c
P3_D = ce13ff299d5c5419994aab0dc574a914a56760aa
ROOT_CAUSE = author display declarations overrode native hidden semantics
HIDDEN_RULE = [hidden]:not([hidden="until-found" i]) { display: none !important; }
HIDDEN_RULE_OWNER = static/css/ui-v2/base.css / @layer reset
DCR = docs/prototype/ui-v2/contracts/DSCR-UIV2-001-HIDDEN-SEMANTICS.md
DCR_PATCH_COMMIT = resolves to DS_PATCH_WORK_COMMIT in this checkpoint
VALIDATION = browser cases A-F PASS; P3-A targeted state/fixture regression PASS; Django check PASS; diff check PASS
PRODUCT_DESIGN_GET_CONTEXT = COMPLETE
PRODUCT_DESIGN_DESIGN_QA = PASS_WITH_FINDINGS / limited to root patch regression
FULL_P3_FAMILY_DESIGN_QA = NOT_RUN / remains a family gate after propagation
P3_FAMILY_FILES_CHANGED = NO
PRODUCTION_CHANGED = NO
P3_D_LOCAL_HIDDEN_WORKAROUND = REQUIRES_REVIEW_AFTER_DS_2_0_1_PROPAGATION
TEMP_VALIDATION_CLEANUP = PASS / archived after stopping local server and removing scratch

P2 approval and P3-0/handoff references to Design System 2.0.0 are historical baselines and were not rewritten. The active CSS and ROOT harness version metadata now state 2.0.1. The 21 screen IDs consuming hidden across P3-A/B/C/D and the zero until-found consumers are listed in the DCR.

No P3-A/B/C/D family branch or artifact was modified or pushed. The temporary P3-A worktree was used only to validate the exact DS_PATCH_WORK_COMMIT and then archived. Product Design QA covered the semantic patch and active variant rendering only; it does not complete family responsive review, named screenshot evidence, human review or overall design QA.

CURRENT_BLOCKERS = none for the ROOT patch; P3 family completion awaits controlled patch propagation and family-specific QA
NEXT_ACTIVITY = controlled propagation of DS_PATCH_WORK_COMMIT to P3-A/B/C/D while keeping the ROOT-only DCR out of family changes; then reassess the family handoffs
NEXT_ACTIVITY_STATUS = PLANNED / NOT AUTHORIZED
P3_D_WORKAROUND_REVIEW = after patch propagation; do not remove automatically
IMPLEMENTATION_AUTHORIZED = NO / the root patch authorization was consumed
LIVE_AUTHORIZED = NO
PROJECT_STATE_UPDATE = PASS / see PROJECT_STATE.md section 37
CONTINUITY_RECONCILIATION = PASS
AGENT_HANDOFF_GATE = PASS
ACTIVITY_COMPLETE = YES / final state checkpoint published and synchronization verified at activity close

### 20.8. BC-00 — baseline documental do backend (2026-10-01)

O usuário reiniciou BC-00 após o gate de sincronização passar. Baseline de
trabalho: `master`, `HEAD = 38db46b2335ac8c1ce47207b3ae015388d839d5f`, inicialmente
igual a `origin/master`, worktree limpa e staging vazio. Índice e authorities:
`docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md`; estado formal
na seção 40 de `PROJECT_STATE.md`.

O domínio canônico de imagens permanece em
`docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`; não criar autoridade paralela.
O checkout tem núcleo local/sintético de scheduler/repository e estado de
monitoramento, além de serviços Django de upload/leitura/preview. Não há
evidência de catálogo/custódia de credenciais de câmera, adapters RTSP/HTTP
reais, worker de produção, engine PostgreSQL selecionada ou homologação de
rede/câmeras. Contratos registram limites e pendências sem convertê-los em
autorização de implementação, conexão, homologação ou LIVE.

O commit documental `7b0135f0e9911e6a03f1a297e606d848eaa44533` foi publicado em
`origin/master`; o push confirmou `master -> master`. O estado de trabalho após
a reconciliação deste checkpoint deve ser confirmado diretamente no Git. O
próximo passo é adjudicação humana do baseline e de qualquer atividade
posterior.

### 20.9. BC-AUTH-02 — integração e publicação (2026-10-01)

BC-AUTH-01 foi commitada como `55651d22a97e19fa342320b15a4f5276beadcf4a`
(`feat(auth): implement camera authorization contract`), filho direto da
baseline `29242953d17988c0d4e14612dbb12fdc40b6f530`. O preflight confirmou
`master` e `origin/master` nessa baseline; a integração foi feita por
fast-forward, sem conflito.

No estado integrado, `makemigrations --check` passou; os 54 testes focais e a
regressão de 209 testes para usuários, segurança do core e governança/autorização
de câmeras passaram. O Técnico não recebe permissões administrativas de
usuários, grupos ou permissões; sua allowlist afeta somente a classificação de
alvos operacionais geridos pelo Administrador ARGOS. A publicação dos commits funcional e documental passou; o fetch confirmou
`HEAD == origin/master` e worktrees limpas. Consultar Git diretamente para a
baseline atual em qualquer retomada. O snapshot detalhado é a seção 43 de `PROJECT_STATE.md`.

### 20.10. CAM-INT-01-FIX03 — integração validada (2026-10-02)

O checkpoint factual está na seção 44 de `PROJECT_STATE.md`. O commit de
implementação é `8d7ec31`; reparos são `9cc1159`, `e612328` e `75cdf70`.
`master` avançou por fast-forward para
`75cdf708b07a61b26cfd40181f163fcb44526083`; validações integradas passaram.
No momento deste registro, o push ainda estava pendente. CAM-INT-02 tem
predecessores técnicos satisfeitos no DAG, mas exige autorização própria e não
foi iniciada. WAVE_2 permanece aberta: CAM-INT-07 e MON-OBS estão em execução;
P5 permanece RUNNING. Atualizar este registro após verificar a publicação.

### 20.11. DOC-EXEC-01 — pipeline e continuidade (2026-10-02)

O snapshot corrente e o payload de retomada estão em `PROJECT_STATE.md`,
seção 45; o mapa de authorities aponta para esse checkpoint. A seção 20.10
registra o estado anterior de CAM-INT-01 e foi supersedida quanto ao estado
operacional atual. Revalidar Git e status de worktrees antes de retomar.

```text
EXECUTION_MODEL = CONTRACT_FIRST_PARALLEL_PIPELINE
PRIMARY_NEXT_ACTION = CAM-INT-02 integration gate, after source checkpoint
ACTIVE_LANES = CAM-INT-07; MON-OBS; P5
GLOBAL_CONTINUITY_OWNER = INTEGRATION_GATE
DO_NOT_WAIT_FOR_FULL_WAVE_COMPLETION = YES
```

### 20.12. CAM-INT-02-INT — integração e validação (2026-10-02)

O checkpoint factual atualizado está em `PROJECT_STATE.md`, seção 46. CAM-INT-02
foi integrado por merge controlado em `971793ef94d806b4165378b05f2060fdd35cdca2`;
compilação, `manage.py check`, migration check, 13 testes focais e 124 testes de
regressão passaram. O estado das lanes CAM-INT-07, MON-OBS e P5 permanece
RUNNING e não foi alterado. O security final gate continua diferido.

```text
CAM_INT_02_STATUS = INTEGRATED / VALIDATED
NEWLY_READY_CONTRACTS = CAM-INT-06 / execução requer autorização específica
CAM_INT_03_04_STATUS = NOT_READY / CAM-INT-07 RUNNING; CAM-INT-06 not implemented
STATE_COMMIT = eac2db3 / PUBLISHED
PUSH_AND_POST_PUSH_VERIFY = PASS / eac2db36560e46e5f254f4a4e536e36aebb4bee8
NEXT_IMPLEMENTATION_ACTION = CAM-INT-06 / READY_NOW, not started in CAM-INT-02-INT
```

O fetch após a publicação confirmou `HEAD == origin/master`, divergência `0/0`,
worktree limpa e staging vazio em `eac2db36560e46e5f254f4a4e536e36aebb4bee8`.
O registro final de fechamento e a releitura pós-publicação do DAG constam na
seção 46.1 de `PROJECT_STATE.md`.

### 20.14. CAM-INT-07-INT — integração controlada (2026-10-02)

Readiness de CAM-INT-03/04 nesta fotografia é histórico e supersedido pela
adjudicação CAM-INT-02-R1-ARCH na seção 20.16 e PROJECT_STATE seção 49.

O checkpoint local validado está na seção 48 de `PROJECT_STATE.md`. CAM-INT-07
foi integrada por merge controlado `7b67b10`; a reconciliação `386b727` usa o
contador moderno `ultima_geracao_configuracao` quando o IPv4 cadastrado muda.
Compilação, Django check, migration check, 26 testes focais e 234 regressivos
passaram. A publicação e o fetch pós-push são o gate restante. O DAG relido após
a integração identifica CAM-INT-03 e CAM-INT-04 como tecnicamente prontas, sob
autorização própria; nenhum sucessor foi iniciado. Rede/câmeras/ambiente real e
produção permanecem pendentes.

### 20.15. CAM-INT-07-INT — publicação confirmada (2026-10-02)

Publicação confirmada permanece factual; prontidão dos successors abaixo é
histórica, supersedida pela seção 20.16 quanto ao novo predecessor R1.

A integração, reconciliação e continuidade inicial foram publicadas em
`f5a3a71eb64c88fa7918caa1405f091bfa6fc4a2`. O fetch pós-push confirmou
`HEAD == origin/master`, divergência `0/0`, worktree limpa e staging vazio.
O fechamento final está na seção 48.1 de `PROJECT_STATE.md`; o DAG relido após
publicação marca CAM-INT-03 e CAM-INT-04 tecnicamente prontas, ainda sujeitas à
autorização própria. Homologação, câmeras, rede e produção continuam pendentes.

### 20.13. CAM-INT-06-INT — integração e validação local (2026-10-02)

O registro factual corrente está na seção 47 de `PROJECT_STATE.md`. CAM-INT-06
foi integrada por fast-forward em `07c811401c7724f779fcbec85b393eab8cf0f94b`;
compilação, checks Django/migration e 132 testes focais/regressivos passaram.
O gate local não valida câmera, rede, dados reais ou produção. O DAG foi relido:
CAM-INT-03/04 aguardam CAM-INT-07; os contratos posteriores seguem bloqueados
pelas dependências registradas na seção 47.

```text
CAM_INT_06_STATUS = IMPLEMENTED / INTEGRATED / VALIDATED_LOCAL / PUBLISHED
ENVIRONMENT_VALIDATION = PENDING
NEWLY_READY_CONTRACTS = []
STATE_COMMIT = a330b06 / PUBLISHED
PUSH_AND_POST_PUSH_VERIFY = PASS / HEAD == origin/master; divergence 0/0; clean
NEXT_IMPLEMENTATION_ACTION = CAM-INT-07 completion, then recheck CAM-INT-03/04 readiness
```

### 20.16. CAM-INT-02-R1-ARCH — boundary interna adjudicada (2026-10-02)

O snapshot vigente está em `PROJECT_STATE.md`, seção 49. Authority completa:
`docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md`;
DAG e registry foram reconciliados. O gap é a ausência de API pública interna
de execução na CAM-INT-02 publicada, cuja crypto continua sob esse ownership.

```text
CAM_INT_02_R1 = IMPLEMENTATION_READY / NOT_IMPLEMENTED / NOT_PUBLISHED
CAM_INT_03 = PAUSED_ARCHITECTURAL_DEPENDENCY / blocker CAM-INT-02-R1
CAM_INT_03_READY_NOW = NO
CAM_INT_04_REQUIRES_R1 = YES / Basic-Digest already contracted
CAM_INT_04_READY_NOW = NO
CAM_INT_04_EXECUTION_STATUS = LOCAL_CHANGES_OBSERVED / pause and completion not established
RUNTIME_RESOLUTION_OWNER = CAM-INT-02
EXECUTION_IS_HUMAN_REVEAL = NO
EXECUTION_REVEAL_PERMISSION_REQUIRED = NO
FICTITIOUS_DJANGO_USER_REQUIRED = NO
NO_NEW_AUDIT_EVENT_REQUIRED = YES
NEXT_ACTIVITY = CAM-INT-02-R1 implementation with Luna/High / separate authority required
CURRENT_DOCUMENTARY_SCOPE = COMPLETE / PASS / PUBLISHED / architecture commit 5efc3fdaecbb83845e891206255c7556146bc3fb
PROJECT_STATE_UPDATE = PASS
CODE_MODIFIED = NO
ARCHITECTURE_COMMIT = 5efc3fdaecbb83845e891206255c7556146bc3fb
PUSH = YES / post-push fetch verified HEAD == origin/master, divergence 0/0, clean worktree and empty staging
```

A API contratada recebe config persistido autorizado pelo caso de uso e
retorna somente credencial ACTIVE efêmera. Human reveal e autorização manual
continuam separados; nenhuma falha permite fallback. Consumers não podem usar
decrypt privado, ciphertext, provider, reveal ou URI autenticada. CAM-INT-03
respeitou o gate, não falhou. CAM-INT-04 tem alterações locais observadas apenas
por Git status; seu worktree não foi alterado nem revisado nesta atividade.
As antigas conclusões READY_NOW de 20.14/20.15 foram supersedidas; R1 exige
implementação, integração, validação e publicação antes de liberar consumers.

### 20.17. CAM-INT-02-R1-INT-R1 — checkpoint integrado e validado localmente (2026-10-02)

O estado operacional está na seção 50 de `PROJECT_STATE.md`. O commit-fonte
imutável `80739e5fa961ecbb27d1fa42a9fbcbe02bc82add` foi integrado à `master`
por fast-forward a partir de `795dc565da40c8ff087da97c1e55bdda5e15ace4` após
verificação remota direta. Somente
`cameras/integracao/credentials.py` e
`cameras/test_camera_credential_resolution.py` foram integrados. Compilação,
diff check, Django check, migration check, 25 testes focais de R1, 21 testes
de regressão BC-AUTH/reveal e 116 testes de regressão integrada passaram.
HUMAN_REVEAL e autorização externa permanecem
separados da resolução runtime; versões inativas/revogadas, ausência,
cross-camera e erros de decrypt falham sem fallback.

```text
CAM_INT_02_R1 = IMPLEMENTED / INTEGRATED / VALIDATED_LOCAL
SOURCE_COMMIT = 80739e5fa961ecbb27d1fa42a9fbcbe02bc82add
PROJECT_STATE_UPDATE = PASS / section 50
PUBLICATION = PASS / origin/master == 57532018dc942876cdd2d383d011576717833e3a
CAM_INT_03 = RESUME_EXISTING_LANE_WITH_NEW_DEPENDENCY / revalidate separate authorization
CAM_INT_04 = DEPENDENCY_RECONCILIATION_REQUIRED / existing local changes remain unreviewed
OTHER_LANES_TOUCHED = NO
```

Não foram iniciadas as lanes CAM-INT-03/04, nem executados testes globais,
SCALE, rede real, câmeras ou produção. O push e a verificação pós-push por
`git ls-remote` passaram; `master` local e remoto coincidem em `5753201`.
CAM-INT-03/04 permanecem lanes separadas e não foram retomadas nesta atividade.

### 20.18. CAM-INT-03-INT — adapter RTSP integrado (2026-10-02)

O estado operacional corrente está em `PROJECT_STATE.md`, seção 51. O commit
`c031ea40233129408fdb9f19c44ce89c6566a972` deriva diretamente da baseline
`0b6692e86b92d9239df92104f4d08bd55a30ba51` e foi integrado localmente por
fast-forward, apenas com seis arquivos CAM-INT-03. Compilação, diff check,
Django check, migration check, 17 testes focais e 130 testes de regressão
integrada passaram. O adapter consome o resolver R1 e CAM-INT-07; nenhuma
credencial é colocada em URI, log ou erro.

```text
CAM_INT_03 = IMPLEMENTED / INTEGRATED / VALIDATED_LOCAL / PUBLISHED
RTSP_WAIT_01 = PASS / empty poll continues; one overall deadline; auth error terminal
CAM_INT_03_DEPENDENCIES = CAM-INT-01; CAM-INT-02; CAM-INT-02-R1; CAM-INT-06; CAM-INT-07
CAM_INT_03_DEPENDENCIES_SATISFIED = YES
GSTREAMER_HOMOLOGATION = PENDING
REAL_CAMERA_NETWORK_PRODUCTION = PENDING
REMOTE_VERIFICATION = PASS / git ls-remote before and after publication
PUSH = PASS / fast-forward; published HEAD 367e98e
OTHER_LANES_TOUCHED = NO
```

CAM-INT-04 mantém trabalho local anterior e requer reconciliação das
dependências. CAM-INT-05 tem a dependência de publicação satisfeita, mas
continua sujeito a autoridade separada; CAM-HEALTH, MON-WORKER e IMG-CAP seguem
bloqueados conforme seção 51.

### 20.19. CAM-INT-03-RUNTIME-02 — homologação bloqueada por defeito no adapter (2026-10-06)

O estado factual e o snapshot Git pré-checkpoint estão na seção 52 de
PROJECT_STATE.md. Esta atividade não alterou código: gst_adapter.py exige a
ligação estática decoder->appsink antes do PLAYING, embora o decoder exponha
pad dinâmico. O callback pad-added está no fluxo, mas o erro de link encerra a
criação do pipeline antes de seu registro. A evidência reportada reproduziu
link() = False com GStreamer real.

~~~~text
CAM_INT_03_RUNTIME_STATUS = BLOCKED / CODE_DEFECT / NOT_HOMOLOGATED
GSTREAMER_RUNTIME = PASS / 1.28.7
GSTREAMER_PIPELINE = FAIL / dynamic decoder pad not linked
RTSP_CONNECTION = NOT_ESTABLISHED
SAMPLES_RECEIVED = 0
FOCAL_TESTS = PASS / prior mocks do not capture this condition
SOURCE_CHANGED = NO
LOCAL_CREDENTIAL_PORTABILITY = NO / depends on ephemeral work-session key
LOCAL_DATABASE_COPIED_OR_VERSIONED = NO
HANDOFF_GATE = PENDING / registry, DAG e contrato CAM-INT-03 requerem reconciliação de status após as publicações de R1 e do adapter
IMPLEMENTATION_AUTHORIZED_IN_CHECKPOINT = NO
NEXT_REQUIRED_ACTIVITY = authorized repair of dynamic decoder->appsink linking and real-GStreamer validation
~~~~

Não registrar nem transportar chave Fernet, variáveis de ambiente, conteúdo de
credencial, URI RTSP sensível ou banco SQLite. A correção do adapter não foi
incluída nesta atividade e precisa de autorização própria. Os cabeçalhos de status do registry, DAG e contrato CAM-INT-03 ainda refletem o estado pré-R1; consultar PROJECT_STATE seção 52 e reconciliá-los em atividade documental separada.

### 20.20. CAM-INT-03-REAL-RTSP-RUNTIME-HOMOLOGATION — bloqueada no gate de policy (2026-10-07)

O reparo local removeu a ligação estática antecipada `decoder.link(sink)` de
`cameras/integracao/rtsp/gst_adapter.py`; o `pad-added` existente continua
registrado antes de `PLAYING`, para ligar a saída dinâmica de vídeo ao
`appsink`. Os testes focais do adapter passaram (17/17), e a montagem do
pipeline passou com GStreamer 1.28.7. Na homologação controlada, a policy
process-local carregou somente `10.143.36.33/32` e `rtsp:554`; outro IP e a
porta 5555 foram negados. A câmera e a configuração foram resolvidas em modo
read-only, mas a autorização positiva foi recusada como
`MISCONFIGURED_POLICY`: o perfil RTSP ativo não define `default_path`. A
execução parou antes do socket, do bootstrap Fernet/credencial e do stream.
Não houve exposição de segredo nem mutação do banco. Os testes focais passaram
novamente (17/17), `manage.py check` passou e `git diff --check` passou.
CAM-INT-03 permanece `NOT_HOMOLOGATED`; para retomar, uma atividade de
configuração autorizada precisa fornecer um path permitido sem ampliar o alvo
ou a porta. Veja `PROJECT_STATE.md`, seção 53. A divergência histórica nos
cabeçalhos de registry, DAG e contrato CAM-INT-03 descrita na seção 52 também
permanece pendente.

### 20.21. CAM-INT-03 — contrato de ambiente e composição TargetPolicy (2026-10-07)

Checkpoint histórico da proposta contratual; o resultado de implementação
mais recente e os próximos gates constam na seção 20.22.

Estado factual: `PROJECT_STATE.md`, seção 54. Contrato proposto completo:
`docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md`.
Decisões do usuário: ambiente confiável; `TargetPolicy.from_environment` como
parser produtivo; nova chave `ARGOS_CAMERA_ALLOWED_PATHS`; policy por invocação;
injeção preservada; sem banco ou Django settings como transporte adicional.

A inspeção confirmou que o parser exige mapping explícito e ainda não transporta
paths. A nova entrada proposta é
`cameras.integracao.rtsp.runtime.run_camera_connection_test_from_environment`:
lê a fonte confiável, exige portas/paths RTSP e injeta policy e portas derivadas
no serviço. Bootstrap inválido retorna `MISCONFIGURED_POLICY` antes do serviço,
credencial ou rede. Não alterar semântica de validate, config, perfil ou adapter.

A instrução atual adjudica que a câmera já resolve o path correto; a explicação
da seção 20.20 que motivava preencher default_path não rege a retomada.
Não houve nova consulta a banco/ambiente real. O gap atual é CASE C, transporte
e composição ausentes. O reparo local anterior do adapter permanece preservado.

```text
CURRENT_ACTIVITY = CONTRACT_PROPOSED / ARCHITECTURE_CONFIRMED
PROJECT_STATE_UPDATE = PASS / seção 54
ACTIVITY_HANDOFF_GATE = PASS / escopo contratual
GLOBAL_STATUS_RECONCILIATION = PENDING / divergência histórica de registry, DAG e contrato RTSP
NEXT_REQUIRED_ACTIVITY = CAM-INT-03-TARGET-POLICY-CONFIGURATION-IMPLEMENTATION
IMPLEMENTATION_AUTHORIZED = NO / DEFERRED_NO_AUTHORITY
REAL_RTSP_HOMOLOGATION = NOT_HOMOLOGATED
CODE_DB_CONFIG_CHANGED = NO / nesta atividade
DOCUMENTS_CHANGED = YES / governança exige contrato e continuidade
RTSP_SESSION_STARTED = NO
COMMIT_PUSH = NOT_AUTHORIZED / NOT_PERFORMED
```

### 20.22. CAM-INT-03 — implementação local da TargetPolicy (2026-10-07)

Estado factual e evidências: `PROJECT_STATE.md`, seção 55. Contrato atualizado:
`docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md`.

`TargetPolicy.from_environment` transporta `ARGOS_CAMERA_ALLOWED_PATHS` e
mantém `from_mapping` como construtor tipado. O composition root
`cameras.integracao.rtsp.runtime.run_camera_connection_test_from_environment`
reconstrói a policy por chamada, exige CIDR/porta/path RTSP e injeta a policy
completa e as portas derivadas no serviço. Bootstrap inválido falha fechado
antes do serviço, credencial, adapter ou socket. `service.py` segue sem acoplar
ao ambiente. Os testes focais e de regressão passaram; veja contagens e o
equivalente disponível para URI na seção 55.

```text
CURRENT_ACTIVITY = CAM-INT-03-TARGET-POLICY-CONFIGURATION-IMPLEMENTATION
IMPLEMENTATION_STATUS = IMPLEMENTED_LOCALLY / TECHNICAL_PASS
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE seção 55
TARGET_POLICY_TESTS = 24/24 PASS
RTSP_RUNTIME_TESTS = 5/5 PASS
RTSP_ADAPTER_TESTS = 17/17 PASS
RTSP_URI_TEST_MODULE = ABSENT / URI EQUIVALENT cameras.test_camera_connection_config 8/8 PASS
DJANGO_CHECK = PASS
GIT_DIFF_CHECK = PASS
REAL_RTSP_SESSION_STARTED = NO
REAL_RTSP_HOMOLOGATION = NOT_HOMOLOGATED
NEXT_REQUIRED_ACTIVITY = CAM-INT-03-REAL-RTSP-RUNTIME-HOMOLOGATION-R2
NEXT_ACTIVITY_AUTHORIZED = NO / requer autoridade própria de homologação
CAMERA_PROFILE_OR_EFFECTIVE_CONFIG_CHANGED = NO
SECRET_ACCESSED = NO
DATABASE_CHANGED = NO / banco temporário de testes criado e destruído
STAGING = EMPTY
COMMIT_PUSH = NOT_PERFORMED
```

### 20.23. CAM-INT-03 — auditoria independente com causa comprovada (2026-10-07)

Estado factual: `PROJECT_STATE.md`, seção 56. Detalhe técnico e evidência:
`docs/projeto/audits/CAM-INT-03_INDEPENDENT_END_TO_END_TECHNICAL_AUDIT.md`.

`rtph264depay` é adicionado no callback source quando o pipeline está PAUSED
com PLAYING pendente, depois da solicitação PLAYING; permanece NULL/pad inativo
porque o adapter não sincroniza seu estado. Comparação limitada TCP usando
composition root e adapter reais: inalterado A/B/C PASS e D TIMEOUT em 15,028 s;
sync-only no harness TEMP A/B/C/D PASS em 0,663 s, encoded/raw/appsink reais.
Decoder observado: d3d12h264dec. Essa prova não modifica nem homologa o código
produtivo. Os 66 testes focais passaram, com lacuna de estados/fluxo nos mocks.

```text
LAST_COMPLETED_ACTIVITY = CAM-INT-03-INDEPENDENT-END-TO-END-TECHNICAL-AUDIT
ROOT_CAUSE_CONFIDENCE = PROVEN
CAM_INT_03_RUNTIME_STATUS = NOT_HOMOLOGATED
NEXT_REQUIRED_ACTIVITY = CAM-INT-03-DYNAMIC-DEPAYLOADER-STATE-FIX-AND-REAL-RUNTIME-REVALIDATION
NEXT_ACTIVITY_AUTHORIZED = NO / DEFERRED_NO_AUTHORITY
IMPLEMENTATION_PRODUCTION_FIX_AUTHORIZED = NO
CODE_OR_TEST_CHANGED_THIS_AUDIT = NO
DATABASE_PERSISTENTLY_CHANGED = NO / rollback e hash idêntico
SECRET_IN_NEW_DIAGNOSTICS_OR_DOCUMENTATION = NO
PIPELINES_FINAL_STATE = NULL
TARGET_POLICY_OR_RBAC_CHANGED = NO
GLOBAL_CONTRACT_STATUS_RECONCILIATION = PENDING / histórica, fora do escopo
PROJECT_STATE_UPDATE = PASS
ACTIVITY_HANDOFF_GATE = PASS / findings e limites recuperáveis no relatório
COMMIT_PUSH = NOT_PERFORMED
```

### 20.24. CAM-INT-03 — correção local validada; homologação aguarda injeção process-local (2026-10-07)

Estado factual e retomada: `PROJECT_STATE.md`, seção 57.

O adapter agora sincroniza o depayloader dinâmico com o estado-alvo do pai e
checa o retorno antes de ligar o pad RTP upstream. Falha de sync é comunicada
ao loop pelo estado compartilhado existente, resulta em diagnóstico
`DYNAMIC_ELEMENT_SYNC_FAILED` e Stage C FAIL, sem liberar mídia. O teste fake
modela PAUSED/PLAYING pendente, depay inicialmente NULL, fluxo após sync e
teardown NULL. Achado separado do retorno ignorado do link decodebin→appsink
permanece aberto e não foi alterado.

Suítes relevantes 68/68 passaram; `manage.py check` e `git diff --check`
passaram. A homologação real não começou: o ator e a configuração existem
localmente, mas o usuário/senha temporários não estão disponíveis ao processo.
O usuário cancelou a alternativa de restaurar material histórico e autorizou
chave Fernet nova efêmera + `replace_camera_credential` dentro de transação
externa com rollback. Essa rota ainda aguarda injeção local dos valores; não
houve runtime real, mutação de credencial nem escrita persistente no banco. Não
inferir A/B/C/D, codec, autorização do alvo ou limpeza de pipeline não criada.

```text
CURRENT_ACTIVITY = CAM-INT-03-DYNAMIC-DEPAYLOADER-STATE-FIX-AND-REAL-RUNTIME-REVALIDATION
LOCAL_FIX = IMPLEMENTED_AND_VALIDATED
ROOT_CAUSE = DYNAMIC_ELEMENT_LIFECYCLE_DEFECT / PROVEN
ADAPTER_TESTS = 19/19 PASS
REGRESSION_TESTS = 49/49 PASS
TOTAL_RELEVANT_TESTS = 68/68 PASS
REAL_RUNTIME = NOT_EXECUTED / TEMPORARY_LAB_CREDENTIAL_NOT_AVAILABLE_TO_PROCESS
CAM_INT_03_RUNTIME_STATUS = NOT_HOMOLOGATED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 57
ACTIVITY_COMPLETE = NO
NEXT_REQUIRED_ACTION = Inject temporary lab username/password only into the local process; generate a fresh in-memory Fernet key; replace credential inside outer transaction; run canonical 5-second validation; roll back
STAGING = EMPTY
COMMIT_PUSH = NOT_PERFORMED
```

Não repetir investigação cega de transporte/decoder nem aumentar timeout para

### 20.25. CAM-INT-03-DATABASE-PERSISTENCE-RECONCILIATION — homologação reconciliada (2026-10-07)

Estado factual: `PROJECT_STATE.md`, seção 58. O harness TEMP compara snapshots
ORM limitados à credencial da câmera 1, suas versões por contagem e eventos de
criação/substituição por contagem. Os dois labels de persistência usam a mesma
comparação; `CREDENTIAL_PERSISTENCE=ROLLED_BACK` junto de
`DATABASE_PERSISTENTLY_CHANGED=YES` é impossível nessa versão. O harness não
calcula SHA-256 do banco; portanto mudança física do arquivo não foi provada.

Inspeção SQLite somente leitura confirmou journal mode `delete`, sem sidecars,
integridade `ok`, uma referência de credencial ativa e duas versões, com a
segunda ativa. O rollback restaurou o snapshot da credencial. Não foram
identificados callbacks `on_commit`, escrita de diagnóstico ou outros modelos
persistidos pela composição RTSP. A classificação é defeito no sinal/rotulagem,
com estado lógico reconciliado; CAM-INT-03 passa a `HOMOLOGATED` pela evidência
real já fornecida: A/B/C/D PASS, H264 e 2,484 s. Warning de giolibproxy segue
não bloqueante/não causal; o finding decodebin→appsink segue OPEN. Nenhum RTSP
foi iniciado nesta atividade.

```text
CURRENT_ACTIVITY = CAM-INT-03-DATABASE-PERSISTENCE-RECONCILIATION
DATABASE_PERSISTENCE_VERDICT = LOGICALLY_UNCHANGED / HARNESS_SIGNAL_DEFECT
CAM_INT_03_RUNTIME_STATUS = HOMOLOGATED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 58
ACTIVITY_COMPLETE = YES
NEXT_REQUIRED_ACTIVITY = CAM-INT-03-FINAL-REVIEW-AND-CHECKPOINT
STAGING = EMPTY
COMMIT_PUSH = NOT_PERFORMED
```

### 20.26. CAM-INT-03-FINAL-REVIEW-AND-CHECKPOINT — commit local (2026-10-07)

Este registro preserva o estado observado antes da publicação; foi supersedido
pelo fechamento posterior na seção 20.27 e não deve ser usado como estado atual.

O estado final desta revisão está em `PROJECT_STATE.md`, seção 59. A causa
`DYNAMIC_ELEMENT_LIFECYCLE_DEFECT` foi resolvida pelo sync checado do depayloader
dinâmico; homologação real A/B/C/D PASS, H264, 2,484 s, timeout de produção de
5 s. A reconciliação SQLite permanece logicamente inalterada, com defeito de
rotulagem do harness. A revisão não reabre os achados secundários.

```text
CURRENT_ACTIVITY = CAM-INT-03-FINAL-REVIEW-AND-CHECKPOINT
STATUS = LOCAL_CHECKPOINT_PASS / REMOTE_PUBLICATION_PENDING
CAM_INT_03_RUNTIME_STATUS = HOMOLOGATED
CAM_INT_03_IMPLEMENTATION = COMMITTED_LOCAL / REMOTE_PUBLICATION_PENDING
ROOT_CAUSE_STATUS = RESOLVED
TARGET_POLICY_BOOTSTRAP_STATUS = RESOLVED
REAL_RUNTIME = PASS / A-B-C-D; H264; 2.484 s; production timeout 5.0 s
DATABASE_PERSISTENCE_VERDICT = LOGICALLY_UNCHANGED / HARNESS_SIGNAL_DEFECT
SECONDARY_PAD_LINK_FINDING = OPEN_NON_BLOCKING
GIOLIBPROXY = NON_BLOCKING / NON_CAUSAL_FOR_INCIDENT
DOCUMENTATION_HISTORICAL_CONFLICT = KNOWN_NON_BLOCKING / prior activity snapshots and contract headers preserved
NEXT_REQUIRED_ACTIVITY = RESUME ARGOS BACKEND FROM NEXT OPEN ACTIVITY AFTER CAM-INT-03
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 59
PUSH = BLOCKED_BY_AUTO_REVIEW / NOT_PERFORMED; explicit user confirmation required
LOCAL_HEAD_EQUALS_UPSTREAM = NO / local checkpoint commit is one commit ahead
REMOTE_CONTINUATION_READY = NO / until normal push is approved and verified
```

### 20.27. CAM-INT-03-POST-PUBLICATION-CONTINUITY-RECONCILIATION — publicação confirmada (2026-10-07)

O commit de implementação `4a0eada4d06b9c61a12c78149257005297ce6a65`
(`fix(camera): homologate CAM-INT-03 RTSP runtime`) está publicado em
`origin/master`. O precheck desta reconciliação confirmou branch `master`,
HEAD local igual ao upstream, worktree limpa e staging vazio. O estado corrente
é o fechamento da seção 60 de `PROJECT_STATE.md`.

```text
CAM_INT_03_RUNTIME_STATUS = HOMOLOGATED
CAM_INT_03_IMPLEMENTATION = PUBLISHED
IMPLEMENTATION_COMMIT = 4a0eada4d06b9c61a12c78149257005297ce6a65
PUSH = PASS
LOCAL_HEAD_EQUALS_UPSTREAM = YES
DIVERGENCE = 0/0
REMOTE_CONTINUATION_READY = YES
SECONDARY_DECODEBIN_APPSINK_LINK_FINDING = OPEN_NON_BLOCKING
GIOLIBPROXY = NON_CAUSAL_FOR_CAM_INT_03
LOCAL_AUTH_PROVISIONING_FINDING = OPEN_NON_BLOCKING
NEXT_RECOMMENDED_ACTIVITY = RESUME ARGOS BACKEND FROM NEXT OPEN ACTIVITY AFTER CAM-INT-03
```

Não repetir RTSP nesta atividade. A revisão automática rejeitou o push para
`origin/master` por ser uma publicação de alto impacto no branch padrão e exigir
confirmação verificável do usuário. Não houve tentativa por outro caminho. O
relatório da auditoria mantém sua conclusão
histórica no momento da auditoria; esta seção registra apenas o follow-up factual
posterior. A divergência histórica de cabeçalhos do registry, DAG e contrato
RTSP permanece conhecida e não bloqueia a continuidade desta lane.


### 20.28. ARGOS-UI-P5-PRODUCTION-INTEGRATION — Camera Detail integrado localmente (2026-10-07)

O estado desta integração está registrado em `PROJECT_STATE.md`, seção 61. O
commit P5 `c91bc6d4658faa408a9f565b9d1c3d6279571cb4` foi integrado por
cherry-pick no `master` sincronizado em `0235c8d`, produzindo
`662e80e16df53ae80a87b0c9c28f6700f6dd2e9b`. A adjudicação humana definiu a P5
como autoridade visual e estrutural para Camera Detail; o master continua
autoridade para contratos funcionais. A comparação não encontrou binding
funcional pós-P5 ausente da implementação aprovada.

```text
UI_P5_STATUS = CLOSED / PRODUCTION_INTEGRATED_LOCALLY
UI_SOURCE_COMMIT = c91bc6d4658faa408a9f565b9d1c3d6279571cb4
MASTER_UI_COMMIT = 662e80e16df53ae80a87b0c9c28f6700f6dd2e9b
CONFLICT_RESOLUTION = P5_VISUAL_AUTHORITY_PRESERVED
UI_FOCUSED_TESTS = 17/17 PASS
INTEGRATED_REGRESSION = 101/101 PASS
DJANGO_CHECK = PASS
GIT_DIFF_CHECK = PASS
HUMAN_VISUAL_APPROVAL = PASS
CAM_INT_03_CHANGED = NO
CAM_INT_04_CHANGED = NO
PUSH = AUTHORIZED / PENDING
REMOTE_CONTINUATION_READY = NO / pending post-push verification
NEXT_ACTION = publish master normally, verify remote equality, then record the publication checkpoint
```

O worktree P5 permaneceu intacto e sujo como solicitado. O ZIP local de
continuidade continua não rastreado e fora do commit. Não reabrir CAM-INT-03:
o checkpoint de runtime permanece conforme `PROJECT_STATE.md`, seção 60.


### 20.29. ARGOS-UI-P5-PRODUCTION-INTEGRATION — publicação confirmada (2026-10-07)

Consulte `PROJECT_STATE.md`, seção 62, para o fechamento factual. O commit de
integração `662e80e16df53ae80a87b0c9c28f6700f6dd2e9b` e o checkpoint documental
pré-publicação foram publicados normalmente em `origin/master`; o fetch posterior
confirmou igualdade local/remota e divergência zero.

```text
UI_P5_STATUS = PUBLISHED_TO_MASTER
CONFLICT_RESOLUTION_STATUS = PASS
P5_VISUAL_AUTHORITY_PRESERVED = YES
POST_P5_FUNCTIONAL_BINDINGS_FOUND = NO
UI_FOCUSED_TESTS = 17/17 PASS
INTEGRATED_REGRESSION = 101/101 PASS
DJANGO_CHECK = PASS
PROJECT_STATE_UPDATE = PASS
ACTIVITY_COMPLETE = YES
REMOTE_CONTINUATION_READY = YES
NEXT_ACTION = resume ARGOS backend from the next open activity after CAM-INT-03
```

O worktree da UI permaneceu intocado; o ZIP local de continuidade segue não
rastreado e preservado. Publicação no repositório não implica deploy operacional.


### 20.30. CAM-INT-05-IMPLEMENTATION — registro inicial (supersedido)

Este registro inicial foi supersedido pela seção 20.31 e pela seção 64 de
`PROJECT_STATE.md`. Os fatos e validações desta fotografia histórica não devem
ser usados como estado atual.

```text
CAM_INT_05_IMPLEMENTATION = LOCAL / PARTIAL / ASYNC_TEST_RUNTIME_BLOCKED / HISTORICAL
CAMERA_HEALTH_SNAPSHOT = MODEL_AND_MIGRATION_CREATED / TEST_DATABASE_APPLIED
AUTOMATIC_MANUAL_ISOLATION = PASS / CAM-INT-05 TESTS 10/10
MON_SNAPSHOT_COMPLETION_ATOMICITY = PASS / ROLLBACK AND FENCING TESTED
PYTHON_SYNTAX = PASS
GIT_DIFF_CHECK = PASS
DJANGO_CHECK = PASS
MIGRATION_CHECK = PASS / NO MODEL DRIFT
TESTS = CAM-INT-05 10/10; RTSP AND POLICY 74/74; SYNCHRONOUS MON 94/94
ASYNC_TESTS = BLOCKED / WINDOWS HOST EVENT LOOP HANG
SECURITY_CHECK = FOCAL BANDIT PASS / BASELINE HAS TWO LOW FINDINGS IN EXISTING CODE
REAL_CAMERA_ACCESS = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md SECTION 63
CAM_HEALTH_IMPLEMENTED = NO
MON_WORKER_STATUS = BLOCKED_BY_BC_02
MON_WORKER_UNBLOCKED = NO
NEXT_ACTIVITY = CAM-INT-05-TECHNICAL-CLOSURE
```

### 20.31. CAM-INT-05-TECHNICAL-CLOSURE — fechamento técnico local (2026-10-10)

O estado factual e as evidências estão na seção 64 de `PROJECT_STATE.md`. A
atividade fechou localmente contra o contrato CAM-INT-05. A branch continua
`codex/cam-int-05-implementation`, com `HEAD` na baseline
`5bd22b06891a9cfa3886aa2dd2fbe0bf97e125c9`; nenhuma publicação ocorreu.

```text
CAM_INT_05 = COMPLETE / CONTRACT_CONFORMANCE_PASS
CAM_INT_05_TESTS = 10/10 PASS
MON_EXTERNAL_REGRESSION = 63/63 PASS / MIXED SYNCHRONOUS AND ASYNCHRONOUS
ASYNCIO_EXTERNAL_SMOKE = PASS
PREVIOUS_RTSP_CREDENTIAL_POLICY_TESTS = 74/74 PASS
PREVIOUS_MON_SYNC_TESTS = 94/94 PASS / OVERLAPPING EVIDENCE, NOT ADDITIVE
DJANGO_CHECK = PASS
MIGRATION_0018_TEST_DATABASE = PASS
MIGRATION_SCHEMA_CHECK = PASS
BANDIT_FOCUSED = PASS
GIT_DIFF_CHECK = PASS
PYTHON = 3.12.14 / COMPATIBLE WITH DJANGO 5.2.16
MIGRATION_COLLISION = CAM-INT-04 ALSO HAS INDEPENDENT 0018 / INTEGRATION RISK
CAM_HEALTH_IMPLEMENTED = NO
MON_WORKER_STARTED = NO
REAL_CAMERA_ACCESS = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
NEXT_ACTIVITY = CAM-INT-05-GIT-CHECKPOINT
```

Os 63 testes da regressão MON incluem casos síncronos e assíncronos; não os
classificar como exclusivamente assíncronos. O teste de rollback registrou
`MONITORING_OPERATIONAL_FAILURE` como esperado e terminou em PASS. A branch
CAM-INT-04 contém `0018_cameracapturejob.py`, também dependente de 0017; a
colisão numérica deve ser resolvida no checkpoint de integração. Nenhuma
migration foi renumerada nesta atividade.

### 20.32. CAM-HEALTH-IMPLEMENTATION — retomada (2026-10-10)

```text
CAM_HEALTH_IMPLEMENTATION = COMPLETE
CAM_HEALTH_LOCAL_VALIDATION = PASS / focal Django suites 41/41; manage.py check; migration check; Bandit; diff check
CAM_HEALTH_PUBLICATION = PENDING_UNTIL_REMOTE_CONFIRMATION
CAM_HEALTH_MASTER_INTEGRATION = PENDING
CAM_INT_05 = PUBLISHED
MON_OBS = PUBLISHED
FRESHNESS_POLICY = shared MonitoringConfig.stale_after_seconds; UTC timestamp; age >= threshold is stale; absent/invalid/future/stale => technical UNKNOWN
AUTHORIZATION_SUMMARY = cameras.view_camera
AUTHORIZATION_DETAILS = cameras.view_camera_diagnostic + require_camera_permission(camera_id)
MIGRATION_REQUIREMENT = NONE / uses CAM-INT-05 CameraHealthSnapshot
BC_02_DEPENDENCIES = CAM-INT-05 source commit is ancestor; no runtime probes or real-camera validation
KNOWN_LIMITATIONS = full MON 63-test suite not rerun; no object/tenant authorization backend; migration 0018 collision remains open
GIT_CHECKPOINT = AUTHORIZED / feature branch only
FEATURE_BRANCH_PUSH = PENDING_UNTIL_REMOTE_CONFIRMATION
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 65
MASTER_UNCHANGED = YES
MON_WORKER_STATUS = BLOCKED_BY_BC_02
MIGRATION_INTEGRATION_RISK = OPEN
NEXT_ACTIVITY = BC-02-INTEGRATION-READINESS-REVIEW
```

O estado completo e os caminhos alterados constam em `PROJECT_STATE.md`,
seção 65. CAM-HEALTH reaproveita o limiar compartilhado do MON e mantém
separados o resumo da câmera e os estágios A-D protegidos. O teste usa relógio
controlável e valores de limiar apenas nos fixtures. A colisão de migrations
0018 CAM-INT-04/CAM-INT-05 permanece para reconciliação serializada antes da
integração; não foi criada nova migration nem alterado o master.

### 20.33. BC-02-INTEGRATION-EXECUTION — integração local validada (2026-10-10)

```text
MON_OBS_PUBLICATION = PASS / 6fc4f708778210c617cf4b5bca6cca441bdb0705
CAM_INT_05_PUBLICATION = PASS / 68d593d88b84b218210dac0fe8ddf16c08fd413a
CAM_HEALTH_PUBLICATION = PASS / 6ef2f7035dae858282eeae76ff5fefff160443bd
BC_02_LOCAL_INTEGRATION = VALIDATED / combined checks pass; local merge pending
BC_02_GIT_PUBLICATION = PENDING
BC_02_MASTER_INTEGRATION = PENDING
INITIAL_MASTER_SHA = 5bd22b06891a9cfa3886aa2dd2fbe0bf97e125c9
INTEGRATION_BRANCH = codex/bc-02-integration
INTEGRATION_HEAD = 6ef2f7035dae858282eeae76ff5fefff160443bd
MERGE_HEAD = 6fc4f708778210c617cf4b5bca6cca441bdb0705
INTEGRATION_TESTS = 275/275 PASS / Django and SQLite in-memory
MIGRATION_GRAPH = PASS / camera leaf 0018; fresh database and 0017→0018 upgrade PASS
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 69
MON_WORKER = NOT_IMPLEMENTED
INDEPENDENT_WORKER_HEARTBEAT = REQUIRED BY RUNTIME CONTRACT / scheduler-cycle heartbeat does not satisfy it
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MASTER_UNCHANGED = YES
NEXT_ACTIVITY = BC-02-INTEGRATION-GIT-CHECKPOINT
```

Os registros MON-OBS anteriores foram preservados no `PROJECT_STATE.md` como
seções 66–68, sem remover os registros CAM-INT-05 e CAM-HEALTH. O conflito era
de numeração documental; não houve conflito de implementação no scheduler. O
merge está resolvido e pronto para revisão/checkpoint, mantendo o merge commit




### 20.34 MON-RUNTIME-V1-CONTRACT-BASELINE-RECONCILIATION (2026-10-10)

A consolidação V1 foi materializada sobre BC-02 sem alterar a baseline publicada, o DAG ou os registros históricos. A decisão aceita é a seção `MON-RUNTIME-CONTRACT-DECISION-CONSOLIDATION — V1` na autoridade-fonte SHA `22c9e3a59fe2be44dd17c2fd2cc90fc63f6059c4`, junto à matriz V1 de MON-OBS. Propostas/estados `OPEN` anteriores nesta linhagem são históricos e supersedidos pela adjudicação final; não há decisão material pendente para o contrato local.

```text
BASELINE = ccc0267527da7cac0a139a68c11982100f627147 / BC-02 PRESERVED
WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos_mon_runtime_v1
BRANCH = codex/mon-runtime-v1-implementation
HEAD = ccc0267527da7cac0a139a68c11982100f627147
MON_WORKER_IMPLEMENTATION = NOT_STARTED
HEARTBEAT_OWNER = WORKER_RUNTIME
HEARTBEAT_CADENCE = INDEPENDENT_OF_SCHEDULER_CYCLES
IMPLEMENTATION_READINESS = PASS / contract baseline reconciliation only
OPERATIONAL_PRODUCTION_READINESS = NOT_ESTABLISHED
PROJECT_STATE_UPDATE = PASS
```

Lease V1 não exige renovação explícita. Claim/release são por tentativa com owner/epoch/config_generation e usam interfaces/repository existentes. Expiry permite takeover com epoch novo, mas não invalida sozinha a completion do owner ainda atual nem comprova término físico do produtor. Fencing não encerra I/O. Antes de release explícito, provar término de adapter/task/ORM; deadlines/cancellation não bastam. Completion permanece atômica no repository. A janela terminal é `W=C+Q`, tentativas totais ficam em `<=2(C+Q)`, callback evicted é rejeitado antes de qualquer write e nenhuma exclusão persistente/ledger é criada.

A extensão futura de `MonitoringConfig` contém somente `db_operation_deadline_seconds`, `recovery_max_attempts` e `recovery_max_elapsed_seconds`, conforme ranges e defaults V1 de MON-OBS. O heartbeat do worker é independente dos ciclos do scheduler, inclusive durante drain/recovery enquanto vivo; cancelamento e falhas operacionais não produzem `OFFLINE`. DC-01..07 são aceites futuros do worker, ainda não validados nesta reconciliação.

PostgreSQL, múltiplos workers, rede/câmera reais, capacidade e deploy permanecem gates externos. Não declarar worker implementado nem operação aprovada com base neste checkpoint.

### 20.35 MON-RUNTIME-V1-IMPLEMENTATION (2026-10-10)

Implementação local concluída no branch `codex/mon-runtime-v1-implementation`, sem migration nem alteração do contrato V1. O entrypoint é `python manage.py run_monitoring_worker`; runtime e wiring vivem em `cameras/monitoramento/runtime.py` e `cameras/management/commands/run_monitoring_worker.py`. A composição reutiliza scheduler, repository, política de confirmação e diagnóstico existentes; heartbeat independente, paginação limitada, deadlines/recovery bounded, fail-closed e drain preservando producers/leases seguem os contratos.

```text
BASELINE_HEAD = ccc0267527da7cac0a139a68c11982100f627147
CURRENT_HEAD = ccc0267527da7cac0a139a68c11982100f627147
STAGING = EMPTY
STATUS = COMPLETE / LOCAL IMPLEMENTATION AND VALIDATION
ACTIVITY_COMPLETION_PERCENT = 100%
TESTS = 921 PASS / temporary SQLite / 1299.244 seconds
DJANGO_CHECK = PASS
MIGRATION_CHECK = PASS / no changes
BANDIT_FOCAL = PASS
SECRET_SCAN_FOCAL = PASS / zero findings
DIFF_CHECK = PASS
REAL_CAMERA_OR_OPERATIONAL_DB = NOT_USED
MON_WORKER_BRANCH_PUBLICATION = PENDING_UNTIL_REMOTE_CONFIRMATION
MON_WORKER_MASTER_INTEGRATION = PENDING
OPERATIONAL_PRODUCTION_READINESS = NOT_ESTABLISHED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 71 final snapshot
ACTIVITY_COMPLETE = YES / local implementation and validation scope
```

O fixture de integração recria de forma idempotente o perfil canônico quando uma `TransactionTestCase` já fez flush da seed da migration. Os dois ajustes aos testes preservam o contrato: falha transacional mantém a tentativa ativa/degradada; o harness MON-08C rastreia candidatos por camera_id para não depender da ordem de admissão. Os 2.300 registros da prova de escala são dados de teste SQLite. Config adiciona somente `db_operation_deadline_seconds=5.0`, `recovery_max_attempts=5` e `recovery_max_elapsed_seconds=900.0`. Nove documentos WIP preexistentes mantêm conteúdo; somente checkpoints de continuidade receberam adições. Não houve commit/push. A suíte completa passou com 921 testes em 1.299,244 segundos; PostgreSQL, multi-worker, ambiente real e operação/deploy continuam pendentes.


### 20.36 ARGOS-DJANGO-PATCH-VALIDATION (2026-10-10)

```text
ROOT = C:\Users\walac\desenvolvimento\projeto_argos_mon_runtime_v1
BRANCH = codex/mon-runtime-v1-implementation
HEAD = 89fac4a19f831fdcf7af496c64c617f3d6e37d62
DJANGO = 5.2.18 / Python 3.14.7 / repository .venv
CI_TEST_HOSTS = PASS / testserver, localhost, 127.0.0.1, ::1, [::1]
PRODUCTION_HOSTS = UNCHANGED / check --deploy PASS
FOCUSED_TESTS = 160 PASS
FULL_REGRESSION = 921 PASS / 1275.335 seconds
DJANGO_CHECK = PASS
MIGRATION_CHECK = PASS
PIP_CHECK = PASS
PIP_AUDIT = 7 records / 4 distinct cryptography advisories / FINDINGS
GENERAL_SECURITY_AUDIT = NOT_PASS
WIP_PRESERVED = cameras/monitoramento/scheduler.py; requirements.txt
FILES_CHANGED = .github/workflows/ci.yml; PROJECT_STATE.md; AGENT_CONTINUITY.md
STAGING = EMPTY
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
READY_FOR_GIT_CHECKPOINT = YES_WITH_FINDINGS_RECORDED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 72
ACTIVITY_COMPLETE = YES / local validation scope
NEXT_ACTIVITY = review and authorize local Git checkpoint; cryptography remediation is separate
```

A atividade paralela foi reconciliada: a alteração dos hosts do CI convergiu para uma única linha e não produziu conflito de conteúdo. Os testes usaram apenas SQLite temporário; nenhum acesso a câmera ou banco operacional ocorreu. `cryptography` continua como dependência direta em `requirements.txt` e no código de credenciais. Os sete registros do audit incluem quatro advisories distintos e continuam sem resolução; não declarar a auditoria geral de segurança como PASS.


### 20.37 ARGOS-CRYPTOGRAPHY-SECURITY-REMEDIATION (2026-10-10)

```text
ROOT = C:\Users\walac\desenvolvimento\projeto_argos_mon_runtime_v1
BRANCH = codex/mon-runtime-v1-implementation
INITIAL_HEAD = 9d5ac5debec3710212f5331a41201c43cb63ced9
FINAL_HEAD = 9d5ac5debec3710212f5331a41201c43cb63ced9
INITIAL_WORKTREE = CLEAN
CRYPTOGRAPHY = 46.0.7 → 50.0.2
PIP_AUDIT = 7 records / 4 distinct advisories → 0 known findings
REMEDIATED = CVE-2026-69248; CVE-2026-69247; CVE-2026-69249; CVE-2026-34180
FOCUSED_TESTS = 68 PASS
LEGACY_FERNET_DECRYPTION = PASS / synthetic token from 46.0.7 read by 50.0.2
FULL_REGRESSION = 921 PASS / 1277.672 seconds
PIP_CHECK = PASS
DJANGO_CHECK = PASS
MIGRATION_CHECK = PASS / no changes
DIFF_CHECK = PASS
SECRET_SCAN = PASS / zero findings
CI_REMOTE = NOT_VERIFIED
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MASTER_UNCHANGED = YES
READY_FOR_GIT_CHECKPOINT = YES
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 73
NEXT_ACTIVITY = ARGOS-CRYPTOGRAPHY-GIT-CHECKPOINT
```

A única alteração de dependência foi o pin direto em `requirements.txt`; Django permaneceu em 5.2.18. A compatibilidade foi exercitada por round-trip, token legado sintético, chave/ciphertext inválido, sanitização de erros e resolução em memória no fluxo de diagnóstico RTSP. Testes CAM-INT-05 e MON Runtime relevantes passaram e a regressão integral de 921 testes passou em SQLite temporário.

O pacote publicado no PyPI oferece wheel Windows x64 `cp311-abi3` compatível com CPython 3.14.7. Os quatro advisories conhecidos não aparecem após a atualização; `pip-audit` não encontrou outros findings conhecidos. Nenhuma migration, fonte do MON Runtime Worker, credencial operacional, banco operacional ou câmera real foi alterada/acessada. A validação é local; CI remoto permanece não verificado. O worktree contém somente o pin e os três documentos de continuidade; staging permanece vazio, sem commit/push. Próxima atividade: revisar e autorizar checkpoint Git local.

### 20.38 MON-RUNTIME-V1-H1-PREFLIGHT-VALIDATION (2026-10-10)

H1 permanece parcial. Baseline Git confirmado em `codex/mon-runtime-v1-implementation`, SHA `4ff2a9260a438a61f3a23e753dfdc3d5c166424a`, worktree inicial limpo. Trinta testes síncronos focais concluíram com PASS: scheduler/bounds, retenção/fencing/shutdown, observabilidade/sanitização e validação da configuração tipada.

```text
ACTIVITY = MON-RUNTIME-V1-H1-PREFLIGHT-VALIDATION
STATUS = PARTIAL / H1 ACCEPTANCE NOT MET
ASYNC_RUNTIME_AND_INTEGRATION = NOT_VALIDATED / test processes did not complete
PREFLIGHT_MATRIX = NOT_VALIDATED
REAL_CAMERA_OR_OPERATIONAL_DATABASE = NOT_ACCESSED
OPERATIONAL_DB_FILE = NOT_OPENED
NATIVE_GSTREAMER = NOT_INSTALLED_OR_INVOKED
TESTS = 30 PASS / completed synchronous focused tests
H1_PASS = NO
H2_POSTGRESQL = PENDING
H3_REAL_CAMERAS = PENDING
PRODUCTION_READINESS = NOT_ESTABLISHED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 74
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
NEXT_RECOMMENDED_ACTIVITY = MON-RUNTIME-V1-H1-RESUME-ISOLATED-TEST-RUNNER
```

O runner de teste anunciou `file:memorydb_default` em uma tentativa, mas os processos de integração não chegaram a um resultado final. `IsolatedAsyncioTestCase` e execução direta de loop asyncio não retornaram no host; causa não determinada. Não inferir defeito no runtime nem H1_PASS. O comando real não foi iniciado. `db.sqlite3` operacional, câmeras, credenciais reais, rede externa e GStreamer não foram acessados. A suíte histórica de 921 testes da seção 20.35 permanece evidência da implementação local, não fechamento desta homologação H1.

### 20.39 MON-RUNTIME-V1-H1-EXECUTION-RECOVERY (2026-10-10)

O precheck de retomada confirmou branch `codex/mon-runtime-v1-implementation` e HEAD `4ff2a9260a438a61f3a23e753dfdc3d5c166424a`. O WIP documental herdado foi preservado; staging permaneceu vazio. Diagnóstico isolado: processo Python simples PASS, asyncio trivial excedeu 12 segundos e foi encerrado com exit 124; importação de Django/settings PASS sem abrir banco, com Python 3.14.7, Django 5.2.18 e settings `config.settings`. A venv referencia Python-base sob `%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe`, e o executável emitiu aviso de localização não encontrada. Isso é evidência de limitação possível do host, ainda sem confirmação comparativa externa.

```text
ACTIVITY = MON-RUNTIME-V1-H1-EXECUTION-RECOVERY
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
PYTHON = 3.14.7 / .venv
DJANGO = 5.2.18
DJANGO_SETTINGS_MODULE = config.settings
DEFAULT_DATABASE = <repo>\db.sqlite3 / not opened
PYTHON_SMOKE = PASS
ASYNCIO_SMOKE = TIMEOUT / 12s / EXIT 124
TESTS_STARTED = NO
RUNNER_ROOT_CAUSE = UNDETERMINED
CLASSIFICATION = UNDETERMINED
ISOLATED_TEST_SETTINGS = PREPARED FOR EXTERNAL POWERSHELL / SQLite under %TEMP%
H1_STATUS = PARTIAL / pending external comparison and terminal test results
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 75
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
```

Não executar testes com settings padrão, pois apontam para `<repo>\db.sqlite3`. Não alterar event-loop policy nem repetir smokes indefinidamente. O próximo passo exige executar, no PowerShell normal, a sequência fornecida ao usuário: settings temporários explícitos sob `%TEMP%`; validar paths de banco antes de cada runner; somente avançar do smoke asyncio se ele passar; executar primeiro `WorkerRuntimeTests`, depois o smoke Django transacional e por fim `WorkerRuntimeIntegrationTests`, sem paralelismo e com timeout/captura por comando. Nenhum resultado externo foi recebido; portanto testes e gates H1 permanecem não demonstrados.

### 20.40 MON-RUNTIME-V1-H1-EXTERNAL-POWERSHELL-RETRY (2026-10-10)

O transcript do PowerShell externo interrompeu o precheck antes de qualquer smoke: dois processos Python foram observados (PIDs 17352 e 39204, ambos iniciados às 22:59:59), sem linha de comando ou processo pai disponíveis no transcript. Foram preservados; ownership permanece desconhecido. O helper então não conseguiu usar `ProcessStartInfo.ArgumentList`, que estava nulo/incompatível com o PowerShell executado. A execução foi colada interativamente, e comandos posteriores rodaram apesar dos erros anteriores. A linha final de sucesso é espúria e deve ser ignorada.

```text
ACTIVITY = MON-RUNTIME-V1-H1-EXECUTION-RECOVERY
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
EXTERNAL_PYTHON_PROCESSES = 2 / owner UNKNOWN / preserved
PYTHON_SMOKE = NOT_RUN
ASYNCIO_SMOKE = NOT_RUN
ISOLATION = NOT_VALIDATED
TESTS_STARTED = NO / TEST_COUNT 0
ATTEMPT_FAILURE = TEST_RUNNER_OR_CONFIGURATION_ISSUE / PowerShell compatibility and interactive execution
UNDERLYING_ASYNC_RUNNER_CAUSE = UNDETERMINED
WORKER_FUNCTIONAL_DEFECT = NOT_ESTABLISHED
STATUS = PARTIAL
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 76
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
```

Próximo passo: solicitar apenas a inspeção read-only dos PIDs 17352 e 39204 (`CommandLine`, `ExecutablePath`, `ParentProcessId`) e preservar ambos. Após esclarecer que não são execuções alheias nem runners ativos, entregar/usar um arquivo `.ps1` compatível com Windows PowerShell 5.1, com parada efetiva após erro. Não interpretar a mensagem final do transcript como resultado terminal.

### 20.41 MON-RUNTIME-V1-H1-RESIDUAL-RUNNER-IDENTIFIED (2026-10-10)

O transcript CIM do usuário identificou PID 39204 como o runner Django anterior para oito suites focais H1/CAM e PID 17352 como processo Python filho (pai 39204). Isso comprova que não são processos alheios e que um runner da execução anterior ainda estava ativo. Os PIDs foram preservados porque o ambiente Codex não tem acesso à tabela CIM externa. Encerramento condicional seguro deve revalidar identidade completa e então terminar somente os dois PIDs. A etapa travada dentro do runner, o output e o banco efetivo não foram capturados.

```text
ACTIVITY = MON-RUNTIME-V1-H1-EXECUTION-RECOVERY
RESIDUAL_RUNNER = IDENTIFIED / prior H1 focused Django suite
PID_PARENT_RUNNER = 39204
PID_CHILD_PYTHON = 17352
PROCESS_RELATION = CONFIRMED / child parent PID = 39204
PROCESS_TERMINATED = NO / external PowerShell action required
ROOT_CAUSE_CLASSIFICATION = TEST_RUNNER_OR_CONFIGURATION_ISSUE / prior runner remains active and blocks isolated retry
HANG_STAGE = UNDETERMINED
TESTS_IN_RETRY = 0
ISOLATION = NOT_VALIDATED
STATUS = PARTIAL
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 77
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
```

A nova tentativa não pode iniciar enquanto esses processos existirem. O script condicional deve confirmar caminho executável, comando esperado e vínculo pai/filho imediatamente antes de terminá-los, e conferir sua ausência imediatamente depois. Em seguida, usar um `.ps1` PowerShell 5.1 compatível, sem paste interativo e sem resultado final incondicional.

### 20.42 MON-RUNTIME-V1-H1-POWERSHELL51-HARNESS-READY (2026-10-10)

O usuário confirmou ausência dos PIDs residuais 17352 e 39204 após revalidação condicional. Foi criado `run_mon_runtime_v1_h1_isolated_tests.ps1`, um harness PowerShell 5.1 compatível, e sua sintaxe foi analisada com sucesso no host atual. O script será executado como arquivo completo, verifica branch/SHA e runners, usa módulo settings temporário com ambos os nomes SQLite dentro de `%TEMP%`, valida caminhos antes de cada runner e interrompe na primeira falha. Cada comando tem timeout e captura de stdout/stderr/código/contagem/etapa; logs são redigidos antes da gravação. Nenhum processo de teste foi iniciado ao preparar o harness.

```text
ACTIVITY = MON-RUNTIME-V1-H1-EXECUTION-RECOVERY
RESIDUAL_PIDS = REPORTED_ABSENT
HARNESS = run_mon_runtime_v1_h1_isolated_tests.ps1 / syntax PASS
HARNESS_RUNTIME = NOT_RUN
ASYNCIO_SMOKE = NOT_RUN
H1_TESTS = NOT_RUN
DB_ISOLATION = PREPARED / needs terminal external proof
STATUS = PARTIAL
RUNNER_ROOT_CAUSE = UNDETERMINED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 78
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
```

O próximo passo é o usuário executar `& .\run_mon_runtime_v1_h1_isolated_tests.ps1` em Windows PowerShell normal e enviar o relatório. Não declarar H1_PASS antes dos resultados terminais. O comando do worker não faz parte do script.

### 20.43 MON-RUNTIME-V1-H1-TEST-DB-TEARDOWN-RECOVERY (2026-10-11)

O transcript da execução isolada confirmou Python e asyncio smoke, isolamento de settings, sete testes assíncronos do runtime, um teste de configuração e o corpo do teste integrado com saída `ok`. O processo integrado terminou com código 1 somente ao remover o arquivo `h1-test.sqlite3`: Django recebeu `PermissionError: [WinError 32]` em teardown. O script parou corretamente e não executou a suíte focal agregada. Não há falha de assertion/produto demonstrada; o handle aberto é provável no fluxo ORM em threads, mas seu dono exato não foi identificado.

```text
ACTIVITY = MON-RUNTIME-V1-H1-EXECUTION-RECOVERY
INTEGRATION_ASSERTIONS = PASS / 1 test
INTEGRATION_RUNNER = FAIL / Windows file deletion in Django teardown
FAILURE_CLASS = TEST_HARNESS_OR_CONFIGURATION_ISSUE
WORKER_PRODUCT_DEFECT = NOT_ESTABLISHED
TEST_DB = changed from a temporary disk file to Django shared in-memory SQLite (:memory:)
DEFAULT_DB = still explicit under the unique %TEMP% root
ISOLATION_PROBE = asserts Django URI file:memorydb_default?mode=memory&cache=shared without opening a connection
FOCUSED_AGGREGATE = NOT_RUN
H1_PASS = NO
STATUS = PARTIAL
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 79
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
```

Django 5.2 constructs a shared-cache memory URI for `TEST.NAME=:memory:` and skips file deletion for the in-memory test DB. The adjusted PowerShell harness still needs one serial external run to demonstrate teardown and the complete focused H1/CAM suite. Keep the no-runner precheck, branch/SHA check, temp default DB, timeouts, and stop-on-first-error behavior. Do not claim H1_PASS unless every script command, including `h1-focused-suite`, exits 0.

### 20.44 MON-RUNTIME-V1-H1-AGGREGATE-MODULE-CORRECTION (2026-10-11)

O segundo transcript prova que o test DB compartilhado em memória eliminou o erro WinError 32: o teste integrado passou e o teardown destruiu normalmente `file:memorydb_default?mode=memory&cache=shared`. Smokes, sete testes de runtime e um teste de config também passaram. A suíte focal encontrou/executou 95 testes e terminou com exit 1 por um único erro de importação: `cameras.test_monitoramento_ownership` não existe. O transcript não reporta falhas de assertions nos testes executados.

A inspeção do repositório confirmou que o label incorreto não corresponde a arquivo. Os módulos reais relacionados são `cameras.test_monitoramento_mon09c` (lease persistente e fencing) e `cameras.test_monitoramento_mon09d` (configuração/diagnóstico operacional e sinais de ownership). O harness foi corrigido para incluir ambos em vez do label inexistente. Nenhum arquivo de produção ou teste foi alterado.

```text
ACTIVITY = MON-RUNTIME-V1-H1-EXECUTION-RECOVERY
INTEGRATION_AND_TEARDOWN = PASS
FOCUSED_AGGREGATE = FAIL / one ModuleNotFoundError for nonexistent label; 95 test cases ran
OWNERSHIP_MODULES = MON-09C and MON-09D / verified present
FAILURE_CLASS = TEST_HARNESS_CONFIGURATION_ISSUE
WORKER_PRODUCT_DEFECT = NOT_ESTABLISHED
HARNESS_TARGETS = corrected
H1_PASS = NO
STATUS = PARTIAL
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 80
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
```

Execute novamente o arquivo `.ps1` atualizado. O gate final requer exit 0 no agregado que agora inclui explicitamente MON-09C e MON-09D; não inferir H1_PASS a partir dos 95 testes parciais.

### 20.45 MON-RUNTIME-V1-H1-EXECUTION-RECOVERY-COMPLETE (2026-10-11)

O relatório final externo confirma que a suíte agregada focal passou: 110 testes em 56,676 segundos, `OK`, test DB compartilhado destruído normalmente e `RESULT` declarando todos os smokes/runners com exit 0. Com os resultados anteriores (smokes Python/asyncio/isolation, 7 testes do runtime, 1 de configuração, 1 integração com teardown limpo), os gates H1 isolados desta atividade estão satisfeitos. A configuração manteve o DB default sob `%TEMP%`, usou `TEST.NAME=:memory:` e não abriu o banco operacional do repositório.

```text
ACTIVITY = MON-RUNTIME-V1-H1-EXECUTION-RECOVERY
H1_FOCUSED_AGGREGATE = PASS / 110 tests / exit 0
ALL_SMOKES_AND_RUNNERS = PASS / user-provided final result
H1_PASS = YES
STATUS = COMPLETE
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 81
ACTIVITY_COMPLETE = YES
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
```

O campo `LAST_COMPLETED_STEP` desse relatório específico ficou uma etapa atrás porque o harness escrevia o valor antes de atualizá-lo. Corrigi a ordem de telemetria no script, validei parsing PowerShell e `git diff --check`; essa correção não altera os comandos/testes e não foi seguida de nova execução. Não há defeito do Worker demonstrado pelos gates H1 concluídos. Esta conclusão não implica homologação PostgreSQL, câmeras reais ou prontidão de produção.

### 20.46 MON-RUNTIME-V1-H2-POSTGRESQL-PREPARATION (2026-10-11)

O prompt H2 completo exige PostgreSQL exclusivamente local e descartável, isolamento de loopback, credenciais temporárias e dados sintéticos; proíbe instalar Docker/serviço permanente automaticamente; e manda registrar o bloqueio mínimo se infraestrutura ou driver faltarem. A baseline foi confirmada em `codex/mon-runtime-v1-implementation` / `4ff2a9260a438a61f3a23e753dfdc3d5c166424a`, preservando os três documentos WIP e o harness H1.

```text
ACTIVITY = MON-RUNTIME-V1-H2-POSTGRESQL-PREPARATION
STATUS = BLOCKED / no PostgreSQL server, Docker or Python driver available
PYTHON = .venv 3.14.7
DJANGO = 5.2.18
DATABASES = config.settings -> SQLite / repo db.sqlite3; not opened
DOCKER_AND_COMPOSE = NOT_FOUND
POSTGRES_BINARIES = NOT_FOUND_ON_PATH_OR_STANDARD_INSTALL_PATH
POSTGRES_SERVICE_TABLE = UNAVAILABLE_IN_SANDBOX
PSYCOPG_AND_PSYCOPG2 = NOT_INSTALLED_IN_VENV
FREE_DISK = 54.03 GB on C:
RAM = UNKNOWN / CIM unavailable
RESOURCE_CREATED_OR_CONNECTED = NO
OPERATIONAL_INFRASTRUCTURE_ACCESSED = NO
MIGRATIONS = NOT_RUN
H2_TESTS = NOT_RUN / 0 executed
STATIC_REPOSITORY_INSPECTION = transaction.atomic/select_for_update/F expressions observed; does not prove PostgreSQL compatibility
MINIMUM_REMEDIATION = make a disposable local PostgreSQL runtime available; install a compatible driver into .venv only
SAFE_RESUME = revalidate loopback host/database/user, then create synthetic isolated DB and run migrations/H2 transaction scenarios
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 82
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
H3 = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
```

Do not retry through an operational database, open the repository SQLite file, install Docker/services, edit requirements, source, tests or migrations, or start H3. The only changes for this checkpoint are the three continuity documents; the existing H1 harness remains untouched.

### 20.47 ARGOS-HOM-ROADMAP-REBASE-01 (2026-10-11)

O roadmap de homologação progressiva está em
`docs/projeto/ROADMAP_ARGOS_V5.md`, seção 23; atividades, gates e backlog estão
em `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 20. A atividade documental fechou
o rebase e atualizou PROJECT_STATE, mas não concluiu a reconciliação de
branches: checkpoints de publicação UI P3/P5 conflitam com ancestry observado.
P3 root/famílias e fonte P5 estão em branches separadas, não ancestrais da
branch atual nem de `origin/master`. HOM-00 deve resolver o baseline canônico e
as referências de publicação antes de HOM-01; não mesclar ou declarar integrado
por inferência.

```text
ACTIVITY = ARGOS-HOM-ROADMAP-REBASE-01
MODE = DOCUMENTATION_ONLY
STATUS = COMPLETE / ROADMAP REBASED; HOM-00 TECHNICAL RECONCILIATION OPEN
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
BRANCH = codex/mon-runtime-v1-implementation
WORKTREE_PRESERVED = YES / existing continuity WIP, audit, and H1 harness
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 83
HOMOLOGATION_GATE = DEFINED / BLOCKED
H1 = PASS / 110 tests / isolated SQLite
H2 = BLOCKED / disposable local PostgreSQL and driver absent
H3 = NOT_STARTED / real-camera authorization required
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_ACTIVITY
LIVE = NOT_AUTHORIZED
PRODUCTION_READINESS = NOT_ESTABLISHED
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
NEXT_ACTIVITY = HOM-00 BASELINE RECONCILIATION
```

A decisão funcional aprovada para XLSX inclui preview, confirmação explícita,
matching único por patrimônio/serial, `ALL_OR_NOTHING`, rollback total e zero
alteração direta de estado MON. O schema e o template XLSX definitivo ainda
exigem homologação. Homologação progressiva proposta usa lotes de 50, 500 e
2.300 câmeras sem disparo em massa de probes. Exportação, galeria/captura,
alertas e retenções seguem backlog; a política registrada de retenção não
autoriza expurgo nesta fase. Consultar PROJECT_STATE §83 para baseline Git e
detalhe de WIP.

### 20.48 ARGOS-HOM-00-ROADMAP-FINAL-RECONCILIATION (2026-10-11)

O snapshot corrente é `PROJECT_STATE.md` seção 84. O baseline Runtime V1 e os
SHAs P3/P5 foram confirmados; P3 permanece protótipo/referência visual e P5
fonte de UI produtiva não integrada. Os worktrees P3/P5 continuam com WIP
`UNVERIFIED`. Não inferir aprovação, integração, validação ou homologação a
partir de publicação ou implementação em branch.

```text
ACTIVITY = ARGOS-HOM-00-ROADMAP-FINAL-RECONCILIATION
STATUS = DOCUMENTARY_RECONCILIATION_COMPLETE
HOM_00 = INTEGRATION_FOUNDATION_PENDING / NOT_PASS
DESIGN_SYSTEM_BASELINE = 2.0.2
DESIGN_SYSTEM_TARGET = 2.4.0 / RECOMMENDED / ADJUDICATION_PENDING
DESIGN_QA = MANDATORY / NOT_RUN
QUICK_DETAIL_IMAGE = LATEST_ACTIVE_IMAGE / CAPTURA_CAMERA OR UPLOAD_MANUAL
LATEST_CAMERA_CAPTURE = DISTINCT / CAPTURA_CAMERA ONLY
IMPORT_XLSX = REQUIRED_BEFORE_HOM / TEMPLATE_SCHEMA_PENDING
H1 = PASS / INHERITED
H2 = BLOCKED_BY_INFRASTRUCTURE
H3 = NOT_STARTED
G1 = BLOCKED
G2 = BLOCKED
G3 = BLOCKED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
LIVE = NOT_AUTHORIZED
PRODUCTION_READINESS = NOT_ESTABLISHED
NEXT_ACTIVITY = ARGOS-HOM-00-INTEGRATION-FOUNDATION / PLANNED / NOT_AUTHORIZED
```

A estratégia recomendada preserva `master`, prepara branch isolada candidata
`codex/hom-v1-integration` após preflight, integra MON Runtime V1 e P5
seletivamente, mantém P3 como referência visual, valida regressões e Design QA,
implementa XLSX e prepara VM. A promoção para `master` depende dos gates
aplicáveis. Nenhuma branch foi criada e nenhum merge foi executado.

Decisões pendentes: adjudicação canônica e compatibilidade da DS 2.4.0; schema
e template XLSX oficiais; diff e seleção exata das mudanças P5. H2 PostgreSQL
segue bloqueado por infraestrutura local ausente; H3 com câmeras reais não
iniciado e exige autorização própria.

### 20.49 ARGOS-HOM-00-CONTINUITY-RECOVERY-01 (2026-10-11)

O snapshot corrente está em `PROJECT_STATE.md`, seção 85. A recuperação ocorreu
entre worktrees no mesmo HEAD base `4ff2a9260a438a61f3a23e753dfdc3d5c166424a`:
origem `codex/mon-runtime-v1-implementation` preservada e destino
`codex/hom-v1-integration` reconciliado apenas com hunks documentais comparados.
A origem mantém seu WIP rastreado e os dois arquivos não rastreados; ambos foram
classificados na seção 85, sem cópia ou alteração.

```text
ACTIVITY = ARGOS-HOM-00-CONTINUITY-RECOVERY-01
SOURCE_WIP_PRESERVED = YES
TARGET_DOCUMENTS_RECONCILED = YES
DOCUMENTS_CHANGED = ROADMAP; SPRINTS; PROJECT_STATE; AGENT_CONTINUITY; ACTIVE_DOCUMENT_MAP; image contract; UI integration spec; UI V2 visual contract
PRODUCTION_CODE_CHANGED = NO
UI_CODE_CHANGED = NO
MIGRATIONS_CHANGED = NO
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 85
CONTINUITY_UPDATE = PASS / THIS SECTION AND ACTIVE_DOCUMENT_MAP section 53
HOMOLOGATION_GATE = BLOCKED
H1 = PASS / INHERITED
H2 = PENDING / BLOCKED_BY_INFRASTRUCTURE
H3 = NOT_STARTED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
LIVE = NOT_AUTHORIZED
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
DEPLOY = NOT_PERFORMED
NEXT_ACTIVITY = ARGOS-HOM-00-INTEGRATION-FOUNDATION
```

P3/P5 permanecem sem integração nesta atividade; nenhum merge ou cherry-pick P5/P3
foi realizado. Consulte `PROJECT_STATE.md` seção 85 para preflight, requisitos
reconciliados, classificação dos não rastreados e validação final.

### 20.50 ARGOS-HOM-01-UI-V2-SELECTIVE-INTEGRATION — preflight (2026-10-11)

O snapshot corrente está em `PROJECT_STATE.md`, seção 87. O destino
`codex/hom-v1-integration` foi confirmado no HEAD esperado
`d1fd9491692afb57da9dcfe0a27964efdb2d19e0`, com worktree limpa. O status das
origens foi verificado por leitura Git; WIP não rastreado em P5 e no branch UI
principal foi identificado e preservado. Nenhum arquivo de aplicação foi
alterado.

```text
ACTIVITY = ARGOS-HOM-01-UI-V2-SELECTIVE-INTEGRATION
STATUS = IN_PROGRESS / IMPLEMENTATION AUTHORIZED; VALIDATION PENDING
SOURCE_WIP_VERIFICATION = PASS / three requested worktrees checked
SOURCE_FILES_SELECTED = NONE
P5_DASHBOARD = METRICS_RETAINED / five-recent-camera list not retained in source composition
MAIN_UI_POST_ADJUSTMENTS = PRESENT / Shell, Inventory, CSS; reconcile before selection
DASHBOARD_REFERENCE = P3-A USER_APPROVED / frozen
INVENTORY_REFERENCE = P3-A USER_VISUAL_APPROVAL_PENDING
DS_BASELINE = 2.0.2
DS_TARGET = 2.4.0 / USER-AUTHORIZED ROUTE-SCOPED ADOPTION / NOT CANONICAL
CAMERA_DETAIL = PRESERVED / no change
QUICK_DETAIL = PROTECTED / no change; LATEST_ACTIVE_IMAGE correction remains pending
FUNCTIONAL_REGRESSION = NOT_RUN
DESIGN_QA = BLOCKED / no integrated rendering; approved Inventory reference pending
HUMAN_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE section 87
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP section 54
HOMOLOGATION_GATE = BLOCKED
IMPLEMENTATION_AUTHORIZATION = USER-REQUESTED CONTROLLED IMPLEMENTATION / DS ADJUDICATION PENDING
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED; MERGE = NOT_PERFORMED; DEPLOY = NOT_PERFORMED
```

### 20.52 ARGOS-HOM-01-DESIGN-QA-EVIDENCE-01 — preparação bloqueada (2026-10-11)

Consultar `PROJECT_STATE.md`, seção 89, e a matriz
`docs/prototype/ui-v2/evidence/hom-01-visual-qa-2026-10-11/README.md`.
Branch e HEAD permanecem `codex/hom-v1-integration` e
`d1fd9491692afb57da9dcfe0a27964efdb2d19e0`. WIP pré-existente foi preservado.

As referências de Shell, Dashboard, Camera Detail e Quick Detail estão
identificadas como aprovadas; Quick Detail permanece protegido, mas sua captura
de referência não foi encontrada no diretório temporário registrado. A
referência do Inventário tem conflito documental: a cobertura P3-A §41 declara
aprovação e os snapshots HOM-01 §§87-88 mantêm `PENDING`. Manter como candidata
até adjudicação humana. Playwright não está disponível no ambiente ativo e no
venv P5; os venvs P3 e principal não abriram por caminho de interpretador
ausente. O sandbox negou a conexão de loopback,
impedindo capturas da aplicação real. Não há screenshots integradas, comparação
visual nem divergências avaliadas. A tentativa usou apenas banco temporário
isolado e dados sintéticos, removidos ao encerrar; nenhum teste foi repetido e
nenhum código de UI/backend/migração mudou.

```text
ACTIVITY = ARGOS-HOM-01-DESIGN-QA-EVIDENCE-01
STATUS = BLOCKED / LOCAL RENDERING UNAVAILABLE
ACTIVITY_COMPLETION_PERCENT = 36%
DESIGN_QA = BLOCKED
INVENTORY_REFERENCE_CANDIDATE = NOT_CAPTURED / loopback blocked
INVENTORY_HUMAN_APPROVAL = PENDING
FUNCTIONAL_REGRESSION = PRIOR_77_TESTS_PASS / NOT_REEXECUTED
SOURCE_WIP_PRESERVED = YES
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §89
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP.md §56
HOMOLOGATION_GATE = BLOCKED
NEXT_RECOMMENDED_ACTIVITY = ARGOS-HOM-01-VISUAL-APPROVAL-AND-REMEDIATION
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED; MERGE = NOT_PERFORMED; DEPLOY = NOT_PERFORMED
```

O usuário autorizou a adoção aditiva do DS 2.4.0 limitada a Shell, Dashboard e
Inventário, mantendo DS 2.0.2 canônico e as superfícies protegidas. Essa decisão
permite avançar na implementação, mas não substitui regressão funcional,
referência aprovada do Inventário, Design QA ou aprovação visual humana. Não
inferir aceitação do protótipo Inventory nem declarar esses gates como PASS.

### 20.51 ARGOS-HOM-01-UI-V2-SELECTIVE-INTEGRATION — integração parcial (2026-10-11)

O snapshot atual está em `PROJECT_STATE.md`, seção 88. Shell, Dashboard e
Inventário receberam integração seletiva no target autorizado, branch
`codex/hom-v1-integration`, sem novo commit. Os testes de frontend, rotas
Visual QA, Camera Detail e Quick Detail passaram: 77 testes; `manage.py check`
sem erros. A referência P3-A do Dashboard está aprovada, mas a aprovação humana
do resultado integrado ainda não ocorreu. A referência de Inventário continua
`PENDING`; seu Design QA está `BLOCKED`.

DS 2.4.0 reside sob `static/css/ui-v2/hom-01-2.4.0/` e só é carregado nas
rotas Dashboard e Inventário. DS 2.0.2 permanece canônico; Camera Detail e seu
CSS original não foram alterados. Quick Detail mantém o contrato funcional e
visual; `LATEST_ACTIVE_IMAGE` segue registrada como pendência funcional.
Próxima ação: obter uma referência aprovada do Inventário, guardar screenshots
integradas nos mesmos viewport/zoom/estado das referências, produzir relatório
de diferenças e obter aprovação visual humana. Até esses gates e a conformidade
final passarem, não marcar a atividade completa nem abrir a entrada de
homologação. WIP das origens continua preservado. O banco e os módulos locais
temporários foram removidos e a porta do servidor está fechada; dois logs da
instância de QA permanecem bloqueados pelo sistema operacional para limpeza
posterior, conforme registrado em `PROJECT_STATE.md`, seção 88.

```text
ACTIVITY = ARGOS-HOM-01-UI-V2-SELECTIVE-INTEGRATION
STATUS = IN_PROGRESS / PARTIAL INTEGRATION; DESIGN QA BLOCKED
SHELL = INTEGRATED / FUNCTIONALLY VALIDATED
DASHBOARD = INTEGRATED / FUNCTIONALLY VALIDATED; HUMAN APPROVAL PENDING
INVENTORY = INTEGRATED / FUNCTIONALLY VALIDATED; REFERENCE AND DESIGN QA BLOCKED
CAMERA_DETAIL = PRESERVED
QUICK_DETAIL = PRESERVED / LATEST_ACTIVE_IMAGE PENDING
FUNCTIONAL_REGRESSION = PASS / 77 TESTS
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md section 88
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP.md section 55
HOMOLOGATION_ENTRY_GATE = BLOCKED
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED; MERGE = NOT_PERFORMED; DEPLOY = NOT_PERFORMED
```

### 20.53 ARGOS-HOM-01-HOST-VISUAL-QA-01 — loopback continua bloqueado (2026-10-11)

Consultar `PROJECT_STATE.md` seção 90 e o README de evidências
`docs/prototype/ui-v2/evidence/hom-01-visual-qa-2026-10-11/README.md`.

```text
ACTIVITY = ARGOS-HOM-01-HOST-VISUAL-QA-01
STATUS = BLOCKED_BY_EXECUTION_ENVIRONMENT
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
SOURCE_WIP_PRESERVED = YES
HOST_CHROME = AVAILABLE
HOST_BROWSER_ACCESS = BLOCKED / net::ERR_CONNECTION_TIMED_OUT at 127.0.0.1:8765
DJANGO_RENDERING = BLOCKED
SYNTHETIC_DATABASE = CREATED, MIGRATED, SEEDED, THEN REMOVED
RENDERED_SCREENSHOTS = NONE
P3_P5_REFERENCE_WORKTREES = INACCESSIBLE / host filesystem permission denied
QUICK_DETAIL_REFERENCE_SCREENSHOT = MISSING
INVENTORY_REFERENCE = CANDIDATE / approval conflict unresolved
DESIGN_QA = BLOCKED
FUNCTIONAL_REGRESSION = PRIOR_77_TESTS_PASS / NOT_REEXECUTED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §90
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP.md §57
HOM_01_STATUS = IN_PROGRESS
HOMOLOGATION_GATE = BLOCKED
```

Foi testado um único acesso pelo Chrome do host à aplicação integrada em
`127.0.0.1:8765`; a navegação expirou. O servidor e o SQLite temporário foram
encerrados/removidos. Não repetir tentativas equivalentes nem alterar código
para contornar a restrição. Os logs da tentativa anterior permanecem intactos.
Sem renderização real, não há screenshots integrados, comparação, resultado de
Design QA ou aprovação visual humana. Preservar as referências existentes; não
promover a referência de Inventário nem substituir a captura ausente de Quick
Detail por protótipo. O runbook Windows está no README de evidências.

### 20.54 ARGOS-HOM-01-ONE-CLICK-RUNTIME-SETUP — launcher implementado (2026-10-11)

Consultar `PROJECT_STATE.md` seção 91, `ACTIVE_DOCUMENT_MAP.md` seção 58 e o
README de evidências HOM-01. A entrada de uso normal é `INICIAR_ARGOS_QA.cmd`.

```text
ACTIVITY = ARGOS-HOM-01-ONE-CLICK-RUNTIME-SETUP
STATUS = IMPLEMENTED / STATIC_VALIDATION_PASS
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
WIP_PRESERVED = YES
LAUNCHER_PATH = INICIAR_ARGOS_QA.cmd
QA_SETTINGS_PATH = scripts/localqa/settings.py
QA_DATABASE_PATH = .local/qa/argos_visual_qa.sqlite3
QA_SEED_STATUS = PASS / 5 fictional cameras / repeated preparation idempotent
QA_USER_STATUS = PASS / qa-visual-hom01 / five minimum view/form permissions / non-admin / ephemeral password
LAUNCHER_STATIC_VALIDATION = PASS
WINDOWS_RUNTIME_VERIFIED = NOT_VERIFIED
RUNTIME_HOST_TEST = NOT_VERIFIED
BROWSER_RENDER_VERIFIED = NOT_VERIFIED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §91
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP.md §58
HOM_01_STATUS = IN_PROGRESS
DESIGN_QA = PENDING
HOMOLOGATION_GATE = BLOCKED
```

O novo settings exige uma variável que somente o launcher define, restringe
hosts ao loopback, força SQLite dedicado e não inicia worker/scheduler. O
SQLite existente na raiz e os logs QA anteriores foram preservados. O usuário
deve executar o CMD no Windows para receber a senha temporária e verificar
disponibilidade HTTP e renderização; não repetir o teste de loopback bloqueado
neste ambiente.

### 20.55 ARGOS-HOM-01-CAMERA-DETAIL-APPROVED-FIXES-RECOVERY (2026-10-11)

Consultar `PROJECT_STATE.md` seção 92, `ACTIVE_DOCUMENT_MAP.md` seção 59, o
adendo de apresentação no `ARGOS_UI_V2_VISUAL_CONTRACT.md` e o relatório de
diferença visual da atividade.

```text
ACTIVITY = ARGOS-HOM-01-CAMERA-DETAIL-APPROVED-FIXES-RECOVERY
EXECUTION_MODE = DIRECT / CONTROLLED_IMPLEMENTATION
STATUS = PARTIAL / IMPLEMENTATION_GATE PASS / VISUAL_GATE BLOCKED
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
OUT_OF_SCOPE_PRESENTATION = OPTION_A / USER_APPROVED
DS_CANONICAL = 2.0.2
FUNCTIONAL_REGRESSION = PASS / 98 targeted tests
RECOVERING = NOT_A_MON_EFFECTIVE_STATE / OFFLINE to ONLINE recovery transition tests pass
DESIGN_QA = BLOCKED / no local listeners or comparable screenshots
HUMAN_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §92
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP.md §59
HOM_01_STATUS = IN_PROGRESS
HOMOLOGATION_GATE = BLOCKED
```

Camera Detail importa os módulos CSS 2.0.2 de forma restrita à rota e repõe
localmente os helpers ausentes. Opção A suprime `monitoring.contexto` somente
para `scope_reason=OUT_OF_SCOPE`; a projeção MON, o partial compartilhado, o
campo Escopo, a configuração incompleta e o aviso stale permanecem preservados.
O contrato MON atual não projeta `RECOVERING` como estado efetivo; dois testes
focados confirmam a recuperação OFFLINE→ONLINE no reducer e no histórico de
indisponibilidade. Não houve mudança de backend, migrations, processo Worker,
commit ou push.

Os ports 8765 e 8766 não tinham listeners. A captura aprovada P5 da Camera
Detail não está na árvore disponível, e a continuidade registra não repetir
acesso de loopback equivalente neste ambiente. Screenshots e comparação visual
não foram produzidos; seguir para Design QA após a obtenção de referência e
render reais e então aguardar aprovação visual humana.

### 20.56 ARGOS-HOM-01-CAMERA-EDIT-RECOVERY — integração técnica (2026-10-11)

Consultar `PROJECT_STATE.md` seção 93, `ACTIVE_DOCUMENT_MAP.md` seção 60 e
`docs/prototype/ui-v2/evidence/argos-hom-01-camera-edit-recovery-2026-10-11/VISUAL_DIFFERENCE_REPORT.md`.

```text
ACTIVITY = ARGOS-HOM-01-CAMERA-EDIT-RECOVERY
STATUS = PARTIAL / IMPLEMENTATION_GATE PASS / DESIGN_QA BLOCKED
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
P3_D_APPROVAL = f5dd0308f46705e03c79609077ed1ec7a12bc766 / APPROVED
DS_CANONICAL = 2.0.2
CREATE_EDIT_FORMS = INTEGRATED / backend contracts preserved
FUNCTIONAL_REGRESSION = PASS / 177 targeted tests
REFERENCE_SCREENSHOTS = 18 / P3 ROOT blobs copied and hash verified
TARGET_SCREENSHOTS = NONE
DESIGN_QA = BLOCKED / no real integrated render
HUMAN_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / section 93
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP.md §60
HOM_01_STATUS = IN_PROGRESS
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED; MERGE = NOT_PERFORMED; DEPLOY = NOT_PERFORMED
```

A adaptação recupera header, cinco cards, grids de duas colunas, labels,
indicadores reais de obrigatoriedade, erros Django, ações e regras responsivas
por CSS restrito às duas rotas. Os wrappers/data attributes de Farm, Codec e
Retenção e o `camera-form.js` atual foram mantidos. Fluxos de criação/edição,
permissões, auditoria, mudança de IP, catálogo e upload em Camera Detail não
foram substituídos nem movidos. Não houve alteração de backend ou Shell.

O ambiente não recebeu um render integrado. Como os checkpoints 90 e 92 já
registram bloqueio de loopback e vedam repetição equivalente neste host,
`DESIGN_QA` permanece `BLOCKED`. As screenshots disponíveis são exclusivamente
as referências P3-D; não inferir equivalência visual nem aprovação. Próxima
etapa: usar o launcher/runbook local, capturar as duas páginas nos quatro
viewports, produzir comparação e obter aprovação visual humana explícita.

### 20.57 ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING (2026-10-11)

Consultar `PROJECT_STATE.md` seção 94, `ACTIVE_DOCUMENT_MAP.md` seção 61 e o
README de uso do launcher HOM-01.

```text
ACTIVITY = ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING
IMPLEMENTATION_AUTHORIZATION = GRANTED / user request
STATUS = PASS / operational account and 101 targeted tests
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
QA_DATABASE = .local/qa/argos_visual_qa.sqlite3 / owner marker verified
VISUAL_QA_ACCOUNT = PRESERVED / five explicit permissions and password hash unchanged
OPERATIONAL_QA_ACCOUNT = qa-operacional-hom01 / active / non-staff / non-superuser / no groups
OPERATIONAL_QA_PERMISSIONS = exactly seven explicit user permissions
OPERATIONAL_PASSWORD = random per launcher run / prior password invalidated / displayed in terminal only
PROVISIONING_IDEMPOTENT = PASS / no duplicate user or camera; existing seed rows preserved
FUNCTIONAL_TESTS = 101 PASS / temporary DB and media isolated under workspace
MON_RUNTIME = PRESERVED / no worker, scheduler or probe started
CAMERA_DETAIL_SOURCE = PRESERVED / no template, view or CSS edits in this activity
DESIGN_QA = BLOCKED / browser render not performed
HUMAN_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §94
CONTINUITY_UPDATE = PASS / this section and ACTIVE_DOCUMENT_MAP.md §61
HOM_01_STATUS = IN_PROGRESS
HOMOLOGATION_GATE = BLOCKED
```

O launcher agora valida a conta visual em modo somente leitura e provisiona
somente o perfil operacional. Colisões de nome sem marcador de propriedade
falham antes da reconciliação do seed. A senha visual não é lida ou alterada
pelo provisionador. O primeiro teste com o TEMP do sistema falhou por
permissão; a bateria repetida usou diretório exclusivo sob o workspace e
passou. Design QA aguarda render real dos dois perfis e aprovação humana.

### 20.58 ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING — checkpoint visual (2026-10-11)

Consultar `PROJECT_STATE.md` seção 95 e `ACTIVE_DOCUMENT_MAP.md` seção 62.

```text
ACTIVITY = ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING
IMPLEMENTATION_GATE = PASS
AUTOMATED_TESTS = 101/101 PASS
OPERATIONAL_QA_USER = qa-operacional-hom01
OPERATIONAL_QA_PERMISSION_VALIDATION = PASS / user-reported
UPLOAD_BUTTON_RENDERING = PASS / user-reported
UPLOAD_BUTTON_HUMAN_VISUAL_APPROVAL = APPROVED / button rendering only
BROWSER_UPLOAD_SUBMISSION = NOT_VERIFIED
RESPONSIVE_QA = PENDING
KEYBOARD_FOCUS_QA = PENDING
PROVISIONING = NOT_REPEATED
CODE_AND_PERMISSIONS = PRESERVED
HOM_01_STATUS = IN_PROGRESS
HOMOLOGATION_GATE = BLOCKED / remaining browser and responsive/keyboard QA
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED
```

O usuário confirmou o acesso com a conta operacional e aprovou a renderização
do botão de upload após validar as permissões. A confirmação é evidência
relatada pelo usuário e tem escopo visual limitado ao botão. Não registra
senha. Envio de arquivo no navegador, responsividade e foco de teclado seguem
pendentes; não inferir aprovação desses critérios nem repetir o provisionamento.

### 20.59 ARGOS-HOM-01 final baseline checkpoint (2026-10-11)

Consultar `PROJECT_STATE.md` §96 e
`docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`. Código-base:
`188afda5470e252fa8cf6fed5556a404073ee4fc`. O check Django passou; a
regressão direcionada tem uma falha de contrato de texto no Dashboard e a
suíte global ficou inconclusiva. Camera Detail e Create/Edit têm aceite humano
da composição integrada, sem aprovação de viewports inferida. O botão de
upload foi aprovado somente quanto à apresentação. Capturas integradas,
responsividade e teclado/foco continuam pendentes. P3/P5 refs foram
preservadas; WIP não versionado nos worktrees externos segue `UNVERIFIED`
porque o host negou acesso. `PUBLISH_READY = NO`; HOM-02 não autorizada.
Aplicar `ARGOS-RECONCILE-BEFORE-BRANCH` na authority de continuidade, §13.

### 20.60 ARGOS-HOM-01-DASHBOARD-CONTRACT-RECONCILIATION (2026-10-12)

Consultar `PROJECT_STATE.md` §97 e `HOM_01_UI_V2_BASELINE_CHECKPOINT.md` §9.
O rótulo aprovado é `Câmeras com IP duplicado`: a métrica soma câmeras em
grupos de IP repetido. A consulta foi corrigida para não filtrar todos os IPs
válidos no SQLite; soma e regra de domínio foram preservadas. As expectativas
legadas usam `Monitoramento e completude` e `Desconhecido`, com estado interno
`UNKNOWN` intacto. Os 28 testes direcionados e os 937 testes globais passaram;
o run global usou SQLite descartável e loopback local para o event loop do
Windows. Não houve câmera real, worker operacional ou probe real. Somente o
texto autorizado do Dashboard e a consulta técnica necessária foram alterados;
layout, CSS, componentes e aprovações visuais anteriores foram preservados.
Design QA humano integrado segue pendente, portanto HOM-01 continua
`IN_PROGRESS`; HOM-02 permanece bloqueada.

### 20.61 ARGOS-HOM-01-INVENTORY-UNKNOWN-PRESENTATION-FIX (2026-10-12)

Consultar `PROJECT_STATE.md` §98 e
`docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md` §10. O mapa compartilhado
apresenta ONLINE como “Online”, OFFLINE como “Offline”, UNKNOWN como
“Desconhecido” e a classificação de escopo OUT_OF_SCOPE como “Não monitorada”.
Os três códigos técnicos permanecem intactos; OUT_OF_SCOPE continua distinto
de UNKNOWN. Inventário, Dashboard, Quick Detail e Camera Detail foram cobertos
sem alterar o payload técnico, cores, CSS ou Design System.

Os 82 testes direcionados, Django check e sintaxe JavaScript passaram. A
instância local permanece em código anterior porque o launcher usa
`runserver --noreload`; não reiniciar evitou repetir preparação/seed e rotação
da senha QA operacional. Renderização visual atualizada, viewport móvel e
aprovação humana seguem pendentes. WIP anterior preservado; HOM-01 continua
`IN_PROGRESS`; nenhuma branch, commit ou push foi feito.

### 20.62 ARGOS-HOM-01-DIAGNOSTIC-A-D-LABEL-RECONCILIATION (2026-10-12)

Consultar `PROJECT_STATE.md` §99 e
`docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md` §11. Os campos
`evidence_state` e `freshness` são valores derivados da projeção de saúde da
câmera, separados dos estados MON e dos enums persistidos. A UI da Camera
Detail apresenta `CURRENT`/`FRESH` como “Atual”/“Atualizado”, `STALE` como
“Desatualizado” e `UNKNOWN` como “Não determinada”/“Não determinado”. Os
códigos técnicos são preservados. “Último estado confirmado” aparece apenas
para estado estável ONLINE ou OFFLINE; UNKNOWN continua apresentado como
“Desconhecido” no estado atual, sem alegar confirmação.

Os 65 testes direcionados, `manage.py check` e `git diff --check` passaram.
Após o usuário recarregar o Django, a Camera Detail real foi conferida no Edge
em 1366x768 e 390x844, zoom 100%, DPR 1 e escala visual 1. Os rótulos “Não
determinada” e “Não determinado” foram renderizados; os códigos A–D crus não
aparecem no resumo, a linha de último estado confirmado não aparece para MON
UNKNOWN, e não há overflow horizontal no documento mobile. A navegação
horizontal interna permanece limitada ao próprio componente. Capturas foram
mostradas inline, sem arquivos persistidos. O usuário aprovou explicitamente
somente os rótulos A–D e a omissão da linha para MON UNKNOWN nesses dois
viewports, em resposta “certo”. Os demais viewports, a composição completa da
Camera Detail e os gates gerais de DESIGN QA continuam pendentes; HOM-01 segue
`IN_PROGRESS` e HOM-02 bloqueada. WIP preservado; sem branch, commit ou push.

### 20.63 ARGOS-HOM-01-INVENTORY-VISUAL-ACCEPTANCE (2026-10-12)

Consultar `PROJECT_STATE.md` §100 e
`docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md` §12. O usuário aprovou a
composição integrada do Inventário com o feedback “O inventário para mim está
legal.” O aceite é da composição como um todo; não deve ser convertido em
aprovação individual de cada viewport nem em evidência de cobertura técnica
completa.

Preservar a tabela desktop, os cards mobile, filtros, ações, paginação, Design
System e funcionalidades. O finding conhecido de quebra do cabeçalho
MONITORAMENTO em 1366px continua aberto: uma observação posterior o mostrou
em uma linha, mas não comprovou a resolução nos quatro viewports. Não fazer
novos ajustes visuais sem finding material ou autorização explícita. Nenhum
código foi alterado nesta atividade; WIP preservado. HOM-01 continua
`IN_PROGRESS` e HOM-02 bloqueada.

### 20.64 ARGOS-HOM-01-SIDEBAR-ACTIVE-STATE-RECOVERY — aprovação (2026-10-12)

Consultar `PROJECT_STATE.md` §101, `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`
§13 e `docs/projeto/ARGOS_HOM_01_SIDEBAR_ACTIVE_STATE_RECOVERY.md`. O usuário
aprovou explicitamente, com a resposta “aprovo”, o padrão visual das cinco
páginas nas capturas atuais e na contact sheet de
`docs/projeto/evidence/sidebar-active-recovery/`.

```text
ACTIVITY = ARGOS-HOM-01-SIDEBAR-ACTIVE-STATE-RECOVERY
HUMAN_VISUAL_APPROVAL = APPROVED / user reply: “aprovo”
APPROVAL_SCOPE = five integrated desktop pages, 2552x866 CSS pixels
RESPONSIVE_MOBILE_APPROVAL = NOT_INFERRED
ACTIVITY_COMPLETE = YES / bounded activity
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §101
HOM_01_STATUS = IN_PROGRESS / remaining gates
HOM02_START = BLOCKED
```

O aceite cobre a evidência integrada desktop em 2552×866 CSS pixels. Não
estende aprovação a visualização mobile ou responsiva. A atividade delimitada
ARGOS-HOM-01-SIDEBAR-ACTIVE-STATE-RECOVERY está completa após a aprovação e as
validações documentadas. HOM-01 continua `IN_PROGRESS` para os demais gates;
este aceite não fecha HOM-01 nem libera HOM-02. Sem commit ou push.

### 20.65 HOM-01-DASHBOARD-V7-VISUAL-CONFORMANCE-RECOVERY (2026-10-12)

Consultar `PROJECT_STATE.md` §103. A recuperação corrigiu a grade desktop e o
empilhamento mobile do overview, a hierarquia/divisores da qualidade cadastral
e a superfície única de atividade recente. O template e o CSS são locais ao
Dashboard; sidebar, topbar, domínio, views e consultas permaneceram intactos.
O Django check e 88 testes direcionados passaram. A inspeção integrada cobriu
1920x1080, 1440x900, 1366x768 e 390x844, em zoom 100%/DPR 1, sem overflow
horizontal; as capturas foram exibidas inline nesta conversa. A QA usa a base
temporária sintética já existente e a prévia local está em
`http://127.0.0.1:8767/dashboard/`.

O finding conhecido é a quebra em duas linhas de “Câmeras com IP duplicado”
na coluna secundária estreita; a terminologia aprovada foi preservada. O estado
vazio passou nos testes, mas não foi capturado no browser. Não foi produzido
diff pixel a pixel salvo. A aprovação visual humana permanece pendente; a
atividade não está completa, HOM-01 segue `IN_PROGRESS` e HOM-02 permanece
bloqueada. Sem branch nova, commit, push, merge, rebase ou deploy.

### 20.66 HOM-01-DASHBOARD-V7-FIDELITY-ROUND-2 (2026-10-12)

Consultar `PROJECT_STATE.md` §104 e `ACTIVE_DOCUMENT_MAP.md` §68. Nesta rodada,
Inventário e Qualidade cadastral passaram a ter títulos e superfícies alinhados
e alturas iguais; os três textos auxiliares do Monitoramento e a faixa inferior
de frescor foram restaurados. Atividade recente foi compactada sem ocultar os
cinco links de câmeras nem o registro de atividade. A convenção de meta usa
`total_atividades` e `cameras_recentes|length` do contexto SSR.

O contrato visual V7 §4 protege a nomenclatura posterior aprovada “Monitoramento
e completude”; portanto, o título antigo “Monitoramento técnico” não foi
reintroduzido. O aside “Estados técnicos das câmeras” foi restaurado. As
capturas integradas estão em
`C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/`
para 1440x900 e 390x844. `manage.py check` e 88 testes direcionados passaram.
Não há diff pixel a pixel; o aceite visual humano continua pendente. WIP
preservado, sem commit ou push. A atividade não está completa, HOM-01 segue
`IN_PROGRESS` e HOM-02 permanece bloqueada.

Capturas principais são `DASHBOARD_1440x900.png` (1440x900) e
`DASHBOARD_390x844.png` (390x844); `DASHBOARD_390x844_ATIVIDADE.jpg` mede
375x812 e é um recorte da viewport 390x844. `DASHBOARD_390x844_MONITORAMENTO.png`
é detalhe da faixa de frescor em 390x844. A imagem completa da página não foi
produzida. Roteamento desta atividade: root em análise/diagnóstico/reconciliação/
revisão, mechanical em código e scribe em materialização documental.

Follow-up de links auxiliares: as capturas `DASHBOARD_LINKS_1440x900.jpg` e
`DASHBOARD_LINKS_390x844.jpg` registram os três links “Ver câmeras” nos cartões
de Produção, Estoque e Desativadas. A captura mobile é crop 375x812 da viewport
390x844. Os dados e filtros de situação foram preservados; não houve mudança
de sidebar/topbar ou submissão de formulário. `manage.py check` e os 88 testes
direcionados passaram. A aprovação visual humana continua pendente.

### 20.67 HOM-01-DASHBOARD-V7-FIDELITY-ROUND-2 — aprovação (2026-10-12)

Consultar `PROJECT_STATE.md` §105 e `ACTIVE_DOCUMENT_MAP.md` §69. O usuário
respondeu “perfeito autorizo stage e commit”, aprovando a composição integrada
do Dashboard mostrada nas capturas recentes e autorizando stage/commit somente
do escopo Dashboard bounded. A aprovação é da composição; não registra aceite
independente para cada viewport da matriz. A atividade limitada do Dashboard
está completa, mas HOM-01 permanece `IN_PROGRESS` e HOM-02 bloqueada.

O root fará o snapshot pré-commit, revisará os paths do índice e preparará o
stage. `HEAD_BEFORE` é `11dcf7db0095416c125f8863ab89a2eef7fb278f`; o commit SHA
deve ser consultado no Git depois da execução. Push não foi autorizado. WIP
fora do Dashboard permanece fora do escopo. Nenhum SHA futuro é presumido.

### 20.68 HOM-01-DASHBOARD-V7-VISUAL-ACCEPTANCE (2026-10-13)

Consultar `PROJECT_STATE.md` §108, `ACTIVE_DOCUMENT_MAP.md` §72 e
`docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md` §15. O usuário aprovou a
composição Dashboard V7 nas capturas integradas de 1920×1080, 1440×900,
1366×768 e 390×844, com o feedback “Eu validei e está ok.” DPR observado:
0,9. Zoom 100% não verificado; comparação pixel a pixel não reivindicada.

Preservar a composição atual, sem novos ajustes visuais e sem repetir a
auditoria aceita. Este aceite conclui somente a atividade delimitada de
aprovação visual. HOM-01 continua `IN_PROGRESS`; HOM-02 continua bloqueada.
Nenhuma alteração de código-fonte, branch nova ou merge para master foi feita.

### 20.69 HOM-01-CAMERA-DETAIL-RESIDUAL-QA-CLOSURE (2026-10-13)

Consultar `PROJECT_STATE.md` §109, `ACTIVE_DOCUMENT_MAP.md` §73 e
`docs/projeto/evidence/camera-detail-residual-qa/REPORT.md`. A busca em
`docs/projeto/evidence/` não encontrou a pasta nem capturas de Camera Detail;
por isso não se repetiu automação do navegador nem captura. O usuário aprovou
formalmente encerrar a auditoria residual com limitações aceitas. Os aceites
anteriores da composição Camera Detail e do Diagnóstico A–D foram preservados;
nenhuma regressão material foi comprovada.

Permanecem `NOT_VERIFIED` a matriz atual dos quatro viewports, teclado/foco,
renderização atual por perfil e comparação visual integral com P5. A validação
histórica de permissões em `PROJECT_STATE.md` §94 continua limitada aos seus
conjuntos e testes de renderização. Nenhum finding P1/P2/P3 foi comprovado;
`DESIGN_QA_GLOBAL = NOT_DECLARED_PASS`. A atividade está
`CLOSED_WITH_LIMITATIONS`; HOM-01 continua `IN_PROGRESS` e HOM-02 permanece
bloqueada. Nenhum código-fonte foi alterado.
