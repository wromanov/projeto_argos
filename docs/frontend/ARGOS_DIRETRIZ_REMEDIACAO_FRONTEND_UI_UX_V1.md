# ARGOS — DIRETRIZ DE REMEDIAÇÃO FRONT-END, UI/UX E ARQUITETURA CSS

**Versão:** 1.0  
**Status:** Diretriz técnica para remediação pós-auditoria UI-AUD-01  
**Projeto:** ARGOS  
**Escopo:** Front-end, UI/UX, arquitetura CSS, responsividade e estabilização visual  
**Documento-base:** `ARGOS_FRONTEND_AUDIT_REPORT.md`

---

## 1. Finalidade

Este documento orienta o agente principal do Projeto ARGOS na remediação estrutural do front-end após a auditoria `UI-AUD-01`.

O objetivo não é redesenhar o produto, substituir sua stack ou introduzir uma SPA.

O objetivo é:

- estabilizar a arquitetura CSS;
- definir ownership claro entre Design System, shell e páginas;
- eliminar conflitos de cascata e regras históricas;
- reduzir hardcodes e overrides compensatórios;
- corrigir densidade e responsividade do desktop;
- estabilizar Inventário, Dashboard e Quick Detail;
- reduzir regressões entre componentes;
- tornar alterações futuras de UI previsíveis e de baixo risco;
- preservar a identidade visual já aprovada do ARGOS.

A auditoria concluiu:

`OVERALL_FRONTEND_HEALTH = STRUCTURAL_REFACTOR_RECOMMENDED`

Essa conclusão deve ser tratada como recomendação de refatoração estrutural do CSS existente, e não como recomendação de troca de stack.

---

## 2. Stack front-end que deve ser preservada

A remediação deve manter a arquitetura atual:

```text
Django SSR
Django Templates
HTML semântico
CSS customizado
JavaScript Vanilla
Progressive Enhancement
componentes nativos do navegador
<dialog> nativo no Quick Detail
Design System próprio do ARGOS
```

Não introduzir como solução estrutural:

```text
React
Vue
Angular
Svelte
Tailwind
Bootstrap
shadcn/ui
SPA
bundler obrigatório
zoom CSS
transform: scale()
scale global
```

A auditoria não encontrou evidência que justifique migrar a aplicação para outra stack.

---

## 3. Diagnóstico consolidado

### 3.1. Causa principal

A dificuldade encontrada nas últimas atividades não decorre de um único componente mal dimensionado.

A causa predominante é a combinação de:

```text
CSS OWNERSHIP DIFUSO
+
CASCATA COM MÚLTIPLOS OVERRIDES
+
REGRAS HISTÓRICAS AINDA PRESENTES
+
VALORES HARDCODED
+
BREAKPOINTS BASEADOS NO VIEWPORT
SEM CONSIDERAR A LARGURA REAL DO CONTEÚDO
+
PATCHES VISUAIS COMPENSATÓRIOS
```

A auditoria identificou conflitos reais de ownership em componentes como:

- `.button`;
- `.metric-card`;
- `.table-region`;
- filtros;
- tabela de câmeras;
- Quick Detail.

Isso explica o comportamento observado durante as tentativas anteriores:

```text
ajusta componente A
↓
regra B passa a vencer na cascata
↓
componente C muda de dimensão
↓
outro breakpoint passa a atuar
↓
surge regressão em outra página
```

Esse ciclo deve ser encerrado.

---

## 4. Gravidade da dívida CSS

A auditoria encontrou aproximadamente:

| Arquivo | Regras | Repetições seletor/propriedade | Pares divergentes | Valores literais de sizing |
|---|---:|---:|---:|---:|
| `design-system.css` | 137 | 14 | 10 | 28 |
| `argos.css` | 95 | 49 | 22 | 69 |
| `portal.css` | 84 | 17 | 8 | 23 |
| `inventario.css` | 599 | 326 | 136 | 349 |
| `governanca.css` | 145 | 77 | 24 | 51 |

O principal ponto de atenção é `inventario.css`.

Essa folha concentra:

- alto volume de regras;
- muitas declarações repetidas;
- muitos valores divergentes;
- grande quantidade de hardcodes;
- regras de Inventário;
- tabela;
- ações;
- filtros;
- Quick Detail;
- responsividade;
- regras históricas acumuladas.

### Política nova

A partir desta diretriz:

```text
REMOVER / CONSOLIDAR
ANTES DE
ADICIONAR NOVOS OVERRIDES
```

Nenhuma atividade futura de UI deve começar automaticamente criando novas regras CSS.

---

## 5. Ownership CSS canônico desejado

O front-end deve convergir para responsabilidades claras.

### 5.1. `design-system.css`

Fonte canônica de:

```text
tokens
tipografia base
button
input
select nativo
card genérico
badge
tabela genérica
focus
estados interativos
control sizing
spacing primitives
semantic component tokens
```

Não deve possuir composição específica de páginas quando isso puder ser mantido no consumidor.

### 5.2. `argos.css`

Fonte canônica de:

```text
application shell
sidebar
topbar
main
page container
navegação global
estrutura responsiva do shell
```

### 5.3. `portal.css`

Fonte canônica de:

```text
Dashboard
Dashboard grids
Dashboard sections
Dashboard metric composition
Dashboard activity composition
```

Não deve redefinir primitives compartilhados do Design System.

### 5.4. `inventario.css`

Fonte canônica de:

```text
Inventory composition
filter panel
Inventory grid
camera table
Inventory actions
Inventory responsive composition
```

Não deve redefinir globalmente componentes compartilhados como `.button`, `.card` ou outros primitives, salvo quando existir variante explicitamente pertencente ao Inventário.

### 5.5. Quick Detail

O Quick Detail pode continuar em `inventario.css`, porém deve existir em uma seção claramente delimitada:

```text
QUICK DETAIL ROOT
QUICK DETAIL HEADER
QUICK DETAIL NAV
QUICK DETAIL PREVIEW
QUICK DETAIL IDENTITY
QUICK DETAIL CARDS
QUICK DETAIL FOOTER
QUICK DETAIL RESPONSIVE
```

As regras do Quick Detail não devem modificar o shell global sem justificativa forte e documentada.

A regra atual com `:has()` que altera o scroll do shell deve ser reavaliada em fase própria.

---

## 6. Regra fundamental de implementação

Antes de alterar qualquer propriedade visual, o executor deve responder:

```text
QUEM DEVERIA POSSUIR ESTA PROPRIEDADE?
```

Exemplos:

```text
height do button?
→ Design System.

largura da sidebar?
→ Shell / argos.css.

largura da coluna Ações?
→ Inventário / inventario.css.

padding do card do Quick Detail?
→ Quick Detail.

grid de Monitoramento do Dashboard?
→ Portal / portal.css.
```

Se uma propriedade estiver sendo controlada pelo arquivo errado, a prioridade é corrigir o ownership.

Não adicionar outro override apenas para vencer a cascata existente.

---

## 7. Baseline provisório atual

Os seguintes valores podem permanecer temporariamente durante a remediação:

```text
MAIN_CONTENT_MAX_WIDTH = 1400px

SIDEBAR_WIDTH = 192px

TOPBAR_TOKEN ≈ 40px

STANDARD_DESKTOP_CONTROL_HEIGHT = 36px

COMPACT_DESKTOP_CONTROL_HEIGHT = 32px

TOUCH_CONTROL_HEIGHT = 44px

PAGE_TOP_SPACING ≈ 32px

PAGE_BOTTOM_SPACING ≈ 40px
```

Esses valores devem ser tratados como:

```text
PROVISIONAL_BASELINE
```

A auditoria validou tecnicamente para a sidebar:

```text
SIDEBAR_MIN_COMFORTABLE_WIDTH = 176px
SIDEBAR_RECOMMENDED_WIDTH = 192px
SIDEBAR_MAX_REASONABLE_WIDTH = 216px
```

Portanto, `192px` é o melhor baseline atual e não deve ser alterado sem nova evidência.

---

## 8. Problemas confirmados — Inventário

### 8.1. Scroll horizontal da tabela

A causa foi identificada.

Em viewport de 1366 px:

- a coluna de Ações possui aproximadamente 120 px;
- o botão renderiza em aproximadamente 108 px;
- o conteúdo `nowrap` exige aproximadamente 126 px;
- a célula precisa de aproximadamente 127 px;
- a tabela excede o espaço disponível.

A região passa aproximadamente de:

```text
clientWidth ≈ 1091px
scrollWidth ≈ 1098px
```

A causa real não é simplesmente “tabela larga”.

É:

```text
NOWRAP
+
COLUNA MENOR QUE O CONTEÚDO INTRÍNSECO
+
MIN-WIDTHS / REGRAS HISTÓRICAS CONCORRENTES
```

#### Direção de correção

A correção deve tratar coluna e ação em conjunto.

Não resolver através de:

```text
overflow:hidden
redução arbitrária de fonte
escala
aumento indiscriminado do container
```

Deve-se revisar:

- largura da coluna Ações;
- `min-width`;
- `white-space`;
- dimensão real do botão;
- regras históricas por `nth-child`;
- mínimos antigos de tabela;
- política de sizing das colunas.

### 8.2. Desalinhamento dos filtros

Em viewport largo, uma regra a partir de `144rem` cria 11 trilhas de aproximadamente 112,5 px dentro de um painel limitado a 1400 px.

Isso provoca:

- labels quebrando em duas linhas;
- `Status legado` e `Situação operacional` desalinhados;
- summaries personalizados com aproximadamente 39 px;
- busca e botão Filtrar com 36 px;
- diferença vertical entre componentes visualmente equivalentes.

#### Causa

A responsividade responde à largura total da janela e não à largura disponível do painel.

#### Direção

A composição de filtros deve responder ao espaço efetivamente disponível.

A regra de 11 colunas em `144rem` deve ser removida ou reformulada.

Não criar novas colunas apenas porque o monitor é largo quando o conteúdo está limitado a 1400 px.

---

## 9. Problemas confirmados — Sidebar

A sidebar não deve mais ser ajustada por tentativa visual.

A auditoria mediu:

- ícone de marca: aproximadamente 36 px;
- gap: 8 px;
- subtítulo: aproximadamente 103 px;
- paddings laterais: aproximadamente 16 px no total.

Necessidade mínima estimada da marca: aproximadamente 163 px sem folga.

Conclusão:

```text
164px = limite excessivamente apertado
192px = recomendado
248px = desperdício de espaço sem benefício proporcional
```

### Decisão

Preservar:

```text
SIDEBAR_WIDTH = 192px
```

até que uma nova necessidade objetiva justifique alteração.

---

## 10. Problemas confirmados — Dashboard

A auditoria encontrou:

```text
metric cards ≈ 125px de altura
12 cards medidos
section gap ≈ 24px
monitoring panel padding ≈ 20px
```

O quarto card de Monitoramento fica sozinho na segunda linha em determinadas larguras.

Também foi identificado que a altura dos cards não vem apenas do `min-height`.

Ela é resultado conjunto de:

```text
min-height
+
grid-template-rows
+
conteúdo interno
```

### Direção

Não corrigir a altura apenas removendo o `min-height`.

A fase de Dashboard deverá analisar simultaneamente:

- `min-height`;
- `grid-template-rows`;
- padding;
- line-height;
- gaps;
- distribuição dos quatro cards.

A composição final deve ser deliberada, não consequência acidental do grid.

---

## 11. Problemas confirmados — Quick Detail Drawer

O elemento que efetivamente rola é:

```text
.camera-quick-detail__body
```

e não o `<dialog>` raiz.

Em 2552×866:

```text
drawer ≈ 512×866px
header ≈ 77px
nav ≈ 41px
preview ≈ 245px
identity ≈ 103px
cada card ≈ 130px
footer ≈ 61px

body disponível ≈ 687px
conteúdo ≈ 802px
```

Portanto há aproximadamente 115 px de excesso.

Em 2048×914 ainda há falta de aproximadamente 67 px.

Em 1920×1080 o conteúdo cabe.

### Causa consolidada

```text
QUICK_DETAIL_SCROLL_ROOT_CAUSE =
BOTH, PREDOMINANTEMENTE LOCAL
```

A densidade global participa, mas a composição local é a principal causa.

### Problema adicional

A regra `@media(max-height:800px)` atualmente:

- reduz tipografia;
- reduz preview;
- reduz cards;
- altera gaps;
- altera footer;
- altera comportamento de scroll;
- interage com o shell através de `:has()`.

Ela é uma compactação compensatória extensa.

### Direção

O Quick Detail deve ser tratado somente após estabilização das fases anteriores.

A solução final deve simplificar, e não adicionar uma terceira camada de compactação.

---

## 12. Responsividade — problema arquitetural

A auditoria identificou aproximadamente 54 grupos `@media` nas folhas carregadas no Inventário.

Problemas principais:

- breakpoints parcialmente sobrepostos;
- regras antigas;
- breakpoints baseados no viewport;
- conteúdo limitado a 1400 px;
- shell ainda ocupando largura relevante;
- comportamento diferente entre 900 px e 896 px;
- transformações da tabela para cards;
- regras específicas por altura do drawer.

### Exemplo crítico

Em 900 px:

```text
sidebar ainda desktop = 192px
main ≈ 650px
```

A sidebar só muda de comportamento próximo a 896 px.

Isso significa que uma diferença mínima de viewport produz grande diferença de composição.

### Direção

Os breakpoints devem ser revisados com foco em:

```text
ESPAÇO REAL DO COMPONENTE
```

e não apenas na largura total da janela.

Quando apropriado e suportado pela arquitetura atual, avaliar uso futuro de container queries para componentes cuja composição depende do espaço do próprio container.

Não introduzir container queries indiscriminadamente.

---

## 13. Tokens e Density System

Os tokens atuais são úteis, porém parcialmente contornados por regras locais.

Deve-se consolidar primeiro o que já existe.

### Modelo recomendado

Avaliar semantic tokens como:

```css
--control-height-desktop
--control-height-compact
--control-height-touch

--page-max-width

--sidebar-width

--topbar-height

--section-gap

--card-padding

--table-row-height
```

### Regra

Não criar aliases novos enquanto existirem tokens duplicados com a mesma semântica.

Exemplo observado:

```text
--font-size-base
--font-size-body
```

Aliases redundantes devem ser consolidados gradualmente.

---

# 14. Estratégia de remediação

A auditoria propôs seis fases.

Esta diretriz acrescenta uma **Fase 0** antes delas.

---

## FASE 0 — Dead CSS / Defeated Rules Cleanup

### Objetivo

Reduzir a complexidade da cascata sem alterar o resultado visual.

### Regra absoluta

```text
COMPUTED_STYLE_BEFORE == COMPUTED_STYLE_AFTER
VISUAL_DELTA = NONE
FUNCTIONAL_DELTA = NONE
```

### Candidatos já identificados

Revisar e remover somente quando comprovadamente vencidos:

- larguras antigas de tabela por `nth-child`;
- sequência antiga de `min-width` `62rem → 64rem`;
- versões anteriores de padding/layout da tabela;
- mínimo antigo do summary personalizado;
- declarações repetidas do frame de preview;
- duplicações históricas comprovadamente sem efeito.

A regra de 11 colunas em `144rem` deve ser tratada com cuidado: ela é problemática, mas pode ainda produzir efeito. Se sua remoção alterar layout, pertence à fase de reparo do Inventário, não a esta limpeza sem delta visual.

### Não remover ainda sem prova

- `!important` da identidade;
- regra `:has()` do drawer;
- compactação `max-height:800px`;
- qualquer regra responsável por comportamento acessível ou responsivo atual.

Esses pontos exigem análise específica antes de remoção.

### Gate

```text
NO_COMPUTED_STYLE_CHANGE = YES
NO_VISUAL_CHANGE = YES
NO_FUNCTIONAL_CHANGE = YES
CSS_RULE_COUNT_REDUCED = YES
GIT_DIFF_REVIEWED = YES
```

---

## FASE 1 — CSS Ownership Consolidation

### Objetivo

Estabelecer uma única fonte de verdade para cada componente.

### Prioridades

1. button;
2. inputs;
3. selects;
4. cards;
5. table-region;
6. multiselect;
7. page header;
8. metric-card.

### Regra

Uma página não deve redefinir um primitive global quando uma variante semântica resolve o problema.

### Gate

```text
OWNER_DOCUMENTED_FOR_SHARED_COMPONENTS = YES
DUPLICATE_GLOBAL_OVERRIDES_REDUCED = YES
NO_VISUAL_REGRESSION = YES
```

---

## FASE 2 — Shell Stabilization

### Escopo

`argos.css` + tokens necessários.

### Preservar como baseline inicial

```text
page max-width = 1400px
sidebar = 192px
topbar ≈ 40px
top spacing ≈ 32px
bottom spacing ≈ 40px
```

### Objetivo

Validar shell em:

```text
2552×866
2048×altura real
1920×1080
1366×768
900×768
390×844
```

### Gate

```text
NO_PAGE_HORIZONTAL_OVERFLOW
SIDEBAR_STABLE
TOPBAR_STABLE
MAIN_CENTERED
NO_CLIPPING
BREAKPOINTS_PREDICTABLE
```

---

## FASE 3 — Shared Component Density

### Objetivo

Consolidar contratos compartilhados.

### Baseline inicial

```text
desktop = 36px
compact = 32px
touch/mobile = 44px
```

### Componentes

- button;
- input;
- native select;
- summary/multiselect;
- badges quando necessário.

### Problema conhecido

O summary personalizado renderiza aproximadamente 39 px enquanto controles equivalentes medem 36 px.

Isso deve ser corrigido no contrato correto, não com patch de alinhamento externo.

### Gate

```text
STANDARD_DESKTOP_CONTROLS_ALIGNED = YES
COMPACT_VARIANT_WORKS = YES
TOUCH_TARGETS_PRESERVED = YES
NO_TEXT_CLIPPING = YES
FOCUS_VISIBLE = YES
```

---

## FASE 4 — Inventory Responsive Repair

Esta é a fase crítica para os problemas atualmente visíveis.

### 4.1. Filtros

Corrigir:

- labels quebrados;
- alturas divergentes;
- grid baseado no viewport;
- alinhamento entre summaries, busca e botão;
- wrapping em 1400 px.

Não remover filtros.

### 4.2. Tabela

Corrigir estruturalmente:

- coluna Ações;
- nowrap;
- botão maior que a coluna;
- min-widths históricos;
- `nth-child` antigos;
- overflow horizontal;
- conteúdo multilinha;
- comportamento em 1366 px;
- conversão para cards em larguras menores.

### 4.3. Dados longos

A auditoria possuía somente uma câmera.

Portanto, testes futuros devem incluir dataset representativo com:

- nome longo;
- modelo longo;
- fabricante longo;
- localização longa;
- patrimônio longo;
- governança longa;
- status variados.

### Gate

```text
FILTERS_ALIGNED = YES
NO_UNINTENDED_LABEL_WRAP = YES
TABLE_ACTIONS_NOT_CLIPPED = YES
NO_HORIZONTAL_SCROLL_CAUSED_BY_ACTIONS = YES
LONG_CONTENT_VALIDATED = YES
MOBILE_CARD_MODE_VALIDATED = YES
```

---

## FASE 5 — Dashboard Refinement

### Objetivo

Ajustar densidade e composição após estabilização compartilhada.

### Analisar

- metric cards;
- `min-height`;
- `grid-template-rows`;
- section gaps;
- Monitoring layout;
- Qualidade cadastral;
- distribuição dos quatro cards.

### Gate

```text
NO_ACCIDENTAL_EMPTY_GRID_SPACE
CARD_HEIGHT_JUSTIFIED
NO_CLIPPING
RESPONSIVE_GRID_VALIDATED
VISUAL_HIERARCHY_PRESERVED
```

---

## FASE 6 — Quick Detail Reconstruction / Cleanup

Somente iniciar depois das fases anteriores.

### Objetivo

Simplificar o Quick Detail.

### Não adicionar outra camada de patch

Primeiro mapear:

```text
CURRENT_REQUIRED_RULES
CURRENT_COMPENSATORY_RULES
CURRENT_REDUNDANT_RULES
CURRENT_SHELL_COUPLING
```

### Investigar

- altura de preview;
- identidade;
- cards;
- footer;
- scroll;
- `max-height:800px`;
- `!important`;
- `:has()`;
- botão de navegação de 32 px;
- comportamento mobile;
- foco.

### Gate

```text
SCROLL_BEHAVIOR_PREDICTABLE = YES
FOOTER_VISIBLE_WHEN_EXPECTED = YES
NO_CONTENT_CLIPPING = YES
FOCUS_MANAGEMENT_PRESERVED = YES
ESC_RESTORE_FOCUS = YES
TOUCH_TARGETS_ACCEPTABLE = YES
LOCAL_RULES_SIMPLIFIED = YES
```

---

# 15. Regras de não-regressão

Toda fase deve preservar:

- Django SSR;
- comportamento funcional;
- rotas;
- APIs;
- modelos;
- contratos de backend;
- navegação por teclado;
- focus-visible;
- retorno de foco do `<dialog>`;
- Escape para fechar dialog;
- transformação de tabela para cards em mobile;
- alvo de toque apropriado;
- reduced motion existente;
- conteúdo integral.

Não remover informação para “fazer caber”.

Não mascarar layout com:

```text
overflow:hidden
clip
scale
zoom
font-size excessivamente pequeno
position:absolute compensatório
```

---

# 16. Política de validação

## 16.1. Browser zoom

Todos os gates principais:

```text
BROWSER_ZOOM = 100%
```

Zoom de 80% continua apenas como referência visual de densidade.

## 16.2. Viewport matrix mínima

Testar:

```text
2552×866
2048×altura real disponível
1920×1080
1366×768
900×768
390×844
```

## 16.3. Evidência

Para alterações visuais:

- screenshot antes;
- screenshot depois;
- computed styles relevantes;
- `scrollWidth/clientWidth` quando houver overflow;
- `scrollHeight/clientHeight` quando houver scroll vertical.

Não declarar PASS baseado apenas em valores teóricos.

## 16.4. Runtime

A validação deve ocorrer no mesmo checkout que contém o diff.

Não validar uma branch usando servidor de outro worktree.

Registrar quando aplicável:

```text
CANONICAL_WORKTREE
BRANCH
HEAD
DJANGO_BASE_DIR
RUNTIME_SOURCE
```

Se não for possível provar que o runtime serve a mesma cópia:

```text
RUNTIME_VALIDATION = BLOCKED
```

Não inventar PASS.

---

# 17. Política de Git durante a remediação

Por padrão, até validação do usuário:

```text
NO git add
NO git commit
NO git push
```

Cada fase deve apresentar:

```text
FILES_MODIFIED
GIT_DIFF_CHECK
GIT_STATUS
STAGING
```

Commits devem ser pequenos e semanticamente relacionados.

Não misturar:

```text
cleanup estrutural
+
mudança visual
+
mudança funcional
```

no mesmo commit.

---

# 18. Acessibilidade

A auditoria confirmou:

- skip link;
- labels;
- região da tabela focável;
- `:focus-visible`;
- `:focus-within`;
- foco transferido para o dialog;
- retorno de foco ao fechar;
- Escape funcional;
- alvos mobile geralmente 44 px.

Esses comportamentos são parte do contrato e devem ser preservados.

### Finding atual

Botões de navegação do Quick Detail permanecem com 32 px por override local.

Isso deve ser avaliado na fase do Quick Detail.

Não declarar conformidade WCAG completa sem auditoria específica de:

- contraste;
- leitor de tela;
- ampliação de texto;
- navegação completa por teclado.

---

# 19. Regras para o agente executor

Antes de implementar qualquer correção:

1. Identificar o owner da propriedade.
2. Identificar a regra vencedora.
3. Identificar regras vencidas.
4. Verificar especificidade.
5. Verificar ordem de carregamento.
6. Verificar media queries ativas.
7. Medir o valor computado.
8. Explicar por que a correção deve ser aplicada naquele arquivo.
9. Preferir remover/consolidar antes de adicionar.
10. Validar em mais de um viewport.

---

# 20. Formato mínimo de diagnóstico por finding

Para cada problema relevante, usar:

```text
FINDING_ID =

SYMPTOM =

ROOT_CAUSE =

EVIDENCE =

WINNING_RULE =

CONFLICTING_RULES =

OWNER_CURRENT =

OWNER_EXPECTED =

AFFECTED_COMPONENTS =

SEVERITY =
LOW | MEDIUM | HIGH

FIX_CLASS =
REMOVE | CONSOLIDATE | MOVE | REWRITE | TOKENIZE | RESPONSIVE_REPAIR

FILES_EXPECTED =

REGRESSION_RISK =
LOW | MEDIUM | HIGH

VALIDATION_GATE =
```

Isso deve substituir decisões do tipo:

> “vou reduzir mais 4 px porque parece grande.”

---

# 21. Critério para criação de novo token

Criar um token novo somente quando:

1. representar conceito semântico reutilizável;
2. possuir mais de um consumidor real ou previsível;
3. não duplicar token existente;
4. eliminar hardcodes/overrides;
5. ownership estiver claro.

Não transformar cada número em CSS variable.

---

# 22. Critério para breakpoint novo

Criar breakpoint novo somente se:

- existir mudança real de composição;
- o breakpoint atual não representar adequadamente o espaço útil;
- o componente possuir comportamento claramente diferente naquele intervalo.

Não criar breakpoints apenas para corrigir um único pixel de overflow.

---

# 23. Critério para container query

Container query pode ser considerada quando:

- o comportamento depende da largura real do componente;
- o viewport não representa adequadamente o espaço disponível;
- a solução reduz breakpoints globais;
- a compatibilidade do ambiente do ARGOS permitir.

Candidatos naturais:

- grid de filtros;
- eventualmente composição da tabela/ações.

Não migrar tudo para container queries sem necessidade.

---

# 24. O que NÃO fazer daqui para frente

Não continuar a sequência:

```text
problema visual
→ novo override
→ nova media query
→ novo !important
→ novo ajuste compensatório
```

Não usar:

- valores arbitrários sem medição;
- `!important` como primeira solução;
- alteração global para resolver problema local;
- alteração local para corrigir primitive global;
- viewport width quando o problema depende do container;
- scroll escondido para mascarar conteúdo maior;
- equalização artificial de alturas sem necessidade semântica.

---

# 25. Meta arquitetural final

Ao final da remediação, o comportamento desejado é:

### Exemplo 1 — Button

Alterar a altura padrão desktop deve exigir mudança em um único contrato compartilhado.

### Exemplo 2 — Sidebar

Alterar largura deve afetar apenas shell, sem exigir correção em Inventário.

### Exemplo 3 — Inventário

Alterar largura de coluna não deve modificar botão global.

### Exemplo 4 — Quick Detail

Alterar padding de card não deve modificar card do Dashboard.

### Exemplo 5 — Responsividade

A mudança de composição deve ocorrer por necessidade real do componente, não por acumulação histórica de breakpoints.

---

# 26. Sequência canônica recomendada

```text
UI-AUD-01
AUDITORIA
PASS
        ↓
PHASE 0
DEAD CSS / DEFEATED RULES CLEANUP
        ↓
PHASE 1
CSS OWNERSHIP CONSOLIDATION
        ↓
PHASE 2
SHELL STABILIZATION
        ↓
PHASE 3
SHARED COMPONENT DENSITY
        ↓
PHASE 4
INVENTORY RESPONSIVE REPAIR
        ↓
PHASE 5
DASHBOARD REFINEMENT
        ↓
PHASE 6
QUICK DETAIL CLEANUP
        ↓
FINAL CROSS-VIEWPORT REGRESSION
        ↓
DESIGN SYSTEM BASELINE CANONICALIZATION
```

---

# 27. Recomendação sobre modelo/esforço

Para atividades estruturais de:

- ownership;
- cascata;
- responsividade;
- consolidação;
- decisões de arquitetura CSS;

usar agente com capacidade de raciocínio alta.

Para implementação mecânica já especificada e de baixo risco, pode-se utilizar executor mais econômico.

Escalar novamente quando houver:

- conflito entre regras;
- regressão cross-page;
- decisão arquitetural;
- breakpoint ambíguo;
- necessidade de adjudicação entre Design System e page-specific CSS.

---

# 28. Próxima atividade autorizável

A próxima frente recomendada é:

```text
ARGOS UI REMEDIATION — PHASE 0
DEAD CSS / DEFEATED RULES CLEANUP
```

### Objetivo

Remover ou consolidar exclusivamente regras comprovadamente vencidas, sem alterar resultado visual ou funcional.

### Gate principal

```text
COMPUTED_STYLE_DELTA = NONE
VISUAL_DELTA = NONE
FUNCTIONAL_DELTA = NONE
CSS_COMPLEXITY_REDUCED = YES
```

Essa fase deve produzir uma base menor e mais previsível antes de qualquer nova alteração visual.

---

# 29. Estado das principais decisões

```text
STACK_MIGRATION = REJECTED / NOT_NEEDED

DJANGO_SSR = PRESERVE
VANILLA_JS = PRESERVE
CUSTOM_CSS = PRESERVE
DESIGN_SYSTEM = PRESERVE_AND_CONSOLIDATE

MAIN_CONTENT_1400 = PROVISIONAL_KEEP

SIDEBAR_192 = RECOMMENDED_KEEP

TOPBAR_40 = PROVISIONAL_KEEP

STANDARD_CONTROL_36 = PROVISIONAL_KEEP

COMPACT_CONTROL_32 = PROVISIONAL_KEEP

TOUCH_CONTROL_44 = KEEP

INVENTORY_TABLE_OVERFLOW = CONFIRMED_STRUCTURAL_FINDING

FILTER_ALIGNMENT = CONFIRMED_STRUCTURAL_FINDING

QUICK_DETAIL_SCROLL = CONFIRMED_LOCAL_PREDOMINANT_FINDING

DASHBOARD_CARD_DENSITY = CONFIRMED_REVIEW_ITEM

NEW_VISUAL_PATCHES = FROZEN UNTIL REMEDIATION PHASES
```

---

# 30. Diretriz final ao agente principal

O agente principal deve conduzir a remediação como trabalho arquitetural de front-end, e não como sequência de ajustes cosméticos.

A prioridade deve ser:

```text
ENTENDER
→ CONSOLIDAR
→ SIMPLIFICAR
→ ESTABILIZAR
→ SÓ ENTÃO REFINAR
```

A meta não é apenas deixar a tela atual bonita.

A meta é garantir que, depois desta remediação, o próximo ajuste visual simples realmente seja simples.
