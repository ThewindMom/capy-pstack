# Terminal harness recipes

Adapted from Cursor's control-cli at revision 53e579f1481697931fc44f5445171397cfa2b24b.
Commands and fixtures below are examples, not a claim that a particular app was tested.

## tmux

Prefer the project's own harness. A temporary isolated tmux session can capture a screen,
send keys, attach for observation and resize its window. Substitute the actual app command:

```bash
SESSION="pstack-cli-$$"
trap 'tmux kill-session -t "$SESSION" 2>/dev/null || true' EXIT
# Run only a caller-authorized executable; never interpolate untrusted input as a command.
tmux new-session -d -s "$SESSION" -x 100 -y 30 -- ./your-cli
tmux capture-pane -p -t "$SESSION"
tmux send-keys -t "$SESSION" 'help' Enter
tmux capture-pane -p -t "$SESSION"
tmux resize-window -t "$SESSION" -x 80 -y 24
tmux capture-pane -p -t "$SESSION"
```

These commands illustrate controls, not a readiness protocol. Between actions wait for a
specific screen state with a bounded probe; capture again to verify it. Exercise arrows,
Escape, Ctrl-C, focus and prompt flows as relevant. A stale screen reference is not evidence.
Capture transcripts and compare layout at the same terminal dimensions. Terminate the owned
session in a trap, including after a failed assertion. Do not kill unrelated tmux sessions.

## Deterministic PTY probe

Use the bundled `scripts/pty_probe.py` for a real PTY with deadline-based patterns:

```json
{
  "timeout": 5,
  "steps": [
    {"expect": "ready>"},
    {"send": "help\n"},
    {"expect": "Commands:"},
    {"resize": [24, 80]},
    {"send": "quit\n"}
  ],
  "exit_code": 0
}
```

`send` also accepts terminal escape sequences such as `\u001b[A` for an arrow. A `signal`
step accepts `INT` or `TERM`. The expected exit code uses POSIX conventions: termination
by signal is negative. Use the actual application's patterns, not these placeholders.
Each expect consumes output through its match, so a later identical expectation needs a
new occurrence. Resize changes the real PTY dimensions. The probe is not a terminal emulator;
verify rendering through the real screen. All probe sessions have explicit ownership and
bounded cleanup. Keep outputs free of credentials and inspect them before publication.

## Profiling

For Node, enable an ephemeral loopback inspector only when profiling is needed:

```bash
NODE_OPTIONS="--inspect=127.0.0.1:0" tmux new-session -d -s "$SESSION" -- ./your-node-cli
```

Read the inspector address from the owned process output. Use existing DevTools-compatible
project tools; do not publish the debug port. Bun may have different inspector commands,
so check its installed help rather than assuming Node flags work everywhere.

Startup: run baseline and treatment interleaved on the same machine, environment and input;
record time to a concrete ready state, not just process creation. Slow operation: start a
CPU profile, drive that operation, stop the profile, compare self-time and call paths.
Memory: take baseline and post-loop heap snapshots; use forced GC only when supported and
record it on both sides. Hang: capture the last screen, active handles/resources and a
stack/CPU sample before interrupting. Optional recording: use the existing demo tool or an
asciinema-compatible recorder when requested, with sanitized data.

Persist accepted artifacts before cleanup or machine replacement. Test a neighboring flow
as well as the fixed case. Report exact command, revision, scenario, result and evidence.
