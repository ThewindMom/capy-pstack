---
name: control-cli
description: Reproduce and verify CLI or TUI behavior on the real Capy machine.
---

# Control a CLI

Read the target project's verification skill and setup commands. Record repository,
base/head, exact executable, input fixture, expected stdout/stderr/exit status, and any
terminal state. Run the actual CLI, using a pseudo-terminal for interactive applications.
Capture the failing behavior before a bug fix, then rerun the identical interaction after
it and a relevant regression case. Include process exit and resulting files, not just
compilation. For long-running tools check readiness first and tear down only processes
this run owns. Preserve evidence in the chosen durable location before cleanup. A native
shared-machine task may inspect the current checkout; a writer must use a fresh machine.
If the required platform/device or credentials are absent, record the exact failed gate
and the smallest human-only action; do not claim the CLI was verified with a mock.
