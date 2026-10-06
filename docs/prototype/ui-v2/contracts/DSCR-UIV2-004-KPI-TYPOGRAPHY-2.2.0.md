# DSCR-UIV2-004 — Capability tipográfica KPI para 2.2.0

```text
ID = DSCR-UIV2-004-KPI-TYPOGRAPHY-2.2.0
ACTIVITY = P5-VR-DSG-01 — KPI Typography Capability
STATUS = APPROVED / IMPLEMENTED / PUBLISHED
CURRENT_VERSION = 2.1.0
TARGET_VERSION = 2.2.0
VERSION_IMPACT = MINOR
COMPATIBILITY = BACKWARD_COMPATIBLE / ADDITIVE
BACKWARD_COMPATIBILITY = PRESERVED
PUBLISHED = YES / commit b9cdc00dbc35915deb922c1a0596574a2b9a12bc
PUBLISHED_BRANCH = codex/ui-v2-p5-production
```

## Change request

```text
CHANGE = shared KPI typography capability
REASON = Camera Detail canonical contract requires a reusable KPI typography style and local typography declaration is prohibited.
AFFECTED_COMPONENTS = Typography / utility capability
AFFECTED_SCREENS = Camera Detail initially; other consumers may reuse capability later.
VERSION_IMPACT = MINOR / 2.1.0 -> 2.2.0
BACKWARD_COMPATIBILITY = PRESERVED
COMPATIBILITY = BACKWARD_COMPATIBLE / ADDITIVE
USER_REAPPROVAL_REQUIRED = NO / exact closed contract
```

## Capability contract

The public `.argos-text-kpi` utility sets only `font-size` from the existing
`--argos-text-kpi` token. The token remains 24px. It adds no page-specific
value, weight, line-height, component, or behavior. Semantic H1–H3 styles
continue to provide the existing semibold weight and tight line-height through
their existing tokens; consumers can compose the capability with those
semantic heading styles.

No standalone public `weight-semibold` or `line-tight` utility selector existed
in 2.1.0. This change does not add such utilities: the Camera Detail contract
uses an H2, for which both properties are already provided by the base layer.
The new selector follows the existing `argos-*` namespace and typography token
naming, in the shared `patterns` layer. It does not replace or alter KPI Card.

```text
EXISTING_KPI_TOKEN = --argos-text-kpi: 24px
PUBLIC_CAPABILITY_ADDED = .argos-text-kpi
CAPABILITY_SEMANTICS = font-size only
TOKEN_CHANGES = NONE
CONSUMER_MIGRATION = NONE
CAMERA_DETAIL_SOURCE_CHANGED = NO
BACKEND_CHANGED = NO
JS_CHANGED = NO
```

The capability is additive and preserves 2.1.0 consumers. It was published in
commit `b9cdc00dbc35915deb922c1a0596574a2b9a12bc` on
`codex/ui-v2-p5-production`. Camera Detail implementation remains a separate
activity with its own authorization and visual acceptance gates; this DSCR does
not change or implement that screen.
