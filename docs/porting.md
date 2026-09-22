# Porting record

## Complete source, native execution

All 158 files in the pstack 0.15.2 source subtree are accounted for in
[the provenance inventory](../provenance/source.json). Skills moved to `.agents/skills`,
agent prompts to `.agents/roles`, and the dormant Benny pack to `.agents/automations`.
References, examples, illustrations, licenses, scripts and script tests are local files.
The editor manifest became `pstack.json`, distribution metadata rather than an invented
Capy SDK. The readme/setup guide were rewritten. The original wrapper/submodule design
and its required upstream checkout are gone.

## Deliberate semantic changes

Task calls became native Capy drafts/starts with explicit shared/fresh placement,
self-contained context, native IDs, accepted dependency branches and transfer_files.
Arena preserves framing, independent candidates, cross-judge, selection, grafting and
verification; a live timeout is not a completed candidate. Architect keeps at least two
structurally different sketches. Reviewers stay independent of implementers.

Provider-specific slugs and reasoning suffix transformations became observed-account
role profiles with parent inheritance as the safe default. Role/panel validation is
executable; an inherited model never appears as a literal model argument. Same-model
panels are disclosed. Reflection retains its three lenses, synthesis, structural check,
explicit approval before skill edits, and evidence of what the agent actually read.
Recall/reflect/eval use native thread/task history rather than local editor databases.

PR workflows use Capy ownership and event wakeups. The full GitHub watcher remains a
bundled optional tool, not the default wake loop. Shipping preserves the contiguous
verified frontier, per-head/patch evidence, bottom-only preparation and one merge at a
time. A green task/check is not permission to merge. Native capabilities and current
user authorization always bound the workflow.

Autonomous programs use native events and authorized schedules, with volume-based run
records rather than detached sleepers or assumed persistent home directories. Pause and
pickup distinguish machine identity from disposable backing. Cleanup audits local Git
worktrees and actual Capy owners without invoking macOS editor/simulator commands.

Benny includes its complete triage/repro instructions, feature/routing references,
configuration template and setup. It handles Slack bursts per root report and consumes
trusted marker events instead of racing a local polling loop. Automation volumes keep
state; discoverable skills live in supported skill volumes or project repositories.
make-bot-ui uses Capy's secret URL webhook protocol, server-side relay, stable idempotency
keys and actual accepted-versus-completed semantics, not editor-specific credentials.

Native create-skill, deslop, control-cli, control-ui and capy-automation workflows replace
external editor-only dependencies. They are new Capy implementations of the required
outcomes, not claims to have copied another plugin's exact implementation.

## Maintenance

Edit the native files directly and refresh their catalog after review. No regeneration
from an external source is required. The provenance hashes identify the imported source
for audit; they do not freeze the native files or fetch anything at install time.
README references to Capy documentation are citations, not executable dependencies.
Local/CI contract tests cannot prove every future agent obeys prose. Live Capy execution
still needs the [smoke checks](live-smoke.md).
