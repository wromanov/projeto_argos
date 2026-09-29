# ROOT-REQ-UIV2-EVIDENCE-CAPTURE-001 — Captura reprodutível de evidência

ID = ROOT-REQ-UIV2-EVIDENCE-CAPTURE-001
STATUS = RESOLVED / EXISTING_ALLOWED_MECHANISM_FOUND

## Mecanismo que falhou

```text
FAILED_CAPTURE_MECHANISM = in-app browser flow that attempted to save a screenshot through a data-URL navigation/download
FAILURE_MODE = browser rejected the data-URL save; the PNG was not written to the P3-A evidence directory
POLICY_OR_TOOL_RESTRICTION = the browser security policy forbids alternate-surface workarounds; no bypass was attempted
BROWSER_RENDER_WORKED = YES
```

P3-A's prior handoff records that the pages rendered and were inspected, while the required PNG download failed. This is a capture-output restriction, not a rendering failure.

## Mecanismo permitido encontrado

Use the already-installed bundled Node.js runtime and Playwright package with the installed Chrome executable. Serve the static prototype over HTTP bound to `127.0.0.1`; open the local route in a Playwright page with an explicit viewport and `deviceScaleFactor: 1`; wait for the screen/fixture to become stable; then call the supported `page.screenshot({ path, fullPage: false })` API directly to the intended evidence path. Do not use a `data:` URL or browser download.

```text
APPROVED_CAPTURE_MECHANISM = Node + Playwright + locally available Chrome
CAPTURE_MODE = LOCAL HTTP PREVIEW ONLY
OUTPUT = PNG directly into controlled evidence paths
RECOMMENDED_CAPTURE_MECHANISM = bundled Node.js + existing Playwright + installed Chrome; local HTTP preview; direct Playwright PNG output
DEPENDENCY_INSTALL_REQUIRED = NO
REPOSITORY_DEPENDENCY_CHANGE = NO
REPO_CHANGE_REQUIRED = NO
IMPLEMENTATION_OWNER = NONE / existing runtime capability
```

The API accepts an absolute path, so the same deterministic capture can target a repo-controlled evidence directory during an authorized family QA activity. Existing P3-C evidence is committed under its own `evidence/screenshots/p3-c/post-ds-2.0.1/` path.

## Prova temporária

```text
PROOF_SCREEN_ID = SCR-INV-001
URL = local HTTP preview of the temporary P3-A worktree at the authorized remote HEAD
VIEWPORT = 390x844
ZOOM = 100% default browser scale
DEVICE_SCALE_FACTOR = 1
PNG_EXISTS = YES / at proof time
PNG_DIMENSIONS = 390x844
PNG_SHA256 = 269cc93795c97c71ec0c707303ef5a7d8fd2e074fe60e059db21de41d66d7c3e
CAPTURE_REPEATABLE = YES / two independent captures produced identical bytes
BROWSER_ERRORS = 0
EXTERNAL_REQUESTS = 0
NON_GET_REQUESTS = 0
```

The PNG was inspected and showed the requested P3-A table state. Both temporary capture files, the temporary capture script and the local HTTP server were removed/stopped after verification. The P3-A evidence matrix was not populated, and this proof is not represented as archived family evidence.

```text
CAPTURE_OUTCOME = EXISTING_ALLOWED_MECHANISM_FOUND
EVIDENCE_GATE = READY / capture mechanism proven; family evidence remains a separate QA gate
TEMP_VALIDATION_CLEANUP = PASS
```

Filename contract for an authorized family capture remains `<screen-id>__<viewport>__<state>__<fixture>.png`. The family owner must save the PNG directly under its repo-controlled evidence path and validate the PNG dimensions before marking the capture complete.
