# P3-C — Product Design design-qa

**final result: PASS — targeted revalidation on Design System 2.0.1**

## Comparison target

- Source visual truth: `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png`, Style Lab C aprovado (ARGOS Hybrid), raster original `1425×1388 px`. É referência do sistema visual, não um mock screen-specific de governança; seu conteúdo é Inventário / Câmeras.
- Rendered implementation: docs/prototype/ui-v2/evidence/screenshots/p3-c/post-ds-2.0.1/scr-gov-substitute-001__1440x900__default__default.png, estado default, viewport CSS 1440×900, DPR 1, zoom 100%, servida pelo preview HTTP local.
- Comparativos pós-patch: docs/prototype/ui-v2/evidence/screenshots/p3-c/post-ds-2.0.1/post-ds-design-qa-source-vs-implementation-1440x900.png, post-ds-design-qa-desktop-before-after-1440x900.png e post-ds-design-qa-mobile-before-after-390x844.png. O source continua sendo referência do sistema visual, sem mock screen-specific.
- Focused-region comparison: `docs/prototype/ui-v2/screens/p3-c/design-qa-table-comparison.png`, recortes originais `1110×412`, sem reamostragem. Compara uma região de linhas da tabela de inventário com linhas da auditoria global para densidade, tokens e legibilidade; os conteúdos/rotas são intencionalmente distintos.
- Screen overview: `docs/prototype/ui-v2/screens/p3-c/design-qa-screen-overview.png`; resumo visual dos dez estados default. Capturas individuais completas estão no diretório de evidence.

## Review

**Information architecture and content.** A família mantém três papéis distintos: histórico/formulário de atividades, ação conceitual de governança e registro imutável de auditoria. Os textos deixam claros objeto e consequência; desativar preserva histórico, substituição separa origem/substituta, e estado técnico continua separado da situação operacional.

**Fonts and typography.** A escala sem serifa, pesos e hierarquia de título/eyebrow/corpo acompanham o Style Lab e os tokens 2.0.1 propagados. Tabelas mantêm texto compacto para comparação; identificadores e conteúdo longo quebram sem corte nas capturas testadas.

**Spacing and layout rhythm.** O shell e navegação seguem o harness P3. Cards, cabeçalhos, divisores, formulário e tabela têm margens e agrupamentos coerentes com o Style Lab. Os avisos críticos ficam restritos à desativação; informações e impactos usam tratamento neutro/âmbar apropriado. As diferenças de largura de sidebar, breadcrumbs e conteúdo vêm do shell P3 canônico, não de deriva local.

**Colors and visual tokens.** A composição usa o navy do shell, superfícies claras, ação azul e semântica verde/âmbar/vermelha do DS. A tabela P3-C mantém cabeçalho discreto e linhas corporativas com densidade similar à referência. Não houve token paralelo nem CSS local.

**Image quality and asset fidelity.** A marca usa o `argos-icon.svg` fornecido pelo Style Lab. Não há imagens de produto decorativas nem placeholders ou desenhos substitutos.

**Copy/content.** Campos e relações foram derivados de forms/templates/serviços atuais; opções de atividade, categoria e origem permanecem factuais. Fixtures são fictícias. Nenhum texto de prompt vazou para a UI.

**Responsive behavior.** Pós-patch, os dez SCREEN_IDs foram verificados em 1440×900 e 390×844; as vinte capturas targeted mantêm a hierarquia e o ritmo responsivo. A medição registrou overflow horizontal zero. Navegação móvel e tabelas seguem nas regiões roláveis do harness; colunas não são ocultadas. O estado longo de substituição continua legível.

**Accessibility.** Baseline cobre título, heading hierarchy, landmarks, `aria-current`, skip link, tabelas semânticas, labels/erros associados, teclado, foco visível, nomes acessíveis e alvos touch do DS. Reduced motion é herdado do DS; a família não introduz animações. Não é declaração de WCAG completa.

## Comparison history

1. A captura inicial do modo `focus` usava `element.focus()` programático. O browser corretamente não aplicou `:focus-visible`, então essa imagem não demonstrava foco de teclado. **Ajuste de QA:** gerar os cinco casos focus com sequência de teclado real (Shift+Tab/Tab) sobre o controle já focado; nenhum token, CSS ou componente local foi criado. A captura posterior mostra o contorno compartilhado (3 px, offset 2 px); métricas confirmam `focusVisible=true` em 5/5. Evidência: `scr-act-create-001__1440x900__focus__default.png` e capturas focus das quatro telas GOV.
2. Nenhuma diferença visual P0/P1/P2 permaneceu após a comparação completa e a revisão das regiões focadas. Não houve mudança visual de produto em resposta ao source comparison.

## Findings

Nenhuma diferença visual acionável P0/P1/P2 permanece. O shell P3 distinto e a diferença de conteúdo entre o Style Lab e as telas governança/auditoria são intencionais e limitam a leitura a nível de sistema visual.

O request compartilhado ROOT-REQ-P3-C-001 foi resolvido pelo DS 2.0.1: [hidden] prevalece sobre os estilos de layout de .argos-alert e .argos-state. A inspeção confirmou zero elementos hidden visíveis sem workaround JavaScript local.

## Implementation checklist

- [x] Comparar Style Lab C e implementação no mesmo input visual.
- [x] Conferir recorte focado para densidade de tabela.
- [x] Revisar tipografia, espaçamento, cores, assets e copy.
- [x] Revisar default, long, erro, vazio, selecionado, sucesso e foco aplicáveis.
- [x] Revisar quatro viewports e baseline de acessibilidade.
- [x] Corrigir captura do foco para usar entrada real de teclado.
- [x] Registrar os limites da referência, comparação e follow-up root.

## Revalidação direcionada — 2026-09-28

- Resultado visual pós-patch: PASS; não surgiu diferença acionável P0/P1/P2. A comparação desktop e mobile antes/depois mostra a mesma composição; o selo de versão é a alteração visível esperada.
- Escopo: Activities, Governance e Events/Audit, dez SCREEN_IDs em 1440×900 e 390×844. SCR-ACT-EDIT-001 foi conferido com mode=edit.
- Regressão complementar: 75 medições, incluindo isolamento de estados e fixtures, [hidden], overflow, sucesso demonstrativo de governança e filtros selecionados de auditoria; zero erro de console, request externo ou request não-GET. Relatório: docs/prototype/ui-v2/evidence/screenshots/p3-c/post-ds-2.0.1/post-ds-regression.json.
- As 84 capturas anteriores foram preservadas. A nova evidência está restrita a docs/prototype/ui-v2/evidence/screenshots/p3-c/post-ds-2.0.1/.
- A avaliação confirma prontidão técnica; aprovação visual humana permanece PENDING.

## QA direcionado pós-DS 2.0.2 — 2026-09-29

### Escopo e resultado

- Reavaliados somente os consumidores afetados: `SCR-ACT-LIST-001`, `SCR-EVENT-LIST-001` e `SCR-EVENT-CAMERA-001`.
- Em 390×844: scroll horizontal contido e funcional nas três regiões (310px client / 760px scroll width); largura global não excedeu o viewport; nenhum token de palavra ou badge foi fragmentado em múltiplas linhas de forma destrutiva. As fixtures default e long foram lidas.
- Ações e links permaneceram descobríveis por nome. As três regiões têm `role=region`, nome acessível e `tabindex=0`. Tab alcançou links em cada tabela; no histórico de atividades, o foco na ação `Editar` rolou o contêiner e deixou a ação totalmente visível.
- Em 1440×900, cada tabela coube no contêiner de 1088px, sem scroll horizontal, com linhas de dados em 64px. O DCR ROOT DSCR-UIV2-002 registra largura e altura de linhas desktop inalteradas nos sete consumidores validados.
- Spot checks P3-C: form Activities, ação Governance e detalhe Event em 390×844 e 1440×900; sem overflow global ou regressão evidente. Estados `default` visíveis; conteúdo `[hidden]` continuou oculto, sem workaround `style.display` local.

### Limites e findings

A inspeção foi por browser conectado, árvore de acessibilidade e medições DOM. A captura persistente não funcionou neste workstation; Node/npm e Playwright local não estão disponíveis, e nenhuma dependência foi instalada. Não houve novas capturas 2.0.2. O total anterior (84 + 20 + 3 = 107 PNGs) permaneceu intacto. Portanto, o gate visual humano segue PENDING.

Finding: as nove páginas P3-C ainda apresentam metadados e selo `Design System 2.0.1`, enquanto o harness e o CSS compartilhados já anunciam `2.0.2`. Registrar para correção/adjudicação visual posterior; não há falha funcional da tabela.

No browser console não foram observados erros; recursos vieram apenas do preview local, sem requests externos ou não-GET. O preview utilizou fixture fictícia e não possui persistência.

`PRODUCT_DESIGN_TARGETED_QA = PASS_WITH_FINDINGS`
`IMPLEMENTATION_REGRESSION = PASS`
`FAMILY_TECHNICAL_LOGIC = PASS`
`EVIDENCE_REFRESH = DEFERRED_BY_WORKSTATION_CAPABILITY`
`USER_VISUAL_APPROVAL = PENDING`
`PROJECT_STATE_UPDATE = DEFERRED_NO_AUTHORITY`

## Adjudicação final da revisão humana — DS 2.0.2 — 2026-09-30

Os status abaixo supersedem os resultados `PENDING` e `PASS_WITH_FINDINGS` dos checkpoints anteriores, que descreviam o estado anterior à resolução dos metadados e à decisão visual humana. Esses registros permanecem como histórico.

```text
DESIGN_SYSTEM_VERSION = 2.0.2
PRODUCT_DESIGN_TARGETED_QA = PASS
P3_C_DS_2_0_2_REGRESSION = PASS
STALE_DS_2_0_1_CURRENT_METADATA = RESOLVED
STALE_METADATA_STATUS = RESOLVED
HUMAN_VISUAL_APPROVAL = PASS
USER_VISUAL_APPROVAL = PASS
P3_C_VISUAL_REVIEW = PASS_WITH_NONBLOCKING_LIMITATIONS
P3_C_OWNED_SCREENS = USER_APPROVED / FROZEN
BLOCKING_FINDINGS = NONE
P3_C_SPECIFIC_BLOCKING_FINDINGS = NONE
SURFACE_REFINEMENT_REQUIRED = NO
DESIGN_SYSTEM_CHANGE_REQUIRED = NO
```

A decisão humana foi baseada em seis capturas atuais DS 2.0.2, cobrindo Activities lista/formulário, Governance estado/ação, Events lista/detalhe e Events lista mobile. Elas estão em `docs/prototype/ui-v2/evidence/screenshots/p3-c/review-2026-09-30/`. Esta rodada não gerou captura nova de cada um dos dez IDs. O aceite dos demais estados da família é apoiado pela QA técnica familiar já registrada e pelo contrato de herança de `SCR-ACT-EDIT-001`.

A checagem direcionada confirmou ARGOS Hybrid, legibilidade e scroll local de tabela, composição de formulário, ações de governança, hierarquia do detalhe de evento e comportamento mobile. O relatório técnico continua sendo a fonte para a regressão completa dos três consumidores de tabela: overflow global ausente, scroll local mobile funcional, nenhuma fragmentação destrutiva e acesso a ações por teclado.

Limitações sem bloqueio:

```text
MOBILE_DS_BADGE_NOT_IN_FRAME = EXPECTED / NONBLOCKING
MOBILE_FULL_PAGE_COMPOSITION = NOT_REVALIDATED_BY_THIS_SPECIFIC_SCREENSHOT
```

A tabela foi o alvo deliberado do enquadramento mobile, deixando o selo fora do frame. A composição mobile integral não foi revalidada por essa captura específica; a versão DS 2.0.2 foi validada antes dela. O shell P3 conserva as diferenças canônicas de sidebar, breadcrumbs e conteúdo frente à referência sistêmica Style Lab C. Não há finding visual acionável nem solicitação de alteração no DS.

```text
P3_C_COMPLETE = YES
P3_C_STATUS = USER_APPROVED / FROZEN / CLOSED / PUBLISHED
REMAINING_P3_C_GATES = NONE / integrated validation remains the next global gate
PROJECT_STATE_UPDATE = PASS / ROOT integration recorded in PROJECT_STATE.md section 40
```

A aprovação é representativa e não afirma nova captura screen-by-screen. Não foi reaberta a suíte histórica.
