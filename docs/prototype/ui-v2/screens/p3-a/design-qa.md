# P3-A — Product Design / Design QA final (2026-09-29)

## Adjudicação humana e freeze — SCR-DASH-001 (2026-09-29)

SCR-DASH-001_VISUAL_REVIEW = PASS
HUMAN_VISUAL_APPROVAL = PASS
SCR-DASH-001_STATUS = USER_APPROVED
F03 = CLOSED
F04 = CLOSED
TECHNICAL_READY_FOR_REVIEW = YES
ACTIVITY_COMPLETION_PERCENT = 100%
ACTIVITY_COMPLETE = YES / atividade restrita a SCR-DASH-001
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md, seção 37
DASHBOARD_FREEZE = ACTIVE
KPI_PATTERN = APPROVED / FREEZE
PAGE_HEADER = APPROVED / desktop e ação mobile
VIEWPORTS = 1920x1080 PASS; 1440x900 PASS; 1366x768 PASS; 390x844 PASS
MOBILE_READING_ORDER = Situação → Monitoramento → Atividade → Câmera / aceita
MOBILE_NAVIGATION = todos os itens visíveis em 390x844; scroll em 320px aceito por teclado/toque
OBSERVATION = timestamp de Atividade pode separar data e hora em 1366x768
OBSERVATION_SEVERITY = NON_BLOCKING
OBSERVATION_FOLLOW_UP = avaliar pattern Activity/List com dataset representativo; sem patch em SCR-DASH-001
FINAL_VERDICT = PASS

A aprovação congela o Dashboard. Novas mudanças dependem de novo requisito
funcional, mudança aprovada de Design System, finding de regressão ou integração
produtiva. O conteúdo demonstrativo e o indicador de perfil planejado continuam
restritos ao protótipo.

NEXT_SURFACE = SCR-INV-001 / Inventário de câmeras
NEXT_SURFACE_BASIS = próxima entrada do Screen Census após Dashboard
NEXT_SURFACE_VISUAL_APPROVAL = PENDING


## SCR-INV-001 — próxima revisão de superfície (2026-09-29)

PRODUCT_DESIGN_DESIGN_QA = PASS / targeted navigation correction and four-viewport evidence
SCR-INV-001_STATUS = TECHNICAL_READY_FOR_REVIEW
USER_VISUAL_APPROVAL = PENDING
VIEWPORTS = 1920x1080, 1440x900, 1366x768, 390x844
ZOOM = 100% / DEVICE_SCALE_FACTOR = 1
FINDING = Eventos label was clipped by the mobile nav edge at 390x844
CAUSE = link padding plus gaps exceeded the available visible nav width
RESOLUTION = screen-local responsive padding, trailing scroll room, conditional instruction, focus reveal
390x844 = five nav items fully visible; page width equals viewport
320px = horizontal scroll remains usable; hint, keyboard focus, and touch gesture pass
GLOBAL_OVERFLOW = NONE
CONSOLE_ERRORS = 0 / PAGE_ERRORS = 0 / DENIED_REQUESTS = 0
SHARED_DESIGN_SYSTEM_CHANGED = NO
DASHBOARD_CHANGED = NO / frozen
PERSISTED_EVIDENCE = 4 fresh Inventory captures, old evidence preserved
HUMAN_VISUAL_APPROVAL = PENDING / does not inherit Dashboard approval
ACTIVITY_COMPLETION_PERCENT = 85%
ACTIVITY_COMPLETE = NO

The mobile table remains in its existing local horizontal scroller: 921px table
inside 360px at 390x844, with no document overflow. The default mobile evidence
was recaptured from scroll position zero. The previous off-position capture
remains preserved and is not treated as the current top-of-page review image.

Review captures:
- docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-29/SCR-INV-001__1920x1080__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-29/SCR-INV-001__1440x900__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-29/SCR-INV-001__1366x768__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-29/SCR-INV-001__390x844__default__default.png

NEXT_SURFACE = SCR-CAM-DETAIL-001 after Inventory approval, following Screen Census roster order

## Registro técnico pré-aprovação humana — SCR-DASH-001 F03/F04 (2026-09-29)

**final result: passed with findings resolved**

BASELINE = commit fb3b2090ab48d164cd320c004e904109038a5674
IMPLEMENTATION = SCR-DASH-001 / page-local responsive refinement
VIEWPORTS = 1920×1080, 1440×900, 1366×768, 390×844
ZOOM = 100% / DEVICE_SCALE_FACTOR = 1
F03 = PASS / independent desktop columns remove the operational row's dead whitespace
F04 = PASS / mobile navigation is fully readable at 390px and reachable at narrower widths
DESKTOP_COLUMN_FLOW = Situação operacional → Atividade recente | Monitoramento e completude → Câmera em destaque
MOBILE_READING_ORDER = Situação operacional → Monitoramento e completude → Atividade recente → Câmera em destaque
MOBILE_ORDER_BASIS = existing semantic source order; no finer sequence is prescribed by the screen census
NAVIGATION_PATTERN = horizontal scroll, visible cue on overflow, keyboard focus reveal, touch-scrollable
GLOBAL_HORIZONTAL_OVERFLOW = NONE
CONSOLE_ERRORS = 0 / PAGE_ERRORS = 0 / DENIED_REQUESTS = 0
TECHNICAL_READY_FOR_REVIEW = YES
USER_VISUAL_APPROVAL = PENDING
ACTIVITY_COMPLETE = NO / human visual review is the next gate
PROJECT_STATE_UPDATE = NOT PERFORMED / outside the current card
PROTOTYPE_CONTENT = demonstration notice and planned profile surface explicitly classified

### Evidência e resultado por viewport

| Viewport | F03 — fluxo vertical | F04 — navegação e overflow |
|---|---|---|
| 1920×1080 | Independência das colunas; Situação 209px; Atividade após 16px; Monitoramento 341px; Câmera após 16px | Sem overflow global |
| 1440×900 | Mesmo fluxo; sem equalização de altura | Sem overflow global |
| 1366×768 | Mesmo fluxo; cards preservam alturas naturais | Sem overflow global |
| 390×844 | Ordem móvel preservada: Situação, Monitoramento, Atividade, Câmera | Os cinco itens cabem e “Eventos” fica integralmente visível; alvo de 44px; sem overflow |
| 320px complementar | Mesma ordem móvel | Rolagem horizontal e dica visível; Tab e gesto de toque alcançam e revelam o item “Eventos” integralmente |

A causa de F03 era uma única linha de grid compartilhada: o painel de
monitoramento, com 341px, controlava a altura do row em que Situação tinha
209px. A linha seguinte começava em y=738, deixando 152px sob o card operacional
depois de descontado o gap entre linhas. O fluxo responsivo agora cria pilhas
independentes: Situação → Atividade e Monitoramento → Câmera. Atividade começa
16px após Situação, reduzindo o vazio em 136px; nenhum card é esticado.

A causa de F04 era a soma de padding/gap dos cinco links sem reserva de espaço
no final do scroller. A 390px, “Eventos” ultrapassava em cerca de 25px a borda
visível da navegação apesar de o documento não transbordar. O ajuste usa os
tokens existentes para reduzir padding lateral, preserva tipografia, rótulos e
alvos de 44px e acrescenta 8px de end-padding/scroll-padding. Em largura estreita,
uma dica aparece somente com overflow; foco por teclado revela o link focado e
a rolagem por toque alcança a extremidade. A navegação horizontal é o padrão
canônico do harness para mobile.

A ordem móvel é Situação → Monitoramento → Atividade → Câmera, preservada da
ordem DOM semântica existente. O census organiza indicadores/painéis e atividade
recente, mas não determina a sequência exata destes quatro cards. O fluxo não foi
alterado acidentalmente pela disposição visual em colunas do desktop.

A inspeção confirmou que os tiles KPI continuam em 220×77px e que o cabeçalho,
ação, cópia, cores, tipografia, espaçamento aprovado, shell e direção ARGOS Hybrid
não regrediram. Design System compartilhado, Button/Card primitives, outras
telas, Quick Detail e produção permanecem sem alterações. O protótipo agora
marca “Valores demonstrativos...” como conteúdo demonstrativo e “Meu Perfil ·
superfície planejada” como superfície planejada.

As quatro capturas F03/F04 estão persistidas no diretório canônico, além das
32 anteriores. Chrome/Playwright rodou com zoom 100%, escala de dispositivo 1 e
guarda que permitiu apenas GET local. Não houve erro de console/página, request
negado/externo/não-GET, persistência ou overflow global. A comparação antes/depois
dos quatro viewports foi inspecionada visualmente.

### Gate

TECHNICAL_READY_FOR_REVIEW = YES
READY_FOR_USER_REVIEW = YES
HUMAN_VISUAL_APPROVAL = PENDING
ACTIVITY_COMPLETE = NO
FINAL_VERDICT = PASS_WITH_FINDINGS / F03 e F04 resolvidos; revisão humana pendente


## Registro histórico anterior — revisão F01/F02
**final result: passed**

DESIGN_SYSTEM_VERSION = 2.0.2
PRODUCT_DESIGN_DESIGN_QA = PASS
PERSISTED_EVIDENCE = PASS / 32 named PNGs: 16 baseline defaults + 12 mobile states + 4 refined Dashboard captures
STATE_AND_RESPONSIVE_QA = PASS / four screens × four viewports
GLOBAL_HORIZONTAL_OVERFLOW = NONE
CONSOLE_ERRORS = 0
EXTERNAL_REQUESTS = 0
NON_GET_REQUESTS = 0
PERSISTENCE_WRITES = NONE
ACCESSIBILITY_BASELINE = PASS_WITH_LIMITS / no WCAG conformance claim
TECHNICAL_READY_FOR_REVIEW = YES
USER_VISUAL_APPROVAL = PENDING
ACTIVITY_COMPLETE = NO / human visual review is the next gate

## Registro anterior — comparação focada do Dashboard F01/F02 (2026-09-29)

**final result: passed**

BASELINE = commit d8600021a8aa9ab809a03b416b0a6acfd5702179
IMPLEMENTATION = SCR-DASH-001 with page-local refinement
VIEWPORTS = 1366×768, 1440×900, 1920×1080, 390×844
ZOOM = 100% / DEVICE_SCALE_FACTOR = 1
PAIRING = same-size baseline and refined full views; focused 1920px summary and header comparisons
F01 = PASS / summary card height follows content rather than equal-height stretching
F02 = PASS / action remains visually attached to the page title and description, including 1920px
MOBILE_SMOKE = PASS / existing stacked composition preserved at 390×844
GLOBAL_HORIZONTAL_OVERFLOW = NONE
CONSOLE_ERRORS = 0 / PAGE_ERRORS = 0 / DENIED_REQUESTS = 0
P0_P1_P2_FINDINGS = NONE
USER_VISUAL_APPROVAL = PENDING

The review used the P3-A Dashboard baseline screenshots from BASELINE and the
four refined screenshots below as same-dimension before-and-after inputs.
The original copy, metrics, shared shell, and 220×77px metric tiles remain
visually unchanged. The summary cards measure 209px and 341px on desktop, so
their different content no longer creates an oversized blank card. At
1920×1080, the page content width is 1280px and the title/action tracks have
a 32px gap. On mobile, the new desktop rules do not apply.

- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-DASH-001__1366x768__refined__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-DASH-001__1440x900__refined__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-DASH-001__1920x1080__refined__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-DASH-001__390x844__refined__default.png

The refinement is limited to SCR-DASH-001. No shared Design System files,
other P3-A screens, Quick Detail, global coverage, production, or project
state were changed. Human visual acceptance remains the next gate.

---
## Base visual, implementação e comparação

- Direção visual: docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png
  (1425×1388 px; JPEG-encoded despite the .png extension; source viewport unknown).
  A imagem é referência direcional, não mock individual para comparação pixel a pixel.
- Shell compartilhado DS 2.0.0: docs/prototype/ui-v2/evidence/screenshots/shell/shell__1440x900__default__default.png
  (1440×900) e shell__390x844__default__default.png (390×844), pareados com as
  implementações nos mesmos viewports para avaliar o shell compartilhado.
- Referência focal de legibilidade: docs/prototype/ui-v2/foundation/screenshots/data-display-390x844.png
  (390×1303; full page), comparada ao crop da tabela móvel de Inventário. A comparação
  considera leitura e quebra de conteúdo; o crop não tem as mesmas dimensões e não é
  tratado como pixel match.
- Capturas da implementação: docs/prototype/ui-v2/evidence/screenshots/p3-a/;
  dimensões CSS de 390×844, 1366×768, 1440×900 e 1920×1080; pixels de saída
  correspondentes, device scale factor 1 e zoom 100%.
- Não há mocks individuais por tela. Composição e fidelidade foram avaliadas contra
  o contrato visual da família, os contratos das telas e a consistência do shell;
  não se declara comparação pixel a pixel com um mock de cada tela.

Foram inspecionadas visualmente comparações lado a lado em dimensões equivalentes,
incluindo shell desktop e móvel, além de comparações focadas de tabela. Cor, shell,
tipografia, espaçamento, superfícies e hierarquia permanecem coerentes com as
referências disponíveis. Nenhum achado P0/P1/P2 foi identificado; não foi necessário
abrir achado cosmético opcional.

## Checklist de fechamento

- As quatro telas foram capturadas nos quatro viewports sem overflow horizontal em
  html ou body.
- As 12 capturas móveis adicionais cobrem Portal empty/long, Dashboard empty/long,
  Inventário empty/loading/error/long/selected e Detalhe empty (history)/error/long.
  Metadados e estado visível correspondem ao nome e à fixture da captura.
- Inventário móvel mantém oito colunas em scroll contido: 921px de tabela num
  scroller de 360px; linha padrão de 127px e linha longa de 217px. Busca, limpar
  filtros, paginação, seleção por Enter, anúncio de status e alcance da ação por
  teclado foram observados.
- Console sem erros; nenhuma requisição externa ou escrita não-GET; sem gravação em
  storage, cookies ou IndexedDB.
- Baseline semântico e de teclado passou com limites; não implica certificação WCAG.
- Quick Detail permanece protegido e inalterado. Produção e escopo de outras famílias
  não foram alterados.

O relatório técnico Product Design está aprovado para a próxima etapa. A aprovação
visual humana ainda está pendente; ACTIVITY_COMPLETE = NO até a revisão do pacote de
capturas. PROJECT_STATE.md e a matriz global não foram atualizados por estarem fora
do escopo deste cartão.

## Pacote curto para revisão humana

- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-PORTAL-001__1440x900__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-DASH-001__1440x900__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-INV-001__1440x900__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-CAM-DETAIL-001__1440x900__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-PORTAL-001__390x844__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-DASH-001__390x844__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-INV-001__390x844__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-CAM-DETAIL-001__390x844__default__default.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-INV-001__390x844__default__long.png
- docs/prototype/ui-v2/evidence/screenshots/p3-a/SCR-INV-001__390x844__selected__default.png

---
# P3-A — Product Design / design QA

## Checkpoint histórico de regressão DS 2.0.2 — evidência não persistida (superado em 2026-09-29)

**final result: blocked**

```text
P3_A_WORKTREE = C:\Users\walacedelgado\PycharmProjects\projeto_argos_ui_v2_p3_a
BRANCH = codex/ui-v2-p3-a-core-inventory
DS_PATCH_SOURCE_COMMIT = 8a480a50a338ef3961a242e9dce0ccaf09cdf49b
P3_A_DS_2_0_2_PROPAGATION_COMMIT = d0c495cea2a302b70845e38e97225dd8daf5c5d2
DESIGN_SYSTEM_VERSION = 2.0.2
CHERRY_PICK_CONFLICT = ROOT_GOVERNANCE_DOCUMENT_ONLY
CONFLICT_RESOLUTION = KEEP_FAMILY_ABSENCE
CANONICAL_DCR_LOCATION = origin/master
ROOT_DOCUMENT_DUPLICATED_IN_P3_A = NO
ROOT_OWNERSHIP_PRESERVED = YES
F01 = PASS / state isolation on DS 2.0.2
F02 = RESOLVED_AT_ROOT / mobile table readability regression PASS
F03 = OPEN / named screenshot persistence unavailable
STATE_QA = PASS / supported variants and Inventory interaction matrix
RESPONSIVE_QA = PASS / four screens × 390x844, 1366x768, 1440x900, 1920x1080
ACCESSIBILITY_BASELINE = PASS_WITH_LIMITS / semantic and keyboard baseline; no WCAG conformance claim
NODE_PLAYWRIGHT_AVAILABLE = NO / node and npm are not installed in PATH
CONSOLE_LOG_CAPTURE = NOT_AVAILABLE
PRODUCT_DESIGN_DESIGN_QA = BLOCKED_BY_MISSING_PERSISTED_EVIDENCE
EVIDENCE_CAPTURE_STATUS = BLOCKED
TECHNICAL_READY_FOR_REVIEW = NO
USER_VISUAL_APPROVAL = PENDING
P3_A_FINAL_COMPLETION_COMMIT = NOT_CREATED
BLOCKED_CHECKPOINT_COMMIT = AUTHORIZED / family-owned records only
PUSH_AUTHORIZED = YES / codex/ui-v2-p3-a-core-inventory only
```

### Fonte visual e capturas

- Direção visual consultada: `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`.
- Shell compartilhado consultado: `docs/prototype/ui-v2/evidence/screenshots/shell/shell__1440x900__default__default.png`.
- A comparação normalizada 1440×900 foi inspecionada lado a lado em Edge: direção de cor, shell, tipografia, espaçamento, superfícies e hierarquia estão coerentes com a referência. A fonte representa direção visual e shell, não um mock individual de cada tela.
- As quatro telas foram exercitadas no preview HTTP local; o browser permite exibir capturas na sessão, mas a interface de captura disponível não oferece caminho de arquivo. Não há PNGs persistidos em `docs/prototype/ui-v2/evidence/screenshots/p3-a/`.
- A revisão final permanece bloqueada porque o contrato pede evidência nomeada persistida. Captura inline da sessão não substitui o artefato.

### Resultado técnico observado

- Quatro telas × quatro viewports CSS: 16 combinações sem overflow horizontal global em `html` ou `body`. Viewports: 390×844, 1366×768, 1440×900 e 1920×1080.
- Inventário em 390×844: rolagem horizontal contida no wrapper (largura útil 360px; tabela 920px); linhas padrão com 127px. Em desktop, sem rolagem local e linhas com 103px. Fixture longa, página 2: registro longo com 217px e demais linhas com 127px.
- Inventário: filtro sem resultados mostra estado vazio; limpar filtros restaura resultados; paginação apresenta a segunda página; Enter seleciona a linha e anuncia a câmera; o Quick Detail continua apontando ao baseline protegido. O link da ação é alcançável pelo teclado e traz alvo de 44px dentro da região rolável.
- Estados: Portal e Dashboard default/empty/long; Inventário default/empty/loading/error/long; Detalhe default (freshness stale), histórico empty/error/long. Uma variante ativa por vez.
- Baseline acessível: `pt-BR`, título, um H1, landmarks `main` e navegação nomeada, nomes de campos/botões, imagens com `alt`, seleção por teclado. Baseline não é declaração de conformidade WCAG. A captura de console não ficou disponível nesta sessão e não é declarada como aprovada.
- F-02: o DS 2.0.2 reduz a altura móvel da linha padrão medida anteriormente em 283px para 127px. Não foi criado workaround P3-A; os dados e ações continuam na tabela compartilhada com rolagem interna.

### Limite de conclusão

A implementação e a regressão técnica estão prontas para revisão, mas o gate Product Design exige PNGs nomeados persistidos; a ferramenta de browser disponível só retorna capturas à sessão. Nenhuma aprovação visual humana foi dada. `final result: blocked` e `DESIGN_QA_COMPLETE = NO` permanecem até anexar evidência no caminho canônico e concluir a revisão visual humana.

O checkpoint anterior abaixo é mantido como histórico; os achados de 283px e o bloqueio de DS 2.0.1 foram resolvidos pela propagação 2.0.2.
---

## Retomada pós-DS 2.0.1 — QA técnico (2026-09-28)

**final result: blocked**

```text
F01 = RESOLVED / DS 2.0.1 hidden semantics regression PASS
F02 = OPEN / mobile inventory table readability / ROOT adjudication required
F03 = OPEN / evidence capture mechanism blocked
PORTAL = QA EXECUTED
DASHBOARD = QA EXECUTED
INVENTORY = QA EXECUTED WITH F02
CAMERA_DETAIL = QA EXECUTED
QUICK_DETAIL = PROTECTED / INHERITED
EVIDENCE_CAPTURE_STATUS = BLOCKED
P3_A_FINAL_COMPLETION_COMMIT = NOT_CREATED / technical gate did not pass
BLOCKED_CHECKPOINT_COMMIT = AUTHORIZED / family-owned records only; SHA reported after creation
PUSH_AUTHORIZED = YES / codex/ui-v2-p3-a-core-inventory only
USER_VISUAL_APPROVAL = PENDING
```

### Fonte visual e evidência

- Direção ARGOS HYBRID: `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`.
- Referência do shell: `docs/prototype/ui-v2/evidence/screenshots/shell/shell__1440x900__default__default.png`.
- Implementação: preview HTTP local em `http://127.0.0.1:8766/docs/prototype/ui-v2/screens/p3-a/`.
- Viewports inspecionados: 1920×1080, 1440×900, 1366×768 e 390×844, zoom 100%.
- Capturas de implementação foram vistas no browser para as quatro telas e estados relevantes; os PNGs não puderam ser persistidos. O caminho `docs/prototype/ui-v2/evidence/screenshots/p3-a/` não contém as capturas nomeadas requeridas.
- Não houve comparação visual pareada arquivada com fonte e implementação no mesmo artefato. Portanto, a revisão de fidelidade permanece parcial.

### Resultado das verificações

- F-01: PASS. Em Portal, Dashboard, Inventário e Detalhe, todos os elementos com `[hidden]` computaram `display: none`; cada estado solicitado ficou isolado. `hidden="until-found"` não é consumido por P3-A.
- Estados: Portal default/empty/long; Dashboard default/empty/long; Inventário default/empty/loading/error/long (página 2) e seleção por Enter; Detalhe default com freshness stale, empty, error e long. Nenhuma colisão de estado foi observada.
- Responsivo: não houve overflow global nas quatro larguras. A tabela preservou rolagem horizontal interna, mas a composição móvel perdeu densidade e scanability.
- Acessibilidade baseline: títulos e um H1 por tela; landmarks `main`/`nav` nomeados; imagens com `alt`; filtros rotulados; Skip Link focável com outline sólido de 3px; seleção da linha via Enter anunciou o resultado. Isso não é declaração de conformidade WCAG.
- Interação/filtros: busca sem resultado exibiu empty state; limpar filtros restaurou três linhas; página 2 expôs os registros longos. Quick Detail continua apenas apontando ao baseline protegido, sem nova página.
- Console: sem erros ou warnings durante a revisão.
- Comparação visual de desktop: cores, shell escuro, fundo claro, cards, hierarquia de títulos e tratamento de estados seguem a direção da fonte. A composição usa conteúdo próprio P3-A e a fonte Style Lab é uma referência de direção, não um mock por tela; sem pareamento salvo não certifica fidelidade final.

### Findings

- **[P2] Linhas do Inventário ficam excessivamente altas em 390px.** A tabela mede 859px dentro de um wrapper de 345px; a coluna de ações cai para 61px e as três linhas visíveis medem 283px cada por quebra intensa de texto. O usuário precisa rolar horizontalmente e também percorre muito espaço vertical para comparar câmeras. O sizing pertence ao pattern compartilhado; registrar como `DSCR-UIV2-002-MOBILE-TABLE-READABILITY` para revisão ROOT. P3-A não introduziu CSS local ou override.
- **Bloqueio de evidência:** não foi possível gravar os PNGs nomeados exigidos no caminho P3-A. O browser recusou a navegação `data:` usada para salvar a imagem e sua política bloqueia contornar a recusa. Capturas mostradas durante a execução não substituem os arquivos persistidos para o gate.

### Histórico de comparação

F-01 foi o bloqueador anterior. O cherry-pick do patch ROOT `8121ed38cc15e1ff6e72cb46bbb2ca865100bce0` corrigiu a semântica global; a regressão atual passou. Nenhum finding P0/P1 foi observado. O finding P2 de densidade móvel e a falta de evidência nomeada permanecem, então o resultado final continua `blocked`.

### Checklist de handoff

- [x] Confirmar DS 2.0.1 e F-01 resolvido em runtime.
- [x] Retestar estados e interação de Inventário.
- [x] Inspecionar os quatro viewports e baseline de acessibilidade.
- [ ] Revisar o request ROOT de sizing da tabela móvel.
- [ ] Persistir screenshots nomeados no diretório canônico.
- [ ] Completar comparação visual pareada e repetir o gate técnico.
- [ ] Apresentar as telas para revisão visual humana.

O relatório anterior abaixo permanece como histórico do checkpoint que estava bloqueado por F-01.

```text
PRODUCT_DESIGN_STATUS = AVAILABLE
PRODUCT_DESIGN_SKILLS_LOADED = get-context, design-qa
PRODUCT_DESIGN_GET_CONTEXT = COMPLETE
PRODUCT_DESIGN_DESIGN_QA = BLOCKED_BY_DS_CHANGE
DESIGN_QA_COMPLETE = NO
USER_VISUAL_APPROVAL = PENDING
```

## Contexto de implementação

O contexto de `$get-context` foi construído a partir dos contratos P3-0, foundation e Style Lab C aprovados, fluxo factual das telas atuais e fronteiras de ownership P3-A. O alvo é ARGOS Hybrid no DS 2.0.0: quatro composições novas — Início, Dashboard, Inventário e Detalhe da câmera — com fixtures locais; Quick Detail continua protegido/herdado. A revisão não autoriza alteração do Design System nem produção.

Referências visuais/factuais consultadas:

- Foundation visual C: `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`.
- Shell aprovado: `docs/prototype/ui-v2/evidence/screenshots/shell/shell__1440x900__default__default.png`.
- Composição renderizada observada em Edge: `http://127.0.0.1:8766/docs/prototype/ui-v2/screens/p3-a/scr-portal-001.html?state=default`.

## Evidência e escopo desta passagem

Preview servido por HTTP local no worktree P3-A. O Edge conectado abriu as quatro telas novas no estado `default` e as capturas de página completa foram inspecionadas visualmente no fluxo da sessão. Foi observada a colisão de estados em todas: Portal mistura os módulos com acesso vazio; Dashboard mostra o painel vazio junto aos indicadores/atividade; Inventário mostra tabela junto a vazio, loading e error; Detalhe mostra histórico junto ao estado de histórico vazio.

As capturas foram apresentadas inline, mas não persistidas como PNG no diretório de evidências; portanto não constituem evidência nomeada do contrato P3-A. Os alvos Style Lab C e shell foram consultados separadamente, não em um artefato combinado normalizado. A passagem não registrou dimensões CSS do viewport nem zoom via instrumentação; não reivindica QA em 1920×1080, 1440×900, 1366×768 ou 390×844.

Não foram verificados os demais estados isoladamente, fixture longa, interações, Quick Detail protegido, estratégia responsiva/tabela ou baseline acessível. Não há screenshots de evidência nomeados persistidos. `DESIGN_QA_COMPLETE` permanece `NO`.

## Finding bloqueador

**F-01 — Variantes de estado `hidden` continuam renderizadas**

**Resultado:** bloqueador para state coverage e para o gate técnico P3-A.


Nas quatro telas renderizadas em `?state=default`, conteúdos de estado alternativo permanecem visíveis simultaneamente com o conteúdo default. O harness alterna variantes usando o atributo/propriedade HTML `hidden`; regras author `display` em patterns/componentes canônicos prevalecem sobre o estilo user-agent de `[hidden]`. Os seletores observados incluem `.argos-state`, `.argos-two-column`, `.argos-alert` e `.argos-docs-nav a`; deve-se validar o conjunto canônico completo.

Isso invalida a distinção visual entre as variantes e pode misturar conteúdos de estado em telas que dependem do mesmo mecanismo. Não é uma inconsistência a corrigir por override local: DS e harness são root-owned/read-only para P3-A. A solicitação está registrada como `DS_CHANGE_REQUEST` em `coverage.md`, com decisão de versão e reaprovação do usuário pendentes.

**Próximo passo de QA:** após adjudicação e eventual correção compartilhada pelo owner, repetir a matriz completa de estados, fixture longa, interação e os quatro viewports; salvar screenshots com naming canônico no diretório de evidence P3-A; então completar revisão visual de tipografia, hierarquia, espaçamento, densidade, alinhamento, imagens, overflow/over-stretch, navegação e acessibilidade baseline. Não declarar conformidade WCAG completa.

## Estado dos gates

```text
FOUR_DEFAULT_RENDERS = OBSERVED_WITH_BLOCKING_STATE_COLLISION
COMPOSITION_REVIEW = PARTIAL; viewport normalizado e comparação pareada pendentes
REQUIRED_STATES = BLOCKED_BY_DS_CHANGE
RESPONSIVE_QA = NOT_RUN
ACCESSIBILITY_BASELINE = NOT_RUN
NAMED_SCREENSHOT_EVIDENCE = NOT_GENERATED
TECHNICAL_READY_FOR_REVIEW = NO
DESIGN_QA_COMPLETE = NO
```

## SCR-INV-001 targeted refinement — 2026-09-30

The legacy F-01 block above is historical for Inventory: this branch includes
the canonical DS 2.0.2 hidden-semantics correction. This review covers only
SCR-INV-001 and does not transfer approval to another P3-A screen.

```text
SCR_INV_001_REFINEMENT_REPORT
STATUS = TECHNICAL_READY_FOR_REVIEW / PASS_WITH_FINDING
F05_MOBILE_FILTER_SOLUTION = button disclosure with aria-controls and aria-expanded; Vanilla JS
SEARCH_ALWAYS_VISIBLE_MOBILE = YES
ADVANCED_FILTERS_PROGRESSIVE_DISCLOSURE = YES / all 8 advanced filters retained
FILTERS_REMOVED = NO
F06_TABLE_PATTERN = KEEP_HORIZONTAL_TABLE_SCROLL / discovery finding open
TABLE_MOBILE_START_EVIDENCE = docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-30/SCR-INV-001__390x844__default__default__table-mobile-start.png
TABLE_MOBILE_SCROLLED_EVIDENCE = docs/prototype/ui-v2/evidence/screenshots/p3-a/review-2026-09-30/SCR-INV-001__390x844__default__default__table-mobile-scrolled.png
MOBILE_TABLE_VISUAL_VERDICT = FINDING
F07_RESULTS_INSTRUCTION = “Nenhuma câmera selecionada · Clique em uma linha ou use Enter/Espaço para selecionar.” / one live status
TABLE_CAPTION_TREATMENT = semantic caption retained; muted, left-aligned, 11px
F08_USER_FACING_QUICK_DETAIL_LABEL = “Visão rápida”; full-detail action = “Ver detalhes”
DESIGN_SYSTEM_CHANGED = NO
DASHBOARD_CHANGED = NO
PRODUCTION_CHANGED = NO
VIEWPORT_1920x1080 = PASS
VIEWPORT_1440x900 = PASS
VIEWPORT_1366x768 = PASS
VIEWPORT_390x844 = PASS
HUMAN_VISUAL_APPROVAL = PENDING
READY_FOR_USER_REVIEW = YES
FINAL_VERDICT = PASS_WITH_FINDING / F06 requires user adjudication before table-pattern changes
ACTIVITY_COMPLETION_PERCENT = 95% / technical review package ready; human F06 adjudication pending
RESPONSIVE_FOCUS_PRESERVED = YES / focused advanced filter remains visible and active in both resize directions
```

### Validação e finding F06

| Viewport | Resultado técnico | Evidência objetiva |
|---|---|---|
| 1920×1080 | PASS | Filtros, botão Limpar e tabela sem regressão de layout; sem overflow/clipping |
| 1440×900 | PASS | Geometria dos 9 controles e de Limpar idêntica à baseline anterior (0 px) |
| 1366×768 | PASS | Geometria dos 9 controles e de Limpar idêntica à baseline anterior (0 px) |
| 390×844 | PASS_WITH_FINDING | busca sempre visível; cinco itens de navegação; scroller local 360 px, tabela 924,3 px |

Em desktop, a comparação da caixa e posição dos 9 filtros e do botão “Limpar”
contra a composição anterior produziu delta de 0 px nos três viewports. No
mobile, os 8 filtros avançados ficam recolhidos inicialmente; há 9 filtros no
DOM contando Busca. Enter abre e fecha o controle com foco visível; toque abre
o painel; selecionar “Produção” e acionar Limpar restaura todos os campos e
retorna o foco à busca. Touch targets de Filtros e Limpar medem 44 px de altura.

Para F06, a captura inicial mostra status, tabela e o começo de uma coluna
seguinte; a captura deslocada mostra “Fabricante / modelo”, “Terminal / setor”,
“Ações” e ambos os links. O deslocamento máximo é 564 px. A instrução existente
para deslizar horizontalmente fica abaixo da tabela e não aparece no primeiro
viewport de captura; não há barra persistente visível. Classificação:
`MOBILE_TABLE_VISUAL_VERDICT = FINDING`. A tabela não foi convertida em cards nem
recebeu mudança de pattern; aguardar adjudicação humana antes de alterar essa
estratégia.

As quatro capturas padrão estão no mesmo diretório de evidências; as duas
capturas de tabela usam sufixos `table-mobile-start` e
`table-mobile-scrolled` para distinguir posição e estado sem substituir os
quatro estados canônicos. Runtime: zoom 100%, device scale factor 1, zero erros
de console/page e zero requisições externas/falhas. Nenhum elemento de conteúdo
fora da tabela/navegação foi cortado. O caption conserva seu texto semântico e
foi reduzido visualmente para texto muted de 11 px. O Quick Detail protegido
permanece apenas como destino do link “Visão rápida”.


## SCR-INV-001 — QA direcionado F06: registros responsivos (2026-09-30)

Escopo: validar a resposta mobile adjudicada pelo usuário e regressão da tabela
desktop em SCR-INV-001. O QA é da tela e deste finding; não declara a família
P3-A inteira aprovada nem faz declaração de conformidade WCAG.

| Viewport | Apresentação | Resultado | Evidência |
|---|---|---|---|
| 1920×1080 | Tabela nativa, oito colunas | PASS | SCR-INV-001__1920x1080__default__desktop-table-regression.png |
| 1440×900 | Tabela nativa, oito colunas | PASS | SCR-INV-001__1440x900__default__desktop-table-regression.png |
| 1366×768 | Tabela nativa, oito colunas | PASS | SCR-INV-001__1366x768__default__desktop-table-regression.png |
| 390×844 | Lista de registros, padrão, seleção e conteúdo longo | PASS | Capturas screen-entry, top-results-final, selected e long |
| 320×844 | Lista de registros, metadados em uma coluna | PASS / smoke | SCR-INV-001__320x844__smoke__responsive-records.png |

A mudança ocorre a 940px de largura disponível do container de resultados.
A largura natural medida da tabela padrão é aproximadamente 924px e a fixture
longa chega a aproximadamente 931px. Assim, a regra troca para cartões antes
de exigir rolagem horizontal. A verificação em larguras próximas ao limite
observou container de 928px com cartões e de 948px com tabela.

A implementação reusa cada objeto da fixture para desenhar a linha da tabela
desktop e o artigo da lista mobile. Ambos mantêm nome, identificador, badges
operacionais, situação de monitoramento e freshness, completude, fabricante,
modelo, terminal, setor, estado de imagem e ações. A fixture longa foi exercitada
na segunda página; textos longos quebram linha sem clipping, as ações mantêm
alvo mínimo de 44px e a paginação permanece depois dos registros.

Na navegação por teclado, a seleção responde a Enter/Espaço e atualiza o estado
aria-pressed; a seleção sincroniza com a linha desktop. Em mudança entre
representações, o foco vai ao controle equivalente. Os filtros F05 conservam
estado aberto e foco; o fluxo de F05 não foi alterado. O tree de acessibilidade
mantém tabela/columnheaders no desktop e expõe ordered list, listitem, article,
heading, definition list, botão e links no mobile. A conversão CSS direta da
tabela foi rejeitada porque o probe removeu roles de cabeçalho e um rowgroup.

Todas as capturas foram feitas em Chrome, zoom 100% e escala 1. Não houve
overflow horizontal do documento, clipping de conteúdo, erros de console ou
página, requests falhos ou externos. O desktop segue com a tabela e não recebeu
mudança de geometria ou estilo nesta implementação. O touch target dos controles
e ações visíveis mede pelo menos 44px.

~~~text
SCR_INV_001_F06_PRODUCT_DESIGN_QA = PASS / targeted technical evidence
TECHNICAL_READY_FOR_REVIEW = YES
HUMAN_VISUAL_APPROVAL = PENDING
ACTIVITY_COMPLETION_PERCENT = 95%
ACTIVITY_COMPLETE = NO
ACCESSIBILITY_BASELINE = PASS_WITH_LIMITS / no WCAG conformance claim
DESIGN_SYSTEM_CHANGED = NO
PRODUCTION_CHANGED = NO
~~~

O pacote ZIP com as oito capturas está em
C:\Users\walac\.codex\visualizations\2026\09\29\01a0ef80-3465-7ca2-95e1-32af86c61e97\ARGOS_P3-A_SCR-INV-001_F06-responsive-records_2026-09-30.zip.
A aprovação visual humana continua sendo o próximo gate.


## SCR-INV-001 — adjudicação visual aprovada e freeze (2026-09-30)

O usuário revisou a entrada mobile, resultados, estado selecionado, conteúdo
longo, smoke 320px e as três regressões desktop. Resultado visual final: PASS.

~~~text
SCR_INV_001_VISUAL_REVIEW = PASS
HUMAN_VISUAL_APPROVAL = PASS
SCR_INV_001_STATUS = USER_APPROVED / FROZEN
F05 = PASS / CLOSED / FREEZE
F06 = PASS / CLOSED / FREEZE
F07 = PASS / CLOSED
F08 = PASS / CLOSED
DESKTOP_TABLE = PASS / PRESERVED / FREEZE
MOBILE_RECORDS = PASS / FREEZE
LONG_CONTENT = PASS
SELECTED_STATE = PASS
VIEWPORT_320x844 = PASS_WITH_ACCEPTED_NON_BLOCKING_NATURAL_WRAP
VIEWPORTS_DESKTOP = 1920x1080 PASS; 1440x900 PASS; 1366x768 PASS
ACTIVITY_COMPLETION_PERCENT = 100%
PROJECT_STATE_UPDATE = PASS / PROJECT_STATE.md seção 41
ACTIVITY_COMPLETE = YES / escopo limitado a SCR-INV-001
DESIGN_SYSTEM_CHANGED = NO
PRODUCTION_CHANGED = NO
NEXT_SURFACE = SCR-CAM-DETAIL-001
~~~

A hierarquia aprovada nos registros móveis é identidade → status →
equipamento/localização → informação da imagem → ações. Os registros mantêm
altura orientada pelo conteúdo; títulos podem quebrar naturalmente em 320px.
Não reduzir fonte, truncar, abreviar informação de domínio ou fixar alturas.
A apresentação de registros é um pattern data-display para conteúdo denso,
não um primitive genérico de Card. A superfície fica congelada após esta
adjudicação; não executar polishing adicional.
