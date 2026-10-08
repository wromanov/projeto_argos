# ARGOS — Active Document Map

STATUS = CURRENT
DOCUMENT_TYPE = PROJECT_SPECIFIC_AUTHORITY_MAP
PROJECT = ARGOS
ACTIVE_DOCUMENT_MAP_READY = YES

## 1. Authorities de continuidade e handoff

| Path | Role | Authority scope | Status |
|---|---|---|---|
| `AGENTS.md` | Entry point / guardrails | Leitura mínima, autoridade, Git, segurança e continuidade | PRESENT / CURRENT CHECKOUT |
| `docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md` | Continuidade e handoff ARGOS | Princípio, critérios do gate, responsabilidades documentais, precedência e recuperação | PRESENT / CANONICAL / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Snapshot operacional | Estado atual, baseline, gates, autorização, decisões, blockers e próxima atividade | PRESENT / CURRENT_SNAPSHOT; CAM-INT-03-RUNTIME-02 section 52 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Continuidade do agente | Contexto necessário, riscos, limites, decisões e referências para assumir | PRESENT / ACTIVE; CAM-INT-03-RUNTIME-02 section 20.19 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Mapa de authorities | Paths, escopo, vigência e precedência documental | PRESENT / CURRENT; UI V2 authority mapped in section 16 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md` | Bootstrap de nova sessão | Ordem de leitura, validação Git e limites para retomada | PRESENT / ACTIVE; read latest PROJECT_STATE first |

## 2. Authorities canônicas do projeto

| Path | Role | Authority scope | Status |
|---|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md` | Roadmap operacional | Macrofases, capacidades, dependências e status macro | PRESENT / CANONICAL; UI V2 is parallel and prototype-driven |
| `docs/projeto/SPRINTS_ARGOS_V5.md` | Mapa de execução | Ordem, atividades/slices, dependências, status e gates | PRESENT / CANONICAL; snapshot amplo de P1 preservado; ver PROJECT_STATE section 37 para status atual da UI-V2 |
| `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md` | Authority operacional da UI V2 | Escopo, princípios, fluxo P0–P7, gates e próxima atividade visual | PRESENT / CANONICAL; P3-0 é o checkpoint anterior; patch ROOT e próximo gate constam no DCR e em PROJECT_STATE section 37 |
| `docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md` | Censo factual de superfícies e matrizes UI-V2-P0 | PRESENT / CANONICAL; P0 CLOSED_PASS |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` | Contrato de domínio de imagem | IMG-01...IMG-09 e consumidores de imagem | PRESENT / CANONICAL; DISPLAY_IMAGE integrated, deferred production backend decision |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` | Especificação UI/design system | Decisões UI-DS, CameraQuickDetailPanel, relação com Fase C e integração | PRESENT / CANONICAL; Quick Detail baseline approved; UI-3 product acceptance pending, section 18 |
| `docs/projeto/ARGOS_UI_DS_UI0_PREFLIGHT_FINDINGS_V1.md` | Registro factual dos findings de UI-0 | Findings do preflight read-only, sem alterar a authority de UI-DS | PRESENT / CURRENT FINDINGS RECORD; NON-BLOCKING |
| `docs/projeto/ADR-019_monitoramento_disponibilidade_gestao_imagens.md` | ADR de arquitetura | Arquitetura de monitoramento e relação com gestão de imagens | PRESENT / AUTHORITY; verificar vigência no escopo aplicável |
| `docs/projeto/ADR-020_contrato_estado_tecnico_monitoramento.md` | Contrato técnico de monitoramento | Estado e semântica de leitura técnica | PRESENT / AUTHORITY; verificar vigência no escopo aplicável |
| `docs/projeto/ADR-021_seguranca_capacidade_monitoramento.md` | ADR de segurança | Capacidade, credenciais e limites de monitoramento/captura | PRESENT / CANONICAL no escopo de segurança |
| `docs/security_audit/auditoria_segurança_001.md` | Estado e matriz de findings de segurança | Status SEC-001...SEC-010, gates por ambiente e sequência de governança SEC | PRESENT / CURRENT SECURITY FINDINGS AUTHORITY |
| `docs/projeto/handoff_continuidade_projeto_argos.md` | Handoff legado / histórico | Evidência histórica; não determina estado corrente | PRESENT / HISTORICAL / SUPERSEDED FOR CURRENT STATE |

## 3. Transversal policy set

CURRENT / ACTIVE:

| Path | Role / authority scope | Status |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.6.md` | Prompts, roteamento cognitivo e execução | CURRENT / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.3-Roteamento-Economico.md` | Execução direta, delegação e papéis | CURRENT / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.2.md` | Skills/plugins e limites de capability | CURRENT / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/policies/Independencia-Analitica-Agente-v1.md` | Independência analítica e qualidade de decisão | CURRENT / ACTIVE |

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

Baseline factual validada antes da reconciliação documental UI V2 em 2026-09-27:

- repository: `C:\Users\walac\desenvolvimento\projeto_argos`
- branch: `master`
- HEAD: `323bfb0856a0bedc2b1b17cb07cb60dbcdd7c816`
- origin/master: `47c6965f3a60c0026117584dae21ca8a280986a5`
- divergence: ahead 16 / behind 0
- worktree no preflight: clean; após a reconciliação: sete documentos modificados/unstaged e um plano UI V2 novo/untracked
- staging no preflight e após a reconciliação: empty
- validar Git diretamente em nova sessão; estes valores registram o baseline anterior às alterações documentais desta atividade

The technical MON-09 checkpoint remains `850efd2381d7f5b7df27e528dc3374ea58e507b3`;
it is historical technical evidence, not the current Git HEAD.

## 4.1 UI-DS continuity

```text
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
SELECTIVE_VISUAL_RETROFIT_RECORDED = YES
SELECTIVE_INTERACTION_ADOPTION_RECORDED = YES
CAMERA_QUICK_DETAIL_PANEL = USER_APPROVED / canonical details in docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md section 7.3
ARGOS_CURRENT_PAGE_COMPOSITION = PRESERVE
LATEST_CAMERA_CAPTURE_FEEDS_PANEL = SECURE PREVIEW AVAILABLE; UI-3 uses PANEL variant
FASE_C_DEPENDENCY = EXPLICIT
BIG_BANG_INTEGRATION = PROHIBITED
INTEGRATION_GATE = REQUIRED_WHEN_APPLICABLE
UI_0 = COMPLETE / PASS_WITH_FINDINGS; READ_ONLY; DOES_NOT_AUTHORIZE_IMPLEMENTATION
UI_1 = COMPLETE / INTEGRATED; COMMIT = c5928e8
UI_2 = COMPLETE / INTEGRATED; COMMIT = b57f959; INTEGRATION_COMMIT = c79fa06
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
UI_3_TECHNICAL_IMPLEMENTATION = COMPLETE; TECHNICAL_COMMIT = bcc7e7d
UI_3_INTEGRATION = COMPLETE; INTEGRATION_COMMIT = 1015a8f; INTEGRATION_GATE = PASS
UI_3_FUNCTIONAL_VALIDATION = PASS
QUICK_DETAIL_VISUAL_BASELINE = APPROVED / PROTECTED
UI_3_VISUAL_ACCEPTANCE = PASS / current Quick Detail baseline explicitly approved by user
UI_3_PRODUCT_ACCEPTANCE = PENDING
UI_3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PASS / PRODUCT_ACCEPTANCE_PENDING
UI_4 = NOT_AUTHORIZED
```

Detalhes permanecem exclusivamente em
`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`; ordem e marcos
estão em `docs/projeto/SPRINTS_ARGOS_V5.md`.


## 5. Historical monitoring workstream continuity

Os status técnicos desta seção registram checkpoints MON já concluídos. A
próxima atividade e autorização vigentes estão na seção 14 e em
`PROJECT_STATE.md`.

MON-07 = COMPLETE / PUBLISHED
MON-08A = PASS
MON-08B = PASS / PUBLISHED
MON-08C-H1 = PASS
MON-08C-H2 = PASS
MON-08C-1 = PASS
MON-08C-2 = PASS
MON-08C-3 = PASS
MON-08C-4 = PASS
MON-08C-5 = PASS
MON-08C = COMPLETE / PASS_WITH_FINDINGS
MON08C6 = PASS / FINAL ADJUDICATION COMPLETE
MON-08 = TECHNICALLY COMPLETE / PASS_WITH_FINDINGS
NEXT_TECHNICAL_MON08_ACTIVITY = NONE
MON08C7 = NOT_CREATED

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
MON-08 = TECHNICALLY COMPLETE / PASS_WITH_FINDINGS; H2 e MON-08C-6 concluídas.
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_REQUIRED_ACTIVITY = IMG-02 — Modelo, storage e proveniência (após adjudicação humana e autorização)
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_PROJECT_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED
NEXT_REQUIRED_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
MON08C6_STATUS = COMPLETE / FINAL ADJUDICATION COMPLETE
MON08C6_IMPLEMENTATION_AUTHORIZATION = NOT_APPLICABLE
MON08_HOMOLOGATION_AUTHORIZED = NO
MON08_DEPLOYMENT_AUTHORIZED = NO
MON08_PRODUCTION_AUTHORIZED = NO
PUSH = NOT_AUTHORIZED


## 6. Historical MON-09 closure snapshot and then-next project phase

Os status MON-09 e a situação da próxima atividade abaixo preservam aquele
checkpoint. O estado corrente após IMG-01 e desta atividade documental está na
seção 8; revalide Git diretamente.

MON-09A = COMPLETE / PASS
MON-09B = COMPLETE / PASS_WITH_SCOPE_DEVIATION
MON-09C = COMPLETE / PASS_WITH_FINDINGS
MON-09D = COMPLETE
MON-09E = COMPLETE / PASS
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_PROJECT_ACTIVITY = IMG-02 — Modelo, storage e proveniência
NEXT_PROJECT_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
NEXT_REQUIRED_ACTIVITY = IMG-02 — Modelo, storage e proveniência (após adjudicação humana e autorização)
NEXT_REQUIRED_ACTIVITY_STATUS = PLANNED / NOT_YET_AUTHORIZED_FOR_IMPLEMENTATION
SECURITY_GATES = LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS; HOMOLOGATION = BLOCKED; DEPLOYMENT = BLOCKED; PRODUCTION = BLOCKED
VALIDATED_ENVELOPE = UNKNOWN / ONLINE / OFFLINE como estados estáveis; SUSPECT efêmero; STALE como freshness; confirmation memory persistente; pending failure streak sobrevive restart; thresholds respeitados; restart sem transição/outage falsa; falha de banco não equivale a câmera offline; CANCELLED neutro; timeout/rede conforme semântica canônica; sem histórico funcional falso em falha operacional e com recovery possível; ownership por câmera, owner persistente e epoch monotônico; lease define elegibilidade operacional de takeover; epoch é fencing token; config_generation é independente; completion de owner obsoleto sem side effects de domínio; owner antigo não libera owner novo; completion válida libera ownership atomicamente; renovação de lease não implementada; MonitoringConfig integrado à configuração ARGOS, config inválida fail-fast; status, backlog/in-flight, falhas operacionais e ownership diagnosticáveis; observabilidade sem histórico funcional e logs sem secrets
FUTURE_VALIDATIONS = PostgreSQL real; multi-processo real em produção; rede real; câmeras reais; credenciais reais; capacidade produtiva; budgets formais de CPU, memória e conexões
LOG_VOLUME_HARDENING_STATUS = HARDENING / NON-BLOCKING — potential high INFO log volume per cycle/attempt

MON-08/MON-09 predecessor entries above are continuity history. IMG-01 is the
completed documentary checkpoint; IMG-02, IMG-03, UI-1 and UI-2 are now
integrated. Fase C is not complete. Do not resume MON-09 or infer production
readiness.

## 7. Image-domain continuity

IMG01_STATUS = COMPLETE / DOCUMENTAL
CANONICAL_IMAGE_CONTRACT = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
LATEST_CAMERA_CAPTURE = select CAPTURA_CAMERA current record by captured_at DESC, recorded_at DESC, immutable_id DESC; assess availability/integrity after selection
NO_SILENT_FALLBACK_TO_OLDER_CAPTURE = YES
PROVENANCES = CAPTURA_CAMERA, UPLOAD_MANUAL
PRIMARY_IMAGE = DEFERRED_TO_IMG07
CAMERA_QUICK_DETAIL_PANEL = user-approved functional content in canonical UI spec; consumes LATEST_CAMERA_CAPTURE; no capture on open; UPLOAD_MANUAL is not an implicit fallback; VMS excluded in favor of location
MONITORING_SEPARATION = CAMERA_AVAILABILITY != IMAGE_CAPTURE_SUCCESS; capture failures do not change ONLINE/OFFLINE
OPEN_DECISION_COUNT = 6; see the canonical contract section 21 for each decision and its closure slice
IMG02_STATUS = COMPLETE / INTEGRATED
IMG02_IMPLEMENTATION_AUTHORIZATION = prior authorization for this slice consumed
PRODUCTION_STORAGE_BACKEND = DEFERRED; contract persistent storage and configurable abstraction recorded in canonical image contract
IMG03_STATUS = COMPLETE / INTEGRATED; COMMIT = f6e08b6; INTEGRATION_COMMIT = 0708797
SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED; TECHNICAL_COMMIT = e3f2d40; INTEGRATION_COMMIT = 7ca5f7c
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
PREVIEW_VARIANTS = THUMB; PANEL; dimensões na authority de imagens, seção 24
UI-3_TECHNICAL_IMPLEMENTATION = COMPLETE; UI-3_INTEGRATION = COMPLETE
QUICK_DETAIL_VISUAL_BASELINE = APPROVED / PROTECTED
UI-3_FUNCTIONAL_VALIDATION = PASS; UI-3_VISUAL_ACCEPTANCE = PASS; UI-3_PRODUCT_ACCEPTANCE = PENDING
UI-3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PASS / PRODUCT_ACCEPTANCE_PENDING
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
IMG-04 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-4 = NOT_AUTHORIZED
NEXT_CANDIDATE = IMG-04 / NOT_AUTHORIZED
UI_V2_P0_STATUS = CLOSED_PASS / ACTIVITY_COMPLETE = YES
NEXT_UI_ACTIVITY = UI-V2-P1 — VISUAL STYLE LAB
FASE_C_COMPLETE = NO

## 8. Continuidade no checkpoint UI-3 (histórico)

ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE
CONTINUITY_AUTHORITY = docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md
CURRENT_MACROPHASE = FASE C — Captura manual e gestão de imagens
CURRENT_GIT_BASELINE = master; HEAD 1015a8f0d7b6165ab057d81afb22007c3ae5e91b; origin/master 20be98d48ccfc19d458e393189168d9ecc93f309
DIVERGENCE = ahead 2 / behind 0
CURRENT_WORKTREE = sete documentos autorizados desta reconciliação modificados e unstaged; staging vazio
LAST_COMPLETED_ACTIVITY = SECURE_IMAGE_PREVIEW_DELIVERY — COMPLETE / INTEGRATED
LATEST_TECHNICAL_UI_ACTIVITY = UI-3 / INTEGRATED / VISUAL_ACCEPTANCE_PENDING
NEXT_CANDIDATE = IMG-04
NEXT_CANDIDATE_STATUS = IMG-04 NOT_AUTHORIZED; UI-3 visual/product acceptance pending; UI-4 NOT_AUTHORIZED
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
UI_DS_STATUS = UI-1 and UI-2 COMPLETE / INTEGRATED; UI-3 integrated / visual acceptance pending
IMG02_STATUS = COMPLETE / INTEGRATED
IMG03_STATUS = COMPLETE / INTEGRATED
LATEST_INTEGRATION_COMMIT = 1015a8f
SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
UI-3_TECHNICAL_COMMIT = bcc7e7d; UI-3_INTEGRATION_COMMIT = 1015a8f
UI-3_FUNCTIONAL_VALIDATION = PASS; UI-3_VISUAL_ACCEPTANCE = PENDING; UI-3_PRODUCT_ACCEPTANCE = PENDING
IMG-04 = NEXT_CANDIDATE / NOT_AUTHORIZED; UI-4 = NOT_AUTHORIZED
OPEN_DECISIONS = 7; detalhes somente no contrato canônico de imagem
SECURITY_GATES = LOCAL_DEVELOPMENT RELEASED_WITH_CONTROLS; HOMOLOGATION BLOCKED; DEPLOYMENT BLOCKED; PRODUCTION BLOCKED

Para o status, os commits e os critérios de handoff, consulte
PROJECT_STATE.md e AGENT_CONTINUITY.md. Este mapa identifica authorities e
escopo; não duplica os detalhes especializados.

## 9. Checkpoint histórico — IMG-02 + UI-1

IMG-02 = COMPLETE / INTEGRATED; commit ceda8f6
UI-1 = COMPLETE / INTEGRATED; commit c5928e8
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS
IMG-03 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-2 = NEXT_CANDIDATE / NOT_AUTHORIZED at that checkpoint
CANONICAL_IMAGE_AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
CANONICAL_UI_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
SPRINT_ORDER_AUTHORITY = docs/projeto/SPRINTS_ARGOS_V5.md

## 10. Checkpoint histórico — IMG-03 + UI-2 (2026-09-25)

IMG-03 = COMPLETE / INTEGRATED; COMMIT = f6e08b6; INTEGRATION_COMMIT = 0708797
UI-2 = COMPLETE / INTEGRATED; COMMIT = b57f959; INTEGRATION_COMMIT = c79fa06
INTEGRATION_GATE = PASS
AGENT_HANDOFF_GATE_RESULT = PASS
CANONICAL_IMAGE_AUTHORITY = docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md
CANONICAL_UI_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
SPRINT_ORDER_AUTHORITY = docs/projeto/SPRINTS_ARGOS_V5.md

INVENTORY_CAMERA_THUMBNAIL = APPROVED; SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = DEFERRED
SECURE_IMAGE_PREVIEW_DELIVERY = REQUIRED / NOT_YET_AUTHORIZED
SECURE_IMAGE_PREVIEW_DELIVERY_STATUS = NEXT_CANDIDATE / NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
UI-3 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE

Consulte `PROJECT_STATE.md` para evidências de integração, limites de
thumbnail, decisões deferred, permissões e estado Git pós-edição. A imagem e a
UI continuam subordinadas às authorities especializadas. A reconciliação
documental não altera security gates nem autoriza implementação, commit ou
push.

## 11. Checkpoint histórico — Secure Image Preview Delivery (2026-09-25)

SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED
TECHNICAL_COMMIT = e3f2d40
INTEGRATION_COMMIT = 7ca5f7c
INTEGRATION_GATE = PASS
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
PREVIEW_VARIANTS = THUMB; PANEL; dimensões na authority de imagens, seção 24
UI-3 = NEXT_CANDIDATE / NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE

No checkpoint, UI-3 era candidata e deveria reutilizar a variante PANEL. Esse
status foi supersedido pelo checkpoint pós-integração abaixo.

## 12. Checkpoint histórico — UI-3 e aceitação visual (2026-09-25)

```text
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
UI-3_TECHNICAL_IMPLEMENTATION = COMPLETE
UI-3_TECHNICAL_COMMIT = bcc7e7d
UI-3_INTEGRATION = COMPLETE
UI-3_INTEGRATION_COMMIT = 1015a8f
INTEGRATION_GATE = PASS
UI-3_FUNCTIONAL_VALIDATION = PASS
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
```

Para baseline, evidências de validação, invariantes, decisões deferred e gates
de segurança, consulte `PROJECT_STATE.md`. A UI-DS authority concentra o
contrato e o gate visual; a authority de imagens concentra detalhes de preview
e decisões do domínio. Esta seção identifica status e autoridade sem duplicar
as especificações.

## 13. Fontes técnicas da remediação front-end (2026-09-27)

| Path | Papel | Vigência |
|---|---|---|
| `docs/frontend/ARGOS_FRONTEND_AUDIT_REPORT.md` | Evidência e conclusão de UI-AUD-01; não é authority normativa | RECEIVED / AUDIT COMPLETE |
| `docs/frontend/ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md` | Diretriz técnica operacional Phase 0..6; subordinada às authorities do projeto e às decisões do usuário | RECEIVED / GUIDANCE ACTIVE |
| `docs/projeto/SPRINTS_ARGOS_V5.md` | Sequência executiva e gates da nova frente | CANONICAL / Phase 0 and Batch A closed; future visual changes gated by UI V2 prototypes |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`, seção 25 | Contrato de DISPLAY_IMAGE e status de IMG-DISPLAY-01 | CANONICAL / implementation integrated |

O estado corrente da integração Batch B está na seção 28 de PROJECT_STATE.md; o handoff
operacional vigente está na seção 19 de AGENT_CONTINUITY.md. Phase 0, Batch A e Batch B
estão integrados localmente; a aceitação visual da origem do Batch B passou, e a revisão
visual pós-integração em master permanece pendente. Este registro de contexto técnico é
anterior ao fechamento do P0; consulte a seção 14 para a próxima atividade UI vigente.

## 14. Authority vigente — ARGOS UI V2

| Path | Papel | Vigência |
|---|---|---|
| docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md | Authority operacional da trilha prototype-driven; define P0–P7, gates e próxima atividade | CANONICAL / ACTIVE; P0 CLOSED_PASS, P1 next / not started |
| docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md | Authority factual do inventário de 35 superfícies e das matrizes do UI-V2-P0 | CANONICAL / SCREEN CENSUS CLOSED_PASS |
| docs/projeto/ROADMAP_ARGOS_V5.md | Direção macro; mantém A2/A3/A4 e registra UI V2 paralela ao backend | CANONICAL / UPDATED; P1 next |
| docs/projeto/SPRINTS_ARGOS_V5.md | Ordem de execução; registra P0 fechado, P1 próximo e candidatas backend sem autorização | CANONICAL / UPDATED |
| docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md | Contratos UI-DS e Quick Detail; seção 18 registra a baseline visual protegida | CANONICAL / ACTIVE |
| docs/frontend/ARGOS_FRONTEND_AUDIT_REPORT.md | Evidência da auditoria UI-AUD-01 | AUDIT EVIDENCE; não normativa |
| docs/frontend/ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md | Guardrails e ownership CSS para implementação | TECHNICAL GUIDANCE; subordinada às authorities de produto e ao gate UI V2 |

O checkpoint de fechamento e o estado Git da atividade estão em
PROJECT_STATE.md, seção 29. UI-V2-P1 é a próxima atividade, mas não foi
iniciada nem autorizada por este checkpoint. O Admin permanece rastreado como
herdado e sem redesenho customizado por padrão. O gate visual pós-integração do
Batch B permanece PENDING_USER_REVIEW; isso não altera a baseline aprovada e
protegida do Quick Detail.

MON-AVAIL-01 e MON-AVAIL-02 foram citados na instrução atual do usuário e
não foram localizados em documentos do checkout nesta reconciliação. O mapa de
sprints mantém IMG-04 como candidata backend/imagens não autorizada; a ordem
entre as candidatas continua sem adjudicação.

## 15. UI-V2-P3-0 — harness compartilhado (2026-09-28)

| Path | Papel | Vigência |
|---|---|---|
| docs/prototype/ui-v2/contracts/P3_PROTOTYPE_HARNESS.md | Contrato operacional do harness, preview, states, fixtures, evidence, ownership, fan-out e integração | CURRENT / P3-0 TECHNICAL PASS / USER REVIEW PENDING |
| docs/prototype/ui-v2/screens/index.html | Entry point P3 e demonstração do shell compartilhado | TECHNICAL_READY_FOR_REVIEW |
| docs/prototype/ui-v2/contracts/SCREEN_COVERAGE.md | Matriz master owned por ROOT; integração das famílias após review individual | CURRENT / ROOT-ONLY |
| docs/prototype/ui-v2/evidence/screenshots/shell/ | Evidence determinística do shell nos quatro viewports requeridos | CAPTURED / PRODUCT DESIGN QA PASS |
| design-qa.md | Relatório acumulado; preserva o histórico P2 e registra o QA P3-0 | CURRENT |

P3_0_WORK_COMMIT = 7bf33de0456fbaaaf46943d73f44f82abb3e3a84
P3_0_STATUS = PASS / TECHNICAL HARNESS COMPLETE
USER_P3_0_APPROVAL = PENDING
FAN_OUT_READY = NO

P2 permanece fechado, Design System 2.0.0 pinado e Quick Detail protegido. O Card B é a autoridade específica para P3-0. Os snapshots amplos de roadmap/sprint ainda citam P1 como próximo; isso não inicia famílias nem autoriza mudança na sequência global. P3-A/B/C/D continuam proibidas até review humano P3-0, integração canônica, validação pós-integração e publicação.

## 16. UI-V2 ROOT — semântica de hidden no Design System 2.0.1 (2026-09-28)

| Path | Papel | Vigência |
|---|---|---|
| `docs/prototype/ui-v2/contracts/DSCR-UIV2-001-HIDDEN-SEMANTICS.md` | DCR ROOT do invariante HTML `hidden`, causa, alcance, versão e validações | CURRENT / APPROVED / PUBLISHED |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 37 | Snapshot atual de Git, gates, autorização e próxima atividade | CURRENT / PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.7 | Decisões recentes, limites, achados e handoff para retomada | CURRENT / AGENT_HANDOFF_GATE PASS |
| `docs/prototype/ui-v2/contracts/P3_PROTOTYPE_HARNESS.md` | Handoff histórico P3-0 e composição compartilhada | BASELINE HISTÓRICO / 2.0.0 |
| `docs/prototype/ui-v2/contracts/SCREEN_COVERAGE.md` | Matriz principal de ownership das telas; não alterada por este patch | SOB OWNERSHIP ROOT / SEM RESULTADOS DE FAMÍLIA ADICIONADOS |

ROOT_PATCH_BRANCH = codex/ui-v2-ds-2.0.1-hidden-semantics
DS_PATCH_WORK_COMMIT = 8121ed38cc15e1ff6e72cb46bbb2ca865100bce0
DS_PATCH_INTEGRATION_COMMIT = 70e996f5e25d9c9b5d0f4ec0a256c44efcec6274
CURRENT_DESIGN_SYSTEM_VERSION = 2.0.1
P3_A/B/C/D_HANDOFFS = unchanged / branches not resumed
NEXT_GATE = aplicar controladamente DS_PATCH_WORK_COMMIT às famílias, mantendo o DCR ROOT fora das alterações familiares, e executar QA específica
NEXT_GATE_STATUS = PLANNED / NOT AUTHORIZED

Os registros históricos de P2/P3-0 permanecem inalterados na versão 2.0.0. Esta seção 16 substitui o status de prontidão registrado na seção 15: P3-0 foi concluída e publicada antes deste patch. A atividade ROOT não autoriza implementação ou integração das famílias, atualização da cobertura global nem integração da UI de produção.

## 17. BC-00 — contratos do backend ARGOS (2026-10-01)

| Path | Papel | Escopo | Vigência |
|---|---|---|---|
| `docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md` | Registro de contratos | Índice, precedência, status de implementação e limites de autoridade | CURRENT / BC-00 |
| `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md` | Contrato de acesso | Grupos, permissões e fronteira web/worker | CURRENT / BC-00 |
| `docs/projeto/contracts/backend/camera/` | Contratos CAM-INT-01..07 e diagnóstico de saúde | Capability, segredo, RTSP/HTTP, diagnósticos, compatibilidade e hardening | CURRENT / baseline; adapters reais não homologados |
| `docs/projeto/contracts/backend/monitoring/` | Contratos MON-AV/PROBE/WORKER/REC/OWN/OBS/HIST | Estado, execução, recuperação, ownership, observabilidade e histórico | CURRENT / core local; runtime de produção não homologado |
| `docs/projeto/contracts/backend/images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` | Integração de captura | Integração com o domínio de imagem canônico, sem duplicá-lo | CURRENT / complemento |
| `docs/projeto/contracts/backend/production/` | Contratos PROD-PERSIST/TOPO/CAP | Persistência, topologia e capacidade | CURRENT / decisões abertas explícitas |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` | Contrato de domínio de imagem | Proveniência, seleção, leitura, preview, lifecycle e consumidor | CANONICAL / mantido como authority |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 40 | Estado de BC-00 | Baseline, status, autorização e próxima atividade | CURRENT / publicação BC-00 registrada; verificar HEAD diretamente |

BC-00 cria baseline documental, não implementação nem autorização de acesso a
câmera. Estado e fronteiras não homologadas estão no registro do backend.

## 18. BC-02 — readiness de implementação local backend (2026-10-01)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md` | Índice e classificação final dos 20 contratos | CURRENT / BC-02 overlay sobre BC-00 |
| `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md` | DAG, waves, ownership, migrations e primeira slice Luna | CURRENT / BC-02 |
| `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md` | Quatro grupos vinculantes e matriz de permissões | CURRENT / BC-02; substitui matriz de três grupos BC-00 |
| `docs/governanca/GOVERNANCA_CAMERAS.md` | Governança operacional das câmeras e quatro perfis | CURRENT / BC-02 alinhado ao contrato BC-AUTH |
| `docs/projeto/contracts/backend/camera/` | Profile, credencial, RTSP/HTTP, A-D, vendor e policy | CURRENT / BC-02 local; validação real pendente |
| `docs/projeto/contracts/backend/monitoring/` | Core local e runtime/observabilidade novos | CURRENT / BC-02; produção pendente |
| `docs/projeto/contracts/backend/images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` | Job de captura separado e domínio de imagem canônico | CURRENT / BC-02; captura real pendente |
| `docs/projeto/contracts/backend/production/` | Persistência, topologia e capacidade | CURRENT / PRODUCTION_ONLY |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 43 | Snapshot BC-AUTH-02 | CURRENT / BC-AUTH published and validated; verify current Git synchronization directly |

BC-02 não implementa runtime nem autoriza câmera, homologação, LIVE, commit
ou push. O domínio de imagem completo continua em
`docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`. A track UI P5 mantém gates
próprios; apenas os pontos de integração backend constam na ordem BC-02.

BC-AUTH-02 registra o commit, fast-forward e validação da primeira wave de
implementação; a publicação permanece pendente neste snapshot. A próxima wave
é CAM-INT-01, CAM-INT-07 e MON-OBS. Nenhum trabalho dessa wave foi iniciado
ou autorizado por esse registro.

## 19. CAM-INT-02 — integração (2026-10-02)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 46 | Snapshot factual de integração, validação, DAG e Git | CURRENT / seção 46.1 registra publicação e verificação pós-push |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.12 | Handoff operacional após CAM-INT-02 | CURRENT / CAM-INT-06 é a próxima slice READY_NOW; autorização própria necessária |
| `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md` | Authority do DAG e ownership | CURRENT / relido após integrar CAM-INT-02 |

CAM-INT-02 foi integrada, validada e publicada. CAM-INT-06 é READY_NOW sob a
ordem serial de Wave 3; CAM-INT-03/04 ainda aguardam CAM-INT-07 e CAM-INT-06.
Consulte a seção 46 de `PROJECT_STATE.md` para evidências, testes e limites, e
a seção 46.1 para a verificação de publicação.

## 20. CAM-INT-07 — integração controlada (2026-10-02)

Snapshot histórico quanto à prontidão de CAM-INT-03/04; seção 21 supersede
essas conclusões devido ao predecessor runtime CAM-INT-02-R1 não publicado.
Evidências de publicação da CAM-INT-07 continuam válidas.

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 48.1 | Snapshot factual da integração, reconciliação, validação, DAG e publicação | CURRENT / PUBLISHED / post-push verified |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.15 | Handoff CAM-INT-07 e limites ambientais | CURRENT / PUBLISHED / post-push verified |
| `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md` | Authority do DAG e ownership | CURRENT / relido após integração |
| `docs/projeto/contracts/backend/camera/CAM-INT-07_INTEGRATION_HARDENING_CONTRACT.md` | Contrato da policy de destino | CURRENT / unchanged |

CAM-INT-07 está integrada, validada e publicada, com `HEAD == origin/master`,
divergência `0/0` e worktree limpa. CAM-INT-03/04 estão tecnicamente prontas e
exigem autorização própria. Nenhuma sucessora, validação ambiental ou execução
de rede foi iniciada.

## 21. CAM-INT-02-R1-ARCH — authority de execução de credencial (2026-10-02)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md` | API/input/output/failures, autorização, lifetime, ownership, testes e AC-R1-01..04 | CANONICAL / IMPLEMENTATION_READY / NOT_IMPLEMENTED |
| `docs/projeto/contracts/backend/camera/CAM-INT-02_CREDENTIALS_CONTRACT.md` | Custódia e lifecycle; ownership da resolução e referência R1 | CANONICAL / implementation published, runtime boundary pending |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Consumer RTSP com dependency R1 e proibições de crypto/reveal | CANONICAL / PAUSED_ARCHITECTURAL_DEPENDENCY / READY_NOW=NO |
| `docs/projeto/contracts/backend/camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md` | Consumer Basic/Digest com mesma dependency R1 | CANONICAL / READY_NOW=NO; local execution completion unverified |
| `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md` | DAG e ownership R1 antes de CAM-INT-03/04 | CURRENT / reconciled |
| `docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md` | Índice e classificação R1 | CURRENT / 20 original specialized contracts + 1 execution sub-slice |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 49 | Snapshot da adjudicação, baseline, limites e próxima atividade | CURRENT / published; architecture commit 5efc3fdaecbb83845e891206255c7556146bc3fb |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.16 | Handoff e invariantes de resolução interna | CURRENT / source for adapter readiness |

Próxima atividade: implementar CAM-INT-02-R1 com Luna/High, mediante autoridade
própria. CAM-INT-03/04 aguardam R1 implementada, integrada, validada e publicada;
a antiga conclusão de readiness imediato após CAM-INT-07 é histórica.
A reconciliação foi publicada no commit 5efc3fdaecbb83845e891206255c7556146bc3fb; as worktrees dos consumers não foram alteradas.

## 22. CAM-INT-02-R1-INT-R1 — integração e validação local (2026-10-02)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 50 | Evidência factual de recuperação, fast-forward, validação local, publicação e DAG | CURRENT / PUBLISHED / post-push verified |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.17 | Handoff de R1 integrada, invariantes e dependências dos consumers | CURRENT / PUBLISHED / post-push verified |
| `docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md` | Boundary, API, autorização e critérios de aceite | CANONICAL / unchanged |
| `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md` | Authority do DAG e ownership | CURRENT / reread after local integration |

R1 está implementada, integrada, validada e publicada pelo commit-fonte
`80739e5fa961ecbb27d1fa42a9fbcbe02bc82add`; a continuidade foi publicada em
`57532018dc942876cdd2d383d011576717833e3a`, que também atualizou `master`.
CAM-INT-03 deve retomar sua lane existente com a nova dependência após revalidar
a autorização; CAM-INT-04 exige reconciliação de suas alterações locais antes
de continuação. Nenhuma lane foi iniciada ou alterada nesta atividade.

## 23. CAM-INT-03-INT — adapter RTSP integrado e validado localmente (snapshot histórico, supersedido quanto ao estado atual)

STATUS = HISTORICAL / consulte a seção 24 deste mapa e PROJECT_STATE seção 52 para a homologação runtime atual.

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 51 | Evidência factual da integração, validação local, bloqueio remoto e DAG | HISTORICAL / supersedido pela seção 24 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.18 | Handoff e invariantes do adapter RTSP integrado | HISTORICAL / supersedido pela seção 24 |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Contrato e critérios AC-01..03 do adapter RTSP | CANONICAL / unchanged |
| `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md` | DAG e ownership da implementação backend | CURRENT / reread after local CAM-INT-03 integration |

CAM-INT-03 está implementada, integrada e validada localmente pelo commit-fonte
`c031ea40233129408fdb9f19c44ce89c6566a972`. A consulta remota falhou; a
publicação permanece pendente e não há evidência de alinhamento com
`origin/master` remoto. Ver seção 51 de `PROJECT_STATE.md` antes de qualquer
continuação. CAM-INT-04 exige reconciliação; nenhum successor foi iniciado.

## 24. CAM-INT-03-RUNTIME-02 — homologação bloqueada por defeito no adapter (2026-10-06)

| Path | Papel | Vigência |
|---|---|---|
| docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md, seção 52 | Snapshot sanitizado, baseline Git, evidências e próxima ação | CURRENT / checkpoint documental solicitado |
| docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md, seção 20.19 | Handoff do defeito, limites locais e autorização | CURRENT / checkpoint documental solicitado |
| docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md | Contrato e critérios do adapter RTSP | CANONICAL / comportamento; cabeçalho de status pré-R1, ver PROJECT_STATE seção 52 |

CAM-INT-03 runtime permanece bloqueada e não homologada. O runtime GStreamer
1.28.7 está disponível, mas a ligação estática do decoder ao appsink falha
antes de o callback pad-added ser registrado. A próxima atividade é uma
correção autorizada dessa ligação, seguida de validação com GStreamer real.
A credencial local depende de chave efêmera da sessão de trabalho e não é
portátil; nenhum segredo ou banco foi copiado para o Git. Os cabeçalhos do contrato CAM-INT-03, do registry e do DAG ainda refletem o estado anterior à publicação de R1 e do adapter; sua reconciliação fica para atividade documental separada.

## 25. CAM-INT-04-HTTP-R1-CALLSITE-01-REMEDIATION — estado local (2026-10-08)

| Path | Papel | Vigência |
|---|---|---|
| docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md, seção 53 | Estado do branch, implementação, testes e gates | CURRENT / IMPLEMENTATION_PRESENT / VALIDATION_PENDING |
| docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md, seção 20.20 | Handoff e invariantes do consumer | CURRENT / VALIDATION_PENDING |
| docs/projeto/contracts/backend/camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md | Adapter e status do callsite R1 | CURRENT / local implementation, not homologated |
| docs/projeto/contracts/backend/images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md | Ownership IMG-CAP e escopo HTTP-only | CURRENT / RTSP pending |
| docs/projeto/contracts/backend/camera/CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md | Boundary pública de resolução | CURRENT / R1 published |
| docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md | Estado factual corrente das dependências | CURRENT / local consumer validation pending |

A implementação não está homologada: os testes focais foram bloqueados pela
revisão automática porque o Django runner aplicaria migrations no banco de teste
e LOCAL_DB_MIGRATION está NOT_AUTHORIZED. O system check e o AST parse passaram.
A migration não foi aplicada; não houve teste de câmera, credenciais, commit,
push ou merge.

A decisão de path limita-se ao default declarado pelo profile. Paths
customizados continuam fechados no worker ambiental até uma extensão
CAM-INT-07 autorizada e configurada; consulte as seções atualizadas de CAM-INT-04
e IMG-CAP.
