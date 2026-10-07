# Model selection contract

With no profile, default policy is `capy-native` for pstack 0.15.15, with a large budget. Read the bundled
`pstack.model-presets.json` from the actual `.agents` or volume root. It retains each
upstream role and panel, rather than changing every task to inheritance. There is no
network fetch. The catalog source is documentation, not account entitlement.

## Profiles and observations are different inputs

`pstack.models.json` is version 2 policy with optional `preset`, `budget`, `max_parallel`,
`roles` and `panels`. An empty object represents no profile. A nonempty profile without `preset` retains upstream-faithful.
Presets are capy-native, upstream-faithful, single-model and custom. Select native explicitly in an existing profile to enable priority adaptation. Single-model/custom require `approved_difference` naming the real
user approval; it is an auditable assertion, not a substitute for permission. Preserve
existing v1 profiles and migrate explicitly; do not silently reinterpret them.

Roles take a choice; panels take lists. A choice has `model`, optional `reasoning_effort`
and optional boolean `fast`. Strings are allowed for inheritance or custom choices.
Native and faithful overrides preserve weights and requested settings, though a documented billing alias
may be selected explicitly. Native also allows explicitly selected `inherit-parent` and `auto`.
Both aliases inherit every parent setting without effort or priority overrides. Alias seats still count toward fan-out, not diversity.
Budget unlimited preserves source efforts. Large sets xhigh, medium sets high, and small sets medium.
A role or panel named in a custom profile keeps an explicit `reasoning_effort`.
For large, medium, or small budgets, a non-alias custom seat that omits
`reasoning_effort` still gets the effort for that budget.
Unsupported settings fail, never silently approximate. Native defaults to large. Existing strict/custom profiles without a budget retain unlimited and their effort pins. No measured reasoning equivalence between platforms is
claimed. Fast is a priority request, not a guaranteed latency.
Native resolution omits unsupported fast. Each work order records the seat, requested value, omitted value, and reason in `adaptations`.
The requested policy retains fast. Strict upstream-faithful, custom, single-model, and inherited parent settings reject unsupported priority.
No policy substitutes an unavailable model or drops unsupported effort.

Observe current native task choices into a JSON object:

```json
{"source":"actual Capy tool result or picker observation reference","models":{},"parent":{"model":"observed/parent-id"}}
```

Populate models with exact observed IDs. Each value has `reasoning_efforts` (the supported
strings) and `fast` (a boolean capability). Include the actual parent effort/fast settings
when needed. An empty observation cannot resolve a faithful panel. Re-observe before use;
a locally saved file can be stale and neither the validator nor this file proves access.
Do not put secrets into the observation. Public documentation only confirms identifiers.

## Bind new upstream identities without guessing a native route

The 0.15.15 preset names `anthropic/claude-opus-5-5` and `xai/grok-4.7` as **policy
identities** derived from upstream's requested models. A current native session may expose those exact routes, but this preset does not confirm access. A name
in this file or in an observation's `models` keys is not sufficient to resolve them.

For each identity, use the current account picker or native tool evidence to record the
actual route and the exact model version. Add a binding to the observation, for example:

```json
{
  "source": "REPLACE with current native capability observation",
  "models": {
    "REPLACE_WITH_ACTUAL_ROUTE": {"reasoning_efforts": ["xhigh"], "fast": false}
  },
  "bindings": {
    "anthropic/claude-opus-5-5": {
      "model": "REPLACE_WITH_ACTUAL_ROUTE",
      "source": "REPLACE with evidence that this route is Opus 5.5"
    }
  }
}
```

This is an incomplete illustrative shape, not account evidence or a launchable panel.
Add the independently observed Grok 4.7 binding and capabilities for a full panel.
The resolver copies the observed route literally, checks its settings, and retains the
policy identity for diversity and cross-judge family selection. It rejects absent bindings,
two identities mapped to one route, and a known older model relabelled as a new version.
Neither an observation file nor its source string authenticates remote access; inspect the
real Capy result. If the account cannot supply the required version, leave the role blocked
or use an explicitly approved custom policy. Never invent native IDs or billing aliases.

Existing explicit model/panel overrides keep their values. A pre-0.15.15 faithful pin may
now fail validation. Back it up and remove only the entries selected for reset, or keep
them under an approved custom profile. Rerunning setup does not reset them automatically.

## Resolve before drafting/starting

Run from the actual bundle root, using absolute paths from other working directories:

```bash
python3 skills/poteto-mode/scripts/models.py validate pstack.models.example.json
python3 skills/poteto-mode/scripts/models.py requested pstack.models.example.json --role 'arena runners'
python3 skills/poteto-mode/scripts/models.py resolve pstack.models.example.json \
  --role 'arena runners' --observed /actual/current-observation.json > /tmp/candidates.json
```

`requested` shows policy only, not a launch. `resolve` requires observations and rejects unavailable IDs and efforts.
It rejects unavailable strict priority and labels native priority omissions. It reports choices, identities, families, adaptations, inherited seats, and concurrency waves.
Two upstream seats mean Opus 5.5 xhigh and Grok 4.7 xhigh-fast across two families. Sol is not a default role.
Subscription and direct-billed routes to the same weights count once.
Both seats run with max_parallel 2 or higher in one wave; a lower cap never drops a seat.

The result is a **work order, not a Capy SDK payload**. Map model, reasoning and priority to
the actual native tool schema. Verify returned settings. If the tool cannot set or reveal
an essential field, block and report it. Native policy can omit only unsupported priority, with its adaptation label.
Do not call adapted execution upstream-faithful. If a seat is in `inherited_seats`, omit native overrides but audit against actual parent
settings. Do not create extra threads as a substitute for native child tasks.

For implementation use feature/refactoring/bug-fix/perf-issue/hillclimb as applicable;
hardest tasks take their own judgment role. How has explorer/explainer; Why has investigators/
synthesizer. Reflect has Grok tooling and Opus judgment/divergent/synthesizer roles, with three reviewer tasks
and one later synthesizer. Swarm uses swarm workers except explicitly framed race arms.
Comment Sicko alone inherits by default. Do not override every role with
the parent or apply the panel defaults to reflection.

## Results and one cross-judge

Record each candidate's zero-based `seat`, unique `native_task_id`, actual `settings` object,
`status`, `accepted` boolean and real `artifact` reference. No summary authenticates itself.

```bash
python3 skills/poteto-mode/scripts/models.py check-run /tmp/candidates.json --records /actual/records.json
python3 skills/poteto-mode/scripts/models.py select-judge pstack.models.example.json \
  --observed /actual/current-observation.json --candidates /tmp/candidates.json \
  --records /actual/records.json
```

Check-run rejects missing/duplicate seats, missing effort, changed billing routes, repeated
task IDs and live/idle/failed results. A pool is not a runnable panel. Select-judge requires
the complete accepted candidate order, selects exactly one pool entry, and prefers a
provider family different from the observed parent. Transfer accepted artifacts first.
The selected judge's work order retains any priority adaptation and inheritance marker for that seat.
An approved dropout needs an explicit revised custom run/order after the failed owner is
reconciled; never treat a timeout as completion or reuse a partial order silently.
The parent reads while the judge works. Independent review is not approval to merge.

## Current limits

An advertised model can still fail at native launch because its billing route lacks
credits, entitlement, or permission. Treat the failed task as failed evidence, not a
completed seat. Report the actual route error and reconcile the owner before a replacement.
A subscription-backed alternative is a deliberate policy choice, not proof that the
requested model ran. Never silently save that alternative into the user's profile.

The resolver checks supplied observations/records, not the remote platform or permission.
Validate actual native IDs, timestamps and artifacts in Capy. Unknown billing aliases are
not automatically equated; update the documented identity registry before making diversity
claims about such routes. Live model dispatch and workflow compliance remain separate
acceptance checks in the repository's smoke checklist.

Platform references checked 2026-09-23:
https://docs.capy.ai/models-and-pricing
https://docs.capy.ai/tasks
