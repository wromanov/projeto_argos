# ARGOS UI V2 — Component Catalog

Baseline da foundation aprovada: 2.0.0. Design System implementado corrente:
2.4.0 local na branch `codex/ui-v2-p5-production`, aguardando revisão e publicação. O catálogo registra ownership para
conter variantes oportunistas em P3.

| COMPONENT | TYPE | OWNER | CASCADE_LAYER | VARIANTS | STATES | RESPONSIVE | KNOWN_CONSUMERS | STATUS |
|---|---|---|---|---|---|---|---|---|
| Button | COMPONENT | component | components | primary, secondary, compact, danger | default, hover, active, focus-visible, disabled | alvo 44px em mobile | forms, actions, toolbar, destructive actions | 2.1.0 published |
| Icon Button | COMPONENT | component | components | square | default, hover, active, focus-visible, disabled | alvo 44px em mobile | shell, actions com ícone local aprovado | foundation specimen |
| Input / Search | COMPONENT | component | components | text, search | default, focus-visible, disabled, placeholder | width fluida; alvo >=44px em mobile/touch | forms, filters | foundation specimen |
| Select | COMPONENT | component | components | default | default, focus-visible, disabled | width fluida; alvo >=44px em mobile/touch | forms, filters | foundation specimen |
| Checkbox | COMPONENT | component | components | default | checked, unchecked, focus-visible, disabled | alvo visual 18px; label clicável com área >=44px em mobile/touch | forms, multi-select | foundation specimen |
| Badge | COMPONENT | component | components | neutral, success, warning, danger, info | static | quebra rótulo extenso | metadata, completeness, event categories | foundation specimen |
| Status Badge | COMPONENT | component | components | neutral, success, warning, danger | static | quebra rótulo extenso | monitoring, operation projections | foundation specimen |
| Card | COMPONENT | component | components | header, body, footer | default | min-width zero | portal, dashboard, detail groups | foundation specimen |
| Alert | COMPONENT | component | components | info, warning, danger | informational | text wraps | freshness, form and request feedback | foundation specimen |
| Spinner | COMPONENT | component | components | inline | loading; reduced motion | fixed visual size | async image / quick detail conventions | foundation specimen |
| Data Pair | COMPONENT | component | components | label/value; mono value via `code` | default | text wraps; `min-width: 0` | future detail groups; Quick Detail remains protected | 2.1.0 published |
| Page Header | PATTERN | pattern | patterns | title, description, actions | default | actions wrap; stacks on mobile | all screen families | foundation specimen / unchanged |
| KPI Typography | UTILITY | pattern | patterns | `argos-text-kpi` | inherits weight and line-height from semantic heading styles | text wraps per consumer | Camera Detail; reusable typography consumers | 2.2.0 published |
| Back Navigation Link | UTILITY | pattern | patterns | `argos-back-link` | inherits shared link hover and focus-visible behavior | text wraps per consumer | Camera Detail initially | 2.3.0 published |
| Section Surface | PATTERN | pattern | patterns | `argos-section-surface`; neutral macro grouping | static; no shadow | padding base constante; layout pertence ao consumidor | Camera Detail: Dados principais, Operação, Governança, Histórico | 2.4.0 local / human visual review pending |
| Section Header | PATTERN | pattern | patterns | title, metadata | default | wraps | detail and grouped pages | CSS available |
| Data Group | PATTERN | pattern | patterns | optional heading; composes `argos-two-column` when columns are useful | default | existing two-column pattern collapses on mobile | future detail groups | 2.1.0 published |
| KPI Card / Grid | PATTERN | pattern | patterns | 1–3 columns | default | two columns tablet, one on mobile | dashboard, portal | foundation specimen |
| Toolbar / Filter Bar | PATTERN | pattern | patterns | filters and actions | default, focus, selected filter state | wraps at narrow widths | inventory, events, substitutions | foundation specimen |
| Data Table | PATTERN | pattern | patterns | default, compact via argos-table--compact | hover, selected | contained horizontal scroll | inventory, events, history | foundation specimen |
| Pagination | PATTERN | pattern | patterns | current, previous, next | current, disabled | 44px targets | paginated lists | foundation specimen |
| Empty State | PATTERN | pattern | patterns | compact, optional action | empty | text wraps | lists, search results, section interiors | 2.1.0 published |
| Loading State | PATTERN | pattern | patterns | inline / area | loading, reduced motion | text wraps | async surfaces where present | foundation specimen |
| Error State | PATTERN | pattern | patterns | inline / area, optional retry | error | text wraps | request and validation feedback | foundation specimen |
| Documentation Shell | PATTERN | pattern | patterns | sidebar / horizontal mobile navigation | current page | sidebar collapses to scrollable nav | P2 executable foundation | foundation pages |

A page may not redefine a shared component without an explicit variant contract. A screen-specific layout stays page-owned until a second real consumer demonstrates reuse. Quick Detail stays protected.

P5-VR-CAMERA-DETAIL-REMEDIATION-01: Camera Detail reutiliza Section Header em
todas as macro headings/Upload e Data Group em Situação/completude. Nome H2
consome `argos-page-title`; empty values consomem `argos-state__copy` em span.
Nenhuma capability pública é criada ou alterada. Section Surface 2.4.0
permanece inalterada/local/não publicada, com aprovação humana pendente.
