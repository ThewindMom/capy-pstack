# Model selection contract

Default policy is `upstream-faithful` for pstack 0.15.2. Read the bundled
`pstack.model-presets.json` from the actual `.agents` or volume root. It retains each
upstream role and panel, rather than changing every task to inheritance. There is no
network fetch. The catalog source is documentation, not account entitlement.

## Profiles and observations are different inputs

`pstack.models.json` is version 2 policy with optional `preset`, `budget`, `max_parallel`,
`roles` and `panels`. Absent fields use the faithful preset. Presets are upstream-faithful,
single-model and custom. Single-model/custom require `approved_difference` naming the real
user approval; it is an auditable assertion, not a substitute for permission. Preserve
existing v1 profiles and migrate explicitly; do not silently reinterpret them.

Roles take a choice; panels take lists. A choice has `model`, optional `reasoning_effort`
and optional boolean `fast`. Strings are allowed for inheritance or custom choices.
Faithful overrides must preserve weights and settings, though a documented billing alias
may be selected explicitly. Budget unlimited preserves source efforts; large/xhigh,
medium/high and small/medium set the requested effort separately. Unsupported settings
fail, never silently approximate. No measured reasoning equivalence between platforms is
claimed. Fast is a priority request, not a guaranteed latency.

Observe current native task choices into a JSON object:

```json
{"source":"actual Capy tool result or picker observation reference","models":{},"parent":{"model":"observed/parent-id"}}
```

Populate models with exact observed IDs. Each value has `reasoning_efforts` (the supported
strings) and `fast` (a boolean capability). Include the actual parent effort/fast settings
when needed. An empty observation cannot resolve a faithful panel. Re-observe before use;
a locally saved file can be stale and neither the validator nor this file proves access.
Do not put secrets into the observation. Public documentation only confirms identifiers.

## Resolve before drafting/starting

Run from the actual bundle root, using absolute paths from other working directories:

```bash
python3 skills/poteto-mode/scripts/models.py validate pstack.models.example.json
python3 skills/poteto-mode/scripts/models.py requested pstack.models.example.json --role 'arena runners'
python3 skills/poteto-mode/scripts/models.py resolve pstack.models.example.json \
  --role 'arena runners' --observed /actual/current-observation.json > /tmp/candidates.json
```

`requested` shows policy only, not a launch. `resolve` requires observations, rejects
unavailable IDs/efforts/priority and reports every choice, real model identity, provider
family and concurrency wave. Four faithful seats mean Fable 5.1, GPT-5.6 Sol, Grok 4.6 and
Opus 5 (three families). Subscription and direct-billed routes to the same weights count
once. All four seats still run with max_parallel 3, in two waves; a cap never drops a seat.

The result is a **work order, not a Capy SDK payload**. Map model, reasoning and priority to
the actual native tool schema. Verify returned settings. If the tool cannot set or reveal
an essential field, block and report it. Do not omit the field and call it faithful. If the
selected policy is inheritance, omit native overrides but audit against actual parent
settings. Do not create four new threads as a substitute for native child tasks.

For implementation use feature/refactoring/bug-fix/perf-issue/hillclimb as applicable;
hardest tasks take their own judgment role. How has explorer/explainer; Why has investigators/
synthesizer. Reflect has tooling/judgment/divergent/synthesizer, with three reviewer tasks
and one later synthesizer. Swarm uses swarm workers except explicitly framed race arms.
Comment Sicko alone keeps the unspecified upstream model. Do not override every role with
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
An approved dropout needs an explicit revised custom run/order after the failed owner is
reconciled; never treat a timeout as completion or reuse a partial order silently.
The parent reads while the judge works. Independent review is not approval to merge.

## Current limits

The resolver checks supplied observations/records, not the remote platform or permission.
Validate actual native IDs, timestamps and artifacts in Capy. Unknown billing aliases are
not automatically equated; update the documented identity registry before making diversity
claims about such routes. Live model dispatch and workflow compliance remain separate
acceptance checks in the repository's smoke checklist.

Platform references checked 2026-09-22:
https://docs.capy.ai/models-and-pricing
https://docs.capy.ai/tasks
