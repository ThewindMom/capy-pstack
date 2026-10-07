# Requirement-to-evidence map

Target: pstack 0.15.15 at source revision df581122cde17e6e27686b5a448bde23e4ad4318.
This map covers the model/default and support-skill gaps addressed in this revision, not a
certificate for every future upstream release or every possible agent execution.

| Requirement | Native implementation | Executable evidence / remaining live check |
| --- | --- | --- |
| Preserve per-role model assignments | [Preset](../.agents/pstack.model-presets.json) and [resolver](../.agents/skills/poteto-mode/scripts/models.py) | ModelPolicyTests compares implementation/exploration, judgment and reflection tooling against literal expected settings. Actual account grants still need observation. |
| Two distinct arena/architect/interrogate models; reflection is three lenses plus synthesis | Preset, complete calling skills and [model policy](../.agents/skills/poteto-mode/references/model-policy.md) | Tests resolve Opus/Grok identities, separate reflection roles and waves without dropping seats. Cross-family native dispatch remains a live check. |
| Reasoning budget separate from model/priority | Version 2 profile and observed-capability resolver | Strict policy rejects unsupported fast. Native policy records omitted priority while preserving model and effort. Both reject unsupported effort. Live tool must confirm returned settings. |
| Subscription routes do not inflate diversity | Documented identity registry | Tests collapse direct/Codex/Copilot/Azure Sol routes, permit an explicit same-weights route and reject a counterfeit faithful panel. Unknown aliases need documented mapping. |
| Single-model/custom only as an explicit deviation | Named profile plus approval reference; no v1 silent migration | Tests reject absent approval and legacy profiles. Approval references are assertions, not authenticated permission. |
| Judge starts after candidates, exactly one independent seat | select-judge and check-run | Tests reject working/waiting/idle/failed/missing or unaccepted candidates, duplicates, missing settings and pool fan-out. Native timestamps/artifact transfers remain live checks. |
| Full deslop cleanup checklist | [Deslop](../.agents/skills/deslop/SKILL.md), with Cursor MIT license | Manual source comparison retains all five focus areas, minimal edits, unchanged behavior and concise summary. A real agent diff-cleanup evaluation remains unrun. |
| CLI prompt/keyboard/resize, readiness, transcripts, interrupt, exit and cleanup | [Control CLI](../.agents/skills/control-cli/SKILL.md), recipes and PTY probe | TerminalProbeTests runs an actual PTY, resize, Ctrl-C, repeat-pattern deadline, nonzero exit and owned-child cleanup. These are fixture/harness tests, not proof of Capy use. |
| UI stable surface selection, fresh targeting and observe-act-verify | [Control UI](../.agents/skills/control-ui/SKILL.md), recipes and browser probe | BrowserProbeTests uses Chromium, ambiguous/missing-page rejection, DOM replacement, resize, console errors and the same test against broken/fixed fixture code. Enabled in CI. |
| Startup/CPU/memory/hang diagnosis recipes | Both control skills and their local references | Source-guided recipe review. Application-specific profiler artifacts and native tool execution remain live verification work. |
| Skill authoring trigger/non-trigger/failure, scope, full instructions, helper validation and behavioral evaluation | [Create skill](../.agents/skills/create-skill/SKILL.md) | Complete native authoring workflow includes fresh-task positive, negative, failure and holdout tests. An LLM trigger evaluation has not been run here. |
| Authorized continuation, native events, state, idempotency and stop | [Capy automation](../.agents/skills/capy-automation/SKILL.md) and Benny | Detailed documented lifecycle, webhook admission vs completion and domain reconciliation gates. Native automation/Benny event testing remains unrun; no job is created by installation. |
| No upstream availability needed at installation | Local files, retained licenses and installer | Existing archive-only project/volume tests; new preset is included in both layouts. No submodule/download dependency. |


## Retained 0.15.3 requirements

| Requirement | Native implementation | Evidence boundary |
| --- | --- | --- |
| Three new default model identities without invented Capy routes | Local preset, observed bindings, resolver and setup | Update tests exercise opaque observed routes, reject missing bindings and relabelled older weights, and preserve old user pins. Account capability observation and native dispatch remain live checks. |
| Code-ready and patch-changing rounds, focused audit lanes, complete fix-forward and current-head merge-prep CI | Both autopilot playbooks and multi-phase template | Explicit workflow text coverage in the update tests. Actual round notifications, verification and merge decisions remain unrun in Capy. |
| Limited lane-result reuse with two old builds and one current build | Shipping playbook | Text coverage retains per-difference noise review and mandatory rerun for dev-server/no-output lanes. Actual application build comparisons remain live work. |
| Child ledger, safe stalled-writer replacement, audit until delegation is reconciled | Autopilot playbooks and native task ownership rule | Reviewed instructions preserve no-duplicate-writer safety. Stop failures, late results and durable ledger recovery remain live tests. |
| Exact SHA and measurement-method receipts; one retry then explicit gap | Swarm | Text coverage checks the requirement, not a claim of observed agent compliance. |
| Header creation cannot truncate existing evidence on false empty stat | Decision logger | Real Bash regression injects the stat error and verifies the existing bytes survive. New/empty/populated files, bad arguments and field sanitization are also tested. |

See the historical [0.15.3 update record](updates/0.15.3.md) and
[per-source-file inventory](../provenance/updates/0.15.3.json) for the full change scope.

Behavioral test sources: [model tests](../tests/test_model_policy.py), [0.15.3 tests](../tests/test_update_0153.py),
[terminal/browser tests](../tests/test_control_probes.py),
[distribution tests](../tests/test_native.py). They deliberately distinguish pure decisions,
real local process/browser behavior, and unobserved Capy agent execution.

The original build environment blocked browser navigation by administrator policy. Those
historical limits do not describe every later runner. Browser fixture checks are optional
locally and enabled in CI. The actual run result is the source of truth, not this prose.

## Additional 0.15.15 requirements

| Requirement | Native implementation | Evidence boundary |
| --- | --- | --- |
| Same-runner and isolated local execution | Native shared/device/fresh placement and task validator | Three actual shared starts returned this parent's Mac machine ID. Device worktree and cloud handoff tests remain unrun. |
| Fresh-agent context without duplicate live owners | Consolidated briefs and ownership reconciliation in calling skills | Workflow contract checks; maintenance workers used separate conversations and disjoint paths. Repeated callback handoffs remain live work. |
| Current model defaults and explicit priority adaptation | Preset, capy-native/strict policies and resolver | Model tests and actual session-capability input; cross-provider execution still needs a native panel trace. |
| Validate measurements before reporting | Benchmark checklist and Explain the Number | Complete seven-question workflow retained. Application-specific benchmark evidence is task-dependent. |
| Eliminate repeated mistake classes structurally | Correct | Architecture/type/lint/test ordering retained, with a real past-mistake proof requirement. No repository-wide correction program was run by installation. |
| Help without executing the suggested task | Poteto help and native guide links | Native frontmatter and link checks; independent positive/negative trigger eval remains separate. |
| No implicit publication or amendment | Authoring and opening-a-PR workflows | Maintenance left changes uncommitted. PR ownership/callback lifecycle remains unrun. |
| Complete source snapshot and new skill destinations | Source inventory tool and 0.15.15 provenance | All 164 blobs verified and the full source subtree reconstructed. Source audit tests reject changed bytes, modes, missing mappings and symlinks. |

See [the current update record](updates/0.15.15.md) and
[current live gates](live-smoke.md). Historical update inventories remain immutable records
of their source releases; they are not claims that current defaults still match old ones.

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
