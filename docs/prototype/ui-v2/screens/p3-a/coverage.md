# P3-A — Cobertura final e evidência (2026-09-29)

## Aprovação humana — SCR-DASH-001 (2026-09-29)

SCR-DASH-001_VISUAL_REVIEW = PASS
HUMAN_VISUAL_APPROVAL = PASS
SCR-DASH-001_STATUS = USER_APPROVED / FROZEN
TECHNICAL_READY_FOR_REVIEW = YES
F03 = CLOSED
F04 = CLOSED
KPI_PATTERN = APPROVED / FREEZE
PAGE_HEADER = APPROVED / inclui adaptação mobile do botão
DESKTOP = PASS / 1920x1080, 1440x900, 1366x768
MOBILE = PASS / 390x844
MOBILE_READING_ORDER = Situação → Monitoramento → Atividade → Câmera / aceita
MOBILE_NAVIGATION = 5/5 itens visíveis a 390x844; scroll de 320px aceito por teclado e toque
ACTIVITY_COMPLETION_PERCENT = 100%
ACTIVITY_COMPLETE = YES / escopo desta adjudicação do Dashboard
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md, seção 37
DASHBOARD_FREEZE = ACTIVE
OBSERVATION = timestamp em Atividade pode quebrar entre data e hora em 1366x768
OBSERVATION_STATUS = NON_BLOCKING / sem patch local; revisar com dataset representativo no pattern Activity/List
PROTOTYPE_CONTENT = aviso demonstrativo e indicador de superfície planejada permanecem protótipo
PRODUCTION_CHANGED = NO
FINAL_VERDICT = PASS

NEXT_SURFACE = SCR-INV-001 / Inventário
NEXT_SURFACE_BASIS = próxima tela P3-A no Screen Census
NEXT_SURFACE_VISUAL_APPROVAL = PENDING / gate independente


## SCR-INV-001 — revisão técnica de navegação e evidência (2026-09-29)

SCR-INV-001_STATUS = TECHNICAL_READY_FOR_REVIEW
FINDING = label Eventos parcialmente cortada em 390x844
CAUSE = soma do padding inline excedia a largura visível da navegação móvel
RESOLUTION = ajuste local da tela; padding inline de 8px, reserva final de scroll de 8px, dica condicional e foco revela link
SHARED_DESIGN_SYSTEM_CHANGED = NO
SCR_DASH_001_CHANGED = NO / frozen
VIEWPORTS = 1920x1080 PASS; 1440x900 PASS; 1366x768 PASS; 390x844 PASS
390_NAV = 5/5 labels fully visible; targets remain 44px
320_NAV = scroll cue visible; keyboard focus and touch reach Eventos
320_KEYBOARD = PASS / Eventos focused; 63px max scroll; label fully visible
320_TOUCH = PASS / 63px max scroll reached; label fully visible
GLOBAL_DOCUMENT_OVERFLOW = NONE / all four viewports
MOBILE_TABLE = 921px inside 360px scroller / no page overflow
CONSOLE_ERRORS = 0
PAGE_ERRORS = 0
DENIED_REQUESTS = 0
PERSISTED_SCREENSHOTS = 40 total / 4 new captures
USER_VISUAL_APPROVAL = PENDING / Inventory review is independent
ACTIVITY_COMPLETION_PERCENT = 85%
ACTIVITY_COMPLETE = NO
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md section 38
NEXT_SURFACE = SCR-CAM-DETAIL-001 after Inventory approval, by Screen Census order

Four new top-of-page default captures use 100% zoom and device scale factor 1.
They are stored in docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-29/.
The prior mobile capture was preserved. Request guard allowed only local GET;
there were no console/page errors or denied requests. Existing P3-A coverage for
Inventory states and row heights (127px default / 217px long) remains in the
preceding family QA record.


## Registro técnico pré-aprovação humana — SCR-DASH-001 F03/F04 (2026-09-29)

DESIGN_SYSTEM_VERSION = 2.0.2 / unchanged
PERSISTED_SCREENSHOTS = 36 / 16 viewport defaults + 12 mobile state captures + 8 Dashboard refinements
NEW_CAPTURES = 4 / F03-F04
F03 = PASS / independent desktop stacks; card heights remain content-sized
F04 = PASS / 390px labels fully visible; narrow layout remains scrollable, signaled, keyboard/touch reachable
TECHNICAL_READY_FOR_REVIEW = YES
PRODUCT_DESIGN_DESIGN_QA = PASS
FINAL_VERDICT = PASS_WITH_FINDINGS / findings resolved
USER_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = NOT PERFORMED / outside this card
ACTIVITY_COMPLETE = NO / awaiting human visual review
GLOBAL_HORIZONTAL_OVERFLOW = NONE / all four Dashboard viewports
CONSOLE_ERRORS = 0 / PAGE_ERRORS = 0 / DENIED_REQUESTS = 0
KPI_HEADER_DS_PRODUCTION_REGRESSION = NONE

| Viewport | Fluxo e medidas | Navegação | Resultado |
|---|---|---|---|
| 1920×1080 | Pilha esquerda: Situação → Atividade; direita: Monitoramento → Câmera. Cards com 209px/341px; gap vertical de 16px; sem stretch | desktop | PASS; sem overflow |
| 1440×900 | Mesmo fluxo em colunas independentes; 136px de espaço morto removidos sob Situação | desktop | PASS; sem overflow |
| 1366×768 | Mesmo fluxo; alturas naturais de 209px/341px | desktop | PASS; sem overflow |
| 390×844 | Ordem móvel preservada: Situação → Monitoramento → Atividade → Câmera | 5/5 itens, inclusive Eventos, totalmente visíveis; alvos de 44px | PASS; sem overflow |
| 320px (stress complementar) | Ordem móvel preservada | rolagem horizontal com aviso visível; Tab e toque alcançam Eventos e revelam o rótulo integral | PASS |

A matriz mobile usa a ordem semântica que já existia na fonte. O contrato census
não prescreve uma sequência mais detalhada para estes quatro cards. O reparenting
responsivo em desktop cria as duas pilhas sem alterar a ordem de leitura móvel.
A navegação continua horizontal e rolável conforme o contrato do harness; o
indicador só aparece quando necessário, e foco por teclado desloca o item para
a área visível.

O espaço anterior entre o fim de Situação (y=586) e a próxima linha (y=738)
era 152px. A pilha separada inicia Atividade após o gap intencional de 16px,
removendo 136px de área vazia. Situação permanece com 209px e Monitoramento
com 341px, sem equalização forçada.

Os textos “Valores demonstrativos...” e “Meu Perfil · superfície planejada”
estão identificados no protótipo como aviso demonstrativo e superfície planejada.
KPI tiles 220×77px, cabeçalho/ação, tokens, primitives compartilhados, outras
telas, Quick Detail, coverage global e produção não mudaram.

Novas capturas: SCR-DASH-001__1920x1080__refined-f03-f04__default.png,
SCR-DASH-001__1440x900__refined-f03-f04__default.png,
SCR-DASH-001__1366x768__refined-f03-f04__default.png e
SCR-DASH-001__390x844__refined-f03-f04__default.png. Total persistido da
família P3-A: 36 PNGs, verificados por nome, presença, assinatura e dimensão.
A rodada foi feita em Chrome/Playwright, zoom 100%, escala 1, com somente GET
local; 0 erros de console/página, requisições negadas ou externas, requests
não-GET, gravações de persistência ou overflow global.


## Registro histórico anterior — cobertura F01/F02
DESIGN_SYSTEM_VERSION = 2.0.2
PERSISTED_SCREENSHOTS = 32 / 16 viewport defaults + 12 mobile state captures + 4 refined SCR-DASH-001 captures
VIEWPORTS = 390x844, 1366x768, 1440x900, 1920x1080
GLOBAL_HORIZONTAL_OVERFLOW = NONE / 16 of 16 combinations
STATE_FIXTURE_MISMATCH = NONE
INVALID_PNG_OR_DIMENSION_MISMATCH = NONE
CONSOLE_ERRORS = 0
EXTERNAL_REQUESTS = 0
NON_GET_REQUESTS = 0
PERSISTENCE_WRITES = NONE
ACCESSIBILITY_BASELINE = PASS_WITH_LIMITS / no WCAG conformance claim
TECHNICAL_READY_FOR_REVIEW = YES
USER_VISUAL_APPROVAL = PENDING
PROJECT_STATE_UPDATE = NOT PERFORMED / excluded by the user card
ACTIVITY_COMPLETE = NO / awaiting human visual review

Captures live at docs/prototype/ui-v2/evidence/screenshots/p3-a/. All 32 files
were checked for PNG signature, expected pixel dimensions, file presence, and
agreement between filename and capture metadata. Browser used Playwright with
Chrome, device scale factor 1, 100% zoom, and a request guard allowing only local
GET requests. No external request, non-GET request, or browser persistence was
observed.

| Tela | Viewports padrão | Estados móveis adicionais | Resultado |
|---|---:|---|---|
| Portal | 4/4 | empty, long | Sem overflow global; evidência persistida |
| Dashboard | 4/4 + 4 refinadas | empty, long | Sem overflow global; evidência persistida |
| Inventário | 4/4 | empty, loading, error, long, selected | Sem overflow global; tabela com scroll local; evidência persistida |
| Detalhe de Câmera | 4/4 | empty (history), error, long | Sem overflow global; evidência persistida |

## Cartão atual — refinamento desktop do Dashboard (2026-09-29)

STARTING_HEAD = d8600021a8aa9ab809a03b416b0a6acfd5702179
F01 = RESOLVED / painéis de resumo dimensionados pelo conteúdo
F02 = RESOLVED / ação Abrir Inventário integrada ao cabeçalho
TARGETED_DESIGN_QA = PASS / comparação visual pareada com o baseline
NEW_CAPTURES = 4 / total da pasta P3-A = 32
GLOBAL_HORIZONTAL_OVERFLOW = NONE / 4 viewports do Dashboard
CONSOLE_ERRORS = 0 / page errors = 0 / denied requests = 0
USER_VISUAL_APPROVAL = PENDING
ACTIVITY_COMPLETE = NO

| Viewport | Sumário operacional | Sumário monitoramento | Início da próxima linha |
|---|---:|---:|---:|
| 1366×768 | 209px | 341px | y=738 |
| 1440×900 | 209px | 341px | y=738 |
| 1920×1080 | 209px | 341px | y=738 |
| 390×844 | fluxo móvel original | fluxo móvel original | sem overflow horizontal |

As capturas refined/default preservam os screenshots baseline e registram
somente a nova execução. O cap de 1280px e o gap de 32px no cabeçalho são
aplicados apenas a partir de 1600px; a tile métrica permanece em 220×77px.
Não houve mudança no conteúdo, na navegação, nos tokens ou no Design System.

---
## Inventário móvel e interação

- Em 390×844, o scroller local tem 360px e contém a tabela de 921px com oito
  colunas; o documento não ganha overflow horizontal.
- A linha padrão mede 127px; na fixture longa, página 2, a linha longa mede 217px.
- Filtro sem resultados apresenta estado vazio; limpar filtros restaura resultados;
  paginação alcança a página 2.
- Enter seleciona uma linha e atualiza o anúncio de status. Tab alcança a ação
  nomeada; a ação fica visível após rolagem horizontal. A captura selected registra
  esse estado.
- Quick Detail segue o baseline protegido; não houve alteração de design.

## Acessibilidade e escopo

Baseline observado: idioma pt-BR, título da página, um H1, landmarks principais
nomeados, controles rotulados, imagens com texto alternativo e seleção por teclado.
Isso não é uma declaração de conformidade WCAG. A cobertura de console terminou com
zero erros.

PROJECT_STATE.md, SCREEN_COVERAGE global, demais famílias e produção não foram
alterados. A aprovação visual humana está pendente e é o próximo gate.
ACTIVITY_COMPLETE permanece NO até esse gate; esta atividade não atualiza o snapshot global.

---
# P3-A — Coverage local

## Checkpoint histórico pós-propagação DS 2.0.2 — captura ainda pendente (superado em 2026-09-29)

```text
REMOTE_HEAD_BEFORE_PROPAGATION = 1f833aed523420db47ba06faa5d5cf5cc114de0b
DS_PATCH_SOURCE_COMMIT = 8a480a50a338ef3961a242e9dce0ccaf09cdf49b
P3_A_DS_2_0_2_PROPAGATION_COMMIT = d0c495cea2a302b70845e38e97225dd8daf5c5d2
PROPAGATION_MODE = CHERRY_PICK_WITH_ROOT_DOCUMENT_EXCLUSION
ROOT_DOCUMENT_EXCLUDED = DSCR-UIV2-002-MOBILE-TABLE-READABILITY.md
EXCLUSION_REASON = ROOT-owned canonical governance artifact absent from family lineage; P3-A consumes shared implementation without duplicating ROOT governance
SHARED_DS_IMPLEMENTATION_PROPAGATED = YES
DESIGN_SYSTEM_VERSION = 2.0.2
CHERRY_PICK_IN_PROGRESS = NO
DCR_FILE_IN_P3_A = ABSENT
CANONICAL_DCR_IN_ORIGIN_MASTER = PRESENT
ROOT_OWNERSHIP_PRESERVED = YES
CHECKOUT_ERROR_CORRECTED = YES
CANONICAL_MASTER_CHANGED = NO
STATE_QA = PASS
RESPONSIVE_QA = PASS / four screens × four viewports
INVENTORY_MOBILE_ROW_HEIGHT = 127px default / 217px long fixture / 283px before DS 2.0.2
ACCESSIBILITY_BASELINE = PASS_WITH_LIMITS
NODE_PLAYWRIGHT_AVAILABLE = NO / node and npm are not installed in PATH
CONSOLE_LOG_CAPTURE = NOT_AVAILABLE
EVIDENCE_CAPTURE_STATUS = BLOCKED / no persistent screenshot destination in available browser capture interface
TECHNICAL_READY_FOR_REVIEW = NO / persisted evidence gate remains open
PRODUCT_DESIGN_DESIGN_QA = BLOCKED
DESIGN_QA_COMPLETE = NO
USER_VISUAL_APPROVAL = PENDING
P3_A_FINAL_COMPLETION_COMMIT = NOT_CREATED
BLOCKED_CHECKPOINT_COMMIT = AUTHORIZED / family-owned records only
PUSH_AUTHORIZED = YES / codex/ui-v2-p3-a-core-inventory only
```

| Área | Resultado observado |
|---|---|
| Portal, Dashboard, Inventário, Detalhe — 390×844, 1366×768, 1440×900, 1920×1080 | 16/16 sem overflow horizontal global em `html`/`body` |
| Estados | Portal/Dashboard default, empty, long; Inventário default, empty, loading, error, long; Detalhe default/stale, history empty, error, long |
| Inventário em 390×844 | wrapper com 360px úteis; tabela 920px com rolagem local; linha default 127px; fixture longa 217px; antes do DS 2.0.2 a linha padrão media 283px |
| Inventário funcional | busca vazia, limpar filtros, página 2, seleção por Enter, link de ação alcançável por teclado e Quick Detail protegido verificados |
| Acessibilidade baseline | `pt-BR`, título, um H1, main/nav nomeados, controles rotulados, imagens com alt e seleção por teclado; não representa certificação WCAG |
| Evidência visual | comparação de referência e implementação inspecionada em Edge, sem PNG nomeado persistido; Product Design permanece bloqueado |

O commit de propagação contém apenas `harness.js`, `index.html` e os quatro CSS
canônicos compartilhados. O arquivo ROOT DCR está ausente no HEAD P3-A e presente
em `origin/master`. As quatro páginas P3-A agora identificam DS 2.0.2 no meta e
no rodapé; nenhum override de CSS específico de família foi adicionado.

O preview HTTP local executa as páginas em Edge. A interface disponível mostra
capturas na sessão, mas não expõe destino de arquivo; o diretório oficial de
evidências P3-A permanece sem as capturas requeridas. `TECHNICAL_READY_FOR_REVIEW`
e `DESIGN_QA_COMPLETE` ficam `NO` até persistir os PNGs e concluir revisão visual
humana. O console não foi capturado nesta sessão.
---

## Checkpoint de retomada após DS 2.0.1 (2026-09-28)

```text
REMOTE_HANDOFF_RECOVERY = PASS / 2ca597826af7b32c884f4efd91cc49381ee646a5
FAN_OUT_BASE_COMMIT = 9943e20d9b1e04159e067c72aa4dd70eab2bdb36
P3_A_HEAD_AFTER_DS_PATCH = cc43b1921f6d8dbb1de7aa32122af90c2ca45706
DS_PATCH_WORK_COMMIT = 8121ed38cc15e1ff6e72cb46bbb2ca865100bce0
DS_PATCH_PROPAGATION = PASS / exact commit; no master merge
DESIGN_SYSTEM_VERSION = 2.0.1
F01_STATUS = RESOLVED_BY_DS_2_0_1
F01_REGRESSION = PASS
F02 = OPEN / mobile inventory table readability / ROOT adjudication required
F03 = OPEN / evidence capture mechanism blocked
STATE_QA = PASS / visible state isolation and hidden computed display checked in HTTP preview
RESPONSIVE_QA = FAIL_WITH_FINDING / inventory mobile row height 283px; shared table sizing
ACCESSIBILITY_BASELINE = PASS_WITH_FINDINGS
PRODUCT_DESIGN_DESIGN_QA = BLOCKED
DESIGN_QA_COMPLETE = NO
EVIDENCE_PATH = docs/prototype/ui-v2/evidence/screenshots/p3-a/
EVIDENCE_SCREENSHOTS = NOT_SAVED / browser policy blocked screenshot download
EVIDENCE_CAPTURE_STATUS = BLOCKED
DS_CHANGE_REQUESTS = DSCR-UIV2-002-MOBILE-TABLE-READABILITY / ROOT_REVIEW_REQUIRED
TECHNICAL_READY_FOR_REVIEW = NO
P3_A_FINAL_COMPLETION_COMMIT = NOT_CREATED / technical gate did not pass
BLOCKED_CHECKPOINT_COMMIT = AUTHORIZED / family-owned records only; SHA reported after creation
PUSH_AUTHORIZED = YES / codex/ui-v2-p3-a-core-inventory only
USER_VISUAL_APPROVAL = PENDING
```

```text
PORTAL = QA EXECUTED
DASHBOARD = QA EXECUTED
INVENTORY = QA EXECUTED WITH F02
CAMERA_DETAIL = QA EXECUTED
QUICK_DETAIL = PROTECTED / INHERITED
```

O teste do inventário em `?fixture=long`, página 2, confirmou que os registros
longos não causam overflow global; a tabela permanece em um contêiner rolável.
O problema observado é densidade: em 390px, a tabela tem 859px de largura,
mas a coluna de ações fica com 61px e cada linha mede 283px. O finding depende
do sizing do pattern compartilhado. Não foi aplicado workaround local.

O navegador exibiu as quatro telas nos viewports pedidos, mas a gravação de
PNG no caminho canônico falhou porque a política do browser recusou navegação
para `data:` e proíbe contornar essa recusa. Nenhuma captura nomeada está
armazenada no diretório de evidências. Por isso, as telas ainda não atingem
`TECHNICAL_READY_FOR_REVIEW`; o commit final permanece bloqueado. O checkpoint
WIP e o push desta branch estão autorizados para preservar o estado.

Snapshot de implementação da família P3-A. Este relatório pertence à família; não substitui nem altera `contracts/SCREEN_COVERAGE.md`.

```text
FAN_OUT_BASE_COMMIT = 9943e20d9b1e04159e067c72aa4dd70eab2bdb36
BRANCH = codex/ui-v2-p3-a-core-inventory
WORKTREE = C:\Users\walacedelgado\PycharmProjects\projeto_argos_ui_v2_p3_a
INITIAL_HEAD = 9943e20d9b1e04159e067c72aa4dd70eab2bdb36
DEDICATED_LINKED_WORKTREE = YES
OWNERSHIP_VALIDATED = YES
OWNERSHIP_CONFLICTS = NONE
DESIGN_SYSTEM_VERSION = 2.0.0
DESIGN_SYSTEM_MODIFIED = NO
PRODUCT_DESIGN_STATUS = AVAILABLE
PRODUCT_DESIGN_GET_CONTEXT = COMPLETE
PRODUCT_DESIGN_DESIGN_QA = BLOCKED_BY_DS_CHANGE
DESIGN_QA_COMPLETE = NO
USER_VISUAL_APPROVAL = PENDING
```

| SCREEN_ID | PROTOTYPE_PATH | Ownership | Implementação | Estados/fixtures previstos | Render/responsivo/evidência | Status |
|---|---|---|---|---|---|---|
| SCR-PORTAL-001 | `docs/prototype/ui-v2/screens/p3-a/scr-portal-001.html` | P3-A | Implementada | `default`, `empty`, `long` | `default` renderizado no Edge; estado vazio também visível | BLOCKED_BY_DS_CHANGE |
| SCR-DASH-001 | `docs/prototype/ui-v2/screens/p3-a/scr-dash-001.html` | P3-A | Implementada | `default`, `empty`, `long` | `default` renderizado no Edge; painel vazio também visível | BLOCKED_BY_DS_CHANGE |
| SCR-INV-001 | `docs/prototype/ui-v2/screens/p3-a/scr-inv-001.html` | P3-A | Implementada | `default`, `empty`, `loading`, `error`, `long`; hover, focus e seleção | `default` renderizado no Edge; resultados, empty, loading e error simultâneos | BLOCKED_BY_DS_CHANGE |
| SCR-CAM-DETAIL-001 | `docs/prototype/ui-v2/screens/p3-a/scr-cam-detail-001.html` | P3-A | Implementada | `default`, `empty` (histórico), `error`, `long`; STALE pela fixture default CAM-DEMO-0103 | `default` renderizado no Edge; histórico vazio também visível | BLOCKED_BY_DS_CHANGE |
| SCR-CAM-QUICK-001 | INHERITED; sem novo arquivo | P3-A | Não alterada | Baseline existente | Protegida; sem evidência nova | PROTECTED / INHERITED |

`loading` e `error` do Dashboard; `loading` da Detail; `loading` e `error` do Portal não estão declarados para essas superfícies no coverage canônico. STALE não é um novo valor de `?state=`: é o qualificador de frescor da câmera demonstrativa CAM-DEMO-0103.

## Implementação

- Cada tela nova importa diretamente os quatro arquivos canônicos em `static/css/ui-v2/`; nenhum CSS local ou componente substituto foi criado.
- O protótipo usa `fixtures/p3-a-camera-inventory.json`, dados fictícios estáveis e fetch apenas do JSON estático local. Não há query GET, API, autenticação, persistência, lógica de domínio ou serviço de imagem.
- Inventário preserva todas as colunas em tabela com rolagem horizontal contida, informa essa estratégia junto à tabela e oferece filtros no cliente, resumo, chips de filtros, paginação, seleção por mouse/teclado e caminhos separados para Detail e Quick Detail protegido.
- Quick Detail apenas aponta ao registro protegido existente em `screens/index.html`; não há reprodução de drawer/dialog nem mudança do baseline.
- Câmera sem imagem ou dado de rede permanece identificada como indisponível/não informado; nenhuma captura, endereço IP operacional ou informação sensível foi fabricada.
- Detalhe mantém situação operacional, saúde do monitoramento, completude e frescor como conceitos separados. Links para superfícies de outras famílias apontam aos placeholders canônicos.

## Validação executada

| Verificação estática | Resultado |
|---|---|
| Ownership, paths e HEAD inicial | PASS |
| JSON da fixture e contagem básica | PASS |
| JavaScript — parse de sintaxe | PASS; execução funcional não verificada |
| Classes HTML contra CSS canônico | PASS |
| Referências relativas `href`/`src` | PASS |
| Valores de rede em branco nas fixtures | PASS |
| Renderização HTTP no Edge; `default` das quatro novas telas inspecionado | PASS PARCIAL — colisão `hidden`/`display` observada nas quatro |
| Renderização dos demais estados isolados e interações no browser | BLOCKED_BY_DS_CHANGE |
| Viewports 1920×1080, 1440×900, 1366×768 e 390×844 a 100% | PENDING |
| Over-stretch, overflow, densidade e responsividade da tabela | PENDING |
| Baseline de acessibilidade em runtime | PENDING |
| Product Design `get-context` | COMPLETE — contratos, foundation, Style Lab C e contexto factual usados |
| Product Design `design-qa` | PARTIAL/BLOCKED_BY_DS_CHANGE; finding F-01 registrado em `design-qa.md` |
| Screenshots/evidence nomeadas e persistidas | PENDING; diretório de família: `docs/prototype/ui-v2/evidence/screenshots/p3-a/` |

`TECHNICAL_READY_FOR_REVIEW = NO`. A renderização observada demonstra que variantes marcadas `hidden` permanecem visíveis quando recebem regras de `display` do Design System. O gate de estado impede a conclusão das quatro telas; nenhum workaround local será criado para contornar o contrato de DS compartilhado. Nenhuma aprovação humana está implícita.

## DS_CHANGE_REQUEST

```text
CHANGE = Fazer com que o estado HTML nativo [hidden] prevaleça nos componentes/patterns canônicos com regras display, quando o harness alterna variantes de tela.
REASON = No preview HTTP do Portal em ?state=default, o painel principal e o estado de acesso vazio aparecem simultaneamente. O harness oculta variantes via elemento.hidden; regras author display dos seletores de pattern/componente prevalecem sobre a apresentação user-agent de [hidden].
AFFECTED_COMPONENTS = Tratamento de [hidden] nos patterns/componentes com display, observado em .argos-state, .argos-two-column, .argos-alert e .argos-docs-nav a; verificar cobertura completa dos componentes canônicos.
AFFECTED_SCREENS = SCR-PORTAL-001, SCR-DASH-001, SCR-INV-001, SCR-CAM-DETAIL-001; revalidar os demais consumidores P3 do harness após resolução.
VERSION_IMPACT = Design System está fixado em 2.0.0; versão/patch e migração requerem decisão do owner do Design System.
USER_REAPPROVAL_REQUIRED = YES
BLOCKED_BY_DS_CHANGE = required state coverage and design QA for all four new P3-A screens
```

```text
ROOT_OWNED_FILES_CHANGED = NO
CROSS_FAMILY_FILES_CHANGED = NO
PRODUCTION_CHANGED = NO
PRODUCTION_UI_V2_INTEGRATION_STARTED = NO
UI_V2_CSS_REFERENCED_BY_PRODUCTION = NO
DS_CHANGE_REQUESTS = 1
BLOCKED_BY_DS_CHANGE = SCR-PORTAL-001, SCR-DASH-001, SCR-INV-001, SCR-CAM-DETAIL-001
ROOT_CHANGE_REQUESTS = 0
COMMIT = NO — gates técnicos visuais ainda pendentes
MERGE_PERFORMED = NO
PUSH_PERFORMED = NO
```

## 39. SCR-INV-001 — refinamento direcionado e adjudicação da tabela (2026-09-30)

Este registro atualiza somente o Inventário após a revisão humana. As entradas
antigas que o marcavam bloqueado por F-01 são históricas: a semântica `hidden`
do Design System 2.0.2 já está integrada nesta branch. O novo finding F06 é
visual e aguarda adjudicação humana; nenhuma mudança no pattern da tabela foi
feita.

```text
SCREEN_ID = SCR-INV-001
STATUS = TECHNICAL_READY_FOR_REVIEW / PASS_WITH_FINDING
ACTIVITY_COMPLETION_PERCENT = 95% / technical review package ready; human F06 adjudication pending
F05 = RESOLVED / mobile advanced filters use an accessible button disclosure
SEARCH_ALWAYS_VISIBLE_MOBILE = YES
ADVANCED_FILTERS_PROGRESSIVE_DISCLOSURE = YES / all 8 controls retained
FILTERS_REMOVED = NO
F06_TABLE_PATTERN = KEEP_HORIZONTAL_TABLE_SCROLL / visual discoverability finding open
TABLE_WIDTH_AT_390 = 924.3px
SCROLLER_WIDTH_AT_390 = 360px
MAX_HORIZONTAL_MOVEMENT_AT_390 = 564px
SCROLLED_COLUMNS_AND_ACTIONS = VISIBLE / later headers and both actions remain legible
TABLE_SCROLL_HELP_VISIBLE_AT_ENTRY = NO / helper falls below the initial viewport
MOBILE_TABLE_VISUAL_VERDICT = FINDING / ask for adjudication before changing table pattern
F07 = RESOLVED / one concise selection status line; semantic table caption retained
F08 = RESOLVED / user-facing labels are “Visão rápida” and “Ver detalhes”
DESIGN_SYSTEM_CHANGED = NO
DASHBOARD_CHANGED = NO
PRODUCTION_CHANGED = NO
BACKEND_CHANGED = NO
VIEWPORT_1920x1080 = PASS
VIEWPORT_1440x900 = PASS
VIEWPORT_1366x768 = PASS
VIEWPORT_390x844 = PASS
DESKTOP_FILTER_GEOMETRY_DELTA = 0px for all 9 controls and “Limpar” at all 3 desktop widths
GLOBAL_HORIZONTAL_OVERFLOW = NO
CONTENT_CLIPPED = NO
MOBILE_NAV_REGRESSION = NO / all five links visible
CONSOLE_ERRORS = 0
PAGE_ERRORS = 0
FAILED_OR_EXTERNAL_REQUESTS = 0
HUMAN_VISUAL_APPROVAL = PENDING
READY_FOR_USER_REVIEW = YES
FINAL_VERDICT = PASS_WITH_FINDING / F06
```

### Evidências desta revisão

As quatro capturas padrão e as duas posições da tabela foram persistidas em
`docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-30/`:

- `SCR-INV-001__1920x1080__default__default.png`
- `SCR-INV-001__1440x900__default__default.png`
- `SCR-INV-001__1366x768__default__default.png`
- `SCR-INV-001__390x844__default__default.png`
- `SCR-INV-001__390x844__default__default__table-mobile-start.png`
- `SCR-INV-001__390x844__default__default__table-mobile-scrolled.png`

F06: a tabela continua legível quando deslocada até as colunas posteriores,
incluindo situação inicial e ações no estado deslocado. Porém, o início não
mostra uma barra horizontal persistente e a orientação para deslizar fica depois
do conteúdo; o recorte parcial da coluna seguinte é a única pista no primeiro
estado. O padrão de tabela permanece intacto enquanto aguarda a decisão do
usuário sobre essa descoberta visual.
