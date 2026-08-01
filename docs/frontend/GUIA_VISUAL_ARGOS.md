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
