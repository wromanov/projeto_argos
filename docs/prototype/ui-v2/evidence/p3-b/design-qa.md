# P3-B — design-qa

**Fonte visual:** `docs/prototype/ui-v2/style-lab/screenshots/argos-style-c.png` (ARGOS Hybrid; 1425×1395 px).
**Implementações:** `SCR-MON-HISTORY-001`, `SCR-SUB-LIST-001`, `SCR-SUB-DETAIL-001`, `SCR-SUB-CAMERA-001`.
**Viewports inspecionadas:** 1440×900 e 390×844 CSS px; capturas atuais ainda não persistidas no diretório canônico.

## Resultado

**DESIGN_QA_COMPLETE = NO**
**final result: blocked**

A revisão visual no Browser do Codex mostrou linguagem visual coerente com a referência: sidebar azul-marinho, azul de seleção, canvas claro, cartões, tabelas, tipografia e chips. A Style Lab C fornece direção visual; não é um mock aprovado da composição P3-B. Os quatro defaults foram vistos em desktop e mobile. Estados funcionais e comportamento responsivo foram revalidados no DOM.

O gate formal está bloqueado porque as capturas do Browser do Codex ficam em memória e não podem ser salvas como PNGs nos caminhos de evidência. A autorização para usar Playwright local foi concedida neste checkpoint. As capturas continuam pendentes porque a instrução de hoje é não iniciar nova QA. As imagens históricas do checkpoint são DS 2.0.0 e não são evidência válida do estado após a propagação.

## Comparação e findings

- **P0/P1:** nenhum observado nas vistas examinadas.
- **P2:** nenhum desvio visual material observado nos defaults; a navegação do shell rola horizontalmente em mobile sem overflow do documento, e as tabelas usam sua própria rolagem horizontal.
- **Correções concluídas durante QA:** contagem dos vazios de monitoramento e consulta por câmera ajustada para `0 registros`; nomes de paginação traduzidos e específicos em estados com e sem resultados.
- **Acessibilidade relacionada ao visual:** foco de teclado visível (contorno de 3 px); campos e controles principais com pelo menos 44×44 CSS px; detalhes imutáveis sem ações de edição/exclusão.

## Para fechar o gate

1. Gerar e persistir as capturas atuais com os nomes e viewports definidos na cobertura P3-B; cobrir os estados aplicáveis e variantes longas.
2. Confirmar zoom/escala e registrar dimensões CSS e pixels das capturas.
3. Fazer a comparação lado a lado por tela/estado, registrar findings por prioridade e atualizar `final result` para `passed` ou manter `blocked` com razão objetiva.
4. Só depois promover as quatro telas a `TECHNICAL_READY_FOR_REVIEW`; manter `USER_VISUAL_APPROVAL = PENDING` para a revisão humana.