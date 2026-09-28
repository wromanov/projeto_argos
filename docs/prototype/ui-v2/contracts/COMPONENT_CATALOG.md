# ARGOS UI V2 — Component Catalog

Versão aprovada: 2.0.0. O catálogo registra ownership para conter variantes oportunistas em P3.

| COMPONENT | TYPE | OWNER | CASCADE_LAYER | VARIANTS | STATES | RESPONSIVE | KNOWN_CONSUMERS | STATUS |
|---|---|---|---|---|---|---|---|---|
| Button | COMPONENT | component | components | primary, secondary, compact | default, hover, active, focus-visible, disabled | alvo 44px em mobile | forms, actions, toolbar | foundation specimen |
| Icon Button | COMPONENT | component | components | square | default, hover, active, focus-visible, disabled | alvo 44px em mobile | shell, actions com ícone local aprovado | foundation specimen |
| Input / Search | COMPONENT | component | components | text, search | default, focus-visible, disabled, placeholder | width fluida; alvo >=44px em mobile/touch | forms, filters | foundation specimen |
| Select | COMPONENT | component | components | default | default, focus-visible, disabled | width fluida; alvo >=44px em mobile/touch | forms, filters | foundation specimen |
| Checkbox | COMPONENT | component | components | default | checked, unchecked, focus-visible, disabled | alvo visual 18px; label clicável com área >=44px em mobile/touch | forms, multi-select | foundation specimen |
| Badge | COMPONENT | component | components | neutral, success, warning, danger, info | static | quebra rótulo extenso | metadata, completeness, event categories | foundation specimen |
| Status Badge | COMPONENT | component | components | neutral, success, warning, danger | static | quebra rótulo extenso | monitoring, operation projections | foundation specimen |
| Card | COMPONENT | component | components | header, body, footer | default | min-width zero | portal, dashboard, detail groups | foundation specimen |
| Alert | COMPONENT | component | components | info, warning, danger | informational | text wraps | freshness, form and request feedback | foundation specimen |
| Spinner | COMPONENT | component | components | inline | loading; reduced motion | fixed visual size | async image / quick detail conventions | foundation specimen |
| Page Header | PATTERN | pattern | patterns | title, description, actions | default | actions wrap; stacks on mobile | all screen families | foundation specimen |
| Section Header | PATTERN | pattern | patterns | title, metadata | default | wraps | detail and grouped pages | CSS available |
| KPI Card / Grid | PATTERN | pattern | patterns | 1–3 columns | default | two columns tablet, one on mobile | dashboard, portal | foundation specimen |
| Toolbar / Filter Bar | PATTERN | pattern | patterns | filters and actions | default, focus, selected filter state | wraps at narrow widths | inventory, events, substitutions | foundation specimen |
| Data Table | PATTERN | pattern | patterns | default, compact via argos-table--compact | hover, selected | contained horizontal scroll | inventory, events, history | foundation specimen |
| Pagination | PATTERN | pattern | patterns | current, previous, next | current, disabled | 44px targets | paginated lists | foundation specimen |
| Empty State | PATTERN | pattern | patterns | optional action | empty | text wraps | lists and search results | foundation specimen |
| Loading State | PATTERN | pattern | patterns | inline / area | loading, reduced motion | text wraps | async surfaces where present | foundation specimen |
| Error State | PATTERN | pattern | patterns | inline / area, optional retry | error | text wraps | request and validation feedback | foundation specimen |
| Documentation Shell | PATTERN | pattern | patterns | sidebar / horizontal mobile navigation | current page | sidebar collapses to scrollable nav | P2 executable foundation | foundation pages |

A page may not redefine a shared component without an explicit variant contract. A screen-specific layout stays page-owned until a second real consumer demonstrates reuse. Quick Detail stays protected.