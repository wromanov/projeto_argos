# Guia visual do ARGOS

## Objetivo

O design system em `static/css/design-system.css` fornece tokens e componentes compartilhados sem dependências externas. Ele não é carregado globalmente nesta etapa.

## Tokens e semântica

As variáveis `--color-*` definem marca, superfícies, texto, bordas, foco e estados. Produção, Online e cadastro completo usam verde; Estoque usa azul; Desativada e Não verificada usam cinza; Offline e erro usam vermelho; cadastro incompleto usa âmbar.

A escala de espaçamento vai de `--space-1` a `--space-12`. A tipografia usa apenas fontes do sistema e inclui família monoespaçada para `.technical-value`. Bordas, raios e sombras usam tokens próprios.

## Componentes

- Botões: `.button`, variantes semânticas, `.button--small` e `.button-group`.
- Cards: `.card`, `.metric-card`, `.module-card` para link explícito e `.info-card` informativo.
- Badges: `.badge` e variantes operacionais, técnicas, de completude e `.badge--sistema`.
- Mensagens: `.messages` e `.message--success|info|warning|error`.
- Formulários: `.form-container`, `.form-section`, `.form-grid`, `.form-field`, `.form-errors-summary` e `.form-actions`.
- Tabelas: `.table-region`, `.data-table`, `.table-actions`, `.table-empty` e `.numeric-column`.
- Paginação, estado vazio e breadcrumbs possuem classes próprias com semântica acessível.

## Acessibilidade e responsividade

O foco visível é global por `:focus-visible`; `.skip-link` e `.visually-hidden` estão disponíveis. Em movimento reduzido, transições e animações não essenciais são reduzidas. Formulários e paginação se reorganizam em telas estreitas; tabelas usam região horizontal, nunca o `body`.

## Regras de uso

Não usar CSS inline, CDN, fontes externas, `@import` ou dependência externa sem aprovação. Aplicar classes explicitamente; não transformar links globais em botões. Manter valores de IP, MAC, VLAN e dados similares em `.technical-value`.

As folhas existentes permanecem responsáveis pelas telas atuais; a adoção gradual do design system ocorrerá nas próximas etapas.

## Base, navegação, login e portal

A ordem do base autenticado é `design-system.css`, `argos.css`, `portal.css` e CSS específico do template. Use o skip link para `#conteudo-principal`, `aria-current="page"` em apenas um item da navegação e `<nav aria-label="Navegação principal">`.

A navegação usa uma lista única e, em telas menores, quebra de linha com rolagem interna quando necessária; ela não pode ser ocultada. O menu do usuário mantém `<details>` e `<summary>`, preservando logout via formulário POST com CSRF.

Mensagens usam `.messages`, `aria-live="polite"` e classes semânticas. O login independente carrega design system e CSS de autenticação, mantém autocomplete de usuário e senha e usa erro genérico. Cartões de módulos devem ser um único link `.module-card` com SVG decorativo.

## Dashboard e inventário

O dashboard é dividido nas seções Inventário, Monitoramento técnico, Qualidade cadastral e Atividade. Use `.metric-card--link` somente em links integrais com destino existente; cartões informativos usam `article.metric-card` sem `href`, cursor ou indicação de navegação.

A lista de câmeras usa breadcrumb estrutural, `.form-container` com filtros GET, `.form-grid`, `.form-field`, `.form-label` e `.form-actions`. A tabela deve permanecer dentro de `.table-region` com `role="region"`, rótulo e foco; use `.data-table`, caption e `scope="col"`. Dados de IP, patrimônio, VLAN e valores equivalentes usam `.technical-value`.

Badges preservam texto completo: `.badge--producao`, `.badge--estoque`, `.badge--desativada`, `.badge--online`, `.badge--offline`, `.badge--nao-verificada`, `.badge--completo` e `.badge--incompleto`. Não comunicar estados apenas pela cor.

Use os partials compartilhados `components/paginacao.html` e `components/estado_vazio.html`. A paginação preserva todos os filtros GET por meio da template tag `querystring`; não duplicar sua implementação em telas individuais.