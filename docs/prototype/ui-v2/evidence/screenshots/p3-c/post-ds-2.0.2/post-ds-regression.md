# P3-C — regressão direcionada pós-DS 2.0.2

Data: 2026-09-29
Branch: `codex/ui-v2-p3-c-governance-audit`
Base recuperada: `c26840e8c9c21b9105b7c3bb42c96bc5186c9227`
Patch ROOT: `8a480a50a338ef3961a242e9dce0ccaf09cdf49b`
Commit de propagação: `f8cd8cea0e1f0cbd1ff072aafa341cbcf5c8c732`
Design System compartilhado: `2.0.2`

## Resultado

`IMPLEMENTATION_REGRESSION = PASS`
`FAMILY_TECHNICAL_LOGIC = PASS`
`DSCR-UIV2-002 = CONSUMED / TARGETED REGRESSION PASS`
`USER_VISUAL_APPROVAL = PENDING`

O DCR ROOT não foi copiado para a família. A única colisão do cherry-pick foi o `modify/delete` desse DCR; ele permaneceu ausente em P3-C conforme a resolução pré-autorizada. O cherry-pick contém somente seis paths compartilhados de harness/index/CSS; não contém implementação P3-C, backend ou produção.

## Medições dos três consumidores

Viewports efetivos confirmados pelo browser: 390×844 e 1440×900. As linhas abaixo usam o estado/fixture default; a coluna mobile long usa `fixture=long`.

| Consumidor | Mobile default | Mobile long | Desktop 1440×900 |
|---|---|---|---|
| `SCR-ACT-LIST-001` | 5 linhas; 77–95px; região 310/760px (client/scroll); ações nomeadas: 10 | 4 linhas; 131–167px; região 310/760px | região/tabela 1088px; 5 linhas de 64px; sem scroll local |
| `SCR-EVENT-LIST-001` | 8 linhas; 64–73px; região 310/760px; links nomeados: 8; badges: 16 | 8 linhas; 73–127px; região 310/760px | região/tabela 1088px; 8 linhas de 64px; sem scroll local |
| `SCR-EVENT-CAMERA-001` | 5 linhas; 64px; região 310/760px; links nomeados: 5 | 5 linhas; 73px; região 310/760px | região/tabela 1088px; 5 linhas de 64px; sem scroll local |

Nos seis casos mobile default/long: `GLOBAL_HORIZONTAL_OVERFLOW = NO`, `LOCAL_TABLE_SCROLL = FUNCTIONAL`, `DESTRUCTIVE_WORD_FRAGMENTATION = NO` e `BADGE_FRAGMENTATION = NO`. Os identificadores separados por hífen quebram nos delimitadores; nenhum segmento textual sem hífen foi partido entre retângulos de linha. No desktop, não houve overflow novo nem regressão material de largura ou altura de linha. O DCR ROOT registra a comparação desktop inalterada para 7/7 consumidores.

`ACTION_ACCESSIBILITY = YES`. As regiões têm nome acessível, `role=region` e `tabindex=0`; links/ações possuem nome. Tab alcançou links nas três tabelas. Em `SCR-ACT-LIST-001`, Tab até `Editar` deslocou o scroll local para 449.78px e deixou a ação totalmente visível dentro da região.

## Composições não-table

Spot check em 390×844 e 1440×900: form de Activities (`SCR-ACT-CREATE-001`), ação Governance (`SCR-GOV-STATE-001`) e detalhe Event (`SCR-EVENT-DETAIL-001`). Todos mantiveram `document/body scrollWidth <= viewport`; nenhuma regressão evidente. Os demais sete estados/telas não foram reabertos.

## Semântica, rede e persistência

Nos consumidores afetados, o estado ativo `default` permaneceu visível; elementos com atributo `[hidden]` continuaram sem retângulo renderizado. Não há inline `style.display` reintroduzido em P3-C. O CSS base preserva a regra nativa de `[hidden]`; F01/ROOT-REQ-P3-C-001 continua resolvido.

O preview foi servido em `127.0.0.1`; assets e fixture vieram do mesmo origin. O JavaScript lê a fixture local via `fetch` GET e não grava estado. `CONSOLE_ERRORS = 0`; `EXTERNAL_REQUESTS = 0`; `NON_GET_REQUESTS = 0`; `PERSISTENCE = NONE`; `PRODUCTION_CHANGED = NO`.

## Comparabilidade e findings

O browser interativo deste workstation reserva 17px para scrollbar clássico: com `innerWidth=390`, `document/body scrollWidth=373`; com `innerWidth=1440`, normalmente 1423. Isso não é overflow (scroll width permaneceu menor ou igual ao viewport) e reduziu a largura útil frente ao relatório headless anterior. Como resultado, páginas mobile ficaram aproximadamente 9–27px mais altas que o relatório 2.0.1; as linhas de dados mantiveram comportamento legível. No Event List desktop, o formulário de filtros ocupou uma linha adicional no ambiente interativo, mas as linhas da tabela mantiveram 64px e o contêiner coube em 1088px. O histórico ROOT DSCR-UIV2-002 registrou no harness desktop exato que larguras e alturas das sete tabelas não mudaram. A diferença total da página é tratada como variação de viewport/scrollbar, não como regressão da tabela.

Finding não funcional: metadados e badges visíveis das nove páginas P3-C ainda dizem `2.0.1`, embora o harness/index/CSS compartilhados estejam em `2.0.2`. A regressão funcional não foi afetada; preservar para adjudicação no gate visual.

## Evidência

O Node/npm e o Playwright local não estão disponíveis neste workstation; nenhuma dependência foi instalada. Browser CUA permitiu medidas DOM e navegação por teclado, mas `Page.captureScreenshot` expirou; não foi possível persistir PNGs 2.0.2 com mecanismo existente.

`EVIDENCE_2_0_2_CAPTURE = DEFERRED_BY_WORKSTATION_CAPABILITY`
`PREVIOUS_EVIDENCE_PRESERVED = YES` — 84 capturas originais + 20 pós-2.0.1 + 3 comparativos (107 PNGs).
`PRODUCT_DESIGN_TARGETED_QA = PASS_WITH_FINDINGS`
`NEXT_GATE = P3-C HUMAN VISUAL REVIEW / EVIDENCE REFRESH IF REQUIRED`
