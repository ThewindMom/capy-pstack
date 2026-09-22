---
name: control-cli
description: Build or adapt a repeatable terminal harness to drive, inspect and profile a real CLI or TUI on a Capy machine. Use for prompt flows, keyboard/resize bugs, startup regressions, memory leaks, hangs and terminal demos.
---

# Control CLI

Use a repeatable local harness, not manual poking or a compilation-only proxy. Reuse the
project's checked-in test/demo harness first. Otherwise assemble a temporary harness from
local tools. This workflow adapts Cursor's MIT-licensed control-cli; its practical
interaction and profiling requirements are retained. See `LICENSE` and `references/recipes.md`.

## Scope and machine

Identify the command, base/head revision, input fixture, expected stdout/stderr/exit code,
terminal size and environment. Use the smallest reproducible workspace. Explore the current
checkout on a shared read-only task. A test that writes fixtures, generated output or code
needs its own fresh machine or the existing implementation owner, not a second shared writer.
Discover available tools before choosing them. No workstation paths or presumed macOS tools.
Do not send credentials or destructive commands into a controlled session.

## Harness loop

1. Discover package scripts, E2E tests, demo recorders, Expect scripts and PTY helpers.
2. Start the actual executable in an isolated terminal with deterministic environment and
   dimensions. Keep a temporary harness outside the project unless a reusable test is requested.
3. Capture the current screen before acting. A transcript is not proof of terminal layout.
4. Send one action: text, Enter, arrows, Escape, Ctrl-C, scroll or resize. Test each interaction
   implicated in the defect rather than merely typing one successful command.
5. Wait for a concrete prompt or screen pattern before the next action. Use a deadline;
   EOF, an unexpected exit or timeout fails the gate. Do not use blind sleeps for readiness.
6. Capture the new screen and transcript; assert the expected state, process exit and changed
   files. For a bug, save a failing run before editing, then replay the same scenario after
   the fix plus a neighboring regression. Keep baseline and treatment conditions equal.
7. Save before/after transcripts, profiles and any requested recording. Retain authorized
   evidence on the selected volume or in a pushed commit before machine cleanup. Use native
   `transfer_files` before another machine relies on it; verify the transferred bytes.
8. Shut down only this run's terminal, child processes, inspector and temporary files, even
   when a check fails. Record remaining blockers rather than claiming success with a mock.

## Harness choices

Use repo-native scripts when available. Otherwise use tmux for interactive sessions,
`capture-pane` and `send-keys`, or a PTY probe for deterministic input/waits. The bundled
`scripts/pty_probe.py` provides a deadline-based PTY runner with input, resize, signals,
exit checks and cleanup. It captures terminal output, not a fully rendered screen; use
an actual terminal renderer or tmux capture for layout claims. See the complete tmux,
inspector, PTY and profiling recipes in `references/recipes.md`.

Run a scenario from the current app checkout:

```bash
python3 /actual/bundle/skills/control-cli/scripts/pty_probe.py \
  --scenario /tmp/scenario.json --output /tmp/cli-evidence.json -- ./your-cli
```

Scenario fields are documented by the helper's `--help` and in the recipes. Never pass a
project path from this example without resolving it. No package installation is performed.

## Profiling and demonstrations

For startup regressions measure baseline and changed startup under the same command,
machine and environment. For a slow operation capture a CPU profile during that operation.
For memory growth take heap snapshots before and after repeated work, forcing GC only if
supported and recording that choice. For a hang capture the screen, handles/resources and
a stack or CPU sample before interruption. Do not infer a root cause from a timing alone.
Use a repo-local recorder or asciinema-compatible tool for requested demos. A video does
not replace assertions, and a machine boot is not the CLI's startup metric.

Capy processes do not survive sleep. Configure required services in the project's idempotent
startup phase, with readiness checks. Keep long test commands tracked by the agent rather
than detaching them and assuming the VM will stay awake. A missing device, runtime or
credential is an explicit blocked gate. Native Capy execution must be verified separately
from the local helper tests.
