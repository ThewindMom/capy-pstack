---
name: control-ui
description: Build or adapt a browser/CDP harness to drive and inspect a real web, IDE or Electron UI. Use for UI bugs, focus/keyboard/scroll/resize flows, screenshots, accessibility snapshots, visual diffs and performance or memory profiles.
---

# Control UI

Use the actual application and repeatable observations. Reuse the project's Playwright,
Cypress, Storybook, Electron or other browser harness first. Otherwise use Capy's available
browser/desktop tools or a temporary local probe. This adapts Cursor's MIT-licensed
control-ui, retaining its setup, selection, interaction, profiling and cleanup requirements.
See `LICENSE` and `references/recipes.md`.

## Set up the right surface

1. Read the project's verification skill and dev-environment commands. Record the exact
   checkout, application route, fixture/user state, viewport and expected visible result.
2. Start the real application and health-check it. Find existing browser and Electron scripts
   before adding tools. Do not add a project dependency just to run a one-off probe unless
   authorized; use installed tooling. Do not hard-code another repository's ports or selectors.
3. For a web app use its local URL. For Electron/Chromium, enable a loopback debug port only
   when the app supports it. Discover that port from the actual launch, not from an example.
4. Select the page using stable positive app markers; optionally exclude a known wrong
   surface with a negative marker. Never choose the first tab by position. If no page or
   multiple pages match, list titles/URLs without secrets and resolve the ambiguity.
5. Prefer accessibility roles, labels and stable data attributes to coordinates. Capture a
   fresh screenshot immediately before any necessary coordinate click.

## Observe, act, verify

1. Capture the current page snapshot or screenshot before acting.
2. Select the target from the current structure, not a stale handle from a previous navigation.
3. Perform one structural action: click, type, keypress, drag, scroll, navigate or resize.
4. Capture a new snapshot/screenshot and assert the expected state change. Read readiness
   or the relevant response; a blind delay is not verification.
5. Repeat for the complete user journey. Capture console exceptions, failed network requests
   and response errors. Investigate unexpected failures rather than hiding them.
6. For a bug, prove the same surface fails before the fix. Replay the identical interaction
   after the fix and run a neighboring regression. Save before/after evidence when requested.

The bundled `scripts/browser_probe.py` can execute role-based scenarios with real Chromium,
marker-based page selection and before/after screenshots when Python Playwright is already
installed. It is optional; native Capy browser tools and existing project harnesses remain
valid. The recipes include the original JavaScript Playwright/CDP approach as well.
A screenshot of source code or a mocked page is not application verification.

## Performance, memory and rendering

Use higher-level browser APIs first. Use raw CDP only for capabilities they cannot supply:
CPU profiles, traces, paint/FPS and layout-shift inspection; heap snapshots and supported
GC; request blocking/throttling/cache controls and network logs; viewport/color-scheme/
reduced-motion emulation and accessibility inspection; console, exceptions and DOM snapshots.
Measure baseline and treatment under matching scenarios. Attach the actual trace/snapshot,
not a confident diagnosis without an artifact. Heap snapshots can expose sensitive data.

## Capy ownership, persistence and safety

Keep one controller for a shared UI instance. Writers and independently modified candidate
apps use fresh machines; the judge gets accepted artifacts via native `transfer_files`.
Verify transferred files before relying on their paths. Read-only task does not mean a UI
interaction cannot mutate application data: use disposable local fixtures and stay within
explicit authorization for external side effects.

Processes and previews sleep with the machine. Put required services in the project's
idempotent startup phase with readiness checks; snapshots cache dependencies, not live
processes. Save evidence in the selected authorized volume or a pushed commit before
cleanup. Do not expose ports, capture a sensitive workspace, or publish private screenshots
without the corresponding authorization. Clean up only this run's dev servers, debug
sessions and temporary profiles; never terminate an externally owned browser. Report an
unsupported platform/device/tool as blocked, not verified. Local probe tests are not
proof of Capy's own browser-tool execution.
