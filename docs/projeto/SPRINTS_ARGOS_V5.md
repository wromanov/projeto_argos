# ARGOS — Plano Canônico de Sprints e Execução v5

```text
STATUS = CANONICAL
DOCUMENT_TYPE = PROJECT_SPRINT_EXECUTION_MAP
LANGUAGE = pt-BR
ROADMAP_AUTHORITY = docs/projeto/ROADMAP_ARGOS_V5.md
UI_DS_DETAIL_AUTHORITY = docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md
REFERENCE_DESIGN_SYSTEM = camera-inventory-design-system-v1.0.1
REFERENCE_PACKAGE_EXTERNAL_PATH = C:\Users\walacedelgado\Downloads\camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_PATH = docs/projeto/camera-inventory-design-system-v1.0.1.zip
REFERENCE_PACKAGE_REPOSITORY_COPY = YES
REFERENCE_PACKAGE_REPOSITORY_SHA256 = 510D75399A5C2F641DB77EF1AF9C982B8A2B3D9C08B06854073CE16FE028DA14
CURRENT_PHASE = PREPARAÇÃO PARA HOMOLOGAÇÃO PROGRESSIVA
CURRENT_PHASE_STATUS = HOM-00 DOCUMENTAL RECONCILIADA; integração, HOM-01..03 e gates de homologação pendentes
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_DOCUMENT
CURRENT_ACTIVITY = ARGOS-HOM-00-INTEGRATION-FOUNDATION / PLANNED / NOT_AUTHORIZED
LAST_COMPLETED_ACTIVITY = ARGOS-HOM-00-ROADMAP-FINAL-RECONCILIATION / DOCUMENTARY
LAST_COMPLETED_ACTIVITY_STATUS = PROJECT_STATE_UPDATE PASS; HOM-00 integration foundation remains pending
NEXT_CANDIDATES = ARGOS-HOM-00-INTEGRATION-FOUNDATION
NEXT_CANDIDATES_STATUS = PLANNED / NOT_AUTHORIZED; Quick Detail visual baseline remains approved and protected
IMG02_IMPLEMENTATION_AUTHORIZATION = GRANTED_BY_EXPLICIT_USER_INSTRUCTION_FOR_THIS_SLICE_ONLY
IMG-01 = COMPLETE após o checkpoint documental; contrato canônico:
docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md.
Esta ordem registra a próxima atividade, não concede autorização de
implementação nem encerra a Fase C.
ARGOS_CONTINUITY_PRINCIPLE = ACTIVE
AGENT_HANDOFF_GATE = ACTIVE
CONTINUITY_AUTHORITY = docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md
UI-0 = COMPLETE / PASS_WITH_FINDINGS (read-only; não concede autorização de implementação)
IMG-02 = COMPLETE / INTEGRATED; COMMIT = ceda8f6
UI-1 = COMPLETE / INTEGRATED; COMMIT = c5928e8
LATEST_INTEGRATION_COMMIT = 1015a8f
INTEGRATION_GATE = PASS
IMG-03 = COMPLETE / INTEGRATED; COMMIT = f6e08b6; INTEGRATION_COMMIT = 0708797
UI-2 = COMPLETE / INTEGRATED; COMMIT = b57f959; INTEGRATION_COMMIT = c79fa06
UI-3_TECHNICAL_IMPLEMENTATION = COMPLETE; TECHNICAL_COMMIT = bcc7e7d
UI-3_INTEGRATION = COMPLETE; INTEGRATION_COMMIT = 1015a8f
UI-3_FUNCTIONAL_VALIDATION = PASS
UI-3_VISUAL_ACCEPTANCE = PASS / current Quick Detail visual baseline explicitly approved by user
UI-3_PRODUCT_ACCEPTANCE = PENDING
UI-3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PASS / PRODUCT_ACCEPTANCE_PENDING
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
DESIGN_QA = MANDATORY / HOM-01
```

Este é o documento canônico de execução de slices para as atividades futuras
registradas abaixo. O roadmap define direção e macrofases; a especificação de
integração define contratos detalhados. Este documento registra somente ordem,
marcos, dependências e gates de execução. Não duplica a specification.

## 1. Estado e precedência

Este mapa registra status, ordem, dependências e gates das slices. O estado
recuperável entre agentes e o contrato de handoff pertencem a
`docs/projeto/ARGOS_CONTINUITY_AND_HANDOFF_RULES_V1.md`.

MON-09 está tecnicamente encerrada. IMG-02, UI-1, IMG-03, UI-2 e
SECURE_IMAGE_PREVIEW_DELIVERY estão integradas. UI-3 está tecnicamente
implementada e integrada, com validação funcional `PASS`; a baseline visual
atual do Quick Detail foi aprovada explicitamente pelo usuário nesta
reconciliação, enquanto a aceitação de produto da UI-3 permanece pendente.
UI-V2-P0 — SCREEN CENSUS está fechado como CLOSED_PASS; sua authority factual
está em docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md. UI-V2-P1 — VISUAL STYLE LAB
é a próxima atividade UI, ainda não iniciada nem autorizada por este mapa.
IMG-04 permanece como candidata de backend/imagens não autorizada;
MON-AVAIL-02 é recomendação registrada sem autorização ou sequência definida. Este mapa registra status e sequência; não concede autorização para implementar candidatas,
avançar slices,
mudar de fase ou executar em homologação/produção.

Em caso de divergência:

1. instrução explícita do usuário;
2. contracts e authorities específicos do ARGOS;
3. `ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` para UI-DS;
4. este mapa para ordem e marcos;
5. `ROADMAP_ARGOS_V5.md` para direção de macrofase.

Conflitos devem ser identificados, classificados, reportados e propostos; nunca
resolvidos silenciosamente.

## 2. Fase C — Captura manual e gestão de imagens

Slices vigentes:

```text
IMG-01 — Contrato funcional
IMG-02 — Modelo, storage e proveniência
IMG-03 — Upload manual
IMG-04 — Captura sob demanda
IMG-05 — Processamento independente
IMG-06 — Histórico visual
IMG-07 — Imagem principal
IMG-08 — Segurança e auditoria
IMG-09 — Hardening
```

A Fase C deve fechar o contrato de `CAPTURA_CAMERA` versus `UPLOAD_MANUAL`,
armazenamento, referência, disponibilidade, histórico e estados de erro. O
`CameraQuickDetailPanel` depende de uma consulta canônica de
`LATEST_CAMERA_CAPTURE`; não deve criar uma fonte paralela.

## 3. UI-DS — frente transversal

```text
UI-DS = Integração seletiva do Camera Inventory Design System v1.0.1
```

Estratégia:

```text
SELECTIVE VISUAL RETROFIT
+ SELECTIVE INTERACTION PATTERN ADOPTION
```

`ARGOS CURRENT PAGE COMPOSITION = PRESERVE` e
`DO_NOT_MIGRATE_FRAMEWORKS = YES`. O padrão aprovado
`CameraQuickDetailPanel` adota o papel de inspeção contextual rápida, sem
substituir a página canônica completa da câmera. Seu conteúdo funcional foi
explicitamente aprovado pelo usuário e está registrado em
`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`; VMS não é adotado
e Localização ocupa esse lugar. Não duplicar a especificação aqui.

### UI-0 — Read-only preflight

```text
STATUS = COMPLETE / PASS_WITH_FINDINGS
READ_ONLY = YES
IMPLEMENTATION = NO
STOP_AFTER_REPORT = YES
FINDINGS_DETAIL = docs/projeto/ARGOS_UI_DS_UI0_PREFLIGHT_FINDINGS_V1.md
```

O preflight read-only está concluído. Seu escopo cobria descobrir stack,
inventário, layout, filtros,
tabela, seleção, rota canônica,
identificador de câmera, fontes de imagem/status, modelos de loading/error/stale,
tokens, componentes, iconografia, tipografia, responsividade e acessibilidade.

Entregar `PRESERVE`, `ADAPT`, `ADOPT`, `DO_NOT_ADOPT`, `TOKEN_MAPPING`,
`COMPONENT_MAPPING`, `CAMERA_QUICK_DETAIL_PANEL_MAPPING`, `RISKS` e
`PILOT_SCOPE`. UI-0 não altera código, CSS ou dependências.

### UI-1 — Token & Component Adapter Foundation

Introduzir a camada reversível de adapter entre tokens do Design System, tokens
do ARGOS e componentes existentes. Não redesenhar páginas nem substituir
composição. Deve preceder o retrofit visual.

### UI-2 — Inventory Visual Retrofit

Aplicar o piloto no inventário, preservando layout, filtros, busca, sorting,
paginação, query string, seleção e comportamento. Escopo visual: background,
cards, table surfaces, borders, status, buttons, inputs, focus e selection.

### UI-3 — CameraQuickDetailPanel

UI-3 está tecnicamente implementada e integrada ao inventário real, com seleção,
identificador, resumo/status canônicos, `LATEST_CAMERA_CAPTURE`, localização e
rota canônica de detalhes completos. VMS permanece `DO_NOT_ADOPT`. A validação
funcional está `PASS`, mas a aceitação visual e de produto permanece pendente
até aprovação explícita do usuário. Reutiliza a entrega segura existente na
variante `PANEL`; não cria backend paralelo de imagens. Os detalhes permanecem
na authority UI-DS, seção 12.

```text
INTEGRATION_GATE = REQUIRED
DRAWER_OPEN_ALONE = NOT_SUFFICIENT
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
UI-3_TECHNICAL_COMMIT = bcc7e7d
UI-3_INTEGRATION_COMMIT = 1015a8f
UI-3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PENDING
```

UI-3 depende de `IMG-01` e `IMG-02` para a semântica e o modelo da imagem, e de
`IMG-04`/`IMG-06` quando a captura real e o histórico forem necessários ao
consumidor. `IMG-03` deve continuar separada por proveniência. `IMG-05`,
`IMG-08` e `IMG-09` fornecem limites de processamento, segurança, auditoria,
concorrência, stale e erro.

### UI-4 — Visual / Functional / Accessibility / Interaction QA

Executar depois da integração de UI-3 e dos contratos da Fase C aplicáveis.
Validar visual, funcional, acessibilidade e interação, preservando baseline
before/after, composição, arquitetura da informação, semântica de status,
viabilidade do painel, ausência de regressão e ausência de mudança não
autorizada de stack.

## 4. Ordem recomendada e dependências

```text
IMG-01 = COMPLETE / checkpoint documental
UI-0 = COMPLETE / PASS_WITH_FINDINGS (read-only)
IMG-02 = COMPLETE / INTEGRATED (ceda8f6)
UI-1 = COMPLETE / INTEGRATED (c5928e8)
IMG-03 = COMPLETE / INTEGRATED (f6e08b6; integration 0708797)
UI-2 = COMPLETE / INTEGRATED (b57f959; integration c79fa06)
INTEGRATION_GATE = PASS (7ca5f7c)
SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED (e3f2d40; 7ca5f7c)
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
↓
UI-3 = INTEGRATED / VISUAL_ACCEPTANCE_PASS / PRODUCT_ACCEPTANCE_PENDING
IMG-04 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-4 = NOT_AUTHORIZED
UI-V2 = DOCUMENTED / P0 CLOSED_PASS / NEXT_UI_ACTIVITY = UI-V2-P1 — VISUAL STYLE LAB / NOT_STARTED / NOT_AUTHORIZED
↓
demais slices seguem as dependências canônicas e exigem autorização própria
```

A ordem pode ser refinada por decisão humana quando uma dependência factual
exigir outra sequência, mas não pode transformar integração final em cleanup
rotineiro.

## 5. Gates transversais

### ARGOS Incremental Integration Rule

```text
IMPLEMENT
↓
INTEGRATE INTO CANONICAL FLOW
↓
VALIDATE INTEGRATED
↓
CLOSE SLICE
```

```text
BIG_BANG_INTEGRATION_AT_END = PROHIBITED
INTEGRATION_SPRINT_AS_ROUTINE_CLEANUP = ANTI_PATTERN
```

Nenhuma capability produtiva é `DONE` enquanto estiver isolada. Se uma grande
sprint de integração for necessária ao final de uma fase, as slices anteriores
devem ser reavaliadas como fechadas incorretamente.

### Integration Gate

Aplicar conforme a natureza da slice:

```text
INTEGRATION_GATE = PASS
FEATURE_REACHABLE_FROM_REAL_ENTRYPOINT = YES
FEATURE_USES_CANONICAL_DOMAIN_PATH = YES
FEATURE_PERSISTS_THROUGH_CANONICAL_PATH = YES_WHEN_APPLICABLE
FEATURE_VISIBLE_TO_REAL_CONSUMER = YES
FEATURE_PERMISSION_PATH_INTEGRATED = YES_WHEN_APPLICABLE
FEATURE_AUDIT_PATH_INTEGRATED = YES_WHEN_APPLICABLE
NO_ORPHAN_IMPLEMENTATION = YES
NO_FUTURE_BIG_BANG_INTEGRATION_REQUIRED = YES
```

Não aplicar mecanicamente persistência/auditoria a uma slice visual que não os
possua, mas sempre exigir o caminho real de consumo quando houver consumidor
produtivo.

### Vertical slice

```text
MIGRATION / IMPLEMENTATION UNIT = VERTICAL SLICE
```

Tokens, componentes e painéis não devem ser implementados em trilhas isoladas
para integração posterior. Cada slice deve alcançar o entrypoint, o domínio,
o storage e a UI reais que lhe correspondem, além da validação e do checkpoint.

## 6. Não escopo deste mapa

- não autoriza UI, CSS ou código de aplicação;
- não autoriza instalação de dependências;
- não autoriza mudança de framework;
- não autoriza captura automática ao abrir o painel;
- não autoriza segunda página de detalhes;
- não autoriza duplicação de domain logic;
- não autoriza commit, push, deploy, LIVE ou homologação;
- não autoriza tratar upload manual como captura de câmera;
- não autoriza big-bang integration.

## 7. Authority detalhada

Para qualquer decisão material da UI-DS, consultar:

`docs/projeto/ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md`

Para direção da macrofase e status global, consultar:

`docs/projeto/ROADMAP_ARGOS_V5.md`

Para continuidade entre chats, consultar os quatro documentos em
`docs/Agent-Continuity-Standard-v1.0/continuity/` listados no
`ACTIVE_DOCUMENT_MAP.md`.


## 10. Registro histórico — checkpoint de integração IMG-02 + UI-1

IMG-02 = COMPLETE / INTEGRATED
UI-1 = COMPLETE / INTEGRATED
IMG-02_COMMIT = ceda8f6
UI-1_COMMIT = c5928e8
LATEST_INTEGRATION_COMMIT = d5f1f54
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; cameras.test_imagens_read_service 13/13 PASS
OPEN_DECISIONS = consultar docs/projeto/ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md

## 11. Registro histórico — integração IMG-03 + UI-2 (2026-09-25)

IMG-03 = COMPLETE / INTEGRATED
IMG-03_COMMIT = f6e08b6
IMG-03_INTEGRATION_COMMIT = 0708797
UI-2 = COMPLETE / INTEGRATED
UI-2_COMMIT = b57f959
UI-2_INTEGRATION_COMMIT = c79fa06
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; makemigrations --check --dry-run PASS (No changes detected); cameras.test_imagens_read_service + cameras.test_imagens_upload = 20/20 PASS
PILLOW = dependência técnica de upload; versão 12.3.0 disponível no venv integrado
MERGE_CONFLICTS_IMG03 = NONE
MERGE_CONFLICTS_UI2 = NONE

INVENTORY_CAMERA_THUMBNAIL = APPROVED
INVENTORY_THUMBNAIL_SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = DEFERRED
BLOCKING_DEPENDENCY = SECURE_IMAGE_PREVIEW_DELIVERY
INVENTORY_THUMBNAIL_STATUS = foundation visual com placeholder neutro; sem dados reais e sem completude funcional

SECURE_IMAGE_PREVIEW_DELIVERY = REQUIRED / NOT_YET_AUTHORIZED
SECURE_IMAGE_PREVIEW_DELIVERY_STATUS = NEXT_CANDIDATE / NOT_AUTHORIZED
SECURE_IMAGE_PREVIEW_DELIVERY_CONSUMERS = Inventory thumbnail; CameraQuickDetailPanel
DELIVERY_ARCHITECTURE = ONE SECURE DELIVERY CONTRACT → MULTIPLE AUTHORIZED CONSUMERS
IMG-04 = NOT_AUTHORIZED
UI-3 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE

O detalhe técnico e as demais decisões deferred ficam no `PROJECT_STATE.md` e
no `AGENT_CONTINUITY.md`; contracts de domínio e UI permanecem nas authorities
especializadas. A ordenação de candidatas neste mapa é planejamento e não
concede autorização. Não houve reexecução de testes nesta reconciliação.

## 12. Registro histórico — Secure Image Preview Delivery (2026-09-25)

```text
SECURE_IMAGE_PREVIEW_DELIVERY = COMPLETE / INTEGRATED
TECHNICAL_COMMIT = e3f2d40
INTEGRATION_COMMIT = 7ca5f7c
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; makemigrations --check --dry-run PASS / no changes; cameras.test_imagens_read_service + cameras.test_imagens_upload + cameras.test_imagens_preview = 28/28 PASS
MERGE_CONFLICTS = NONE
INVENTORY_CAMERA_THUMBNAIL = APPROVED; SOURCE = LATEST_CAMERA_CAPTURE
INVENTORY_THUMBNAIL_VISUAL_FOUNDATION = COMPLETE
INVENTORY_THUMBNAIL_REAL_DATA_WIRING = COMPLETE
PREVIEW_VARIANTS = THUMB; PANEL; dimensões na authority de imagens, seção 24
UI-3 = NEXT_CANDIDATE / NOT_AUTHORIZED
IMG-04 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
```

A variante PANEL existente atende à UI-3. Este checkpoint foi supersedido pela
integração da UI-3 abaixo.

## 13. Checkpoint histórico — UI-3 pós-integração (2026-09-25)

```text
UI-3_TECHNICAL_IMPLEMENTATION = COMPLETE
UI-3_TECHNICAL_COMMIT = bcc7e7d
UI-3_INTEGRATION = COMPLETE
UI-3_INTEGRATION_COMMIT = 1015a8f
INTEGRATION_GATE = PASS
INTEGRATION_VALIDATION = manage.py check PASS; makemigrations --check --dry-run PASS; 32/32 tests PASS (cameras.test_quick_detail, cameras.test_imagens_read_service, cameras.test_imagens_upload, cameras.test_imagens_preview); evidência fornecida, não reexecutada
GIT_DIFF_CHECK = PASS (evidência fornecida antes desta reconciliação; reconfirmar após as alterações documentais)
UI_VISUAL_ACCEPTANCE_GATE = MANDATORY
UI-3_FUNCTIONAL_VALIDATION = PASS
UI-3_VISUAL_ACCEPTANCE = PENDING
UI-3_PRODUCT_ACCEPTANCE = PENDING
UI-3_OVERALL_STATUS = INTEGRATED / VISUAL_ACCEPTANCE_PENDING
IMG-04 = NEXT_CANDIDATE / NOT_AUTHORIZED
UI-4 = NOT_AUTHORIZED
NEXT_PROJECT_ACTIVITY_AUTHORIZED = NONE
```

O painel usa `Secure Image Preview Delivery` na variante `PANEL`, baseada em
`LATEST_CAMERA_CAPTURE`, sem fallback para `UPLOAD_MANUAL`, `PRIMARY_IMAGE` ou
captura anterior. Abrir o painel não captura imagem nem altera monitoramento.
A authority UI-DS concentra o contrato e a nova regra de aceitação visual; a
authority de imagens concentra o contrato do preview e as decisões deferred.
O gate de integração passou. Nenhuma rodada de reparo visual foi iniciada.

## 14. Frente planejada — ARGOS UI Remediation (2026-09-27)

UI-AUD-01 foi concluída; relatório em `docs/frontend/ARGOS_FRONTEND_AUDIT_REPORT.md`.
A diretriz técnica completa está em
`docs/frontend/ARGOS_DIRETRIZ_REMEDIACAO_FRONTEND_UI_UX_V1.md`.

| Ordem | Slice | Gate essencial |
|---|---|---|
| Phase 0 | Dead CSS / Defeated Rules Cleanup | Nenhum delta de computed style, visual ou funcional; complexidade reduzida |
| Phase 1 | CSS Ownership Consolidation | Owners de componentes compartilhados documentados; sem regressão visual |
| Phase 2 | Shell Stabilization | Sidebar, topbar e main estáveis; sem clipping/overflow |
| Phase 3 | Shared Component Density | Controles alinhados, toque e foco preservados |
| Phase 4 | Inventory Responsive Repair | Filtros e tabela sem clipping; dados longos e mobile validados |
| Phase 5 | Dashboard Refinement | Grids e hierarquia estáveis em viewports alvo |
| Phase 6 | Quick Detail Cleanup | Scroll previsível, footer visível, foco e acessibilidade preservados |

Após Phase 6: regressão entre viewports e canonicalização do baseline do
Design System. `Phase 0 = PLANNED / NOT_STARTED` era o status na abertura desta
frente; seu fechamento atual está registrado na seção 15. Este mapa não autoriza
implementação. Patches visuais novos ficam sujeitos às fases de remediação e,
para mudanças de apresentação, ao gate prototype-driven da UI V2. A baseline
visual atual do Quick Detail foi aprovada pelo usuário; a aceitação de produto
da UI-3 permanece pendente e UI-4A aguarda aceitação visual. O checkpoint
`768844d` apenas preserva o trabalho anterior. IMG-DISPLAY-01 já foi integrado
em `cad0760`.

## 15. Fechamento — ARGOS UI Remediation Phase 0 (2026-09-27)

```text
PHASE0_TECHNICAL_IMPLEMENTATION = PASS
PHASE0_USER_VISUAL_REVIEW = PASS
PHASE0_CANONICAL_CODE_INTEGRATION = PASS
POST_INTEGRATION_VISUAL_GATE = PASS
USER_POST_INTEGRATION_ACCEPTANCE = PASS
PHASE0_CANONICAL_CLOSURE = PASS
PHASE0_STATUS = CLOSED
BASELINE_HEAD = c210fe62f49ec2ba259b0d3a64a1f6ea1e6fdf83
IMPLEMENTATION_COMMIT = 7b938a33b3c6192b8294da98decd7b245c27d8db
REVIEW_RECONCILIATION_COMMIT = baa51c61a942a1387990f73fea98b367568167c1
CANONICAL_MERGE_COMMIT = 9bdea6a9f39a908a2f19b33b8132102631868066
PHASE1 = READY_NOT_STARTED
NEXT_ACTIVITY = ARGOS UI REMEDIATION — PHASE 1 / CSS OWNERSHIP CONSOLIDATION
PUSH = NOT_PERFORMED
```

As métricas e os resultados detalhados da Phase 0 permanecem em
`docs/Agent-Continuity-Standard-v1.0/continuity/PROJECT_STATE.md`, seção 20.
Phase 1 está pronta para planejamento, mas não foi iniciada nem autorizada por
este registro.

## 16. Reconciliação vigente — ARGOS UI V2 prototype-driven (2026-09-27)

A autoridade operacional da trilha é
docs/projeto/ARGOS_UI_V2_MASTER_PLAN.md; o census factual concluído está em
docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md. UI V2 é transversal e paralela ao
backend. O roadmap mantém A2 — Visual 5, A3 — Visual 6 e A4 — Visual 7; suas
entregas visuais passam pelo fluxo P0–P7 sem invalidar seus objetivos funcionais.

```
UI_V2_TRACK_STATUS = DOCUMENTED / PARALLEL_TO_BACKEND
P0_STATUS = CLOSED_PASS / ACTIVITY_COMPLETE = YES
SCREEN_CENSUS_AUTHORITY = docs/projeto/ARGOS_UI_V2_SCREEN_CENSUS.md
NEXT_UI_ACTIVITY = UI-V2-P1 — VISUAL STYLE LAB
P1_STATUS = NOT_STARTED / NOT_AUTHORIZED
ADMIN_UI_V2_SCOPE = TRACKED_AS_INHERITED / NO_CUSTOM_REDESIGN_BY_DEFAULT
PROTOTYPE_STACK_COMPATIBILITY = REQUIRED_GATE
IMPLEMENTATION_BEFORE_APPROVED_PROTOTYPE = PROHIBITED
PROTOTYPE_VISUAL_ACCEPTANCE_GATE = REQUIRED
POST_IMPLEMENTATION_VISUAL_ACCEPTANCE_GATE = REQUIRED
QUICK_DETAIL_VISUAL_BASELINE = APPROVED / PROTECTED
BATCH_B_POST_INTEGRATION_VISUAL_GATE = PENDING_USER_REVIEW
UI-3_VISUAL_ACCEPTANCE = PASS / current Quick Detail baseline approved by user
UI-3_PRODUCT_ACCEPTANCE = PENDING
```

Phase 0 e Fast Track Batch A continuam fechados. O census mantém os escopos
pendentes do Batch B como contexto; qualquer alteração visual de Inventário,
Dashboard ou Quick Detail deverá seguir o protótipo aprovado da família
correspondente. O gate visual pós-integração do Batch B continua pendente de
revisão humana. Os achados e guardrails técnicos da auditoria e diretriz CSS
continuam válidos; esta reconciliação documental não inicia P1 nem implementação.

O Admin fica rastreado no census como herdado, sem redesenho customizado por
padrão. IMG-04 permanece como candidata de backend/imagens registrada
anteriormente e não autorizada. MON-AVAIL-01 = BLOCKED_HISTORICAL_COVERAGE_GAP
e a recomendação MON-AVAIL-02 foram fornecidas na instrução atual do usuário;
não foram encontradas referências locais a esses identificadores no checkout.
A sequência entre IMG-04 e MON-AVAIL-02 permanece em aberto, sem fabricação
de métricas de availability ou coverage.

## 17. BC-00 — Complete Backend Contract Baseline (2026-10-01)

```text
STATUS = COMPLETE / DOCUMENTARY BASELINE
REPOSITORY_SYNC = PASS_ALREADY_CURRENT / master == origin/master at 38db46b
SCOPE = registry + access, camera integration, monitoring, image integration and production contracts
IMPLEMENTATION = NO
REAL_CAMERA_ACCESS = NO
HOMOLOGATION = NO
LIVE = NO
COMMIT = 7b0135f0e9911e6a03f1a297e606d848eaa44533 / docs(backend): add BC-00 contract baseline
PUSH = YES / origin/master
```

O detalhe normativo e a matriz de decisões abertas estão em
`docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md` e nos
contratos indexados. `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` permanece a authority
canônica do domínio de imagens. O baseline foi commitado e publicado após
autorização explícita do usuário. Esta atividade documenta capacidades observadas
e fronteiras; não reordena silenciosamente IMG-04/MON-AVAIL-02, não autoriza
implementação posterior e não substitui validação de produção. Próxima atividade
de backend: adjudicação humana deste baseline antes de escolher implementação.

## 18. BC-02 — fechamento de readiness contratual backend (2026-10-01)

O [registro BC-02](contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md) classifica
20 contratos. O [DAG](contracts/backend/BACKEND_IMPLEMENTATION_ORDER.md) define
BC-AUTH como primeira slice Luna; waves 2–6 incluem fundamentos, adapters,
diagnóstico, captura e worker com ownership sem colisão. A validação local
integrada vem depois, e os contratos PROD-* permanecem em gate de ambiente.
BC-02 é documental: nenhum código, migration, câmera, rede, UI, commit ou push
é executado por este checkpoint. Cada slice requer autorização própria.

```text
BC_02_STATUS = CONTRACT READINESS CLOSED / DOCUMENTARY
FIRST_LUNA_SLICE = BC-AUTH
IMPLEMENTATION_AUTHORIZED_BY_SPRINT_MAP = NO
PRODUCTION_VALIDATION = PENDING
UI_P5 = PARALLEL / OWN GATES
```

## 19. Pipeline por contrato, lanes isoladas e integração controlada (2026-10-02)

### Máquina de estado da slice

```text
NOT_STARTED -> READY -> RUNNING -> PASS_LOCAL -> SOURCE_CHECKPOINTED
             -> INTEGRATING -> INTEGRATED -> VALIDATED -> PUBLISHED
Exceções/saídas: BLOCKED | DEFERRED
DEPENDENCY_SATISFIED = INTEGRATED + VALIDATED + PUBLISHED
```

O contrato/DAG pode especificar estado de dependência diferente. `PASS_LOCAL` isolado não satisfaz por padrão predecessor. Ciclo padrão: contrato READY; worktree/branch isolada com SHA conhecido; implementação; validação estática, testes focais e regressão relevante; PASS_LOCAL; adjudicação; source checkpoint; integration gate; validação integrada (incluindo migration/static quando aplicável); continuidade no gate de integração; state checkpoint; publicação autorizada; confirmar igualdade HEAD/origin e divergência 0/0; reler DAG e iniciar imediatamente sucessor READY_NOW autorizado. `git diff --check` é obrigatório. Validar primeiro testes focais e regressão pertinente; testes globais/scale requerem justificativa. Não alegar câmera/rede/PostgreSQL/produção sem execução real.

### Worktrees, baselines e ownership

`master` é a branch canônica de integração; implementar em `master` é proibido. Cada lane declara `ISOLATED_BRANCH`, `ISOLATED_WORKTREE`, `KNOWN_BASE_SHA`, `PRIMARY_FILES`, `SHARED_FILES`, `MIGRATION_OWNERSHIP` e `TEST_SURFACES`. Usar `codex/<slice-description>` e registrar caminhos locais apenas no snapshot, nunca como regra universal. Duas lanes não alteram simultaneamente o mesmo arquivo material sem estratégia explícita. Colisões e migrations compartilhadas são reconciliadas no integration gate/owner único.

Uma lane pode terminar sobre baseline X mesmo se master avançar para Y: não reiniciar automaticamente. No gate, confirmar master atual, ownership e colisões; integrar sem perda, preferir fast-forward quando possível e permitido; merge controlado requer authority; nunca rebase/reset/cherry-pick por conveniência. Revalidar no estado integrado. Nenhuma slice paralela edita `PROJECT_STATE.md`, `ACTIVE_DOCUMENT_MAP.md`, roadmap ou sprints. `GLOBAL_CONTINUITY_OWNER = INTEGRATION_GATE`.

### Git e continuidade

Lane de implementação faz validação local e não publica por padrão. Após PASS_LOCAL, source checkpoint/commit depende de adjudicação e authority; push não é automático. Integration gate integra, valida, atualiza continuidade e publica somente com autorização apropriada. `PASS_LOCAL` pode fechar o trabalho técnico de uma lane sem alterar PROJECT_STATE. Fechamento formal exige `PROJECT_STATE_UPDATE = PASS`; nenhuma activity formal é `ACTIVITY_COMPLETE = YES` antes disso. Cada publicação dispara DAG recheck; não esperar wave inteira. Implementação backend e frontend P5 são paralelas quando dependências/ownership permitem.

## 20. Rebase de atividades para homologação progressiva (2026-10-11)

Esta sequência foi aprovada pelo usuário para a entrada progressiva em
homologação. Ela preserva os IDs e históricos deste mapa. Os status abaixo são
da branch e do worktree verificados nesta atividade; presença em outra branch
não equivale a integração. Homologação é ambiente controlado pré-produção e não
declara produção pronta.

### HOM-00 — Reconciliação documental e preparação de integração

```text
STATUS = DOCUMENTED / BASELINE AND P3/P5 CLASSIFICATION RECONCILED
BLOCKING = YES
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_ACTIVITY
```

- **Objetivo:** recuperar baseline, WIP e authorities; reconciliar os snapshots
  de integração/publicação com Git; fixar o conjunto canônico de código e
  documentos que servirá à homologação.
- **Escopo mínimo:** confirmar root, branch, HEAD, upstream, divergência,
  worktree e staging; preservar WIP; mapear dependências e diferenças entre
  branches; classificar P3/P5 sem big-bang merge; registrar estratégia e gates
  de integração.
- **Dependências:** nenhuma além do checkout e das refs de Git disponíveis.
- **Estado comprovado:** branch `codex/mon-runtime-v1-implementation`, HEAD
  `4ff2a9260a438a61f3a23e753dfdc3d5c166424a`; P3 root
  `e381df04f59ce146bf53fc6929fb7ca272c26e2c`; P5 production
  `4676a32c78cecab33a157a0a9d4fd2cabbc90a87`; P5 conformance
  `4a2d40da502ea4dafd8bc78202e707416695bee3`. Os três SHAs de fonte não são
  ancestrais do baseline nem de `master`. P3 = `PROTOTYPE / VISUAL_REFERENCE`;
  P5 = `PRODUCTION_UI_SOURCE / NOT_INTEGRATED`. WIP dos worktrees P3/P5 segue
  `UNVERIFIED`. No checkout corrente, três continuity docs e roadmap/sprints
  já estavam modificados; auditoria de persistência e harness H1 estavam não
  rastreados; tudo foi preservado.
- **Evidências de conclusão documental:** baseline e relações de ancestry
  registrados; estados P3/P5 distinguidos; estratégia, dependências, decisões
  abertas e gates documentados; inventário de WIP preservado; diff documental
  revisado. A branch de integração não foi criada.
- **Aceite:** nenhum arquivo WIP descartado; fatos de integração reconciliados;
  decisões de autoridade/compatibilidade que ainda dependem de adjudicação
  ficam abertas com gate; baseline Runtime V1 identificada como proposta para
  a branch isolada `codex/hom-v1-integration` (não criada). `git diff --check`
  sem erros.
- **Estratégia recomendada (planejamento):** preservar `master`; após preflight
  de segurança, preparar branch de integração isolada; integrar MON Runtime
  V1, integrar seletivamente P5 e preservar P3 como referência visual; validar
  regressões; passar Design QA; implementar importação XLSX; preparar VM; e só
  promover para `master` após os gates aplicáveis. Esta sequência não autoriza
  criar branch, fazer merge ou promover.
- **Critérios mínimos por etapa:** integração exige ancestry/diff e migrations
  coerentes, dependências resolvidas e regressões funcionais PASS; UI exige
  contrato e referência aprovados mais Design QA; XLSX exige schema/template
  adjudicados, preview, confirmação, validação canônica e atomicidade; VM exige
  owner/autorização, configuração segregada, banco/migrations, acesso,
  recuperação e worker controlado; promoção exige todos os gates de
  homologação aplicáveis e aprovação humana.
- **Reaproveitar:** P3 prototype harness, P3-A/B/C/D, checkpoints P5, contratos
  UI V2 e WIP de H1/H2; confirmar conteúdo exato antes de integrar.

### HOM-01 — Finalização UI V2

```text
STATUS = BLOCKED / P3 AND P5 CANONICAL INTEGRATION NOT PROVEN
BLOCKING = YES
```

- **Objetivo:** concluir e validar o frontend inicial necessário para cadastro,
  navegação pelo inventário e consulta de câmera na homologação.
- **Escopo mínimo:** reconciliar/integrar sob gate as superfícies UI V2 de
  shell/portal, dashboard, inventário, Camera Detail, cadastro/edição/login
  aplicáveis; validar estados, permissões, responsividade e consultas. Quick
  Detail conserva baseline aprovada e protegida; sem redesign implícito.
- **Dependências:** HOM-00; approvals de protótipo já exigidas pelas authorities
  UI V2; adjudicação do alvo DS 2.4.0 e compatibilidade; capabilities backend
  existentes ou fechamento explícito da dependência. HOM-01 e HOM-02 podem
  avançar parcialmente em paralelo depois da definição das interfaces e do
  baseline de integração. Não introduzir comportamento ou endpoint fictício.
- **Estado comprovado:** UI-V2-P0/P1/P2 e P3-0 têm registros de fechamento; o
  master do coverage ainda mostra superfícies como `PLANNED`, enquanto branches
  de família e P5 têm entregas próprias. O estado do runtime dessas telas na
  baseline canônica permanece NÃO COMPROVADO. O UI P5 source branch
  `codex/ui-v2-p5-production` e `codex/p5-camera-detail-production-conformance`
  não devem ser tratados como integrados sem diff e gate.
- **Evidências de conclusão:** refs/código integrados no baseline escolhido;
  validação funcional do Django para os fluxos iniciais; evidências de QA visual
  e acessibilidade nos viewports contratados; estados de coverage atualizados;
  autorização/permissão dos fluxos comprovadas.
- **Aceite:** telas iniciais integradas, rotas/consultas reais, cadastro/edição e
  inventário utilizáveis; Quick Detail visual preservado; sem regressões
  funcionais; `DESIGN_QA = PASS`, `FUNCTIONAL_REGRESSION = PASS` e
  `HUMAN_VISUAL_APPROVAL = PASS`; PROJECT_STATE e coverage atualizados após o
  gate integrado. Sem referência aprovada ou renderização comprovada, Design QA
  fica `BLOCKED`; diferença visual material ou regressão funcional resulta em
  `FAIL`.
- **Reaproveitar:** código/QA disponível nas branches P3-A e P3-D, shell
  aprovado, design system pinado, Camera Detail P5, `ARGOS_UI_V2_MASTER_PLAN.md`,
  `ARGOS_UI_V2_SCREEN_CENSUS.md`, coverage e contratos de detalhe/Quick Detail.

### HOM-02 — Importação XLSX de inventário

```text
STATUS = NOT_IMPLEMENTED / SCHEMA AND FINAL XLSX TEMPLATE NOT HOMOLOGATED
BLOCKING = YES
```

- **Objetivo:** importar cadastro em lote com prévia compreensível, resolução
  inequívoca de atualização e nenhuma gravação parcial.
- **Escopo mínimo:** planilha XLSX sem coluna de ID ARGOS; novos registros usam
  ID interno gerado pelo banco. Atualizar somente por patrimônio ou serial
  único, inequívoco e sem conflito; nome/IP isolados não identificam update.
  Reusar `CameraCriacaoForm`, `CameraEdicaoForm`, models, validators e business
  services Django aplicáveis, respeitando obrigatoriedade, normalização,
  unicidade, choices, permissões e regras administrativas. Exigir
  prévia, confirmação explícita, lote `ALL_OR_NOTHING`, erro em qualquer linha
  impede confirmação e rollback integral em falha transacional. Não tocar o
  estado técnico MON.
- **Dependências:** HOM-00; validar schema/migrations e constraints no branch
  canônico; contrato de autorização/auditoria; modelo e colunas XLSX
  adjudicados antes da homologação da planilha definitiva.
- **Estado comprovado:** não foi localizado importador XLSX no código
  inspecionado. O model atual declara unicidade em `patrimonio` e `serial`,
  nomes ativos sem distinção de caixa e MAC não nulo sem distinção de caixa;
  isso não determina sozinho a regra de matching completa nem o template.
- **Evidências de conclusão:** template/versionamento homologados após schema
  review; matriz de criação/atualização/conflitos; testes de preview,
  confirmação, validação de linha, autorização/auditoria, atomicidade e rollback
  no banco alvo; relatório de importação auditável sem segredos.
- **Aceite:** import válido só grava após confirmação; uma linha inválida ou
  conflito bloqueia o lote inteiro; erro no commit não deixa efeitos parciais;
  nenhuma coluna ID manual; nenhuma transição MON causada pela importação.
- **Reaproveitar:** `Camera`, forms/services/validators e auditoria existentes,
  após comprovar a origem canônica e cobertura real. Não criar modelo de campos
  por suposição.

Exportação está aprovada, mas continua `NON-BLOCKING`; não exige ID manual nem
autoriza reintroduzir coluna ID na planilha.

### HOM-03 — Preparação da VM

```text
STATUS = NOT_STARTED / VM READINESS UNVERIFIED
BLOCKING = YES
```

- **Objetivo:** preparar ambiente de homologação isolado, repetível e
  recuperável, sem chamá-lo de produção.
- **Escopo mínimo:** confirmar ownership/acesso da VM; separar configuração e
  secrets; database/schema e migrations; usuário/login/permissões; serviço web
  e controle explícito da execução do worker; logs/diagnósticos; backup/restore
  ou rollback básico; smoke tests mínimos e instruções de recuperação.
- **Dependências:** HOM-00; escolhas de topologia e persistência conforme
  `RUNTIME_TOPOLOGY_CONTRACT.md` e `PRODUCTION_PERSISTENCE_CONTRACT.md`;
  infrastructure owner e autorização operacional apropriada. A preparação da
  VM pode avançar parcialmente em paralelo, isoladamente, sem antecipar deploy.
- **Estado comprovado:** não existe evidência inspecionada nesta atividade de
  VM preparada, banco de homologação, migrations aplicadas, login, permissões,
  recuperação ou smoke na VM. Configuração local usa SQLite; H1 local não prova
  PostgreSQL. O H2 de PostgreSQL está bloqueado no host local por runtime e
  driver ausentes; executar H2 assim que infraestrutura isolada permitir.
- **Evidências de conclusão:** registro da configuração não secreta, alvo de
  banco isolado, migrations e schema verificados, contas/roles testadas, smoke
  de aplicação, prova de rollback/restore e prova de worker sem autoexecução
  inadvertida.
- **Aceite:** configuração segregada; mínimo privilégio; login e permissões
  validados; migrations aplicáveis/consistentes; restore/rollback executável;
  workers/probes não disparam automaticamente em massa; monitoramento inicia
  somente por autorização explícita e progressiva.
- **Reaproveitar:** contracts backend de autorização, persistência, topologia,
  runtime Worker e observabilidade; H1 local PASS como evidência limitada a
  SQLite sintético.

### HOM-04 — Abertura de homologação progressiva

```text
STATUS = BLOCKED / READINESS EVIDENCE NOT PRESENT
BLOCKING = GATE
```

Abrir somente com HOM-00 a HOM-03 aceitos e evidência arquivada. Gate bloqueante
inclui: UI inicial integrada e validada; cadastro/inventário utilizáveis;
importação XLSX e modelo homologado; matching/validação cadastral consistente;
prévia/confirmação/atomicidade; autorização e auditoria; banco e migrations;
VM isolada; login/permissões; smoke mínimo; recuperação/rollback; controle
explícito da execução automática do monitoramento. H2/PostgreSQL deve ser
executado quando infraestrutura isolada permitir e é requisito de evidência para
persistência PostgreSQL; H1 (110 testes SQLite temporário) não o substitui.

H3 de câmeras reais, credenciais reais, rede/firewall/VLAN e protocolos exige
autorização e plano de teste próprios; não é pré-condição para abrir a primeira
rodada de Inventário/UI. `HOMOLOGATION_OPEN != PRODUCTION_READY`; qualquer uso
externo ou carga real obedece aos gates de operação e aprovação próprios.

### Gates para entrada progressiva

| Gate | Critérios mínimos | Estado neste checkpoint |
|---|---|---|
| **G1 — INTEGRATION_GATE** | Branch isolada integrada; código e migrations coerentes; dependências resolvidas; regressões funcionais PASS. | `BLOCKED` / integração não executada |
| **G2 — DESIGN_QA_GATE** | Referência aprovada; screenshot renderizado sob condições equivalentes; comparação visual; correções materiais; aprovação humana. | `BLOCKED` / Design QA obrigatório, não executado |
| **G3 — HOMOLOGATION_ENTRY_GATE** | Frontend inicial funcional; importador XLSX validado; banco operacional na VM; login/permissões; logs e observabilidade mínima; backup/rollback; deploy verificável; monitoramento automático controlado. | `BLOCKED` / HOM-01..03 e evidências pendentes |

Para G2, registrar `REFERENCE_SCREENSHOT`, `RENDERED_SCREENSHOT`,
`VISUAL_DIFFERENCE_REPORT`, `CORRECTION_EVIDENCE` e
`HUMAN_VISUAL_APPROVAL`. Sem referência aprovada ou renderização real, o
resultado é `BLOCKED`; diferença visual material ou regressão funcional é
`FAIL`. Aprovação de HOM-01 exige Design QA, regressão funcional e aprovação
visual humana em `PASS`. G3 não depende de validação com câmeras reais (H3),
mas isso não autoriza monitoramento real ou produção.

Deploy integrado requer validação prévia do conjunto aplicável de HOM-01, HOM-02
e HOM-03, além dos gates de segurança e operação correspondentes.

```text
H1 = PASS / HERDADO / 110 TESTES / SQLITE TEMPORÁRIO
H2 = BLOCKED_BY_INFRASTRUCTURE / POSTGRESQL DESCARTÁVEL E DRIVER AUSENTES
H3 = NOT_STARTED / AUTORIZAÇÃO E PLANO PRÓPRIOS
```

### HOM-05 — Evolução funcional durante homologação

```text
STATUS = PLANNED / BACKLOG PRESERVED
BLOCKING_FOR_HOM_04 = NO
```

- **Objetivo:** implementar capabilities restantes e remediar achados enquanto
  a homologação progride, com cada alteração submetida aos contratos, gates e
  autorização próprios.
- **Escopo mínimo:** backlog abaixo, resultados de homologação, métricas de
  performance e problemas de integração; sem transformar evidência de
  homologação em autorização de produção.
- **Dependências:** HOM-04 aberto; priorização/adjudicação por atividade; dados
  de teste autorizados e controle de mudança.
- **Evidências/aceite:** cada slice com baseline, contrato, teste, gate integrado
  e atualização de continuidade; medir e classificar achados antes de mudar
  targets ou promover ambiente.
- **Reaproveitar:** contratos e código de branches pendentes somente depois de
  confirmar ancestor, diff, migration lineage e validation no baseline escolhido.

Backlog não bloqueante da abertura inicial: exportação; galeria de até três
imagens em ordem cronológica crescente no Camera Detail; ações manuais de captura
e importação de imagens; CAM-INT-04; rotação, holds/proteção e expurgo auditado
(contrato/validações pendentes); Central de Alertas interna, lifecycle e
deduplicação; detector de Worker independente; retenção MON de 24 meses após
encerramento; alertas resolvidos por 12 meses; logs técnicos por 30 dias;
imagens sob política de 12 meses com preservação e condições de expurgo;
integrações das branches restantes; performance observada durante a
homologação; auditoria e pendências corporativas. Nada disso fica marcado como
concluído por este plano. Quick Detail consome a última imagem ativa registrada
independentemente de proveniência. Rotação, holds, lifecycle de alertas e
expurgo permanecem sem autorização/contrato fechado; nenhum expurgo está incluído
nesta atividade.

### Cargas e medições da homologação

Planejar etapas de **50**, **500** e **2.300 câmeras**, avançando somente após
revisão dos resultados e autorização para a etapa seguinte. Para cada lote
registrar tempo de importação; latência da listagem; filtros/paginação; resposta
de Camera Detail; CPU/memória; banco; erros/logs; estabilidade. Fixtures são
sintéticas ou formalmente autorizadas. Não iniciar milhares de probes, não
habilitar autoexecução em massa e não acessar câmeras reais como efeito de carga
de inventário.

### Reconciliações contratuais requeridas

As seguintes decisões funcionais foram aprovadas pelo usuário para esta
sequência. Elas ainda precisam ser incorporadas pelas authorities especializadas
antes das atividades de implementação correspondentes; este mapa não substitui
esses contratos:

- **Retenção MON:** a decisão aprovada é 24 meses após `closed_at` para
  indisponibilidades encerradas. O contrato MON-HIST/auditoria registra lacuna
  de retenção; reconciliar prazo, transições vinculadas e elegibilidade antes
  de planejar expurgo. Sem expurgo nesta atividade.
- **Alertas e logs:** decisões aprovadas: alertas internos, 12 meses após
  resolução e logs técnicos por 30 dias. Lifecycle/contrato de alertas e destino
  efetivo/lifecycle de logs ainda faltam ou estão sem comprovação; formalizar
  regras antes de implementação/limpeza.
- **Imagens:** decisão aprovada de política de 12 meses deve ser reconciliada
  com IMG Domain/IMG-CAP e auditoria de persistência, incluindo holds,
  preservação, rotação, autoridade, elegibilidade e prova do expurgo físico.
  `retirada lógica` não é autorização para apagar bytes.
- **UI P3/P5:** a reconciliação Git registra P3 como `PROTOTYPE /
  VISUAL_REFERENCE` e P5 como `PRODUCTION_UI_SOURCE / NOT_INTEGRATED`; publicação
  ou aprovação em branch não prova integração. Histórico preservado; integrar
  seletivamente após diff, compatibilidade e gates.

As condições acima são decisões/requisitos, não evidência de implementação nem
autorização de expurgo. Para abertura inicial HOM-04, alertas, lifecycle de
imagens e retenção histórica permanecem não blockers, desde que controles de
segurança, preservação e operação não sejam comprometidos.

### Autoridades e próximo passo

- UI: `ARGOS_UI_V2_MASTER_PLAN.md`, `ARGOS_UI_V2_SCREEN_CENSUS.md`,
  `prototype/ui-v2/contracts/SCREEN_COVERAGE.md`, `SPRINTS_ARGOS_V5.md`,
  `ARGOS_UI_DESIGN_SYSTEM_INTEGRATION_SPEC_V1.md` e contrato Camera Detail da
  branch conforme adjudicação HOM-00.
- Importação/acesso: model/forms/validators correntes, contrato de
  autorização `contracts/backend/01_ACCESS_ROLES_AUTHORIZATION_CONTRACT.md` e
  trilha de auditoria; o modelo XLSX ainda não tem authority específica.
- Persistência/topologia/worker/imagens: `contracts/backend/production/`,
  `contracts/backend/monitoring/MONITORING_WORKER_RUNTIME_CONTRACT.md`,
  `contracts/backend/camera/CAM-INT-04_HTTP_SNAPSHOT_CONTRACT.md`,
  `contracts/backend/images/IMAGE_CAPTURE_INTEGRATION_CONTRACT.md` e
  `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md`.
- Auditoria de dados: `docs/auditoria/ARGOS-DATA-PERSISTENCE-CONTRACT-AUDIT.md`
  (WIP preexistente, manter como finding/source de reconciliação; não editar nem
  tratar como implementação ou nova autorização).

```text
H1 = PASS / 110 TESTS / ISOLATED TEMPORARY SQLITE
H2 = BLOCKED / DISPOSABLE POSTGRESQL RUNTIME AND DRIVER UNAVAILABLE LOCALLY
H3 = NOT_STARTED / REAL CAMERAS; OWN AUTHORIZATION REQUIRED
NEXT_ACTIVITY = ARGOS-HOM-00-INTEGRATION-FOUNDATION / PLANNED / NOT_AUTHORIZED
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_ACTIVITY
COMMIT = NOT_PERFORMED
PUSH = NOT_PERFORMED
MERGE = NOT_PERFORMED
```
