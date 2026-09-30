# P3-A — Cobertura final e evidência (2026-09-29)

DESIGN_SYSTEM_VERSION = 2.0.2
PERSISTED_SCREENSHOTS = 28 / 16 viewport defaults + 12 mobile state captures
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

Captures live at docs/prototype/ui-v2/evidence/screenshots/p3-a/. All 28 files
were checked for PNG signature, expected pixel dimensions, file presence, and
agreement between filename and capture metadata. Browser used Playwright with
Chrome, device scale factor 1, 100% zoom, and a request guard allowing only local
GET requests. No external request, non-GET request, or browser persistence was
observed.

| Tela | Viewports padrão | Estados móveis adicionais | Resultado |
|---|---:|---|---|
| Portal | 4/4 | empty, long | Sem overflow global; evidência persistida |
| Dashboard | 4/4 | empty, long | Sem overflow global; evidência persistida |
| Inventário | 4/4 | empty, loading, error, long, selected | Sem overflow global; tabela com scroll local; evidência persistida |
| Detalhe de Câmera | 4/4 | empty (history), error, long | Sem overflow global; evidência persistida |

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
