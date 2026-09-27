# ARGOS_FRONTEND_AUDIT_REPORT

**Conclusão:** auditoria concluída.  
**OVERALL_FRONTEND_HEALTH = STRUCTURAL_REFACTOR_RECOMMENDED**  
**IMPLEMENTATION_PERFORMED = NO**  
**GIT_STATE_UNCHANGED = YES**  
**READY_FOR_ARCHITECTURAL_REVIEW = YES**

## Resumo executivo

A dificuldade de ajustar a interface vem principalmente de responsabilidades CSS sobrepostas, regras históricas ainda presentes na cascata e breakpoints baseados na largura da janela quando o conteúdo já está limitado a 1400 px. O Design System oferece uma base útil; a remediação deve consolidar essa base e estabilizar seus consumidores.

A arquitetura Django SSR, templates, HTML semântico e JavaScript Vanilla pode ser preservada. Não há evidência que justifique migrar para SPA, React, Vue, Angular, Tailwind ou Bootstrap.

## Escopo, estado e limites

Inspecionei o checkout indicado em `C:\Users\walac\desenvolvimento\projeto_argos`: branch `master`, HEAD `cad076099258e96b13f9e5ef11b301fc68891c4d`, upstream `origin/master`, três commits à frente. Antes e depois, não havia arquivos staged ou untracked. Os mesmos cinco arquivos estavam modificados antes e depois: `AGENT_CONTINUITY.md`, `PROJECT_STATE.md`, `argos.css`, `design-system.css` e `inventario.css`.

Dashboard, Inventário e Quick Detail foram observados em navegador local, zoom 100%, nas dimensões indicadas abaixo. O banco apresentou uma câmera; portanto, clipping e conteúdo intrínseco de nomes e valores mais longos não foram cobertos. O sistema operacional negou acesso à identificação do processo que serve `127.0.0.1:8000`; os valores CSS observados coincidiram com os arquivos inspecionados, mas a origem do processo não ficou comprovada. Não havia captura da referência visual a 80% para comparação direta. Nenhum arquivo do checkout canônico foi editado.

## Root cause analysis

| Causa | Evidência | Gravidade | Classe de correção |
|---|---|---|---|
| Ownership CSS concorrente | `.button`, `.metric-card` e `.table-region` têm regras em folhas diferentes; tabela e drawer recebem várias camadas no `inventario.css`. | Alta | Consolidar e remover regras |
| Breakpoints baseados no viewport | Em 2552 px, 11 colunas de 112,5 px cabem num painel de 1400 px. Em 900 px, a sidebar ainda ocupa 192 px; o shell muda em 896 px. | Alta | Rever composição responsiva |
| Ação maior que a coluna | Em 1366 px, a ação renderiza em 108 px, mas o texto `nowrap` exige 126 px. | Alta | Dimensionar coluna e ação em conjunto |
| Compactação compensatória do drawer | Regra de altura em 800 px muda tipografia, padding, gaps, imagem e scroll do shell. | Média/alta | Simplificar depois de estabilizar densidade |
| Tokens parcialmente contornados | Busca e botão Filtrar medem 36 px; o summary mede 39 px. O token do topbar é 40 px, mas a altura renderizada é 43 px. | Média | Definir contratos dos componentes |

## Mapa CSS e ownership

A ordem de carregamento no Inventário é **Design System → shell → portal → inventário → governança**, conforme `templates/base.html` e `cameras/templates/cameras/lista.html`. `portal.css` é carregado em todas as páginas do shell.

| Folha | Responsabilidade pretendida e real | Conflitos, tokens e media |
|---|---|---|
| `design-system.css` | Tokens, tipografia, botões, cards, campos, badges, tabela genérica e foco. Também contém composição de filtros. | Define alturas, cores, spacing, radius, larguras e tipografia. Tem 4 grupos media na folha carregada. Regras de campos e filtros são reestilizadas por consumidores. |
| `argos.css` | Shell: sidebar, topbar, page container e navegação. Também define multiselect e filtros ativos. | `.table-region` também aparece no Design System e no Inventário. 8 grupos media; filtros compartilhados tornam o ownership ambíguo. |
| `portal.css` | Composição do portal e do Dashboard: grids, seções, métricas e atividade. | `.metric-card` é um primitivo compartilhado; há versões anteriores de `.dashboard-section`/métricas. 5 grupos media. |
| `inventario.css` | Página de inventário, filtros, tabela de câmeras, ações e Quick Detail; também estilos de outros fluxos de câmera. | Redefine `.button`, `.button--primary`, `.metric-card`, tabela e drawer. 36 grupos media e a maior concentração de hardcodes/overrides. |
| `governanca.css` | Componentes específicos de governança e substituição. | É carregado depois do Inventário nessa tela, podendo sobrepor componentes compartilhados. 1 grupo media. |

Não encontrei container queries nas folhas principais.

**Ownership recomendado:**

- `design-system.css`: button, input, select nativo, card, badge, tabela genérica e tokens.
- `argos.css`: sidebar, topbar, shell e page container.
- `portal.css`: grids e composição exclusiva do Dashboard.
- `inventario.css`: filtros do Inventário, seletor personalizado, tabela de câmeras e ações.
- Uma seção delimitada no `inventario.css`: dialog, drawer cards e footer.
- O multiselect deve ter uma única folha canônica. O page header compartilhado deve ter um contrato único; as páginas apenas o compõem.

## Cascata, especificidade e tokens

- **Busca:** a regra comum de campos do Design System fornece `min-height:36px`; sua regra seguinte reduz o padding vertical para 4 px. A combinação de `:is()` e `:not()` tem especificidade alta, aproximadamente **(0,4,1)**, o que dificulta ajustes locais.
- **Filtros:** o controle é `<details><summary>`, não `<select>` nativo. `.filter-multiselect__summary` declara mínimo 44 px, mas uma regra posterior aplica o token de 36 px. Padding vertical de 8 px resulta em altura computada de 39 px.
- **Filtrar:** `.button` do Design System vence com 36 px; `.filter-panel__actions .button` adiciona `white-space:nowrap`.
- **Botões da tabela:** `.button--small` usa 32 px. `.table-actions .button` define `width:100%`, `min-width:0` e `nowrap`; a regra posterior `.camera-table .table-actions .button` vence com `width:auto` e `min-width:108px`.
- **Tabela:** o mínimo genérico de 42 rem é substituído por 62 rem e depois 64 rem (1024 px), com `table-layout:fixed`. Larguras antigas por `nth-child` ainda competem com regras posteriores.
- **Dashboard:** `.metric-card.dashboard-metric` zera um mínimo anterior, mas `.dashboard-metric-grid .dashboard-metric` o impõe novamente em 124 px. Altura observada: 125 px.
- **Quick Detail:** UI-3 reescreve as regras anteriores e UI-4 acrescenta a compactação por altura. A identidade usa `!important`; a regra de altura repete o override.

Os tokens de spacing, font-size, line-height, radius, cores, alturas, largura de conteúdo e sidebar são usados em parte. Existem aliases de compatibilidade e pares com a mesma semântica, por exemplo `--font-size-base` e `--font-size-body`. `--table-row-min-height` não se aplica à `.camera-table` pelo seletor atual. Padding, gaps e algumas alturas continuam em valores literais nas folhas de página.

## Densidade e matriz de viewports

Medições em zoom 100%:

| Viewport | Main | Filtros | Tabela | Quick Detail |
|---|---:|---|---|---|
| 2552×866 | 1400 px | 11 colunas; labels quebram | `clientWidth 1398`, `scrollWidth 1400` | Corpo rola: 802/687 px |
| 2048×914 | 1400 px | 6 colunas, 2 linhas | 2 px de excesso | Corpo rola: 802/735 px |
| 1920×1080 | 1400 px | 6 colunas, 2 linhas | 2 px de excesso | Corpo cabe: 901/901 px |
| 1366×768 | 1093 px | 6 colunas, 2 linhas | 1098/1091 px | Compactação por altura; 621/621 px |
| 900×768 | 650 px | 3 colunas | Tabela vira cards | Compactação por altura; 621/621 px |
| 390×844 | 343 px | 1 coluna | Cards, sem overflow horizontal observado | Corpo rola: 836/613 px |

No desktop, a sidebar mede 192 px, o topbar 43 px, o container chega a 1400 px, o espaçamento superior é 32 px e o inferior 40 px. Busca e “Filtrar” medem 36 px; summaries personalizados medem 39 px; o header de tabela mede cerca de 39 px. A linha observada mede 100 px em 2552 e 116,5 px em 1366, em parte por conteúdo quebrado. A interface combina áreas amplas do shell com filtros estreitos e ações comprimidas. A referência a 80% é direção visual; não deve ser reproduzida matematicamente.

## Inventário

### Causa do scroll horizontal

Em 1366 px, as colunas renderizam aproximadamente **120 / 186 / 145 / 134 / 186 / 200 / 120 px**. Governança tem `min-width` de célula de 168 px; Ações declara 7,5 rem, enquanto o botão exige no mínimo 6,75 rem. O botão mede 108 px, tem `clientWidth:106` e `scrollWidth:126`. Como o texto não quebra, a célula de ações chega a `scrollWidth:127` para 120 px visíveis. A região e a tabela passam a 1098 px para 1091 px disponíveis. Em 2552 px, sobram 2 px de conteúdo. A região com `overflow-x:auto` contém o excesso, mas não corrige o sizing. Os demais conteúdos da única linha observada couberam ou quebraram; max-content de dados longos não foi verificado.

### Alinhamento dos filtros

Em 2552 px, a regra de viewport a partir de 144 rem ativa 11 trilhas de 112,5 px dentro de um painel de 1400 px. Os labels “Status legado” e “Situação operacional” quebram em duas linhas. Busca e botão Filtrar começam 3 px abaixo dos summaries, cuja altura é 39 px; os demais medem 36 px. Em 1366 px, seis trilhas de aproximadamente 165 px produzem duas linhas e menos quebra de label, mas mantêm a diferença de altura. A regra responde à largura da janela, não à largura disponível no painel.

O header do painel de resultados apresenta título e contagem alinhados; o count fica à direita e há espaçamento consistente. O problema principal nessa seção é a largura da tabela e o clipping das ações.

## Sidebar

A marca usa ícone de 36 px, gap de 8 px, texto de subtítulo em torno de 103 px e 8 px de padding lateral em cada lado: cerca de 163 px sem folga. O maior label observado (“Governança”) mede cerca de 78 px e não supera a exigência da marca.

- **SIDEBAR_MIN_COMFORTABLE_WIDTH = 176 px**
- **SIDEBAR_RECOMMENDED_WIDTH = 192 px**
- **SIDEBAR_MAX_REASONABLE_WIDTH = 216 px**

164 px fica no limite e tende a truncar a marca; 192 px acomoda o conteúdo observado; 248 px consome 56 px extras da área de trabalho sem benefício proporcional. A estimativa não inclui outras fontes ou textos localizados.

## Dashboard

Em 1920×1080, os 12 cards medidos têm 125 px de altura. Inventário ocupa uma linha; Monitoramento usa três colunas para quatro cards e deixa o último sozinho na segunda linha. O painel de Monitoramento mede 362 px, com padding de 20 px. As seções têm 24 px de separação. Em 900 px, grids passam a duas colunas; em 390 px, a uma coluna, sem overflow horizontal observado.

O mínimo de 7,75 rem não explica sozinho a altura dos cards: o grid interno já reserva três linhas que somam quase esse mínimo. Uma remediação deve avaliar o mínimo e `grid-template-rows` juntos.

## Quick Detail Drawer

O elemento rolável é `.camera-quick-detail__body` (`overflow-y:auto`), não o `<dialog>` raiz. Em 2552×866, o drawer mede 512×866 px: header 77, navegação 41, preview 245, identidade 103, cada card 130 e footer 61 px. O corpo oferece 687 px para 802 px de conteúdo. Em 2048×914 ainda faltam 67 px; em 1920×1080 cabe. `@media(max-height:800px)` comprime preview, cards, gaps e tipografia e, no exemplo, faz caber em 768 px. Também muda o scroll do `main` atrás do modal por meio de `:has()`.

**QUICK_DETAIL_SCROLL_ROOT_CAUSE = BOTH, predominantemente local.** Limite vertical e composição local determinam o scroll; tipografia e tokens compartilhados participam da altura. O acoplamento via `:has()` estende a regra local ao shell.

## Responsividade

| Breakpoint | Arquivos | Efeito e conflito |
|---|---|---|
| 144 rem mínimo | Inventário | Força 11 colunas dentro de painel de 1400 px; labels ficam estreitos. |
| 75–84 rem e 75 rem máximo | Inventário | Ajusta colunas e troca tabela por cards com base no viewport, não no espaço útil. |
| 64 rem | Shell, Portal | Reorganiza grids; regra da sidebar repete o token sem alterar seu valor. |
| 56 rem | Shell, Portal, Inventário | Sidebar vira barra superior e grids mudam. Em 900 px (4 px acima de 896), sidebar ainda comprime o main. |
| 44 rem | Folhas principais | Mobile, toque, tabela e drawer; vários componentes são redefinidos em blocos distintos. |
| 34 rem, 32,5 rem, 30 rem; 760/480 px | Inventário, Portal e legados | Degraus adicionais parcialmente sobrepostos. |
| 800 px de altura | Inventário | Compacta o drawer e acopla seu estado ao scroll do shell. |

Não encontrei container queries. A CSSOM das cinco folhas carregadas no Inventário contém aproximadamente 54 grupos `@media`.

## Acessibilidade e interação

Há skip link, labels, região de tabela focável, estilos `:focus-visible` e `:focus-within`. Abrir o dialog moveu o foco para o botão Fechar; fechar pelo botão e por Escape devolveu o foco ao gatilho. Busca, filtro e ações principais atingem 44 px em mobile. Botões de navegação do Quick Detail permanecem em 32 px por override local. O texto da ação da tabela é cortado/ultrapassa a célula no desktop. Não foram feitos teste formal de contraste, leitor de tela ou ampliação de texto; não declaro conformidade WCAG.

## Métricas aproximadas de dívida CSS

Medições da CSSOM. Repetições incluem variantes responsivas intencionais e indicam volume para revisão, não quantidade de defeitos.

| Arquivo | Regras | Declarações repetidas para mesmo seletor/propriedade | Pares com valores divergentes | Valores literais de sizing |
|---|---:|---:|---:|---:|
| Design System | 137 | 14 | 10 | 28 |
| Shell | 95 | 49 | 22 | 69 |
| Portal | 84 | 17 | 8 | 23 |
| Inventário | 599 | 326 | 136 | 349 |
| Governança | 145 | 77 | 24 | 51 |

## Patches para remover ou consolidar antes de adicionar regras

- Larguras antigas de tabela por `nth-child` e sequência de `min-width` 62→64 rem.
- Versões anteriores de padding/layout de tabela que já perderam na cascata.
- Mínimo anterior do summary personalizado, sobrescrito pelo token posterior.
- Regra de 11 colunas em 144 rem; o painel continua limitado a 1400 px.
- Declarações repetidas do frame de preview no drawer.
- `!important` da identidade e partes da compactação por altura, após provar qual comportamento cada uma sustenta.
- Regra `:has()` que muda o shell quando o drawer abre, revisar separadamente antes de remover.

Preservar durante a transição a contenção de scroll da tabela, transformação em cards, estados de foco, alvos de toque, semântica/gestão de foco do dialog e suporte a movimento reduzido. Preservar o comportamento não exige manter os valores atuais.

## Modelo de tokens recomendado

Manter alturas semânticas de controle para desktop (36 px), compacto (32 px) e toque (44 px), mais tokens de largura máxima de página, sidebar, espaçamento de seção e padding de card. Cada componente deve consumir o contrato apropriado; regras locais não devem anular o alvo de toque. Consolidar aliases e valores existentes antes de criar tokens novos. Não usar `zoom`, `transform:scale()` nem redução global de 20%.

## Plano de remediação

| Fase | Objetivo e arquivos prováveis | Risco | Gate de aceitação |
|---|---|---|---|
| 1. Ownership e consolidação | `design-system.css`, `argos.css`, `portal.css`, `inventario.css` | Alto para seletores globais | Cascata documentada; componentes sem mudança acidental. |
| 2. Shell | Design System e `argos.css` | Médio/alto | Sidebar, topbar e container estáveis nas seis larguras. |
| 3. Densidade compartilhada | Design System e consumidores | Alto | Controles obedecem alturas de desktop, compacto e toque. |
| 4. Responsividade do Inventário | `inventario.css`, template se necessário | Alto | Sem clipping nem scroll por ações; filtros alinhados; testar dados longos. |
| 5. Dashboard | `portal.css` | Médio | Alturas justificadas e disposição deliberada dos quatro cards de monitoramento. |
| 6. Quick Detail | Seção do drawer no `inventario.css` | Alto | Scroll previsível em alturas intermediárias; footer e foco acessíveis. |

**HIGHEST_RISK_CHANGES:** seletores globais `.button` e campos, largura do shell, breakpoint da tabela e regra de altura/scroll do drawer.  
**LOW_RISK_QUICK_WINS:** remover declarações comprovadamente vencidas e consolidar duplicações sem alterar valores computados.  
**FILES_EXPECTED_TO_CHANGE_DURING_REMEDIATION:** quatro folhas principais; possivelmente `governanca.css` e templates que consumam contratos compartilhados.

## Campos finais

- **EXECUTIVE_SUMMARY:** ownership CSS difuso, breakpoints inconsistentes com a largura útil e overrides compensatórios explicam a maioria das regressões.
- **CSS_ARCHITECTURE_FINDINGS:** cinco folhas disputam componentes; 54 grupos media nas folhas carregadas no Inventário; nenhuma container query encontrada.
- **CSS_OWNERSHIP_CONFLICTS:** button, metric-card, table-region, filter summary, camera-table e Quick Detail.
- **CASCADE_CONFLICTS:** summary final de 39 px, busca/botão 36 px, ações de tabela 32 px com conteúdo maior, tabela mínima 1024 px.
- **TOKEN_FINDINGS:** tokens existem e são parcialmente reutilizados; aliases e valores locais competem com eles.
- **HARDCODED_VALUE_FINDINGS:** 520 valores literais de sizing somados nas cinco folhas, segundo a contagem CSSOM acima.
- **RESPONSIVE_FINDINGS:** regras por viewport sobrepostas; 900 px mantém shell desktop, filtros desktop e pouco espaço horizontal.
- **INVENTORY_FINDINGS:** filtros e tabela respondem a breakpoints de viewport; botão de ação excede sua coluna.
- **TABLE_OVERFLOW_ROOT_CAUSE:** `nowrap` mais coluna de ações menor que o conteúdo intrínseco.
- **FILTER_ALIGNMENT_ROOT_CAUSE:** 11 colunas em painel limitado, labels quebrados, padding e altura diferentes entre controls.
- **SIDEBAR_FINDINGS:** mínimo confortável 176 px; 192 px recomendado; 216 px máximo razoável.
- **DASHBOARD_FINDINGS:** quarto card de monitoramento fica sozinho na segunda linha; min-height e grid rows juntos determinam a altura.
- **QUICK_DETAIL_FINDINGS:** body interno rola; compactação por altura é extensa e acoplada ao shell.
- **QUICK_DETAIL_SCROLL_ROOT_CAUSE:** ambos os fatores, com predominância local.
- **ACCESSIBILITY_FINDINGS:** foco e retorno do foco observados; alvos de toque no mobile geralmente 44 px, navegação do drawer 32 px; contraste e leitor de tela não foram formalmente avaliados.
- **IMPLEMENTATION_PERFORMED:** NO.
- **GIT_STATE_UNCHANGED:** YES.
- **READY_FOR_ARCHITECTURAL_REVIEW:** YES.

**Limitações:** processo que serve a aplicação não foi atribuído ao checkout por bloqueio de acesso do sistema operacional; somente uma câmera estava disponível; capturas foram inspecionadas no navegador, mas não persistidas como arquivos. O `AGENTS.md` do repositório exige atualização de `PROJECT_STATE` para atividades formais, mas a auditoria proibiu qualquer edição, então esse gate documental permanece pendente.
