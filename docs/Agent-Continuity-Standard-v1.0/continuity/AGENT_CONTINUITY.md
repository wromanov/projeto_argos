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

## 8. Estado atual e próxima atividade

MON-09A = COMPLETE / PASS; MON-09B = COMPLETE / PASS_WITH_SCOPE_DEVIATION; MON-09C = COMPLETE / PASS_WITH_FINDINGS; MON-09D = COMPLETE; MON-09E = COMPLETE / PASS.

MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_PROJECT_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
NEXT_REQUIRED_ACTIVITY = IMG-02 — Modelo, storage e proveniência (após adjudicação humana e autorização)
NEXT_REQUIRED_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
UI_DS_CANONICAL_SPEC = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
UI_DS_CANONICAL_SPRINT_MAP = docs/projeto/SPRINTS_ARGOS_V5.md
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
CAMERA_QUICK_DETAIL_PANEL = USER_APPROVED / details in docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md section 7.3
CAMERA_QUICK_DETAIL_PANEL_VMS = DO_NOT_ADOPT; VMS_REPLACEMENT = LOCATION
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
SECURITY_FINDINGS_AUTHORITY = docs/security_audit/auditoria_segurança_001.md; ver matriz vigente antes de reclassificar SEC-001...SEC-010
LOG_VOLUME_HARDENING_STATUS = HARDENING / NON-BLOCKING — potential high INFO log volume per cycle/attempt

A frente de monitoramento está encerrada tecnicamente; não retomar MON-09 nem criar outra atividade MON. Limites futuros continuam: PostgreSQL real, multi-processo de produção, rede/câmeras/credenciais reais, capacidade produtiva e budgets formais de CPU, memória e conexões. Potencial volume de logs INFO é HARDENING / NON-BLOCKING. A Fase C está em andamento no checkpoint documental IMG-01; IMG-02 é a próxima atividade planejada e ainda sem autorização de implementação. O baseline Git acima descreve a validação imediatamente anterior a este commit documental; revalidar Git ao iniciar nova sessão.

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

## 10. UI-DS e continuidade de produto

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

## 11. Handoff ARGOS

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

## 13. Checkpoint vigente — integração IMG-03 + UI-2 (2026-09-25)

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
