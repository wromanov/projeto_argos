# DSCR-UIV2-002 — Legibilidade móvel da tabela de inventário

ID = DSCR-UIV2-002-MOBILE-TABLE-READABILITY
STATUS = ADJUDICATED / SHARED_DESIGN_SYSTEM_DEFECT / IMPLEMENTATION_AUTHORIZED_FOR_SEPARATE_ROOT_ACTIVITY
OUTCOME = SHARED_DESIGN_SYSTEM_DEFECT
P3_A_REMOTE_HEAD = 1f833aed523420db47ba06faa5d5cf5cc114de0b
REPRODUCTION = PASS / temporary detached worktree at the exact remote HEAD
TABLE_PATTERN_OWNER = ROOT / static/css/ui-v2/patterns.css / .argos-table
RESPONSIVE_TABLE_CONTRACT = Data Table pattern uses contained horizontal scrolling; compact variant is .argos-table--compact; no mobile column reduction is defined
MOBILE_OVERFLOW_POLICY = local horizontal scrolling is intentional; global page overflow is not
APPROVED_MOBILE_DATA_TABLE_POLICY = preserve all factual fields; preserve local horizontal scrolling; prevent destructive word fragmentation; establish readable minimum column/cell behavior; preserve action accessibility; do not hide columns arbitrarily; do not convert shared tables to cards in this patch
CROSS_FAMILY_REGRESSION_REQUIRED = YES

## Reprodução factual

```text
SCREEN_ID = SCR-INV-001
STATE = default
FIXTURE = default / five records paginated; three visible table rows
VIEWPORT = 390x844 CSS pixels
BROWSER = installed Chrome through the bundled Playwright runtime
ZOOM = 100% default browser scale
DEVICE_SCALE_FACTOR = 1
PAGE_WIDTH = 390px
INVENTORY_CONTAINER_OUTER_WIDTH = 390px
AVAILABLE_CONTENT_WIDTH = 362px
TABLE_SCROLLPORT = 362px outer / 360px client width
TABLE_SCROLL_WIDTH = 859px
TABLE_RENDERED_WIDTH = 858.78px
ACTION_COLUMN_WIDTH = 61.08px
ROW_HEIGHTS = 283px / 283px / 283px
TABLE_FONT_SIZE = 12px
GLOBAL_HORIZONTAL_OVERFLOW = NO
LOCAL_TABLE_OVERFLOW = YES / 859px scroll width inside 360px client width
ACTIONS_ACCESSIBLE = YES / Tab reached the first named action; the table scroller moved 499px and the action became fully visible
TEXT_READABLE = NO / labels and status text break into narrow fragments
ROW_HEIGHT_PATHOLOGICAL = YES / 283px rows versus the 56px compact row-height token
```

The result reproduces on the ordinary `default` fixture; the long fixture is not required to trigger it. The image and status badges, camera identity, model/location and two action links remain present. The first viewport makes the table’s local scroll instruction visible; the page itself stays within 390px.

Two fresh table-position captures were produced at 390x844, device scale 1, with the same deterministic filename in separate temporary directories. Both PNGs were 390x844 and had SHA-256 `269cc93795c97c71ec0c707303ef5a7d8fd2e074fe60e059db21de41d66d7c3e`. The saved image was inspected. These proof files were deleted after review and are not P3-A family evidence.

## Root-cause decomposition

### Shared table pattern

The common rules in `patterns.css` set `.argos-table-region` to `overflow-x: auto`, `.argos-table` to `width: 100%` and `min-width: 760px`, and all table cells to `overflow-wrap: anywhere`. Headers stay `white-space: nowrap`. The compact row-height token is 56px, but it does not cap a row when its contents wrap. Shared badges in `components.css` also use `overflow-wrap: anywhere`. Together with automatic table layout, those rules permit words and action labels to split into narrow fragments instead of using the intentional horizontal scroll area for their natural width.

The P3-A table uses the shared pattern correctly and has no local table CSS. The 8-column inventory (including two links in its action cell) amplifies the shared behavior; it does not explain the arbitrary mid-word breaks by itself. The default fixture reproduces the finding, so fixture-only content is ruled out.

```text
ROOT_CAUSE = shared cell and badge wrapping / intrinsic sizing does not preserve readable table content under the documented local-scroll policy
OWNER = ROOT / UI-V2 Design System
AFFECTED_FILES = static/css/ui-v2/patterns.css; static/css/ui-v2/components.css (candidate repair surfaces; unchanged in this activity)
FIXTURE_CONTENT_DEFECT = NO
P3_A_MARKUP_MISUSE = NO
```

### Product Design review

1. **Scanability at 390px:** No. Cells split names and badge text into fragments; 283px rows make side-by-side camera comparison slow.
2. **Primary actions:** Yes, reachable. The action column is initially outside the visible part of the local scroller; keyboard focus moves the scroller to the named action. Touch users have the explicit horizontal-scroll instruction.
3. **Overflow clarity:** Yes. The hint explains horizontal movement and the measured overflow stays inside the table region. It is not global page overflow.
4. **283px rows:** Not acceptable for this compact data table; it is content expansion, not a defined mobile adaptation.
5. **Information hierarchy:** Degraded on mobile by the vertical height and fragmented cell text.
6. **ARGOS HYBRID coherence:** The shared shell, palette and components remain visually coherent; mobile data density does not meet the intended compact table behavior.
7. **Owner:** The shared Data Table cell/badge sizing rules. Inventory composition is a stress case, not an independently proven page defect; no columns should be hidden by assumption.

## Cross-screen impact

The same table selectors are used by these real screen consumers:

```text
P3-A = SCR-INV-001
P3-B = SCR-MON-HISTORY-001; SCR-SUB-LIST-001; SCR-SUB-CAMERA-001
P3-C = SCR-ACT-LIST-001; SCR-EVENT-LIST-001; SCR-EVENT-CAMERA-001
P3-D = no real .argos-table consumers found
```

P3-B and P3-C use the same table declarations (P3-B's Design System header remains 2.0.0; the table rules match 2.0.1). Their handoffs describe contained local scrolling and do not report the same 283px issue. Current P3-C revalidation at `c26840e8c9c21b9105b7c3bb42c96bc5186c9227` records 75 measurements, 20 post-2.0.1 captures and zero failures; its three table screens had no global horizontal overflow at 390x844. That is evidence about overflow and capture, not proof that every table is readable. A shared patch would require targeted regressions across P3-A and representative P3-B/P3-C consumers.

```text
SHARED_PATTERN_IMPACT = BROAD
CROSS_FAMILY_IMPACT = P3-B and P3-C share the pattern; no defect is claimed there without a targeted readability check
AFFECTED_SCREEN_IDS = SCR-INV-001; SCR-MON-HISTORY-001; SCR-SUB-LIST-001; SCR-SUB-CAMERA-001; SCR-ACT-LIST-001; SCR-EVENT-LIST-001; SCR-EVENT-CAMERA-001
```

## Adjudication and version policy

```text
VERSION_BEFORE = 2.0.1
DESIGN_SYSTEM_VERSION_IMPACT = PATCH / if canonical shared table rules change
DESIGN_SYSTEM_TARGET_VERSION = 2.0.2 / approved target for the separate ROOT implementation activity
VERSION_PROMOTED = NO
USER_REAPPROVAL_REQUIRED = NO / the user approved the mobile table policy in the final adjudication checkpoint
IMPLEMENTATION_AUTHORIZED = YES / separate follow-up ROOT activity only
IMPLEMENTATION_PERFORMED = NO
ROOT_FIX_COMMIT = NONE
P3_A_FIX_AUTHORIZED = NO / no separate page-level fix was established
P3_A_CHANGED = NO
PRODUCTION_CHANGED = NO
```

Approved policy for the separate ROOT patch: preserve every factual field and the contained horizontal scroller; prevent destructive word fragmentation; establish readable minimum column/cell behavior; preserve keyboard and touch access to actions; do not hide columns arbitrarily or convert shared tables to cards. Run cross-family regression on P3-A and representative P3-B/P3-C consumers. If canonical shared CSS changes, promote 2.0.1 to 2.0.2. Keep this adjudication checkpoint documentary only.

NEXT_GATE = new ROOT activity to implement the approved DS 2.0.2 mobile data table policy; return its commit SHA for human adjudication before integration or propagation
