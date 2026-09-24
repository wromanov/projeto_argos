# ARGOS — Active Document Map

STATUS = CURRENT
DOCUMENT_TYPE = PROJECT_SPECIFIC_AUTHORITY_MAP
PROJECT = ARGOS
ACTIVE_DOCUMENT_MAP_READY = YES

## 1. Project continuity authorities

| Path | Role | Status |
|---|---|---|
| `AGENTS.md` | Project entrypoint / agent authority map | PRESENT / CURRENT CHECKOUT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/AGENT_CONTINUITY.md` | Project-specific continuity instance | PRESENT / ACTIVE |
| `docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md` | Current operational snapshot | PRESENT / CURRENT_SNAPSHOT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/ACTIVE_DOCUMENT_MAP.md` | Active authority/document map | PRESENT / CURRENT |
| `docs/Agent-Continuity-Standard-v1.0/continuity/NEW_CHAT_BOOTSTRAP_PROMPT.md` | New-chat recovery contract | PRESENT / ACTIVE |

## 2. Known project canonical documents

| Path / identity | Role | Status |
|---|---|---|
| `docs/projeto/ROADMAP_ARGOS_V5.md` | Project roadmap / workstream direction | PRESENT / CANONICAL; MON-09 technically closed; Fase C next |
| `docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` | UI-DS visual/interactions/Fase C/incremental integration authority | PRESENT / CANONICAL; reference `camera-inventory-design-system-v1.0.1` |
| `docs/projeto/SPRINTS_ARGOS_V5.md` | Canonical sprint/slice execution map | PRESENT / CANONICAL; UI-0 next preparatory activity |
| `docs/projeto/ADR-019_monitoramento_disponibilidade_gestao_imagens.md` | Monitoring architecture/behavior authority | PRESENT; verify current content |
| `docs/projeto/ADR-020_contrato_estado_tecnico_monitoramento.md` | Monitoring state/read semantics authority | PRESENT; verify current content |
| `docs/projeto/ADR-021_seguranca_capacidade_monitoramento.md` | Monitoring security/capability authority | PRESENT / CANONICAL; verify current content |

## 3. Transversal policy set

CURRENT / ACTIVE:

- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-Prompts-Agente-v1.7-R2.4.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/AGENTS-Multiagente-Generico-v1.7-R2.1-Roteamento-Economico.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Politica-de-Uso-de-Skills-e-Plugins-Codex-Work-v1.1.md`
- `docs/Agent-Continuity-Standard-v1.0/policies/Independencia-Analitica-Agente-v1.md`

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

Current validated baseline snapshot before this UI-DS documentary activity:

- repository: `C:\Users\walacedelgado\PycharmProjects\projeto_argos`
- branch: `master`
- HEAD = origin/master: `202e4f353551e7ab05667d86f9216cc102f351cc`
- divergence: ahead 0 / behind 0
- worktree: clean
- staging: empty
- snapshot: baseline before this documentary activity; revalidate Git after its documentary commit and in a new session

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
CAMERA_QUICK_DETAIL_PANEL = ADOPT
ARGOS_CURRENT_PAGE_COMPOSITION = PRESERVE
LATEST_CAMERA_CAPTURE_FEEDS_PANEL = YES_WHEN_CANONICAL_CONTRACT_AVAILABLE
FASE_C_DEPENDENCY = EXPLICIT
BIG_BANG_INTEGRATION = PROHIBITED
INTEGRATION_GATE = REQUIRED_WHEN_APPLICABLE
UI_0 = READ_ONLY_PREPARATORY_NEXT_ACTIVITY
UI_1 = TOKEN_COMPONENT_ADAPTER_FOUNDATION
UI_2 = INVENTORY_VISUAL_RETROFIT
UI_3 = INTEGRATED_CAMERA_QUICK_DETAIL_PANEL
UI_4 = INTEGRATED_VISUAL_FUNCTIONAL_ACCESSIBILITY_INTERACTION_QA
```

Detalhes permanecem exclusivamente em
`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`; ordem e marcos
estão em `docs/projeto/SPRINTS_ARGOS_V5.md`.


## 5. Monitoring workstream continuity

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
NEXT_REQUIRED_ACTIVITY = UI-0 — READ-ONLY PREFLIGHT (UI-DS; após adjudicação humana e autorização)
NEXT_PROJECT_ACTIVITY = FASE C — Captura manual e gestão de imagens
NEXT_PROJECT_ACTIVITY_STATUS = PLANEJADA
NEXT_REQUIRED_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED
NEXT_REQUIRED_ACTIVITY != EXECUTION_AUTHORIZATION
MON08C6_STATUS = COMPLETE / FINAL ADJUDICATION COMPLETE
MON08C6_IMPLEMENTATION_AUTHORIZATION = NOT_APPLICABLE
MON08_HOMOLOGATION_AUTHORIZED = NO
MON08_DEPLOYMENT_AUTHORIZED = NO
MON08_PRODUCTION_AUTHORIZED = NO
PUSH = NOT_AUTHORIZED


## 6. Current MON-09 closure and next project phase

MON-09A = COMPLETE / PASS
MON-09B = COMPLETE / PASS_WITH_SCOPE_DEVIATION
MON-09C = COMPLETE / PASS_WITH_FINDINGS
MON-09D = COMPLETE
MON-09E = COMPLETE / PASS
MON09_TECHNICALLY_COMPLETE = YES
MONITORING_TECHNICAL_FRONT_COMPLETE = YES
NEXT_TECHNICAL_MON_ACTIVITY = NONE
TECHNICAL_BASELINE = 850efd2381d7f5b7df27e528dc3374ea58e507b3
NEXT_PROJECT_ACTIVITY = FASE C — Captura manual e gestão de imagens
NEXT_PROJECT_ACTIVITY_STATUS = PLANEJADA
NEXT_REQUIRED_ACTIVITY = UI-0 — READ-ONLY PREFLIGHT (UI-DS; após adjudicação humana e autorização)
NEXT_REQUIRED_ACTIVITY_STATUS = RECOMMENDED_NOT_AUTHORIZED
SECURITY_GATES = LOCAL_DEVELOPMENT = RELEASED_WITH_CONTROLS; HOMOLOGATION = BLOCKED; DEPLOYMENT = BLOCKED; PRODUCTION = BLOCKED
VALIDATED_ENVELOPE = UNKNOWN / ONLINE / OFFLINE como estados estáveis; SUSPECT efêmero; STALE como freshness; confirmation memory persistente; pending failure streak sobrevive restart; thresholds respeitados; restart sem transição/outage falsa; falha de banco não equivale a câmera offline; CANCELLED neutro; timeout/rede conforme semântica canônica; sem histórico funcional falso em falha operacional e com recovery possível; ownership por câmera, owner persistente e epoch monotônico; lease define elegibilidade operacional de takeover; epoch é fencing token; config_generation é independente; completion de owner obsoleto sem side effects de domínio; owner antigo não libera owner novo; completion válida libera ownership atomicamente; renovação de lease não implementada; MonitoringConfig integrado à configuração ARGOS, config inválida fail-fast; status, backlog/in-flight, falhas operacionais e ownership diagnosticáveis; observabilidade sem histórico funcional e logs sem secrets
FUTURE_VALIDATIONS = PostgreSQL real; multi-processo real em produção; rede real; câmeras reais; credenciais reais; capacidade produtiva; budgets formais de CPU, memória e conexões
LOG_VOLUME_HARDENING_STATUS = HARDENING / NON-BLOCKING — potential high INFO log volume per cycle/attempt

MON-08/MON-09 predecessor entries above are continuity history. Current roadmap status is Fase C planned; do not resume MON-09 or infer production readiness.
