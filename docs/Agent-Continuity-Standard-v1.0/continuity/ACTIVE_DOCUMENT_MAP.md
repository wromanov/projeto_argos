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
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Snapshot operacional | Estado atual, baseline, gates, autorização, decisões, blockers e próxima atividade | PRESENT / CURRENT_SNAPSHOT; reconciliation §124; HOM-03 blocked pending authorized SSH key; HOM-04 opening not established |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Continuidade do agente | Contexto necessário, riscos, limites, decisões e referências para assumir | PRESENT / ACTIVE; current handoff §20.83; resume HOM-03 after authorized SSH key |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Mapa de authorities | Paths, escopo, vigência e precedência documental | PRESENT / CURRENT; current pointer §87; root validation and diff check PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md` | Bootstrap de nova sessão | Ordem de leitura, validação Git e limites para retomada | PRESENT / ACTIVE; read latest PROJECT_STATE first |

## 2. Authorities canônicas do projeto

| Path | Role | Authority scope | Status |
|---|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md` | Roadmap operacional | Macrofases, capacidades, dependências e status macro | PRESENT / CANONICAL; current reconciliation §24; preserve earlier snapshots |
| `docs/projeto/SPRINTS_ARGOS_V5.md` | Mapa de execução | Ordem, atividades/slices, dependências, status e gates | PRESENT / CANONICAL; current reconciliation §21; preserve §20 historical snapshot |
| `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md` | Authority operacional da UI V2 | Escopo, princípios, fluxo P0–P7, gates e próxima atividade visual | PRESENT / CANONICAL; P3-0 é o checkpoint anterior; patch ROOT e próximo gate constam no DCR e em PROJECT_STATE section 37 |
| `docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md` | Censo factual de superfícies e matrizes UI-V2-P0 | PRESENT / CANONICAL; P0 CLOSED_PASS |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` | Contrato de domínio de imagem | IMG-01...IMG-09 e consumidores de imagem | PRESENT / CANONICAL; §26 approves Quick Detail LATEST_ACTIVE_IMAGE; implementation/integration/validation/homologation not established |
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

## 24. CAM-INT-03-RUNTIME-02 — checkpoint histórico do defeito no adapter (2026-10-06)

| Path | Papel | Vigência |
|---|---|---|
| docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md, seção 52 | Snapshot sanitizado, baseline Git, evidências e próxima ação | HISTORICAL / supersedido pelos checkpoints posteriores |
| docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md, seção 20.19 | Handoff do defeito, limites locais e autorização | HISTORICAL / reparo local registrado depois |
| docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md | Contrato e critérios do adapter RTSP | CANONICAL / comportamento; cabeçalho de status pré-R1, ver PROJECT_STATE seção 52 |

CAM-INT-03 runtime permanece bloqueada e não homologada. O runtime GStreamer
1.28.7 está disponível, mas a ligação estática do decoder ao appsink falha
antes de o callback pad-added ser registrado. A próxima atividade é uma
correção autorizada dessa ligação, seguida de validação com GStreamer real.
A credencial local depende de chave efêmera da sessão de trabalho e não é
portátil; nenhum segredo ou banco foi copiado para o Git. Os cabeçalhos do contrato CAM-INT-03, do registry e do DAG ainda refletem o estado anterior à publicação de R1 e do adapter; sua reconciliação fica para atividade documental separada.

O diagnóstico do defeito dinâmico foi posteriormente reparado localmente; este
checkpoint não descreve a causa ou o estado técnico corrente.

## 25. CAM-INT-03-REAL-RTSP-RUNTIME-HOMOLOGATION — bloqueada no gate de policy (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md, seção 53 | Snapshot do reparo, gate de policy, validações e status de homologação | HISTORICAL / retomada atual na seção 55 |
| docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md, seção 20.20 | Handoff do reparo, resultado fail-closed e limite da validação real | HISTORICAL / retomada atual na seção 20.22 |
| docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md | Comportamento e critérios do adapter RTSP | CANONICAL / sem alteração nesta atividade |

O defeito de ligação estática foi removido localmente; a prova dinâmica
sintética e os 17 testes focais passaram. Na tentativa real, a policy exata
carregou e os controles negativos passaram, mas o destino autorizado foi
recusado porque o perfil RTSP não define `default_path`. A atividade parou
antes de TCP ou stream real e permanece `NOT_HOMOLOGATED`; não houve geração de
chave, acesso a segredo ou mutação de credencial. `manage.py check` e
`git diff --check` passaram. Os cabeçalhos de status do registry, DAG e
contrato CAM-INT-03 mantêm a divergência histórica registrada na seção 52 de
`PROJECT_STATE.md`; não foram alterados nesta atividade.

Este registro antecede a implementação do transporte de paths e do composition
root; use a seção 27 para o estado atual.

## 26. CAM-INT-03 — contrato de configuração TargetPolicy (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md` | Contrato, implementação e evidências técnicas em §8 | CURRENT / IMPLEMENTED_LOCALLY / TECHNICAL_PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 54 | Snapshot da adjudicação contratual anterior | HISTORICAL / proposta supersedida pela seção 55 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.21 | Handoff da proposta contratual | HISTORICAL / supersedido pela seção 20.22 |
| `docs/projeto/contracts/backend/camera/CAM-INT-07_INTEGRATION_HARDENING_CONTRACT.md` | Semântica de validação de destino e baseline de hardening | CANONICAL / preservado |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Comportamento RTSP e credenciais | CANONICAL / cabeçalho histórico divergente já registrado |

As seções 24–25 preservam tentativas históricas. Para a causa do gate de policy e
a próxima ação, prevalece a adjudicação atual: URI da câmera resolvida corretamente,
gap no transporte de paths pelo ambiente e no composition root. Não preencher
default_path nem modificar câmera/perfil. Policy de ambiente segue independente da
configuração da câmera. Implementação, configuração efetiva e nova homologação
dependem de autorização própria. A reconciliação geral de status pré-R1 no registry,
DAG e contrato RTSP continua pendente, fora deste escopo contratual.

## 27. CAM-INT-03 — implementação local da configuração TargetPolicy (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md`, §8 | Contrato aplicado, comportamento e evidências das suítes | CURRENT / IMPLEMENTED_LOCALLY / TECHNICAL_PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 55 | Snapshot de implementação, baseline dirty, testes e gates | CURRENT / local / sem staging |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.22 | Handoff da implementação e próxima atividade | CURRENT |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Contrato RTSP preservado; comportamento do adapter | CANONICAL / sem alteração nesta implementação |
| `docs/projeto/contracts/backend/camera/CAM-INT-07_INTEGRATION_HARDENING_CONTRACT.md` | Semântica independente de autorização de destino | CANONICAL / sem alteração nesta implementação |

`ARGOS_CAMERA_ALLOWED_PATHS` e o composition root foram implementados e
validados localmente. CAM-INT-03 permanece `NOT_HOMOLOGATED`; nenhuma sessão
real foi executada. Próximo passo recomendado: homologação RTSP real R2, que
exige authority própria. A divergência histórica de status pré-R1 em registry,
DAG e contrato RTSP permanece fora desta atividade.

## 28. CAM-INT-03-INDEPENDENT-END-TO-END-TECHNICAL-AUDIT — causa comprovada (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/audits/CAM-INT-03_INDEPENDENT_END_TO_END_TECHNICAL_AUDIT.md` | Prova causal, stages/topologia, harness/logs, ambiente, testes, matriz e recomendação | CURRENT / EVIDENCE_REPORT; não autoriza patch |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 56 | Baseline, resultado, proteção de estado e próxima atividade | CURRENT / audit complete; fix not authorized |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.23 | Retomada, causa comprovada e limites | CURRENT / fix deferred; NOT_HOMOLOGATED |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Comportamento normativo RTSP | CANONICAL / unchanged; status histórico divergente explícito |

A auditoria isolou a ausência de sync do depayloader: controle produtivo
falha D; intervenção única no harness TEMP entrega vídeo raw ao appsink.
Código/testes preservados; transaction revertida e hash do banco idêntico.
Próxima atividade recomendada: correção de estado dinâmico e revalidação real,
somente sob autorização própria. Não promover homologação/readiness ou outras
lanes; reconciliação global de status históricos permanece pendente.

## 29. CAM-INT-03 — correção do estado dinâmico e checkpoint de homologação (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `cameras/integracao/rtsp/gst_adapter.py` e `cameras/test_camera_rtsp_adapter.py` | Correção de lifecycle e cobertura sync/falha | LOCAL / 19 TESTS PASS; preserva alteração baseline do adapter |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 57 | Baseline, validações, pré-requisito ausente e retomada | HISTORICAL / superseded by section 58 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.24 | Handoff do patch e bloqueio ambiental | HISTORICAL / superseded by section 20.25 |
| `docs/projeto/audits/CAM-INT-03_INDEPENDENT_END_TO_END_TECHNICAL_AUDIT.md` | Autoridade da causa raiz comprovada | CANONICAL EVIDENCE / unchanged |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Contrato comportamental do adapter | CANONICAL / unchanged |

O patch e 68 testes relevantes passaram, mas a homologação real não foi
executada porque os valores de usuário/senha temporários não estavam disponíveis
ao processo. O usuário autorizou uma chave Fernet nova, efêmera, e uso de
`replace_camera_credential` dentro de transação externa com rollback;
restauração de material histórico foi explicitamente cancelada. CAM-INT-03
permanece `NOT_HOMOLOGATED`. Retomar a validação canônica de 5 segundos quando
a credencial temporária estiver disponível por injeção process-local segura.


## 30. CAM-INT-03-DATABASE-PERSISTENCE-RECONCILIATION — homologação reconciliada (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 58 | Snapshot da reconciliação SQLite, veredicto do sinal e homologação | CURRENT / PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.25 | Handoff e próxima atividade | CURRENT / HOMOLOGATED |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Índice dos documentos atuais | CURRENT / esta atividade |
| `docs/projeto/audits/CAM-INT-03_INDEPENDENT_END_TO_END_TECHNICAL_AUDIT.md` | Evidência da causa raiz e runtime anterior | CANONICAL EVIDENCE / unchanged |

O harness mede snapshot de linhas de credencial, não hash do arquivo. Seus dois
labels conflitantes derivam da mesma comparação; classificado como defeito de
sinal/rotulagem. Snapshot lógico restaurado, sem outro caminho de escrita
persistente identificado, SQLite íntegro. CAM-INT-03 está homologada pela
execução real já registrada no pedido (A/B/C/D PASS, H264, 2,484 s). Hash e
mudança de metadados físicos não têm baseline anterior verificável. Warning de
giolibproxy não bloqueia nem causa o resultado; achado decodebin→appsink segue
OPEN.

## 31. CAM-INT-03-FINAL-REVIEW-AND-CHECKPOINT — revisão final e commit local (2026-10-07)

Este mapa registra o estado observado antes da publicação. O status local/push
pendente abaixo é histórico e foi supersedido pela seção 32.

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 59 | Resultado de revisão, regressão, reconciliação e checkpoint local | HISTORICAL / LOCAL_CHECKPOINT_PASS / PUSH_PENDING |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.26 | Handoff e próxima atividade | HISTORICAL / HOMOLOGATED / COMMITTED_LOCAL |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_TARGET_POLICY_CONFIGURATION_CONTRACT.md` | Contrato de ambiente/composição; status de implementação histórica | CURRENT CONTRACT / historical status snapshots preserved |
| `docs/projeto/audits/CAM-INT-03_INDEPENDENT_END_TO_END_TECHNICAL_AUDIT.md` | Evidência da causa e execução observada durante a auditoria | HISTORICAL TECHNICAL EVIDENCE / unchanged |
| `docs/projeto/contracts/backend/camera/CAM-INT-03_RTSP_CONNECTION_CONTRACT.md` | Contrato de comportamento RTSP; cabeçalho de status histórico | CANONICAL BEHAVIOR / known non-blocking status conflict |

CAM-INT-03 foi revista e comprometida localmente; o push está pendente de
confirmação direta após rejeição da revisão automática. Causa dinâmica resolvida; TargetPolicy e
composition root resolvidos; runtime real homologado com A/B/C/D PASS, H264 e
2,484 s. Persistência lógica permaneceu inalterada após rollback; o sinal
contraditório do harness é defeito de rotulagem. O finding secundário de ligação
decodebin→appsink e o aviso giolibproxy permanecem abertos/não bloqueantes. Não
reabrir esta lane sem regressão. `REMOTE_CONTINUATION_READY` só será `YES` após
push aprovado e verificação de igualdade com `origin/master`.

## 32. CAM-INT-03-POST-PUBLICATION-CONTINUITY-RECONCILIATION — estado atual (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 60 | Fechamento documental e estado publicado | CURRENT / CONSISTENT / PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.27 | Handoff corrente e próxima atividade | CURRENT / PUBLISHED / REMOTE_CONTINUATION_READY |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`, seção 32 | Índice da reconciliação corrente | CURRENT |
| `4a0eada4d06b9c61a12c78149257005297ce6a65` | Implementação CAM-INT-03 | PUBLISHED / HOMOLOGATED |

CAM-INT-03 está homologada e publicada. A implementação foi publicada com
`PUSH=PASS`; `HEAD=origin/master`, divergência `0/0`, worktree limpa, staging
vazio e continuação remota pronta. Os findings secundários de ligação
decodebin→appsink e de provisionamento local de autenticação permanecem abertos
e não bloqueantes; giolibproxy permanece não causal para CAM-INT-03. A próxima
atividade recomendada é retomar o backend ARGOS pela próxima atividade aberta
após CAM-INT-03.


## 33. ARGOS-UI-P5-PRODUCTION-INTEGRATION — Camera Detail (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 61 | Estado factual da sincronização local, integração, conflitos, testes e gates | CURRENT / LOCAL_INTEGRATION_VALIDATED / PUSH_PENDING |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.28 | Handoff, autoridade visual P5 e próximo gate remoto | CURRENT / P5_INTEGRATED_LOCALLY |
| `cameras/templates/cameras/detalhe.html` | Implementação aprovada da tela Camera Detail | P5 CANONICAL / integrated by `662e80e` |
| `static/css/ui-v2/camera-detail.css` | Estilos de produção Camera Detail | P5 CANONICAL / restored by `662e80e` |

O commit P5 `c91bc6d` foi integrado localmente no `master` por cherry-pick
como `662e80e`. A autoridade visual da tela é a P5 aprovada; não foi encontrado
binding funcional pós-P5 adicional a preservar. Testes focados 17/17 e
regressão integrada 101/101 passaram. A publicação remota ainda aguarda push
normal autorizado e verificação `HEAD = origin/master`; consulte a seção 61 de
`PROJECT_STATE.md` antes de continuar.


## 34. ARGOS-UI-P5-PRODUCTION-INTEGRATION — publicação (2026-10-07)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 62 | Fechamento publicado, gates e estado remoto final | CURRENT / COMPLETED / REMOTE_EQUAL |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.29 | Handoff após a publicação P5 | CURRENT / REMOTE_CONTINUATION_READY |
| `cameras/templates/cameras/detalhe.html` | Tela Camera Detail P5 | PUBLISHED / P5 CANONICAL |
| `static/css/ui-v2/camera-detail.css` | Estilos Camera Detail | PUBLISHED / P5 RESTORED |

A publicação foi verificada em `origin/master` com divergência zero. A seção 62
de `PROJECT_STATE.md` supersede o status de push pendente da seção 61.


## 35. CAM-INT-05-IMPLEMENTATION — registro inicial (supersedido em 2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 63 | Registro inicial da implementação e validação parcial | HISTORICAL / SUPERSEDED BY SECTION 64 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.30 | Registro inicial da fronteira CAM-INT-05 | HISTORICAL / SUPERSEDED |
| `cameras/integracao/diagnostics.py` | Boundary automática A-D e resultado sanitizado | LOCAL / VALIDATED |
| `cameras/models.py`, `cameras/migrations/0018_camera_health_snapshot.py` | Snapshot automático por câmera | LOCAL / MIGRATION AND SCHEMA VALIDATED |
| `cameras/monitoramento/repository.py`, `cameras/monitoramento/scheduler.py` | Completion integrada com snapshot e fencing MON | LOCAL / VALIDATED |
| `cameras/test_camera_diagnostics.py` | Testes da slice CAM-INT-05 | AUTHORED / 10 PASS |

O snapshot é derivado e automático; o worker MON e CAM-HEALTH continuam fora
desta atividade. O fechamento e as evidências validadas estão na seção 64 de
`PROJECT_STATE.md` e na seção 20.31 de `AGENT_CONTINUITY.md`. O risco de
colisão com a migration 0018 da branch CAM-INT-04 permanece para reconciliação
no checkpoint de integração.

## 36. CAM-INT-05-TECHNICAL-CLOSURE — fechamento técnico local (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 64 | Resultado, evidências, fileset e risco de integração | CURRENT / COMPLETE / NOT PUBLISHED |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.31 | Handoff de fechamento e próximo checkpoint | CURRENT / COMPLETE |
| `docs/projeto/contracts/backend/camera/CAM-INT-05_TECHNICAL_DIAGNOSTICS_CONTRACT.md` | Contrato de aceite | ACTIVE / CONFORMANT |
| `cameras/integracao/diagnostics.py`; `cameras/integracao/rtsp/*` | Evidência técnica A-D, adaptador RTSP e isolamento de fonte | LOCAL / VALIDATED |
| `cameras/models.py`; `cameras/migrations/0018_camera_health_snapshot.py` | Snapshot derivado, constraints e índice | LOCAL / TEST DATABASE AND SCHEMA PASS |
| `cameras/monitoramento/repository.py`; `cameras/monitoramento/scheduler.py` | Revalidação, fencing e completion atômica | LOCAL / VALIDATED |
| `cameras/test_camera_diagnostics.py` | Testes CAM-INT-05 | AUTHORED / 10 PASS |

As evidências externas confirmadas e sua reconciliação, incluindo a suíte MON
mista síncrona/assíncrona, constam na seção 64 de `PROJECT_STATE.md`. A branch
CAM-INT-04 tem uma migration 0018 independente; reconciliar o grafo antes da
integração, sem tratar a colisão como defeito do contrato local.

## 37. CAM-HEALTH-IMPLEMENTATION — projeção A-D local (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 65 | Baseline, fileset, validações, freshness, permissões e limitações | CURRENT / IMPLEMENTATION COMPLETE / PUBLICATION PENDING REMOTE CONFIRMATION |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.32 | Handoff, status do checkpoint e próxima atividade | CURRENT / FEATURE BRANCH CHECKPOINT |
| `docs/projeto/contracts/backend/camera/CAMERA_HEALTH_DIAGNOSTIC_CONTRACT.md` | A-D, stale/UNKNOWN, autorização separada e limites SSR | CANONICAL / IMPLEMENTED LOCALLY |
| `cameras/monitoramento/read_service.py` | Projeção read-only e freshness compartilhada do MON | LOCAL / FOCAL VALIDATION PASS |
| `cameras/views.py`; `cameras/templates/cameras/detalhe.html` | Resumo SSR e detalhes A-D autorizados | LOCAL / FOCAL VALIDATION PASS |
| `cameras/test_camera_health_projection.py` | Freshness, A-D, isolamento e autorização HTML | LOCAL / 41 focused tests across requested suites PASS |

Não houve migration nova. A colisão 0018 entre CAM-INT-04 e CAM-INT-05 segue
aberta para checkpoint serializado; MON Worker continua bloqueado por BC-02.

## 38. BC-02-INTEGRATION-EXECUTION — integração local validada (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 69 | Baselines, merge pendente, validação combinada, migrations e gates | CURRENT / READY_FOR_CHECKPOINT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.33 | Handoff BC-02, status de publicação/master e obrigação do worker | CURRENT / LOCAL_INTEGRATION_VALIDATED |
| `cameras/monitoramento/scheduler.py` | Completion integrada, fencing, snapshot CAM-INT-05 e telemetria MON-OBS | VALIDATED / MERGE PENDING |
| `cameras/monitoramento/observability.py`; `cameras/test_monitoramento_observability.py` | Sink e testes MON-OBS | VALIDATED / MERGE PENDING |
| `cameras/migrations/0018_camera_health_snapshot.py` | Snapshot CAM-INT-05 único no grafo desta integração | VALIDATED / fresh DB and 0017→0018 upgrade PASS |

MON-OBS, CAM-INT-05 e CAM-HEALTH estão publicados em suas referências fonte. A
integração local BC-02 foi validada em worktree exclusiva; o branch integrado
não foi publicado e ainda não foi integrado ao master. `MERGE_HEAD` permanece
presente para checkpoint Git posterior. O MON Runtime Worker e seu heartbeat


## 39. MON-RUNTIME-V1-CONTRACT-BASELINE-RECONCILIATION (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/contracts/backend/monitoring/MONITORING_WORKER_RUNTIME_CONTRACT.md` | Decisões locais V1, bounds e gates DC-01..07 | CURRENT / V1 CLOSED / WORKER NOT STARTED |
| `docs/projeto/contracts/backend/monitoring/MONITORING_OBSERVABILITY_CONFIG_CONTRACT.md` | Matriz V1 e três campos mínimos de configuração futura | CURRENT / CONFIG CONTRACT CLOSED / EXTENSION NOT IMPLEMENTED |
| `docs/projeto/contracts/backend/monitoring/MONITORING_OWNERSHIP_CONTRACT.md` | Claim/release por tentativa, expiry e fencing | CURRENT / NO EXPLICIT LEASE RENEWAL V1 |
| `docs/projeto/contracts/backend/monitoring/MONITORING_FAILURE_RECOVERY_CONTRACT.md` | Recovery serial bounded, callback fail-closed e sem OFFLINE operacional | CURRENT / V1 |
| `docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md`; `BACKEND_IMPLEMENTATION_ORDER.md` | Overlay factual sobre classificação e ordem BC-02 | CURRENT OVERLAY / BC-02 COUNTS AND DAG PRESERVED |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 70 | Snapshot da reconciliação e estado Git verificado | CURRENT / PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.34 | Decisões e handoff desta reconciliação | CURRENT / V1 CHECKPOINT |

```text
BASELINE = BC-02 / ccc0267527da7cac0a139a68c11982100f627147 / PRESERVED
SOURCE_DECISION = 22c9e3a59fe2be44dd17c2fd2cc90fc63f6059c4
WORKTREE = C:\Users\walac\desenvolvimento\projeto_argos_mon_runtime_v1
BRANCH = codex/mon-runtime-v1-implementation
HEAD = ccc0267527da7cac0a139a68c11982100f627147
MON_WORKER_IMPLEMENTATION = NOT_STARTED
HEARTBEAT_OWNER = WORKER_RUNTIME
HEARTBEAT_CADENCE = INDEPENDENT_OF_SCHEDULER_CYCLES
IMPLEMENTATION_READINESS = PASS / LOCAL CONTRACT BASELINE RECONCILED
OPERATIONAL_PRODUCTION_READINESS = NOT_ESTABLISHED
HISTORICAL_OPEN_PROPOSALS = SUPERSEDED_BY_FINAL_V1_ADJUDICATION
```

Os registros de BC-02 e os checkpoints anteriores permanecem históricos sem alteração. PostgreSQL, multi-worker, rede/câmera reais, capacidade e deploy são gates externos futuros. Esta reconciliação não implementa runtime, schema/migration, ledger ou estado `RECOVERING`, e não autoriza operação produtiva.

## 40. MON-RUNTIME-V1-IMPLEMENTATION (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `cameras/monitoramento/runtime.py`; `cameras/management/commands/run_monitoring_worker.py` | Runtime local e comando de worker isolado | IMPLEMENTED / LOCAL V1 / 921 TESTS PASS |
| `cameras/monitoramento/scheduler.py`; `repository.py`; `schemas.py`; `observability.py`; `config/environment.py` | Bounds, paginação, budgets de configuração e heartbeat/runtime | IMPLEMENTED / CONTRACT V1 CLOSED |
| `cameras/test_monitoramento_worker_runtime.py` e testes MON/CAM associados | Provas de runtime, fencing, drain, persistência, observabilidade e recuperação | VALIDATED / 921 TESTS PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 71 | Snapshot técnico, validação e gates externos | CURRENT / PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.35 | Decisões e handoff da implementação | CURRENT / LOCAL IMPLEMENTATION COMPLETE |

```text
BRANCH = codex/mon-runtime-v1-implementation
HEAD = ccc0267527da7cac0a139a68c11982100f627147
STAGING = EMPTY
STATUS = COMPLETE / LOCAL IMPLEMENTATION AND VALIDATION / 100%
MON_WORKER_IMPLEMENTATION = COMPLETE / LOCAL
MON_WORKER_LOCAL_VALIDATION = PASS / FULL_REGRESSION 921 PASS
MON_WORKER_BRANCH_PUBLICATION = PENDING_UNTIL_REMOTE_CONFIRMATION
MON_WORKER_MASTER_INTEGRATION = PENDING
PRODUCTION_READINESS = NOT_ESTABLISHED
POSTGRESQL_HOMOLOGATION = PENDING
MULTI_WORKER_HOMOLOGATION = PENDING
REAL_CAMERA_HOMOLOGATION = PENDING
TESTS = 921 PASS / temporary SQLite / 1299.244 seconds
NEXT = separate operational homologation only if authorized
```


## 41. ARGOS-CRYPTOGRAPHY-SECURITY-REMEDIATION (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `requirements.txt` | Pin direto de cryptography | CURRENT / 50.0.2 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 73 | Baseline, advisories, compatibilidade, validação e limitações | CURRENT / LOCAL REMEDIATION COMPLETE |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.37 | Handoff e estado do checkpoint | CURRENT / READY_FOR_GIT_CHECKPOINT |

```text
BRANCH = codex/mon-runtime-v1-implementation
INITIAL_HEAD = 9d5ac5debec3710212f5331a41201c43cb63ced9
FINAL_HEAD = 9d5ac5debec3710212f5331a41201c43cb63ced9
CRYPTOGRAPHY = 46.0.7 → 50.0.2
PIP_AUDIT = 0 known findings after remediation
FULL_REGRESSION = 921 PASS
CI_REMOTE = NOT_VERIFIED
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
NEXT_ACTIVITY = ARGOS-CRYPTOGRAPHY-GIT-CHECKPOINT
```


## 42. MON-RUNTIME-V1-H1-PREFLIGHT-VALIDATION (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/contracts/backend/monitoring/MONITORING_WORKER_RUNTIME_CONTRACT.md` e contracts MON-OWN/MON-REC/MON-OBS, MON Core, CAM-INT-05/CAM-HEALTH/Target Policy | Critérios normativos H1 e invariantes | CURRENT / V1; não alterados |
| `cameras/monitoramento/runtime.py`; `cameras/management/commands/run_monitoring_worker.py` | Runtime local e entrypoint sob validação H1 | IMPLEMENTED / LOCAL; command real não executado nesta atividade |
| `cameras/test_monitoramento_worker_runtime.py`; `cameras/test_monitoramento_scheduler_laboratorio.py`; observabilidade e suites CAM associadas | Evidências focais H1 | PARTIAL / 30 testes síncronos pass; async/integration NOT_VALIDATED |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 74 | Evidência, limites e status H1 | CURRENT / PARTIAL; PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.38 | Handoff de retomada H1 | CURRENT / H1 incompleta |

```text
BRANCH = codex/mon-runtime-v1-implementation
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
STATUS = PARTIAL / H1 ACCEPTANCE NOT MET
ISOLATION = PARTIAL / test runner announced in-memory SQLite; no operational DB or worker command accessed
ASYNC_RUNTIME_AND_PREFLIGHT = NOT_VALIDATED
NATIVE_RUNTIME = NOT_PERFORMED
H2_POSTGRESQL = PENDING
H3_REAL_CAMERAS = PENDING
PRODUCTION_READINESS = NOT_ESTABLISHED
NEXT = MON-RUNTIME-V1-H1-RESUME-ISOLATED-TEST-RUNNER
```

## 43. MON-RUNTIME-V1-H1-EXECUTION-RECOVERY (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `cameras/test_monitoramento_worker_runtime.py` | Alvos focais async, configuração Django transacional e composição H1 | NOT_RUN / bloqueados até smoke externo |
| `config/settings.py`; `.venv/pyvenv.cfg` | Settings padrão e proveniência do interpretador | INSPECTED / configuração padrão aponta a `<repo>\db.sqlite3` |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 75 | Evidência de diagnóstico e dependência externa | CURRENT / PARTIAL |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.39 | Handoff de execução H1 | CURRENT / aguarda PowerShell externo |

```text
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
PYTHON = 3.14.7 / repository .venv
DJANGO = 5.2.18
PYTHON_SIMPLE_PROCESS = PASS
ASYNCIO_TRIVIAL_SMOKE = TIMEOUT / 12s / EXIT 124
DEFAULT_DATABASE = <repo>\db.sqlite3 / not opened
TEST_RUNNERS = NOT_STARTED
RUNNER_ROOT_CAUSE = UNDETERMINED
STATUS = PARTIAL / external PowerShell comparison required
ISOLATION = NOT_YET_PROVEN_BY_TEST_RUNNER
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
```

Continuar com o script PowerShell temporário fornecido ao usuário. Não usar `config.settings` sem override do banco; não avançar a runners se `asyncio.run` não terminar; preservar execução serial e artefatos de log em `%TEMP%`.

## 44. MON-RUNTIME-V1-H1-EXTERNAL-POWERSHELL-RETRY (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| Transcript PowerShell fornecido pelo usuário | Evidência de tentativa externa | PRECHECK BLOCKED / dois processos encontrados; helpers não executados |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 76 | Resultado da tentativa e próximos gates | CURRENT / PARTIAL |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.40 | Handoff para retry seguro | CURRENT / requer identificação read-only dos processos |

```text
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
EXTERNAL_PYTHON_PROCESSES = PID 17352; PID 39204; ownership UNKNOWN / preserved
POWERSHELL_ARGUMENT_API = INCOMPATIBLE / ArgumentList unavailable
TESTS_STARTED = NO
TEST_COUNT = 0
FALSE_SUCCESS_OUTPUT = DISREGARDED
RUNNER_ROOT_CAUSE = UNDETERMINED
STATUS = PARTIAL
ISOLATION = NOT_PROVEN
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
```

Obter dados read-only de processo antes de nova execução. Usar script `.ps1` compatível com Windows PowerShell 5.1, não paste interativo; manter banco temporário explícito em `%TEMP%` e exigir smokes aprovados antes dos runners.

## 45. MON-RUNTIME-V1-H1-RESIDUAL-RUNNER-IDENTIFIED (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| Transcript CIM do usuário | Identificação da execução residual | CURRENT EVIDENCE / suite H1/CAM ativa, parent/child provados |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 77 | Ownership dos PIDs e causa do conflito de retry | CURRENT / aguardando encerramento condicional |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.41 | Próximo passo seguro | CURRENT / interromper runner anterior antes de novo runner |

```text
PID_39204 = prior Django H1/CAM suite runner
PID_17352 = its Python child
OWNER = PRIOR TEST EXECUTION / not unrelated
TERMINATED = NO
HANG_STAGE = UNDETERMINED
RETRY_BLOCKED = YES / processes remain active
CLASSIFICATION = TEST_RUNNER_OR_CONFIGURATION_ISSUE for retry blockage
H1_STATUS = PARTIAL
```

Revalidate and terminate only these identified test processes in the external PowerShell session; verify exit before starting any test. The Codex sandbox cannot access the external CIM process table.

## 46. MON-RUNTIME-V1-H1-POWERSHELL51-HARNESS-READY (2026-10-10)

| Path | Papel | Vigência |
|---|---|---|
| `run_mon_runtime_v1_h1_isolated_tests.ps1` | Harness externo PS 5.1 com timeouts, isolamento temporário e runners H1 seriais | PREPARED / syntax PASS / runtime NOT_RUN |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 78 | Estado factual após identificação/ausência dos PIDs e preparação do harness | CURRENT / PARTIAL |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.42 | Próximo passo externo | CURRENT / aguarda execução do `.ps1` |

```text
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
RESIDUAL_PIDS = REPORTED_ABSENT
HARNESS_SYNTAX = PASS
HARNESS_RUNTIME = NOT_RUN
TESTS = NOT_RUN
STATUS = PARTIAL
ISOLATION = NOT_YET_PROVEN_BY_TEST_RUNNER
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
```

Executar o arquivo `.ps1` como unidade, não colar os comandos no prompt. A própria sequência para no primeiro erro e não imprime sucesso antecipado.

## 47. MON-RUNTIME-V1-H1-TEST-DB-TEARDOWN-RECOVERY (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `run_mon_runtime_v1_h1_isolated_tests.ps1` | Harness H1 com test DB SQLite compartilhado em memória e default temporário em `%TEMP%` | UPDATED / aguarda nova execução PS 5.1 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 79 | Resultado dos gates unit/config/integration e falha de teardown | CURRENT / H1 partial |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.43 | Diagnóstico restrito ao teardown e próximo passo | CURRENT / rerun externo pendente |

```text
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
PYTHON_AND_ASYNCIO_SMOKES = PASS
RUNTIME_UNIT_AND_CONFIG = PASS / 8 tests
INTEGRATION_BODY = PASS / 1 test
INTEGRATION_TEARDOWN = FAIL / WinError 32 deleting temporary file DB
RECOVERY = TEST.NAME=:memory: / shared cache URI asserted by isolation probe
FOCUSED_AGGREGATE = NOT_RUN
H1_STATUS = PARTIAL
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
```

Run the updated `.ps1` as a file in normal Windows PowerShell. It now uses Django shared-memory SQLite for test DB teardown while keeping the default DB path under the unique `%TEMP%` root; the script must reach the focused aggregate with all commands at exit 0 before H1 is complete.

## 48. MON-RUNTIME-V1-H1-AGGREGATE-MODULE-CORRECTION (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `run_mon_runtime_v1_h1_isolated_tests.ps1` | Runner focal corrigido para importar módulos ownership reais MON-09C/MON-09D | UPDATED / aguardando rerun |
| `cameras/test_monitoramento_mon09c.py`; `cameras/test_monitoramento_mon09d.py` | Cobertura existente de lease/fencing e ownership operacional | SOURCE INVENTORY / alvo do próximo agregado |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 80 | Saída agregada parcial e correção do label | CURRENT / H1 partial |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.44 | Próxima ação e classificação do import inválido | CURRENT / rerun externo pendente |

```text
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
INTEGRATION_AND_DB_TEARDOWN = PASS
FOCUSED_AGGREGATE = 95 tests / 1 import error / invalid cameras.test_monitoramento_ownership label
REPLACEMENT_MODULES = cameras.test_monitoramento_mon09c; cameras.test_monitoramento_mon09d
ASSERTION_FAILURES_REPORTED = NO
H1_STATUS = PARTIAL
```

Rerun `& .\run_mon_runtime_v1_h1_isolated_tests.ps1` em Windows PowerShell normal; aguardar exit 0 da suíte focal corrigida para avançar o gate H1.

## 49. MON-RUNTIME-V1-H1-EXECUTION-RECOVERY-COMPLETE (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `run_mon_runtime_v1_h1_isolated_tests.ps1` | Harness H1 com DB de teste em memória e telemetria de etapa corrigida | H1 AGGREGATE PASS / 110 testes; telemetria ajustada após o run |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 81 | Resultado final da recuperação de execução e gates H1 | CURRENT / COMPLETE para a atividade H1 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.45 | Fechamento e limites da evidência | CURRENT / H1_PASS |

```text
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
H1_FOCUSED_AGGREGATE = PASS / 110 tests / exit 0
ALL_SMOKES_AND_RUNNERS = PASS
H1_STATUS = COMPLETE
H2_POSTGRESQL = NOT_STARTED
H3_REAL_CAMERAS = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
```

A atividade de recuperação H1 está concluída. A suíte focal cobriu runtime, scheduler, observabilidade, ownership/fencing e alvos/credenciais de câmera sob banco temporário; a execução não abriu o DB operacional. Os gates H2 PostgreSQL, H3 câmeras reais e produção permanecem fora desta validação.

## 50. MON-RUNTIME-V1-H2-POSTGRESQL-PREPARATION (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/contracts/backend/monitoring/MONITORING_WORKER_RUNTIME_CONTRACT.md`; contracts MON-OWN/MON-REC/MON-OBS | Invariantes locais V1, ownership/fencing e limites do worker | CURRENT / PostgreSQL remains an external validation gate |
| `config/settings.py`; `.venv` | Database engine and local Python/Django/driver availability | INSPECTED / SQLite only; Django 5.2.18; psycopg drivers absent |
| `cameras/monitoramento/repository.py`; migrations MON; `cameras/test_monitoramento_worker_runtime.py` | Static compatibility surface and candidate transactional validation | INSPECTED / dynamic H2 validation NOT_RUN |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, section 82 | H2 precheck, evidence boundary and remediation | CURRENT / BLOCKED; PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, section 20.46 | H2 block and safe resume condition | CURRENT / BLOCKED |

```text
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
BRANCH = codex/mon-runtime-v1-implementation
H1 = PASS / 110 TESTS
DOCKER = NOT_AVAILABLE
LOCAL_POSTGRESQL = NOT_FOUND
PSYCOPG_DRIVER = NOT_INSTALLED
CONFIGURATION_INSPECTION = PASS / before resource creation
DATABASE_ISOLATION = NOT_CREATED
MIGRATIONS_AND_H2_TESTS = NOT_RUN
H2_STATUS = BLOCKED / infrastructure and driver unavailable
H3_REAL_CAMERAS = NOT_STARTED
PRODUCTION_READINESS = NOT_ESTABLISHED
```

Resume only after a local disposable PostgreSQL runtime is available. Install any required PostgreSQL driver only into `.venv`; do not change requirements files. Revalidate host/database/user/loopback isolation before connecting, then apply migrations and execute the bounded H2 transactional scenarios. No operational infrastructure, SQLite file, product/test source, migration or dependency declaration was touched in this blocked attempt.

## 51. ARGOS-HOM-ROADMAP-REBASE-01 (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md`, seção 23 | Sequência macro HOM-00..HOM-05 e status | CURRENT / DOCUMENTARY REBASE |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 20 | Critérios, dependências, evidências, readiness gate, cargas e backlog | CURRENT / HOMOLOGATION PLAN |
| `docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md`; `ARGOS_UI_V2_SCREEN_CENSUS.md`; `prototype/ui-v2/contracts/SCREEN_COVERAGE.md`; P3/P5 branch authorities | Escopo UI V2 e evidência de integração | CURRENT AUTHORITIES / publication lineage conflict open in HOM-00 |
| `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md`; `production/PRODUCTION_PERSISTENCE_CONTRACT.md`; `production/RUNTIME_TOPOLOGY_CONTRACT.md` | Permissões, persistência e topologia de homologação | CURRENT / decisions to validate on canonical target |
| `docs/projeto/contracts/backend/monitoring/MONITORING_WORKER_RUNTIME_CONTRACT.md`; `camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md`; `images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md`; `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` | Worker, CAM-INT-04, captura, leitura e lifecycle de imagens | CURRENT / specialized authorities |
| `docs/auditoria/ARGOS-DATA-PERSISTENCE-CONTRACT-AUDIT.md` | Gaps e retenção que afetam readiness | PREEXISTING WIP / preserve; not implementation authority |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 83 | Baseline, branch conflict, H1/H2/H3, status e autorização | CURRENT / PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.47 | Handoff e próxima atividade | CURRENT / HOM-00 required |

```text
ACTIVITY = ARGOS-HOM-ROADMAP-REBASE-01
STATUS = COMPLETE / DOCUMENTATION_ONLY
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
BRANCH = codex/mon-runtime-v1-implementation
WORKTREE_PRESERVED = YES
ROADMAP = HOM-00..HOM-05 / CURRENT
HOMOLOGATION_GATE = DEFINED / BLOCKED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
NEXT = HOM-00 BASELINE RECONCILIATION
```

## 52. ARGOS-HOM-00-ROADMAP-FINAL-RECONCILIATION (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md`, seção 23 | Sequência e status macro HOM-00..05 | CURRENT / HOM-00 documentary reconciliation |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 20 | Estratégia de integração, critérios, dependências e gates | CURRENT / HOM-00 integration foundation pending |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`, seção 26 | Seleção visual do Quick Detail e galeria Camera Detail | CANONICAL / decision documented; implementation not established |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`, seção 20 | Regra de imagem Quick Detail e Design QA de HOM-01 | CANONICAL / Design QA mandatory, not run |
| `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md`, adendo de 2026-10-11 | Baseline DS e target recomendado | CURRENT / DS 2.4.0 adjudication pending |
| `docs/auditoria/ARGOS-DATA-PERSISTENCE-CONTRACT-AUDIT.md` | Findings de persistência/readiness | PREEXISTING WIP / preserve; not implementation authority |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 84 | Snapshot, status, gates, blockers e próxima atividade | CURRENT / PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.48 | Handoff e resumo de retomada | CURRENT |

```text
ACTIVITY = ARGOS-HOM-00-ROADMAP-FINAL-RECONCILIATION
STATUS = DOCUMENTARY_RECONCILIATION_COMPLETE
BASELINE_SHA = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
BRANCH = codex/mon-runtime-v1-implementation
WORKTREE_PRESERVED = YES
P3 = PROTOTYPE / VISUAL_REFERENCE / WIP UNVERIFIED
P5 = PRODUCTION_UI_SOURCE / NOT_INTEGRATED / WIP UNVERIFIED
DESIGN_SYSTEM_BASELINE = 2.0.2
DESIGN_SYSTEM_TARGET = 2.4.0 / RECOMMENDED / ADJUDICATION PENDING
DESIGN_QA = MANDATORY / NOT_RUN
IMAGE_AUTHORITY = QUICK_DETAIL LATEST_ACTIVE_IMAGE / LATEST_CAMERA_CAPTURE DISTINCT
IMPORT_XLSX = REQUIRED_BEFORE_HOM / SCHEMA AND TEMPLATE PENDING
H1 = PASS / INHERITED; H2 = BLOCKED_BY_INFRASTRUCTURE; H3 = NOT_STARTED
HOM_00 = INTEGRATION_FOUNDATION_PENDING / NOT PASS
HOM_01 = BLOCKED; HOM_02 = NOT_IMPLEMENTED; HOM_03 = NOT_STARTED
HOM_04 = BLOCKED; HOM_05 = PLANNED / NON_BLOCKING
NEXT = ARGOS-HOM-00-INTEGRATION-FOUNDATION / PLANNED / NOT_AUTHORIZED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED; MERGE = NOT_PERFORMED
```

## 53. ARGOS-HOM-00-CONTINUITY-RECOVERY-01 (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md`, seção 23 | Sequência HOM-00..HOM-05 e status | CURRENT / reconciled to integration target |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 20 | Critérios, dependências, evidências e gate | CURRENT / HOM-00 foundation pending |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`, seção 26 | Imagem do Quick Detail | CANONICAL / `LATEST_ACTIVE_IMAGE`; no implementation claim |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`, seção 20 | Design QA de HOM-01 | CANONICAL / mandatory, not run |
| `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md` | Baseline e adjudicação DS | CURRENT / DS 2.4.0 recommended, adjudication pending |
| `docs/auditoria/ARGOS-DATA-PERSISTENCE-CONTRACT-AUDIT.md` | Findings de persistência/readiness | SOURCE UNTRACKED WIP / preserved; candidate documentary evidence after review |
| `run_mon_runtime_v1_h1_isolated_tests.ps1` | Harness H1 | SOURCE UNTRACKED WIP / preserved; candidate test/evidence artifact after provenance and reproducibility review |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 85 | Snapshot desta recuperação | CURRENT / PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.49 | Handoff desta recuperação | CURRENT / continuity update PASS |

```text
SOURCE_BRANCH = codex/mon-runtime-v1-implementation
SOURCE_HEAD = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
TARGET_BRANCH = codex/hom-v1-integration
TARGET_HEAD = 4ff2a9260a438a61f3a23e753dfdc3d5c166424a
SOURCE_WIP_PRESERVED = YES
TARGET_DOCUMENTS_RECONCILED = YES
HOMOLOGATION_GATE = BLOCKED
H1 = PASS / INHERITED; H2 = PENDING / BLOCKED_BY_INFRASTRUCTURE; H3 = NOT_STARTED
PRODUCTION_CODE_CHANGED = NO
UI_CODE_CHANGED = NO
MIGRATIONS_CHANGED = NO
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
DEPLOY = NOT_PERFORMED
```

## 54. ARGOS-HOM-01-UI-V2-SELECTIVE-INTEGRATION — preflight (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 87 | Fatos Git, WIP, comparação de fontes e gates HOM-01 | CURRENT / preflight complete; implementation awaits DS adjudication |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.50 | Handoff e blockers de HOM-01 | CURRENT / no application files integrated |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 20 | Aceite funcional e visual de HOM-01 | CANONICAL / mandatory gates |
| `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md` | DS baseline and target adjudication | CURRENT / 2.4.0 recommended, adjudication pending |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`, seção 20 | Evidências de Design QA | CANONICAL / Inventory reference approval pending |

```text
TARGET_BRANCH = codex/hom-v1-integration
TARGET_HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
SOURCE_WIP_VERIFICATION = PASS / untracked items preserved
SOURCE_FILES_SELECTED = NONE
DS_ADJUDICATION = PASS / additive, route-scoped adoption; DS 2.0.2 remains canonical
FUNCTIONAL_REGRESSION = NOT_RUN
DESIGN_QA = BLOCKED
HUMAN_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / section 87
HOMOLOGATION_ENTRY_GATE = BLOCKED
```

## 56. ARGOS-HOM-01-DESIGN-QA-EVIDENCE-01 (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 89 | Registro desta tentativa, referências, bloqueio de renderização e gates | CURRENT / blocked by loopback socket permission |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.52 | Handoff e estado resumido | CURRENT / Design QA blocked |
| `docs/prototype/ui-v2/evidence/hom-01-visual-qa-2026-10-11/README.md` | Matriz de referências e evidências esperadas | CURRENT / renders not captured; Inventory approval conflict recorded |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`, seção 20 | Contrato normativo do gate visual HOM-01 | CANONICAL / mandatory |
| `C:/Users/walac/desenvolvimento/projeto_argos_ui_v2_p3_root/docs/prototype/ui-v2/screens/p3-a/coverage.md` | Aprovações e capturas P3-A | SOURCE WORKTREE / conflict for Inventory approval |
| `C:/Users/walac/desenvolvimento/projeto_argos_ui_p5/docs/prototype/ui-v2/evidence/screenshots/` | Capturas P5 de referência visual | SOURCE WORKTREE / not copied |

```text
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
SOURCE_WIP_PRESERVED = YES
RENDERED_SCREENSHOTS = NONE
INVENTORY_REFERENCE = CANDIDATE / approval status conflict unresolved; QUICK_DETAIL_REFERENCE_SCREENSHOT = MISSING
DESIGN_QA = BLOCKED
PROJECT_STATE_UPDATE = PASS / section 89
CONTINUITY_UPDATE = PASS / AGENT_CONTINUITY.md section 20.52 and this section
```

## 55. ARGOS-HOM-01-UI-V2-SELECTIVE-INTEGRATION — integração parcial (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 88 | Snapshot da integração, seleção de fontes, testes e bloqueios | CURRENT / partial implementation; Design QA and human approval pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.51 | Handoff HOM-01 | CURRENT / Shell, Dashboard and Inventory integrated; approval gates remain |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 20 | Aceite funcional e visual HOM-01 | CANONICAL / all required QA gates remain mandatory |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`, seção 20 | Contrato e evidências de Design QA | CANONICAL / Inventory reference approval and matching screenshots pending |
| `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md` | Baseline e adjudicação DS | CURRENT / DS 2.0.2 canonical; additive 2.4.0 authorized only for HOM-01 routes |

```text
TARGET_BRANCH = codex/hom-v1-integration
HEAD_BEFORE = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
HEAD_AFTER = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
SHELL = INTEGRATED / FUNCTIONALLY VALIDATED
DASHBOARD = INTEGRATED / FUNCTIONALLY VALIDATED / HUMAN APPROVAL PENDING
INVENTORY = INTEGRATED / FUNCTIONALLY VALIDATED / APPROVED REFERENCE PENDING
CAMERA_DETAIL = PRESERVED
QUICK_DETAIL = PRESERVED / LATEST_ACTIVE_IMAGE PENDING
DS_ADJUDICATION = PASS / DS 2.4.0 route-scoped; DS 2.0.2 remains canonical
FUNCTIONAL_REGRESSION = PASS / 77 TESTS
DESIGN_QA = BLOCKED / Inventory reference missing; matching render evidence and human approval pending
QA_TEMP_ARTIFACTS = hom01-qa-server.log; hom01-qa-server.err / OS-locked local request logs pending cleanup
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md section 88
CONTINUITY_UPDATE = PASS / AGENT_CONTINUITY.md section 20.51 and this section
HOMOLOGATION_ENTRY_GATE = BLOCKED
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED; MERGE = NOT_PERFORMED; DEPLOY = NOT_PERFORMED
```

## 57. ARGOS-HOM-01-HOST-VISUAL-QA-01 — bloqueio ambiental (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 90 | Tentativa no host, resultado, gates e estado do WIP | CURRENT / loopback blocked; no rendered screenshots |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.53 | Handoff e blockers de captura | CURRENT / HOM-01 remains IN_PROGRESS |
| `docs/prototype/ui-v2/evidence/hom-01-visual-qa-2026-10-11/README.md` | Tentativa no host e procedimento Windows reproduzível | CURRENT / render blocked; human approvals pending |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`, seção 20 | Contrato normativo de Design QA | CANONICAL / mandatory |
| `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md` | Baseline visual, viewport/condições equivalentes e gates | CURRENT / DS 2.0.2 canonical |

```text
ACTIVITY = ARGOS-HOM-01-HOST-VISUAL-QA-01
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
SOURCE_WIP_PRESERVED = YES
HOST_BROWSER_ACCESS = BLOCKED / loopback timeout
SYNTHETIC_DATABASE = CREATED, MIGRATED, SEEDED, THEN REMOVED
RENDERED_SCREENSHOTS = NONE
DESIGN_QA = BLOCKED
INVENTORY_HUMAN_APPROVAL = PENDING
QUICK_DETAIL_BASELINE_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / section 90
CONTINUITY_UPDATE = PASS / AGENT_CONTINUITY.md §20.53 and this section
HOMOLOGATION_GATE = BLOCKED
```

## 58. ARGOS-HOM-01-ONE-CLICK-RUNTIME-SETUP (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 91 | Resultado, validações e limites do launcher | CURRENT / static validation pass; runtime and browser not verified |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.54 | Handoff e instrução de retomada | CURRENT / HOM-01 remains IN_PROGRESS |
| `INICIAR_ARGOS_QA.cmd` | Entrada local de uso único | CURRENT / starts isolated QA and local server |
| `scripts/localqa/settings.py` | Settings exclusivo do QA local | CURRENT / loopback and dedicated SQLite |
| `scripts/localqa/prepare_qa.py` | Owner marker, migrations, existing identity provisioning and checks | CURRENT / refuses unrecognized database |
| `scripts/localqa/seed_qa.py` | Idempotent fictional camera data | CURRENT / five synthetic records |
| `scripts/localqa/start_argos_qa.ps1` | Python selection, port guard, HTTP wait and browser launch | CURRENT / not runtime-tested here |
| `docs/prototype/ui-v2/evidence/hom-01-visual-qa-2026-10-11/README.md` | Uso do launcher e status das evidências visuais | CURRENT / browser render pending |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção 20 | Gates de aceite HOM-01 | CANONICAL / unchanged |

```text
ACTIVITY = ARGOS-HOM-01-ONE-CLICK-RUNTIME-SETUP
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
SOURCE_WIP_PRESERVED = YES
QA_DATABASE = .local/qa/argos_visual_qa.sqlite3 / launcher-owned marker
QA_SEED = PASS / 5 records / idempotent
QA_USER = PASS / five minimum view/form permissions / non-admin
WINDOWS_RUNTIME_VERIFIED = NOT_VERIFIED
BROWSER_RENDER_VERIFIED = NOT_VERIFIED
DESIGN_QA = PENDING
HOMOLOGATION_GATE = BLOCKED
PROJECT_STATE_UPDATE = PASS / section 91
CONTINUITY_UPDATE = PASS / AGENT_CONTINUITY.md §20.54 and this section
```

## 59. ARGOS-HOM-01-CAMERA-DETAIL-APPROVED-FIXES-RECOVERY (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 92 | Implementação, regressão e gates atuais da Camera Detail | CURRENT / partial; implementation pass; visual blocked |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.55 | Handoff e próximo passo | CURRENT / HOM-01 remains in progress |
| `docs/prototype/ui-v2/contracts/STATE_MATRIX.md` | Tratamento visual atualizado de OUT_OF_SCOPE | CURRENT / Option A recorded |
| `docs/prototype/ui-v2/contracts/ARGOS_UI_V2_VISUAL_CONTRACT.md` | Decisão aprovada e limite DS 2.0.2 | CURRENT / Option A addendum; 2.4.0 not canonical |
| `docs/prototype/ui-v2/evidence/hom-01-camera-detail-recovery-2026-10-11/VISUAL_DIFFERENCE_REPORT.md` | Evidência de bloqueio visual e itens faltantes | CURRENT / blocked; screenshots unavailable |

```text
ACTIVITY = ARGOS-HOM-01-CAMERA-DETAIL-APPROVED-FIXES-RECOVERY
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
OUT_OF_SCOPE_PRESENTATION = OPTION_A / USER_APPROVED
DS_CANONICAL = 2.0.2
REGRESSION_TEST_TOTAL = 98 PASS
DESIGN_QA = BLOCKED
HUMAN_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / section 92
CONTINUITY_UPDATE = PASS / AGENT_CONTINUITY.md §20.55 and this section
HOMOLOGATION_GATE = BLOCKED
```

## 60. ARGOS-HOM-01-CAMERA-EDIT-RECOVERY (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 93 | Resultado técnico, regressões e gates pendentes | CURRENT / implementation pass; visual blocked |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.56 | Handoff e próximo passo de review | CURRENT / HOM-01 remains in progress |
| `cameras/templates/cameras/formulario.html` | Template SSR compartilhado de criação e edição | CURRENT / P3-D composition adapted to Django Forms |
| `cameras/templates/cameras/includes/campo_formulario_p3d.html` | Labels, required markers and linked field errors | CURRENT / camera forms only |
| `cameras/templates/cameras/includes/resumo_erros_formulario_p3d.html` | Django error summary with links to controls | CURRENT / camera forms only |
| `static/css/ui-v2/camera-form.css` | Route-specific adaptation using canonical DS 2.0.2 tokens/primitives | CURRENT / no global route changes |
| `cameras/test_camera_form_ui_recovery.py` | Render, field coverage, CSRF, permission and error-state checks | CURRENT / included in 177 passing tests |
| `docs/prototype/ui-v2/evidence/argos-hom-01-camera-edit-recovery-2026-10-11/VISUAL_DIFFERENCE_REPORT.md` | P3-D reference provenance, known adaptations and visual blocker | CURRENT / target render and human approval pending |
| `docs/prototype/ui-v2/evidence/argos-hom-01-camera-edit-recovery-2026-10-11/reference/` | 18 P3-D create/edit reference screenshots, hash-verified from P3 ROOT | CURRENT / reference only; no target captures |

```text
ACTIVITY = ARGOS-HOM-01-CAMERA-EDIT-RECOVERY
BRANCH = codex/hom-v1-integration
HEAD_BEFORE = HEAD_AFTER = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
P3_D_APPROVAL = f5dd0308f46705e03c79609077ed1ec7a12bc766
DS_CANONICAL = 2.0.2
DJANGO_CHECK = PASS
FUNCTIONAL_REGRESSION = PASS / 177 tests
REFERENCE_SCREENSHOTS = 18 / verified
TARGET_SCREENSHOTS = NONE
DESIGN_QA = BLOCKED
HUMAN_VISUAL_APPROVAL = PENDING
HOM_01_STATUS = IN_PROGRESS
COMMIT = NOT_PERFORMED; PUSH = NOT_PERFORMED; MERGE = NOT_PERFORMED; DEPLOY = NOT_PERFORMED
```

## 61. ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 94 | Resultado do provisionamento e testes | CURRENT / account and automated authorization PASS; Design QA blocked |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.57 | Handoff e estado resumido | CURRENT / HOM-01 remains IN_PROGRESS |
| `scripts/localqa/provisioning.py` | Validação sem escrita do perfil visual e seed controlado do operacional | CURRENT / refuses unmarked username collisions |
| `scripts/localqa/prepare_qa.py` | Isolamento, preflight, migrations, seed e provisionamento | CURRENT / visual account is never rewritten |
| `scripts/localqa/start_argos_qa.ps1` | Geração/exibição da senha operacional rotativa | CURRENT / terminal only, no persistence |
| `cameras/test_operational_qa_provisioning.py` | Provisionamento, autorização HTTP e produção/desativada | CURRENT / included in 101 passing tests |
| `scripts/localqa/test_settings.py` | Banco e mídia efêmeros sob `.local/qa/test-runs` | CURRENT / used for targeted regression |
| `docs/prototype/ui-v2/evidence/hom-01-visual-qa-2026-10-11/README.md` | Instrução de acesso dos dois perfis e evidência visual pendente | CURRENT |

```text
ACTIVITY = ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING
BRANCH = codex/hom-v1-integration
HEAD = d1fd9491692afb57da9dcfe0a27964efdb2d19e0
VISUAL_QA_USER = PRESERVED / password hash unchanged
OPERATIONAL_QA_USER = CREATED / exactly seven permissions / password rotates per launcher run
TARGETED_TESTS = 101 PASS
DESIGN_QA = BLOCKED / no rendered captures
HUMAN_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = PASS / section 94
CONTINUITY_UPDATE = PASS / AGENT_CONTINUITY.md §20.57 and this section
HOMOLOGATION_GATE = BLOCKED
```

## 62. ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING — aprovação do botão de upload (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 95 | Checkpoint informado pelo usuário, aprovação visual do botão e critérios ainda pendentes | CURRENT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, seção 20.58 | Handoff do QA operacional após validação visual restrita | CURRENT / HOM-01 remains in progress |

```text
ACTIVITY = ARGOS-HOM-01-OPERATIONAL-QA-PROVISIONING
OPERATIONAL_QA_USER = qa-operacional-hom01
OPERATIONAL_QA_PERMISSION_VALIDATION = PASS / user-reported
UPLOAD_BUTTON_RENDERING = PASS
UPLOAD_BUTTON_HUMAN_VISUAL_APPROVAL = APPROVED / button rendering only
BROWSER_UPLOAD_SUBMISSION = NOT_VERIFIED
RESPONSIVE_QA = PENDING
KEYBOARD_FOCUS_QA = PENDING
PROVISIONING = NOT_REPEATED
CODE_AND_PERMISSIONS = PRESERVED
HOM_01_STATUS = IN_PROGRESS
HOMOLOGATION_GATE = BLOCKED
```

## 63. ARGOS-HOM-01-FINAL-BASELINE-CHECKPOINT (2026-10-11)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md` | Baseline integrada, classificação Git, gates, aceite visual e manifesto | CURRENT / `188afda`; HOM-01 remains IN_PROGRESS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §96 | Snapshot técnico e próximos gates | CURRENT / PROJECT_STATE_UPDATE PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.59 | Handoff para retomada | CURRENT / publication and HOM-02 blocked |
| `docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`, §13 | Política `ARGOS-RECONCILE-BEFORE-BRANCH` | CANONICAL / user approved; default branch creation blocked |
| `docs/prototype/ui-v2/evidence/hom-01-visual-qa-2026-10-11/README.md` | Runbook e limitações de captura humana | CURRENT / integrated screenshots pending |

```text
ACTIVITY = ARGOS-HOM-01-FINAL-BASELINE-CHECKPOINT
CODE_BASELINE = 188afda5470e252fa8cf6fed5556a404073ee4fc
DOCUMENT_CHECKPOINT_COMMIT = 6e3550077bf682a11889f3a554875c62d115ee00
TECHNICAL_GATE = FAIL / directed suites 405/406, global run inconclusive
VISUAL_GATE = BLOCKED / partial human approvals, integrated evidence pending
GIT_RECONCILIATION_GATE = PARTIAL / external worktree WIP inaccessible
PUBLISH_READY = NO
LIVE_REMOTE_LOOKUP = BLOCKED / DNS
HOM01_STATUS = IN_PROGRESS
HOM02_START_AUTHORIZATION = NOT_GRANTED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §96
```

## 64. ARGOS-HOM-01-INVENTORY-UNKNOWN-PRESENTATION-FIX (2026-10-12)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §98 | Implementação da nomenclatura e evidência de testes | CURRENT / 82 targeted PASS; visual review pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.61 | Handoff da correção e blocker de render integrado | CURRENT / HOM-01 remains IN_PROGRESS |
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, §10 | Follow-up do checkpoint HOM-01 | CURRENT / no human visual approval inferred |
| `cameras/monitoramento/presentation.py` | Mapeamento compartilhado para estados efetivos | CURRENT / ONLINE, OFFLINE, UNKNOWN, OUT_OF_SCOPE |
| `cameras/test_monitoramento_ui.py` | Verificação dos rótulos, stale e fora de escopo | CURRENT / included in 82 passing tests |
| `C:\Users\walac\.codex\visualizations\2026\10\12\01a1317f-9dc2-73a1-8c9a-d85e80e64126\evidence\CURRENT\ARGOS_INVENTARIO_CURRENT_1366x768.png` | Captura integrada previamente recuperada | PARTIAL / only physical CURRENT screenshot; reference P3-A is separate |
| `C:\Users\walac\.codex\visualizations\2026\10\12\01a1317f-9dc2-73a1-8c9a-d85e80e64126\evidence\VISUAL_DIFFERENCE_REPORT.md` | Proveniência das capturas e findings | CURRENT / human approval pending |

```text
ACTIVITY = ARGOS-HOM-01-INVENTORY-UNKNOWN-PRESENTATION-FIX
TARGETED_TESTS = 82 PASS
HUMAN_VISUAL_APPROVAL = PENDING
DESIGN_QA = PENDING
HOM_01_STATUS = IN_PROGRESS
PROJECT_STATE_UPDATE = PASS / section 98
```

## 65. ARGOS-HOM-01-DIAGNOSTIC-A-D-LABEL-RECONCILIATION (2026-10-12)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §99 | Investigação, mapeamentos, testes e renderização desktop/mobile | CURRENT / 65 targeted PASS; bounded A–D approval recorded |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.62 | Handoff da localização e validação do diagnóstico A–D | CURRENT / visual render PASS |
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, §11 | Follow-up do checkpoint HOM-01 | CURRENT / bounded A–D approval recorded; broader Design QA pending |
| `cameras/monitoramento/presentation.py` | Rótulos de apresentação para a projeção de saúde | CURRENT / UNKNOWN separado dos estados MON |
| `cameras/templates/cameras/detalhe.html` | Exibição localizada de Evidência automática e Frescor | CURRENT / rendered in integrated Edge at desktop and mobile |
| `cameras/test_monitoramento_ui.py` | Cobertura de todos os valores da projeção e da linha de estado confirmado | CURRENT / included in 65 passing tests |

```text
ACTIVITY = ARGOS-HOM-01-DIAGNOSTIC-A-D-LABEL-RECONCILIATION
EVIDENCE_UNKNOWN_LABEL = Não determinada
FRESHNESS_UNKNOWN_LABEL = Não determinado
INTERNAL_CODES_AND_CONTRACTS = PRESERVED
TARGETED_TESTS = 65 PASS
DJANGO_CHECK = PASS
GIT_DIFF_CHECK = PASS
INTEGRATED_RENDER = PASS / actual Django Camera Detail reloaded by user
VISUAL_VIEWPORTS = PASS / 1366x768 and 390x844; Edge; zoom 100%; DPR 1
MOBILE_PAGE_OVERFLOW = NO / navigation scroll stays within its component
SCREENSHOT_FILES = NONE / inline capture only
HUMAN_APPROVAL = APPROVED / bounded A–D labels and UNKNOWN last-confirmed-row behavior at 1366x768 and 390x844 only; user reply: “certo”
DESIGN_QA = PENDING / broader HOM-01 gates remain
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / section 99
```

## 66. ARGOS-HOM-01-INVENTORY-VISUAL-ACCEPTANCE (2026-10-12)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §100 | Registro do aceite da composição e do finding de cabeçalho | CURRENT / composition approved; viewport-specific approval not inferred |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.63 | Continuidade do aceite visual do Inventário | CURRENT / known 1366px header-wrap finding remains open |
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, §12 | Checkpoint documental HOM-01 | CURRENT / Inventory composition accepted |

```text
ACTIVITY = ARGOS-HOM-01-INVENTORY-VISUAL-ACCEPTANCE
USER_FEEDBACK = “O inventário para mim está legal.”
INVENTORY_HUMAN_VISUAL_APPROVAL = APPROVED / integrated composition
VIEWPORT_APPROVAL_SCOPE = COMPOSITION_LEVEL / individual viewport approval not inferred
KNOWN_HEADER_WRAP_FINDING = OPEN / MONITORAMENTO at 1366px; cross-viewport resolution not established
CODE_CHANGED = NO / this activity
WIP_PRESERVED = YES
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / section 100
```

## 67. HOM-01-DASHBOARD-V7-VISUAL-CONFORMANCE-RECOVERY (2026-10-12)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §103 | Causas, alterações, validação e estado de aceite | CURRENT / visual QA partial; human approval pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.65 | Retomada e limites da atividade | CURRENT / HOM-01 remains IN_PROGRESS |
| `core/templates/core/dashboard.html` | Composição da atividade recente em uma superfície | CURRENT / two internal panels retained |
| `static/css/dashboard-v7.css` | Geometria responsiva do Dashboard V7 | CURRENT / desktop and mobile matrix inspected |
| `core/test_frontend.py` | Asserções estruturais da atividade recente | CURRENT / included in 88 passing targeted tests |

```text
ACTIVITY = HOM-01-DASHBOARD-V7-VISUAL-CONFORMANCE-RECOVERY
VIEWPORTS = 1920x1080; 1440x900; 1366x768; 390x844
DJANGO_CHECK = PASS
TARGETED_TESTS = 88 PASS
HUMAN_VISUAL_APPROVAL = PENDING
ACTIVITY_COMPLETE = NO
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / section 103
```

## 68. HOM-01-DASHBOARD-V7-FIDELITY-ROUND-2 (2026-10-12)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §104 | Findings, alterações, capturas e gates | CURRENT / integrated captures and tests recorded; human approval pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.66 | Handoff da rodada 2 | CURRENT / HOM-01 remains IN_PROGRESS |
| `docs/prototype/new_ui_dashboard/handoff/VISUAL_CONTRACT_V7.md`, §4 | Precedência das nomenclaturas do Dashboard | CANONICAL / later approved title protected |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_1440x900.png` | Captura principal integrada desktop | CURRENT / exact 1440x900, DPR 1, zoom 100% |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_1440x900_ATIVIDADE.jpg` | Captura suplementar da atividade desktop | CURRENT / 1440x900; all five camera rows and activity retained |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_390x844.png` | Captura principal integrada mobile | CURRENT / exact 390x844, DPR 1, zoom 100%, no horizontal overflow |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_390x844_MONITORAMENTO.png` | Detalhe da faixa de frescor mobile | CURRENT / exact 390x844 |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_390x844_ATIVIDADE.jpg` | Captura suplementar da atividade mobile | CURRENT / 375x812 crop from 390x844 viewport; all five camera rows and activity retained |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_CADASTRO_1440x900.png` | Captura da ação e formulário de cadastro | CURRENT / 1440x900; create action visible; GET form loaded without submission |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_LINKS_1440x900.jpg` | Captura dos links “Ver câmeras” | CURRENT / exact 1440x900; production, stock and deactivated filters |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_LINKS_390x844.jpg` | Captura mobile dos links “Ver câmeras” | CURRENT / 375x812 crop from 390x844 viewport; all three links visible |
| `http://127.0.0.1:8768/dashboard/` | Prévia local para revisar ação/formulário de cadastro condicionado por permissão | CURRENT / isolated cloned SQLite; original read-only QA profile preserved; no form submission |

```text
ACTIVITY = HOM-01-DASHBOARD-V7-FIDELITY-ROUND-2
F01_F02_F03_F05_F06_F07 = FIXED / see PROJECT_STATE §104
F04 = PARTIAL_BY_AUTHORITY / later approved monitoring title preserved; V7 aside restored
DJANGO_CHECK = PASS
TARGETED_TESTS = 88 PASS
VISUAL_CAPTURE = PASS / integrated desktop and mobile files listed above
PIXEL_DIFF = NOT_PRODUCED
FULL_PAGE_CAPTURE = NOT_PRODUCED
ROLE_ROUTING = ROOT: analysis/diagnosis/reconciliation/review; MECHANICAL: code; SCRIBE: documentary materialization
RUNTIME_REVIEW = PASS / old :8767 listener stopped; new :8768 preview showed “Nova Câmera” and opened the registration form without submission; five synthetic cameras retained
CADASTRO_CAPTURE = CAPTURED / DASHBOARD_CADASTRO_1440x900.png; viewport 1440x900; no overflow; no submission
QUICK_LINKS = PASS / three auxiliary “Ver câmeras” links restored for PRODUCAO, ESTOQUE and DESATIVADA; numeric links/values retained; no clipping or overflow at desktop/mobile
HUMAN_VISUAL_APPROVAL = PENDING
ACTIVITY_COMPLETE = NO
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / section 104
```

## 69. HOM-01-DASHBOARD-V7-FIDELITY-ROUND-2 — aprovação e stage/commit autorizado (2026-10-12)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §105 | Registro da aprovação, encerramento limitado e autorização Git | CURRENT / bounded Dashboard activity approved; Git operation pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.67 | Handoff da aprovação e limites do commit autorizado | CURRENT / HOM-01 remains IN_PROGRESS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`, §69 | Este mapa | CURRENT |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_1440x900.png` | Composição principal integrada | APPROVED / composition-level capture |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_CADASTRO_1440x900.png` | Ação Nova Câmera e formulário GET | APPROVED / shown without submission |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_LINKS_1440x900.jpg` | Links de Produção, Estoque e Desativadas | APPROVED / category shortcuts visible |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_TOTAL_REGISTRADO.jpg` | Caption e contadores do Inventário | APPROVED / support text and values visible |
| `C:/Users/walac/.codex/visualizations/2026/10/12/01a1326d-bc56-7602-beca-3c0751a5db43/evidence/dashboard-v7-round2/DASHBOARD_390x844.png` | Composição principal mobile | Included in composition-level presentation; individual viewport acceptance not inferred |

```text
ACTIVITY = HOM-01-DASHBOARD-V7-FIDELITY-ROUND-2
USER_APPROVAL = APPROVED / “perfeito autorizo stage e commit”
APPROVAL_SCOPE = Dashboard V7 integrated composition, latest captures; not independent approval of every requested viewport
DASHBOARD_ACTIVITY_COMPLETE = YES / bounded activity
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
COMMIT_AUTHORIZED = YES
COMMIT_STAGE = PREPARED / root to inspect bounded index and pre-commit Git snapshot
COMMIT_REFERENCE = PENDING / resolve actual commit using Git after execution
PUSH_AUTHORIZED = NO
PROJECT_STATE_UPDATE = PASS / section 105
```

## 70. HOM-01-SAFE-CHECKPOINT-AND-PUSH (2026-10-13)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §106 | Estado Git publicado, resultados de validação, aprovações e instruções cross-PC | CURRENT / checkpoint published; HOM-01 remains in progress |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Resumo atual de retomada | CURRENT / aponta para §106 e registra a branch publicada |
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, §14 | Resumo de continuidade HOM-01 e limites dos aceites | CURRENT / no HOM-01 closure |
| `docs/projeto/ARGOS_HOM_01_SIDEBAR_ACTIVE_STATE_RECOVERY.md` | Causa, correção, aprovações e evidências da sidebar | CURRENT / accepted desktop scope |
| `docs/projeto/evidence/sidebar-active-recovery/` | Capturas integradas e estilos computados das cinco páginas | CURRENT / synthetic QA; 2552x866 CSS px desktop |
| `https://github.com/wromanov/projeto_argos/tree/codex/hom-v1-integration` | Checkout remoto de continuidade para outro computador | CURRENT / branch published and SHA verified against local HEAD |

```text
ACTIVITY = HOM-01-SAFE-CHECKPOINT-AND-PUSH
BRANCH = codex/hom-v1-integration
V7_COMMIT = b122ece404c3b67afdbd1acf9087e340d1c07d2c / preserved
IMPLEMENTATION_COMMITS = 7c4fac3a81ba6311ecaf9bad2e080240759cfd0c; d0b4c2f5bef8d4533834898a67e4d2f03b0e2d1e
TEST_HARDENING_COMMIT = db0b10bc2a11ec6a20b8b8f9b36ba43573919814
TARGETED_TESTS = 105 PASS / six modules; isolated temporary SQLite
DJANGO_CHECK = PASS
REMOTE_BRANCH = origin/codex/hom-v1-integration
PUSH = NORMAL / SHA equality verified after publication
WORKTREE = CLEAN / index empty / no relevant untracked files
DASHBOARD_V7_OVERALL_HUMAN_APPROVAL = PENDING / composition-level approval in PROJECT_STATE §105 remains valid
SIDEBAR_DESKTOP_APPROVAL = PASS / five pages; no responsive approval inferred
OPEN_FINDING = Inventory MONITORAMENTO header wrap at 1366px
HOM_01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §106
```

Para a recuperação em outra máquina, leia primeiro `PROJECT_STATE.md` §106,
inspecione origem, worktree, branch e ancestralidade antes do checkout/fast-
forward e recrie localmente o ambiente `.venv`/`.local/qa`. Não copie
configuração, banco, sessão ou credenciais do computador de origem.

## 71. HOM-01-WORK-PC-QA-BOOTSTRAP-CLOSURE (2026-10-13)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §107 | Fechamento factual da recuperação QA no computador do trabalho e estado de HOM-01 | CURRENT / work environment prepared; HOM-01 remains in progress |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Ponto de retomada e instruções de handoff | CURRENT / points to PROJECT_STATE §107 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`, §71 | Este índice de continuidade | CURRENT |

```text
ACTIVITY = HOM-01-WORK-PC-QA-BOOTSTRAP-CLOSURE
WORK_PC_RECOVERY = COMPLETE
QA_ENVIRONMENT = PREPARED / isolated local environment
DASHBOARD_V7_VISUAL_QA = PENDING
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §107
```

## 72. HOM-01-DASHBOARD-V7-VISUAL-ACCEPTANCE (2026-10-13)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §108 | Registro do aceite visual humano e escopo da atividade | CURRENT / four approved viewports; HOM-01 remains in progress |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.68 | Handoff, restrições visuais e estado de HOM-01 | CURRENT / preserve V7; no repeat audit |
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, §15 | Checkpoint de aceite do Dashboard V7 | CURRENT / bounded visual acceptance |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/REPORT.md` | Capturas e métricas da inspeção integrada | CURRENT / user approval appended; DPR 0.9; zoom unverified |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/current-1920x1080.png` | Captura integrada aprovada | APPROVED / user visual acceptance |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/current-1440x900.png` | Captura integrada aprovada | APPROVED / user visual acceptance |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/current-1366x768.png` | Captura integrada aprovada | APPROVED / user visual acceptance |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/current-390x844.png` | Captura integrada aprovada | APPROVED / user visual acceptance |

```text
ACTIVITY = HOM-01-DASHBOARD-V7-VISUAL-ACCEPTANCE
APPROVED_VIEWPORTS = 1920x1080, 1440x900, 1366x768, 390x844
DPR_OBSERVED = 0.9
ZOOM_100_PERCENT = NOT_VERIFIED
PIXEL_PERFECT_COMPARISON = NOT_CLAIMED
SOURCE_CODE_CHANGE = NO
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §108
```

## 73. HOM-01-CAMERA-DETAIL-RESIDUAL-QA-CLOSURE (2026-10-13)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §109 | Resultado factual da revisão residual e disposição humana | CURRENT / closed with accepted limitations; no material regression proven |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.69 | Handoff, aceites anteriores, limitações e estado dos gates | CURRENT / prior approvals preserved; global QA not passed |
| `docs/projeto/evidence/camera-detail-residual-qa/REPORT.md` | Inventário de evidências, matriz residual e findings | CURRENT / accepted limitations; no Camera Detail captures |

```text
ACTIVITY = HOM-01-CAMERA-DETAIL-RESIDUAL-QA-CLOSURE
CAPTURES_FOUND = NO
CAMERA_DETAIL_PRIOR_APPROVAL = PRESERVED
RESIDUAL_QA_STATUS = CLOSED_WITH_LIMITATIONS
HUMAN_LIMITATION_ACCEPTANCE = APPROVED
NOT_VERIFIED = four viewports; keyboard/focus; current rendering by profile; full P5 visual comparison
DESIGN_QA_GLOBAL = NOT_DECLARED_PASS
P1_FINDINGS = NONE_PROVEN
P2_FINDINGS = NONE_PROVEN
P3_FINDINGS = NONE_PROVEN
HOM01_STATUS = IN_PROGRESS
HOM02_START = BLOCKED
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §109
```

## 74. HOM-01-FINAL-CLOSURE (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §111 | Consolidação dos aceites e resultado anterior da regressão sob sandbox | HISTORICAL / superseded by §112 for current regression status |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.70 | Resumo anterior de retomada e bloqueio | HISTORICAL / superseded by §20.71 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`, §74 | Este índice de continuidade | HISTORICAL / superseded by §75 |
| `docs/projeto/evidence/camera-detail-residual-qa/REPORT.md` | Limitações aceitas da Camera Detail | PRESERVED / closed with limitations; not reopened |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/REPORT.md` | Escopo e evidências do aceite Dashboard V7 | PRESERVED / visual QA not repeated |

```text
ACTIVITY = HOM-01-FINAL-CLOSURE
GLOBAL_DJANGO_REGRESSION = FAIL / 948 tests; 42 errors; Django system check PASS
REGRESSION_RERUN = NO / single run
OBSERVED_BLOCKER = WinError 5 while creating/cleaning temporary media directories under .local/qa/test-runs
HOM01_READY = NO
HOM01_STATUS = IN_PROGRESS
HOM02_READINESS = BLOCKED
CLOSURE_RECOMMENDATION = HOLD until a passing global regression
VISUAL_QA_REPEATED = NO
ACCEPTED_LIMITATIONS = PRESERVED / PROJECT_STATE.md §§108–109
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §111 (historical; current state in §112)
```

## 75. HOM-01-REGRESSION-UNBLOCK (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §112 | Causa ambiental, remediação, regressão consolidada e decisão técnica de prontidão | CURRENT / regression PASS; HOM-01 ready for user approval |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.71 | Handoff atual, causa, resultado e limites de autorização | CURRENT / points to §112 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md`, §75 | Este índice de continuidade | CURRENT |
| `docs/projeto/evidence/camera-detail-residual-qa/REPORT.md` | Limitações aceitas da Camera Detail | PRESERVED / closed with limitations; not reopened |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/REPORT.md` | Escopo e evidências do aceite Dashboard V7 | PRESERVED / visual QA not repeated |

```text
ACTIVITY = HOM-01-REGRESSION-UNBLOCK
ENVIRONMENT_ISSUE = YES / sandbox filesystem ACL for nested temporary paths
ERRORS_ROOT_CAUSE = ENVIRONMENTAL / WinError 5 creating/cleaning nested temporary directories
REMEDIATION = one global regression run with filesystem access outside sandbox restriction; no code/config edits
REGRESSION_RESULT = PASS / 948 tests; OK; Django system check PASS
REMAINING_MATERIAL_BLOCKERS = NONE / HOM-01 technical regression
HOM01_READY = YES / recommend technical closure for user approval
HOM01_STATUS = READY_FOR_USER_APPROVAL / formal closure subject to user authority
HOM02_READINESS = BLOCKED / no HOM-02 authorization
VISUAL_QA_REPEATED = NO
ACCEPTED_LIMITATIONS = PRESERVED / PROJECT_STATE.md §§108–109
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md §112
```

## 76. HOM-01-CLOSE-AND-HOM02-PREPARATION — encerramento aprovado (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §113 | Aprovação humana e registro formal de fechamento HOM-01 | CURRENT / CLOSED; regression PASS 948 tests; no material blockers |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.72 | Handoff do fechamento e preservação das limitações | CURRENT / HOM-01 closed; prior acceptances preserved |
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, §16 | Checkpoint de fechamento da HOM-01 e abertura preparatória HOM-02 | CURRENT / closure approved; no QA repeated |
| `docs/projeto/evidence/dashboard-v7-integrated-qa/REPORT.md` | Escopo/evidência do aceite Dashboard V7 | PRESERVED / limitations in PROJECT_STATE §108 |
| `docs/projeto/evidence/camera-detail-residual-qa/REPORT.md` | Limitações aceitas de Camera Detail | PRESERVED / CLOSED_WITH_LIMITATIONS per PROJECT_STATE §109 |

```text
HOM01_FORMAL_CLOSURE = APPROVED
HOM01_STATUS = CLOSED
GLOBAL_REGRESSION = PASS / 948 tests / 600.522s
MATERIAL_BLOCKERS = NONE
VISUAL_QA_REPEATED = NO
```

## 77. HOM-02-XLSX-IMPORT-PREPARATION (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/projeto/HOM_02_XLSX_IMPORT_PREPARATION.md` | Proposta funcional, decisões já aprovadas, questões abertas, defaults recomendados e critérios propostos | CURRENT / preparation authorized; implementation not authorized |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção HOM-02 | Decisões-base e gates já aprovados | CANONICAL / reuse; schema/template and homologation pending |
| `docs/projeto/HOM_01_UI_V2_BASELINE_CHECKPOINT.md`, §16 | Handoff de fechamento HOM-01 e autorização apenas preparatória HOM-02 | CURRENT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §114 | Estado da preparação e fronteira de autorização | CURRENT / decisions pending; no implementation authority |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.73 | Próximo handoff da proposta HOM-02 | CURRENT / implementation not yet authorized |

A proposta separa aceites existentes de decisões funcionais abertas. Defaults
recomendados não representam aprovação. Reutilizar shell/componentes existentes;
nenhum redesenho, alteração de MON Runtime ou implementação fica autorizado por
este registro.

## 78. HOM-02-XLSX-IMPORT-IMPLEMENTATION (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §115 | Snapshot de implementação, evidências, validações e status de aceitação | CURRENT / implementation technically complete; human acceptance pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.74 | Handoff atualizado; §20.73 passa a histórico | CURRENT |
| `docs/projeto/HOM_02_XLSX_IMPORT_PREPARATION.md`, adendo de implementação | Registro da autorização que resolveu decisões abertas e da entrega | CURRENT / preparation history preserved |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, seção HOM-02 | Status do item de sprint e evidências técnicas | CANONICAL / implemented; human acceptance pending |
| `cameras/xlsx_import.py`, `cameras/views.py`, `cameras/urls.py` | Parser, template, matching, preview, confirmação, autorização e transação | IMPLEMENTATION |
| `cameras/models.py`, `cameras/migrations/0019_alter_camera_options_cameraimportpreview.py` | Permissão de importação e armazenamento da prévia expirada/consumida | IMPLEMENTATION |
| `cameras/templates/cameras/importacao.html`, `importacao_resultado.html`, `cameras/templates/cameras/lista.html` | SSR de envio, prévia, resultado e entrada no Inventário | IMPLEMENTATION / existing Design System reused |
| `cameras/test_xlsx_import.py` | Cobertura funcional, integração SSR, parser/template, rollback e escala 2.300 | VALIDATION / PASS |

```text
HOM01_STATUS = CLOSED
HOM02_IMPLEMENTATION = IMPLEMENTED / TECHNICAL VALIDATION PASS
HOM02_HUMAN_ACCEPTANCE = PENDING
MON_RUNTIME_CHANGED = NO
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
DEPLOY = NOT_PERFORMED
```

## 79. HOM-02-HUMAN-ACCEPTANCE — preparação local (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §116 | Estado do QA local, usuário, artefatos e fronteira sem confirmação | CURRENT / QA running locally; human acceptance pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.75 | Handoff operacional para a validação humana | CURRENT |
| `.local/qa/argos-template-importacao-cameras-v1.xlsx` | Template oficial v1 gerado pelo produtor da aplicação | LOCAL / ignored by Git |
| `.local/qa/argos-exemplo-importacao-create-update.xlsx` | Exemplo sintético com uma linha CREATE e uma linha UPDATE | LOCAL / ignored by Git; no preview or confirmation |

```text
QA_URL = http://127.0.0.1:8765/cameras/importacao/
OPERATIONAL_USER = qa-operacional-hom01
OPERATIONAL_PERMISSIONS = view_camera + importar_cameras + add_camera + change_camera
SYNTHETIC_CAMERA_COUNT = 5 / preserved
IMPORT_CONFIRMATION = NOT_EXECUTED
HOM02_HUMAN_ACCEPTANCE = PENDING
CODE_CHANGED = NO
TESTS_OR_AUDITS_REPEATED = NO
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §116 and continuity pointers updated
```

## 80. HOM-02-XLSX-UI-CONFORMANCE-FIX (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §117 | Causa raiz, arquivos, checks e limites da conferência integrada | CURRENT / visual fix implemented; authenticated desktop/mobile review pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.76 | Handoff para autenticação e revisão visual humana | CURRENT |
| `templates/base.html`, `templates/components/sidebar.html`, `templates/components/navegacao_principal.html` | Gate da variante compartilhada do shell somente para rotas XLSX | IMPLEMENTATION / Dashboard e Inventário preservados |
| `cameras/templates/cameras/importacao.html`, `importacao_resultado.html` | Breadcrumb, ações, upload, resumo, prévia e resultado com componentes ARGOS | IMPLEMENTATION / fluxo preservado |
| `static/css/importacao-xlsx.css` | Espaçamentos e adaptação responsiva local com tokens existentes | IMPLEMENTATION |
| `cameras/test_xlsx_import.py` | Fluxo direcionado XLSX | VALIDATION / 13 tests PASS; unchanged by this activity |

```text
ROOT_CAUSE = XLSX routes omitted from shared UI V2 shell gate
IMPORTER_LOGIC_CHANGED = NO
DJANGO_SYSTEM_CHECK = PASS
TARGETED_XLSX_TESTS = PASS / 13
GIT_DIFF_CHECK = PASS
AUTHENTICATED_DESKTOP_SCREEN = PENDING / reauthentication required
MOBILE_VIEWPORT = PENDING / authenticated review required
IMPORT_CONFIRMATION = NOT_EXECUTED
HOM02_HUMAN_ACCEPTANCE = PENDING
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §117 and continuity pointers updated
```

## 81. HOM-02-XLSX-FORM-COMPACTNESS (2026-10-14)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §118 | Evidência e estado do ajuste de largura/altura do upload | CURRENT / targeted checks pass; human acceptance pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.77 | Handoff do CSS e validação direcionada | CURRENT |
| `static/css/importacao-xlsx.css` | Larguras compactas desktop, altura do seletor, gaps e regras mobile | IMPLEMENTATION |
| `cameras/templates/cameras/importacao.html` | Parâmetro de versão para atualizar o CSS em cache | PRESENTATION / stylesheet link only; form markup unchanged |
| `cameras/test_xlsx_import.py` | Upload, preview e comportamento funcional XLSX | VALIDATION / 13 tests PASS; unchanged |

```text
CARD_MAX_WIDTH = 800px / left aligned
FILE_INPUT_MAX_WIDTH = 560px / 44px height
RESPONSIVE_RESULT = CSS_RULE_VERIFIED / 100% widths at max-width 680px; no mobile viewport capture
FUNCTIONAL_RESULT = PASS / targeted XLSX tests
DJANGO_SYSTEM_CHECK = PASS
GIT_DIFF_CHECK = PASS
HOM02_HUMAN_ACCEPTANCE = PENDING
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §118 and continuity pointers updated
```

## 82. HOM-02-XLSX-IMPORT-UPLOAD-FIELD-VERTICAL-ALIGNMENT (2026-10-15)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §119 | Implementação, checks e limite da confirmação visual | CURRENT / code and tests PASS; integrated visual pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.78 | Handoff e limites de validação | CURRENT |
| `static/css/importacao-xlsx.css` | Alinhamento vertical local do campo nativo XLSX | IMPLEMENTATION / `#id_arquivo` only |
| `cameras/templates/cameras/importacao.html` | Versão de cache da folha XLSX | PRESENTATION / stylesheet query only |
| `cameras/test_xlsx_import.py` | Fluxo de upload e prévia | VALIDATION / 13 tests PASS; unchanged |

```text
CARD_MAX_WIDTH = 800px / preserved
FILE_INPUT_MAX_WIDTH = 560px / preserved
FILE_INPUT_HEIGHT = 44px / preserved
VERTICAL_ALIGNMENT = CSS_RULES_APPLIED / integrated visual pending authenticated session
DJANGO_SYSTEM_CHECK = PASS
TARGETED_XLSX_TESTS = PASS / 13
FUNCTIONAL_RESULT = PASS / no importer logic changed
HOM02_HUMAN_ACCEPTANCE = PENDING
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §119 and continuity pointers updated
```

## 83. HOM-03-POSTGRESQL-INTEGRATION (2026-10-15)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §120 | Escopo entregue, checks locais e limites de validação da VM | CURRENT / config slice implemented; real PostgreSQL and filesystem permissions pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.79 | Handoff da configuração e validações restantes | CURRENT |
| `config/settings_homologation.py` | Perfil seguro de homologação com PostgreSQL, logs, mídia e estáticos em `/dados/argos` | IMPLEMENTATION |
| `env.homologation.example` | Nomes e valores não secretos das variáveis do serviço | EXAMPLE / secrets omitted |
| `docs/seguranca/CONFIGURACAO_DE_AMBIENTES.md` | Provisionamento de diretórios, variáveis e comandos de validação/estáticos | OPERATIONAL DOCUMENTATION |
| `requirements.txt` | Driver Psycopg 3.3.6 | DEPENDENCY |

```text
DEVELOPMENT_SQLITE = PRESERVED
WSGI_ENV_SELECTION = PASS
DJANGO_CHECK = PASS / SQLite profile
PSYCOPG_LOCAL = ABSENT
VM_POSTGRESQL_CONNECTION = NOT_TESTED
VM_FILESYSTEM_PERMISSIONS = NOT_TESTED
MIGRATIONS_ON_VM = NOT_RUN
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §120 and continuity pointers updated
ACTIVITY_COMPLETE = NO / external environment checks pending
```

## 84. HOM-03-POSTGRESQL-VM-VALIDATION (2026-10-15)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §121 | Tentativa de acesso, dependências, payload e bloqueios de VM | CURRENT / blocked pending SSH key; no remote changes |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.80 | Handoff de retomada após chave autorizada disponível | CURRENT |
| `.local/hom03-transfer-20261015/argos-hom03-postgresql-transfer.zip` | Payload seletivo de settings/dependencies e checksums | READY / ignored by Git; no secrets/databases/WIP |
| `requirements.txt` | Psycopg C implementation on Linux and binary implementation on Windows | IMPLEMENTATION / platform markers validated |

```text
SSH_TARGET = [PRIVATE_VM_ENDPOINT_REDACTED]
SSH_AUTHENTICATION = BLOCKED / no authorized key available in session
VM_FILE_CHANGES = NONE
SYSTEMD_ENVIRONMENT = NOT_CONFIGURED
SERVICE_ACCOUNT_PERMISSIONS = NOT_VERIFIED
POSTGRESQL_CONNECTION = NOT_TESTED
DJANGO_CHECK_ON_VM = NOT_RUN
MIGRATION_PLAN_ON_VM = NOT_VERIFIED / none executed
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §121 and continuity pointers updated
ACTIVITY_COMPLETE = NO
```

## 85. HOM-03-SSH-LOGIN-HELPER (2026-10-15)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §122 | Helper de login interativo sem persistência de credenciais | CURRENT / script syntax PASS; not executed |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.81 | Uso do helper e limites de autenticação | CURRENT |
| `.local/hom03-transfer-20261015/login_vm.py` | Inicia OpenSSH interativo para `[PRIVATE_VM_ENDPOINT_REDACTED]`; sem senha/chave no código | LOCAL / ignored by Git; no credentials saved |

```text
SSH_HELPER = READY
SSH_EXECUTION = NOT_RUN
SECRET_PERSISTENCE = NO
VM_CHANGES = NONE
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §122 and continuity pointers updated
ACTIVITY_COMPLETE = NO / SSH access remains blocked
```

## 86. HOM-02-XLSX-UPDATE-PREVIEW-FIX (2026-10-15)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §123 | Correção da prévia, testes isolados e limites da atividade | CURRENT / bounded fix complete; HOM-02 human acceptance remains pending |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.82 | Handoff e validações da correção | CURRENT |
| `cameras/xlsx_import.py` | Snapshot original antes do ModelForm para diff e identificação | IMPLEMENTATION |
| `cameras/test_xlsx_import.py` | Casos de UPDATE renomeado, sem mudança e auditoria persistida | TESTS |

```text
UPDATE_RENAME_PREVIEW = PASS
UNCHANGED_UPDATE_PREVIEW = PASS
CREATE_MATCHING_CONFLICTS_ROLLBACK_AUDIT = PASS
TARGETED_XLSX_TESTS = PASS / 14
RELATED_REGRESSION = PASS / 31
TEST_DATABASE = SQLITE_IN_MEMORY / DESTROYED_AFTER_TESTS
VM_POSTGRESQL = NOT_ACCESSED
EXISTING_PREVIEW = NOT_CONFIRMED
COMMIT_SHA = 5a1d9e63c97712b9ee5ddbdf8f26b802eded801e / 16 HOM-02 files
WORKTREE_WIP_PRESERVED = YES / no push
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE §123 and continuity pointers updated
ACTIVITY_COMPLETE = YES / bounded fix complete; overall HOM-02 acceptance remains pending
```

## 87. ARGOS-ROADMAP-SPRINTS-RECONCILIATION (2026-10-16)

| Path | Papel | Vigência |
|---|---|---|
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, §124 | Baseline, status/gates e limites da reconciliação | CURRENT / root delta validated; `git diff --check` PASS |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md`, §20.83 | Handoff vigente e recomendação de retomada | CURRENT |
| `docs/projeto/ROADMAP_ARGOS_V5.md`, §24 | Status macro atualizado e direção de trilhas | CURRENT POINTER / prior snapshots preserved |
| `docs/projeto/SPRINTS_ARGOS_V5.md`, §21 | Ordem, IDs, gates e status por escopo | CURRENT POINTER / §20 preserved as historical snapshot |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`, §26 | Seleção Quick Detail, provenance e limites aprovados de imagem | CANONICAL AUTHORITY / implementation not established |
| `docs/projeto/contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md`, §2 | DAG e waves de BC-02 | CANONICAL AUTHORITY |
| `docs/projeto/contracts/backend/camera/CAM-INT-02_CREDENTIALS_CONTRACT.md`, `CAM-INT-02-R1_RUNTIME_CREDENTIAL_RESOLUTION_CONTRACT.md`, and `docs/projeto/contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md` | Backend credential lifecycle/resolver and access boundaries | CANONICAL REFERENCES / do not duplicate security rules |

```text
ACTIVITY = ARGOS-ROADMAP-SPRINTS-RECONCILIATION
HOM-01 = CLOSED / APPROVED / PROJECT_STATE §113
HOM-02 = implementation and technical validations §§115-123 / user-confirmed functional acceptance in this activity
HOM-02_ACCEPTANCE = supersedes only prior PENDING acceptance; no new validation/readiness/deploy/homologation
HOM-03 = FORMAL_READINESS_PENDING / BLOCKED_PENDING_SSH_AUTHENTICATION / §§121-122
HOM-04 = FORMAL_OPENING_NOT_ESTABLISHED / HOM-00..03 accepted evidence remains required
HOM-05 = future backlog / independent activity, authorization and gates
MON-01..09 = TECHNICALLY_COMPLETE / current user input; no tests rerun
MON_WORKER = code present in HEAD; §71 SQLite evidence historical; PostgreSQL/multi-worker/production readiness NOT_ESTABLISHED
UI_V2 = P0-P2 CLOSED PASS; P3 references; P4 scope-specific; P5 selective baseline integration; P6 scope-specific; P7 global completion NOT_ESTABLISHED
BC-02 = stage/checkpoint scoped; do not promote wave-7/production to global PASS
IMG = IMG-01..09 statuses and evidence boundaries in SPRINTS §21
NEXT_RECOMMENDATION = resume HOM-03 after authorized SSH key; then reevaluate HOM-04 gates; HOM-05 separately authorized
AGENT_HANDOFF_GATE_RESULT = PASS / root independently validated the delta
ROOT_DELTA_VALIDATION = PASS
GIT_DIFF_CHECK = PASS
ACTIVITY_COMPLETION_PERCENT = 100%
PROJECT_STATE_UPDATE = PASS
ACTIVITY_COMPLETE = YES
```

Atividade documental apenas. Baseline fornecida: root atual, branch
`codex/hom-v1-integration`, HEAD
`5a1d9e63c97712b9ee5ddbdf8f26b802eded801e`, staging vazio. Os worktrees
CAM-INT-04, IMG-CAP, UI P3-A/B/C/D e P5 foram inspecionados read-only; branches
isoladas não são integração canônica. WIP pré-existente foi preservado conforme
`PROJECT_STATE.md` §124. Sem alteração de código/testes, execução de testes,
acesso a banco, purge ou operações de Git. O root validou o delta e confirmou
`git diff --check` sem erros; staging vazio. O conjunto ativo de políticas
transversais permanece o identificado na seção 3 deste mapa: PM-02 R2.6,
PM-03 R2.3, PM-04 v1.2 e Independence v1. PM-01/PM-05 não foram adicionadas
como authorities.
