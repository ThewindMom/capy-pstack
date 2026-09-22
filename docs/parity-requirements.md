# Requirement-to-evidence map

Target: pstack 0.15.2 at source revision 53e579f1481697931fc44f5445171397cfa2b24b.
This map covers the model/default and support-skill gaps addressed in this revision, not a
certificate for every future upstream release or every possible agent execution.

| Requirement | Native implementation | Executable evidence / remaining live check |
| --- | --- | --- |
| Preserve per-role model assignments | [Preset](../.agents/pstack.model-presets.json) and [resolver](../.agents/skills/poteto-mode/scripts/models.py) | ModelPolicyTests compares implementation/exploration, judgment and reflection tooling against literal expected settings. Actual account grants still need observation. |
| Four distinct arena/architect/interrogate models; reflection is three lenses plus synthesis | Preset, complete calling skills and [model policy](../.agents/skills/poteto-mode/references/model-policy.md) | Tests resolve all four identities, separate reflection roles and waves without dropping seats. Native task trace remains required. |
| Reasoning budget separate from model/priority | Version 2 profile and observed-capability resolver | Tests reject unsupported effort/fast, preserve budget requests and prevent hidden downgrade. Live tool must expose and confirm these settings. |
| Subscription routes do not inflate diversity | Documented identity registry | Tests collapse direct/Codex/Copilot/Azure Sol routes, permit an explicit same-weights route and reject a counterfeit four-model faithful panel. Unknown aliases need documented mapping. |
| Single-model/custom only as an explicit deviation | Named profile plus approval reference; no v1 silent migration | Tests reject absent approval and legacy profiles. Approval references are assertions, not authenticated permission. |
| Judge starts after candidates, exactly one independent seat | select-judge and check-run | Tests reject working/waiting/idle/failed/missing or unaccepted candidates, duplicates, missing settings and pool fan-out. Native timestamps/artifact transfers remain live checks. |
| Full deslop cleanup checklist | [Deslop](../.agents/skills/deslop/SKILL.md), with Cursor MIT license | Manual source comparison retains all five focus areas, minimal edits, unchanged behavior and concise summary. A real agent diff-cleanup evaluation remains unrun. |
| CLI prompt/keyboard/resize, readiness, transcripts, interrupt, exit and cleanup | [Control CLI](../.agents/skills/control-cli/SKILL.md), recipes and PTY probe | TerminalProbeTests runs an actual PTY, resize, Ctrl-C, repeat-pattern deadline, nonzero exit and owned-child cleanup. These are fixture/harness tests, not proof of Capy use. |
| UI stable surface selection, fresh targeting and observe-act-verify | [Control UI](../.agents/skills/control-ui/SKILL.md), recipes and browser probe | BrowserProbeTests uses Chromium, ambiguous/missing-page rejection, DOM replacement, resize, console errors and the same test against broken/fixed fixture code. Enabled in CI. |
| Startup/CPU/memory/hang diagnosis recipes | Both control skills and their local references | Source-guided recipe review. Application-specific profiler artifacts and native tool execution remain live verification work. |
| Skill authoring trigger/non-trigger/failure, scope, full instructions, helper validation and behavioral evaluation | [Create skill](../.agents/skills/create-skill/SKILL.md) | Complete native authoring workflow includes fresh-task positive, negative, failure and holdout tests. An LLM trigger evaluation has not been run here. |
| Authorized continuation, native events, state, idempotency and stop | [Capy automation](../.agents/skills/capy-automation/SKILL.md) and Benny | Detailed documented lifecycle, webhook admission vs completion and domain reconciliation gates. Native automation/Benny event testing remains unrun; no job is created by installation. |
| No upstream availability needed at installation | Local files, retained licenses and installer | Existing archive-only project/volume tests; new preset is included in both layouts. No submodule/download dependency. |

Behavioral test sources: [model tests](../tests/test_model_policy.py),
[terminal/browser tests](../tests/test_control_probes.py),
[distribution tests](../tests/test_native.py). They deliberately distinguish pure decisions,
real local process/browser behavior, and unobserved Capy agent execution.

The local build environment blocks browser navigation by administrator policy. No policy
was changed. The HTTP browser tests run in GitHub CI instead. The test result on the actual
commit, not this document's prose, is the source of truth for their pass/fail status.

## Support-skill provenance

Control CLI, Control UI and Deslop are adapted from Cursor team kit at the same source
revision. Their original MIT license is retained in each skill folder. Source files:

- https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/cursor-team-kit/skills/control-cli/SKILL.md
- https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/cursor-team-kit/skills/control-ui/SKILL.md
- https://github.com/cursor/plugins/blob/53e579f1481697931fc44f5445171397cfa2b24b/cursor-team-kit/skills/deslop/SKILL.md

Create-skill follows https://docs.capy.ai/skills and the bundled pstack authoring/eval
playbooks. Capy-automation follows https://docs.capy.ai/automations and the bundled long-run
playbooks. They preserve needed outcomes; they are not presented as identical external
Cursor built-in implementations. All references are attribution, not runtime fetches.
