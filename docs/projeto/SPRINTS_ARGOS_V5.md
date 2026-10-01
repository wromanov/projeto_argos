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
CURRENT_PHASE = FASE C — Captura manual e gestão de imagens
CURRENT_PHASE_STATUS = FASE C EM_ANDAMENTO; UI V2 DOCUMENTED as a parallel track; Phase 0 and Batch A closed; pending visual scopes flow through approved prototypes
IMPLEMENTATION_AUTHORIZATION = NOT_GRANTED_BY_THIS_DOCUMENT
CURRENT_ACTIVITY = UI-V2-P1 — VISUAL STYLE LAB / NOT_STARTED / NOT_AUTHORIZED
LAST_COMPLETED_ACTIVITY = UI-V2-P0 — SCREEN CENSUS / CLOSED_PASS
LAST_COMPLETED_ACTIVITY_STATUS = CLOSED / DOCUMENTARY / PROJECT_STATE_UPDATE PASS
NEXT_CANDIDATES = UI-V2-P1 — VISUAL STYLE LAB; IMG-04; MON-AVAIL-02 (recommendation)
NEXT_CANDIDATES_STATUS = UI-V2-P1 NOT_STARTED / NOT_AUTHORIZED; IMG-04 NOT_AUTHORIZED; MON-AVAIL-02 RECOMMENDED / NOT_AUTHORIZED; Quick Detail visual baseline approved
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
COMMIT = NOT AUTHORIZED / NOT PERFORMED
PUSH = NOT AUTHORIZED / NOT PERFORMED
```

O detalhe normativo e a matriz de decisões abertas estão em
`docs/projeto/contracts/backend/00_BACKEND_CONTRACT_REGISTRY.md` e nos
contratos indexados. `ARGOS_IMAGE_DOMAIN_CONTRACT_V1.md` permanece a authority
canônica do domínio de imagens. Esta atividade documenta capacidades observadas
e fronteiras; não reordena silenciosamente IMG-04/MON-AVAIL-02, não autoriza
implementação posterior e não substitui validação de produção. Próxima atividade
de backend: adjudicação humana deste baseline antes de escolher implementação.
