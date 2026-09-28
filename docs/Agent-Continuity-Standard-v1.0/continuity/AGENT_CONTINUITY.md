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
CURRENT_CANONICAL_GIT_BASELINE = f4e88146c1146cdf04d657eb6e3cefa560639b61
CURRENT_BASELINE_BEFORE_DOCUMENTARY_COMMIT = f4e88146c1146cdf04d657eb6e3cefa560639b61
LAST_VERIFIED_HEAD = f4e88146c1146cdf04d657eb6e3cefa560639b61
LAST_VERIFIED_ORIGIN_MASTER = f4e88146c1146cdf04d657eb6e3cefa560639b61
LAST_VERIFIED_DIVERGENCE = HEAD ahead 0 / behind 0
LAST_VERIFIED_WORKTREE = CLEAN (baseline antes deste commit documental)
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

## 4. Contexto histórico do estado técnico (status vigente na seção 19 e em PROJECT_STATE.md)

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
