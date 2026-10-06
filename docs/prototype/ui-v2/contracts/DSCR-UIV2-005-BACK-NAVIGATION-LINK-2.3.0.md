# DSCR-UIV2-005 — Capability compartilhada de link de retorno 2.3.0

```text
ID = DSCR-UIV2-005-BACK-NAVIGATION-LINK-2.3.0
ACTIVITY = P5-VR-DSG-02 — Back Navigation Link Capability
STATUS = IMPLEMENTED / TECHNICALLY VALIDATED LOCALLY / NOT PUBLISHED
CURRENT_VERSION = 2.2.0
TARGET_VERSION = 2.3.0
VERSION_IMPACT = MINOR
COMPATIBILITY = BACKWARD_COMPATIBLE / ADDITIVE
BACKWARD_COMPATIBILITY = PRESERVED
```

## Change request

```text
CHANGE = public Back Navigation Link capability
PUBLIC_CLASS = .argos-back-link
REASON = Camera Detail canonical contract requires a reusable back-navigation visual style and page-local typography is prohibited.
VERSION = 2.2.0 -> 2.3.0
VERSION_IMPACT = MINOR
COMPATIBILITY = ADDITIVE / BACKWARD_COMPATIBLE
INITIAL_CONSUMER = Camera Detail
OTHER_CONSUMERS = NONE migrated in this activity
```

## Capability contract

The public `.argos-back-link` utility sets only `font-size`, `font-weight`, and
`color`, using the existing `--argos-text-secondary`,
`--argos-weight-medium`, and `--argos-color-action` tokens. Link hover remains
owned by the shared base rule, and visible keyboard focus remains owned by the
global `:focus-visible` rule. The capability adds no spacing, positioning,
layout, surface, or container behavior and does not create a parallel focus
mechanism.

```text
TEXT_SECONDARY_SOURCE = --argos-text-secondary: 12px
WEIGHT_MEDIUM_SOURCE = --argos-weight-medium: 500
COLOR_ACTION_SOURCE = --argos-color-action: #2563a6
FOCUS_SOURCE = base.css global :focus-visible rule using --argos-focus-width, --argos-color-action, and --argos-focus-offset
TOKEN_CHANGES = NONE
PAGE_SPECIFIC_SELECTOR = NONE
LEGACY_DETAIL_BACK_LINK_CHANGED = NO
CONSUMER_MIGRATION = Camera Detail only, by separate S2B activity
```

The selector follows the public `argos-*` namespace and is defined once in the
shared `patterns` layer. It preserves existing 2.2.0 consumers. The legacy
`.detail-back-link` remains untouched; other screens are not migrated here.

```text
BACKEND_CHANGED = NO
JS_CHANGED = NO
CAMERA_DETAIL_IMPLEMENTATION_CHANGED_BY_THIS_ACTIVITY = NO
```
