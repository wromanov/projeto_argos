# ARGOS · Dashboard V7 — Design QA do protótipo

## Evidência

- HTML renderizado via Chromium com conteúdo fornecido em memória, após bloqueio de abertura `file://` pelo ambiente de automação.
- Viewports: 1920×1080, 1440×900, 1366×768 e 390×844 (DPR 1).
- Fixtures: `default`, `scale`, `long`, `empty`.
- Resultado: **16/16 cenários renderizados**, **0 exceções de página**, **0 erros de JavaScript capturados**, **0 overflow horizontal global**.
- Capturas de referência das quatro resoluções incluídas. Capturas `full_page` podem exceder a altura nominal do viewport quando há rolagem vertical legítima.
- O DOM da sidebar e o DOM da topbar foram comparados à referência V3 anexada: **idênticos**, sem alteração de conteúdo nesses elementos.

## Limites

Este QA valida apenas o protótipo HTML isolado. Não comprova a equivalência dos estilos computados da sidebar integrada no Django, nem testes de teclado/foco, operações de navegação, banco, permissions, services MON, funcionalidades ou integração. Tais testes são posteriores, no runtime Django. Não declarar `DESIGN_QA_INTEGRATED = PASS` com base nestas capturas.

## Findings não bloqueantes para transposição

- Elemento `<title>` do HTML V7 ainda contém texto histórico de V5. A fonte visual permanece V7, aprovada pelo usuário; não confundir metadados do protótipo com autoridade da composição.
- A terminologia aprovada no Django pode divergir dos rótulos históricos do protótipo. Consultar `VISUAL_CONTRACT_V7.md` antes de implementar.

`PROTOTYPE_VISUAL_GATE = PASS (human)`  
`PROTOTYPE_TECHNICAL_QA = PASS (scoped)`  
`DJANGO_INTEGRATION = PENDING`
