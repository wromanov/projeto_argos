# ARGOS UI V2 · Visual Style Lab

Abra `index.html` no navegador. O seletor superior alterna A, B e C sem trocar HTML, dados ou composição. `?direction=a`, `?direction=b` e `?direction=c` permitem abrir cada direção diretamente.

Capturas da mesma tela em 1440 × 900: [A](screenshots/argos-style-a.png) · [B](screenshots/argos-style-b.png) · [C](screenshots/argos-style-c.png).

Tela de referência: **SCR-INV-001 — Inventário de câmeras**, conforme `ARGOS_UI_V2_SCREEN_CENSUS.md`. O protótipo replica os componentes conceituais da página e usa dados fictícios. A ação de filtrar e os controles de paginação são demonstrativos; não fazem consultas ao backend. O Quick Detail protegido e o Django Admin ficam fora deste Style Lab.

## Contrato de comparação

| Item | A · Shadcn Corporate | B · PatternFly Enterprise | C · ARGOS Hybrid |
|---|---|---|---|
| Estrutura, textos e dados | Idênticos | Idênticos | Idênticos |
| Superfícies | Branco e cinza neutro | Camadas azuladas sóbrias | Grafite e azul ARGOS |
| Controles | Bordas finas, cantos suaves | Bordas nítidas, maior densidade | Contornos e acentos operacionais |
| Ênfase | Legibilidade calma | Varredura rápida de dados | Identidade técnica do produto |

As três direções são interpretações originais, inspiradas por conceitos dos sistemas pesquisados. Nenhuma API, biblioteca, runtime, stylesheet ou asset remoto desses sistemas é carregado.

## Decisão de seleção visual — UI-V2-P1

```text
USER_SELECTION = C — ARGOS HYBRID
USER_VISUAL_SELECTION_GATE = PASS
DIRECTION_A_STATUS = HISTORICAL_ALTERNATIVE / NOT_SELECTED
DIRECTION_B_STATUS = HISTORICAL_ALTERNATIVE / NOT_SELECTED
DIRECTION_C_STATUS = SELECTED / VISUAL_DIRECTION_AUTHORITY
UI-V2-P1 = CLOSED / PASS
P2_STARTED = NO
NEXT_ACTIVITY = UI-V2-P2 — VISUAL FOUNDATION
```

A decisão humana seleciona C como direção visual do ARGOS UI V2. A e B permanecem documentadas e versionadas como alternativas históricas, sem serem tratadas como inválidas ou erradas. Esta seleção encerra P1 e não inicia P2.

Baselines e escopo preservados:

```text
QUICK_DETAIL = APPROVED / PROTECTED
ADMIN_UI_V2_SCOPE = TRACKED_AS_INHERITED / NO_CUSTOM_REDESIGN_BY_DEFAULT
PROTOTYPE_STACK_COMPATIBILITY = REQUIRED_GATE
PRODUCTION_FILES_CHANGED = NO
```

## Fontes oficiais pesquisadas

- [shadcn/ui · Theming](https://ui.shadcn.com/docs/theming): pares semânticos de fundo/texto, borda, foco, raio.
- [PatternFly · About tokens](https://www.patternfly.org/tokens/about-tokens/) e [Table](https://www.patternfly.org/components/table/): tokens e tratamento de tabelas empresariais.
- [IBM Carbon · Color](https://preview.carbondesignsystem.com/building-blocks/foundations/color/overview): alternância de camadas e hierarquia de superfície.
- [Ant Design · Colors](https://ant.design/docs/spec/colors/): cor funcional e neutros em ferramentas corporativas.
- [Fluent 2 · Design tokens](https://fluent2.microsoft.design/design-tokens) e [Color](https://fluent2.microsoft.design/color): aliases semânticos, estados e contraste.
- [MUI · Theming](https://mui.com/material-ui/customization/theming/) e [MUI X · Accessibility](https://mui.com/x/react-data-grid/accessibility/): hierarquia de temas, densidade e navegação de dados.

## Compatibilidade e limites

`PROTOTYPE_STACK_COMPATIBILITY_A/B/C = PASS`: HTML semântico, CSS local, JavaScript nativo pequeno e ícone de marca copiado dos assets locais do ARGOS. A troca de direção é exclusiva do laboratório; a apresentação selecionada poderia ser transferida para Django Templates + CSS customizado sem framework. Não é implementação de produção nem decisão visual final.

Estados expostos no mesmo documento: badges de monitoramento e governança, alerta de dados defasados, foco/hover/selected/disabled, mensagem de vazio e mensagem de erro. O foco é visível, há skip link e a tabela pode rolar horizontalmente em largura reduzida sem cortar células.

Validação no Chrome: A, B e C renderizadas com o mesmo viewport de 1440 × 900; cinco linhas idênticas; nenhuma com overflow horizontal da página. Em 390 × 844, a página não transbordou e a rolagem ficou confinada à região da tabela (largura interna 1040 px, janela da tabela 345 px). Contraste básico medido no navegador para texto geral, sidebar, botão principal e badges Online/Offline/Defasado: menor razão observada 6,09:1. Isso não substitui auditoria WCAG completa nem validação de todos os estados com tecnologia assistiva.

`USER_VISUAL_SELECTION_GATE = PASS` · `UI-V2-P1 = CLOSED / PASS` · `P2_STARTED = NO`.
