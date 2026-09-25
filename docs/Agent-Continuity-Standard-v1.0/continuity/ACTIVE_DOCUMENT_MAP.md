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
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Snapshot operacional | Estado atual, baseline, gates, autorização, decisões, blockers e próxima atividade | PRESENT / CURRENT_SNAPSHOT; updated 2026-09-25 after IMG-03 + UI-2 integration |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Continuidade do agente | Contexto necessário, riscos, limites, decisões e referências para assumir | PRESENT / ACTIVE; latest checkpoint IMG-03 + UI-2 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Mapa de authorities | Paths, escopo, vigência e precedência documental | PRESENT / CURRENT; latest checkpoint IMG-03 + UI-2 |
| `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md` | Bootstrap de nova sessão | Ordem de leitura, validação Git e limites para retomada | PRESENT / ACTIVE; latest checkpoint IMG-03 + UI-2 |

## 2. Authorities canônicas do projeto

| Path | Role | Authority scope | Status |
|---|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md` | Roadmap operacional | Macrofases, capacidades, dependências e status macro | PRESENT / CANONICAL; IMG-03 + UI-2 integrated checkpoint |
| `docs/projeto/SPRINTS_ARGOS_V5.md` | Mapa de execução | Ordem, atividades/slices, dependências, status e gates | PRESENT / CANONICAL; IMG-03 + UI-2 integrated; next candidate not authorized |
| `docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` | Contrato de domínio de imagem | IMG-01...IMG-09 e consumidores de imagem | PRESENT / CANONICAL; image-domain contract and deferred production backend decision |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` | Especificação UI/design system | Decisões UI-DS, CameraQuickDetailPanel, relação com Fase C e integração | PRESENT / CANONICAL; decisão funcional do painel aprovada pelo usuário na seção 7.3 |
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
| `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.4.md` | Prompts, roteamento cognitivo e execução | CURRENT / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md` | Execução direta, delegação e papéis | CURRENT / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md` | Skills/plugins e limites de capability | CURRENT / ACTIVE |
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

Baseline factual validada no início da reconciliação documental IMG-03 + UI-2:

- repository: `C:\Users\walac\desenvolvimento\projeto_argos`
- branch: `master`
- HEAD: `c79fa06775ccb707b6753f2a8ed0e988e8a9c86d`
- origin/master: `547678de9c70ee9eda2fc30599417d217c878006`
- divergence: ahead 4 / behind 0
- worktree antes da reconciliação: clean
- staging: empty
- validação: 2026-09-25; Git permanece a fonte factual e deve ser revalidado em nova sessão

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
LATEST_CAMERA_CAPTURE_FEEDS_PANEL = YES_WHEN_CANONICAL_CONTRACT_AVAILABLE
FASE_C_DEPENDENCY = EXPLICIT
BIG_BANG_INTEGRATION = PROHIBITED
INTEGRATION_GATE = REQUIRED_WHEN_APPLICABLE
UI_0 = COMPLETE / PASS_WITH_FINDINGS; READ_ONLY; DOES_NOT_AUTHORIZE_IMPLEMENTATION
UI_1 = COMPLETE / INTEGRATED; COMMIT = c5928e8
UI_2 = COMPLETE / INTEGRATED; COMMIT = b57f959; INTEGRATION_COMMIT = c79fa06
UI_3 = PENDING / NOT_AUTHORIZED; CameraQuickDetailPanel integration
UI_4 = INTEGRATED_VISUAL_FUNCTIONAL_ACCESSIBILITY_INTERACTION_QA
```

Detalhes permanecem exclusivamente em
`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`; ordem e marcos
estão em `docs/projeto/SPRINTS_ARGOS_V5.md`.


## 5. Historical monitoring workstream continuity

Os status técnicos desta seção registram checkpoints MON já concluídos. A
próxima atividade de projeto e a autorização vigentes estão na seção 8.

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
OPEN_DECISION_COUNT = 7; see the canonical contract for each decision and its closure slice
IMG02_STATUS = COMPLETE / INTEGRATED
IMG02_IMPLEMENTATION_AUTHORIZATION = prior authorization for this slice consumed
PRODUCTION_STORAGE_BACKEND = DEFERRED; contract persistent storage and configurable abstraction recorded in canonical image contract
IMG03_STATUS = COMPLETE / INTEGRATED; COMMIT = f6e08b6; INTEGRATION_COMMIT = 0708797
NEXT_CANDIDATE = SECURE_IMAGE_PREVIEW_DELIVERY / NOT_AUTHORIZED
FASE_C_COMPLETE = NO

## 8. Continuidade e estado atual

ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE
CONTINUITY_AUTHORITY = docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md
CURRENT_MACROPHASE = FASE C — Captura manual e gestão de imagens
CURRENT_GIT_BASELINE = master; HEAD c79fa06775ccb707b6753f2a8ed0e988e8a9c86d; origin/master 547678de9c70ee9eda2fc30599417d217c878006
DIVERGENCE = ahead 4 / behind 0
CURRENT_WORKTREE = seis documentos desta reconciliação modificados e unstaged; staging vazio
LAST_COMPLETED_ACTIVITY = IMG-03 + UI-2 — COMPLETE / INTEGRATED
NEXT_CANDIDATE = SECURE_IMAGE_PREVIEW_DELIVERY
NEXT_CANDIDATE_STATUS = NOT_AUTHORIZED
IMPLEMENTATION_AUTHORIZED = NO
LIVE_AUTHORIZED = NO
COMMIT_AUTHORIZED = NO
PUSH_AUTHORIZED = NO
UI_DS_STATUS = UI-1 and UI-2 COMPLETE / INTEGRATED; UI-3 NOT_AUTHORIZED
IMG02_STATUS = COMPLETE / INTEGRATED
IMG03_STATUS = COMPLETE / INTEGRATED
LATEST_INTEGRATION_COMMIT = c79fa06
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

## 10. Checkpoint vigente — IMG-03 + UI-2 (2026-09-25)

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
