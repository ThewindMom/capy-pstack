# Browser and CDP recipes

Adapted from Cursor's control-ui at revision 53e579f1481697931fc44f5445171397cfa2b24b.
Use a checked-in project harness first. The examples require the project's installed
Playwright and actual app URL/marker; do not install or alter dependencies implicitly.

## Local web harness

```javascript
import { chromium } from "playwright";
const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto("http://127.0.0.1:<port>");
  await page.locator("<app-root-selector>").waitFor();
  await page.screenshot({ path: "/tmp/ui-before.png", fullPage: true });
  await page.getByRole("button", { name: /submit/i }).click();
  // Assert the app-specific visible outcome before calling this successful.
  await page.locator("<success-selector>").waitFor();
  await page.screenshot({ path: "/tmp/ui-after.png", fullPage: true });
} finally {
  await browser.close();
}
```

## Existing Electron or Chromium surface

Launch the owned app with a loopback remote-debugging port when supported. Connect using
`chromium.connectOverCDP("http://127.0.0.1:<debug-port>")`. Search all contexts/pages by
stable positive app markers. A negative marker can rule out a background window. Require
exactly one matching surface. On zero/multiple matches report titles and URLs, not a guessed
first tab. Preserve externally owned browsers when disconnecting; closing an owned test
browser is different from terminating someone else's app.

Do not enable or publicly expose CDP just for convenience. CDP grants control of the browser.
For a disposable reproduction, prefer a browser process owned by this test run.

## Bundled Python probe

When Python Playwright is already available:

```bash
python3 /actual/bundle/skills/control-ui/scripts/browser_probe.py \
  --url http://127.0.0.1:3000 --scenario /tmp/ui-scenario.json \
  --output /tmp/ui-evidence --executable /actual/path/to/chromium
```

A scenario has a CSS `marker`, optional `exclude_marker`, optional `[width,height]`
`viewport`, and `steps`. Each click/fill/press step selects by exact `role` and `name`.
An `expect` specifies a CSS selector and exact visible text. All steps save fresh screens.

```json
{
  "marker": "[data-app='counter']",
  "viewport": [1280, 800],
  "steps": [
    {"action": "click", "role": "button", "name": "Increment",
     "expect": {"selector": "[data-testid='count']", "text": "1"}},
    {"action": "resize", "value": [800, 600],
     "expect": {"selector": "[data-testid='count']", "text": "1"}}
  ]
}
```

`--cdp <loopback URL>` selects an existing page by marker; it does not open the example URL
on a random tab. Supported actions are click, fill, press, scroll, resize, navigate and drag.
For drag, supply `target_role` and `target_name`. Each action must include its own visible
expectation. Prefer native/project tools for richer accessibility or visual assertions.

## Profiling and recovery

Start a trace/CPU profile immediately before the operation, stop immediately after, and
compare the same work at baseline and head. For memory, compare heap snapshots around a
repeated operation with consistent GC policy. Inspect network failures, console exceptions,
layout shifts and rendering conditions alongside timings. Use throttling, cache disablement,
color scheme and reduced motion only when relevant, and record them on both runs.

After a surprising result, capture current state, diagnose/reset through the project's
harness, then drive again. Reacquire targets after every structural change. Never treat a
stale reference as evidence that the application is broken. Keep fixtures disposable;
screenshots, recordings and heaps from sensitive workspaces require explicit authorization.
Transfer accepted artifacts to the reviewing machine and retain them before deleting owned
dev servers, debug sessions and temporary browser profiles.

The browser probe keeps page-load readiness separate from action assertions.
`navigation_timeout_ms` defaults to 30000; `timeout_ms` defaults to 5000 for
interactions and visible expectations. Set measured performance gates explicitly;
a short action deadline must not accidentally become a cold-start page-load limit.
