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
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Snapshot operacional | Estado atual, baseline, gates, autorização, decisões, blockers e próxima atividade | PRESENT / CURRENT_SNAPSHOT; CAM-INT-03 post-publication reconciliation section 60 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Continuidade do agente | Contexto necessário, riscos, limites, decisões e referências para assumir | PRESENT / ACTIVE; CAM-INT-03 post-publication reconciliation section 20.27 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Mapa de authorities | Paths, escopo, vigência e precedência documental | PRESENT / CURRENT; CAM-INT-03 post-publication reconciliation section 32; UI V2 authority mapped in section 16 |
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
