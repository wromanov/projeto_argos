# P3-A — Coverage local

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
