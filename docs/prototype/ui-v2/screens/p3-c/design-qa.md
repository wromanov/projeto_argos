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
