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

## Implementação ROOT — Design System 2.0.2

```text
IMPLEMENTATION_STATUS = PASS / ROOT PATCH COMPLETE
ROOT_CAUSE = .argos-table th/td and nested badges used overflow-wrap:anywhere, allowing min-content sizing to compress table columns and split ordinary words; P3-A's 8-column table amplified this shared behavior
PATCH_RULES = remove anywhere from shared table cells; use overflow-wrap:break-word on table data cells and badges/status badges inside those cells; retain automatic table layout, 760px table minimum, local overflow-x:auto, and all columns/actions
CURRENT_SELECTORS = .argos-table th, .argos-table td; .argos-table td; .argos-table td .argos-badge; .argos-table td .argos-status-badge
CURRENT_PROPERTIES = overflow-wrap:anywhere → removed; overflow-wrap:break-word on table data cells and their badges
CURRENT_OWNER_FILE = static/css/ui-v2/patterns.css / ROOT
FILES_CHANGED = static/css/ui-v2/{tokens,base,components,patterns}.css; docs/prototype/ui-v2/screens/{index.html,harness.js}; this DSCR
AFFECTED_CONSUMERS = 7 / SCR-INV-001; SCR-MON-HISTORY-001; SCR-SUB-LIST-001; SCR-SUB-CAMERA-001; SCR-ACT-LIST-001; SCR-EVENT-LIST-001; SCR-EVENT-CAMERA-001
REPRODUCED_CONSUMERS = SCR-INV-001; SCR-SUB-LIST-001; SCR-SUB-CAMERA-001; SCR-ACT-LIST-001; SCR-EVENT-LIST-001
NON_REPRODUCED_CONSUMERS = SCR-MON-HISTORY-001; SCR-EVENT-CAMERA-001
VERSION_AFTER = 2.0.2
```

### ROOT regression results

Baseline and candidate runs used temporary copies at P3-A `1f833aed523420db47ba06faa5d5cf5cc114de0b`, P3-B remote HEAD `b57ad0044722a838e761f987eeb0aa556c6646b0`, and P3-C `c26840e8c9c21b9105b7c3bb42c96bc5186c9227`. P3-B's temporary copy received the canonical 2.0.1 CSS before baseline; no P3 family branch or worktree was changed.

| Screen | 2.0.1 max row | 2.0.1 split words / badges | 2.0.2 max row | 2.0.2 split words / badges |
|---|---:|---:|---:|---:|
| SCR-INV-001 | 283px | 20 / 11 | 127px | 0 / 0 |
| SCR-MON-HISTORY-001 | 56px | 0 / 0 | 56px | 0 / 0 |
| SCR-SUB-LIST-001 | 91px | 8 / 0 | 81px | 0 / 0 |
| SCR-SUB-CAMERA-001 | 85px | 4 / 0 | 81px | 0 / 0 |
| SCR-ACT-LIST-001 | 95px | 10 / 0 | 95px | 0 / 0 |
| SCR-EVENT-LIST-001 | 73px | 10 / 2 | 73px | 5 / 0 |
| SCR-EVENT-CAMERA-001 | 64px | 0 / 0 | 64px | 0 / 0 |

All seven mobile runs at 390x844 retained contained horizontal scroll and had no page-level horizontal overflow. Every action in the four screens that expose actions (17 links total) remained reachable by Tab; focusing the action column scrolled its table region. The five residual multi-rectangle text ranges on SCR-EVENT-LIST-001 are hyphenated factual identifiers wrapping at their hyphen separators; no ordinary word or badge remains fragmented. The long inventory fixture reduced its maximum row from 283px to 217px; its long status badge wrapped at spaces without fragmentation, and its single long identifier used the fallback break.

At 1440x900, table widths and maximum row heights were unchanged on all seven consumers. SCR-INV-001 was also checked at 1366x768 with unchanged 1072px table width and 103px maximum row height. There was no global overflow, browser error, or production/runtime change. Desktop horizontal scrolling was absent because each table fit its container.

```text
BASELINE_7_CONSUMERS = PASS / DS 2.0.1, 390x844
CROSS_FAMILY_REGRESSION = PASS / 7 of 7, DS 2.0.2, 390x844
GLOBAL_HORIZONTAL_OVERFLOW = NO / 7 of 7
LOCAL_TABLE_SCROLL = FUNCTIONAL / 7 of 7
WORD_FRAGMENTATION = NO DESTRUCTIVE FRAGMENTATION; hyphenated identifiers wrap at delimiters and a long unbroken identifier uses fallback break
BADGE_FRAGMENTATION = NO / all seven; long status wraps at spaces
ACTION_ACCESSIBILITY = PASS / 17 of 17 available action links
KEYBOARD_ACCESSIBILITY = PASS / all available actions reached by Tab
DESKTOP_REGRESSION = PASS / 1440x900 all seven; 1366x768 SCR-INV-001
MOBILE_REGRESSION = PASS / 390x844 all seven; SCR-INV-001 default and long fixture
ROOT_DS_2_0_2_DESIGN_QA = PASS
DESIGN_QA = readability and scanability improved in consumers with split words; action access and hierarchy preserved; desktop density and table widths unchanged
EVIDENCE_CAPTURE = PASS / Node + Playwright + installed Chrome; HTTP bound to 127.0.0.1; captures and metrics retained temporarily under the system temp directory, not family evidence
PRODUCTION_CHANGED = NO
P3_FAMILY_BRANCHES_CHANGED = NO
```
