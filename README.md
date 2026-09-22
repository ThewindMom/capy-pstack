# capy-pstack

**pstack's engineering discipline, built for Capy's cloud agents.**

Start with the problem, investigate before changing code, compare designs when the choice matters, and verify the actual result. Then use Capy's isolated task machines, durable threads, and event-driven PR follow-up to carry the work through.

This repository contains the full, self-contained Capy port of [Lauren Tan's pstack for Cursor](https://github.com/cursor/plugins/tree/53e579f1481697931fc44f5445171397cfa2b24b/pstack), based on version **0.15.2**. The skills and workflows are ordinary files you can read, edit, and install without the original repository.

[Features](#what-pstack-brings) · [Why Capy](#how-this-port-plays-to-capys-strengths) · [Differences and limits](#what-does-not-carry-over-from-cursor) · [Get started](#get-started) · [Full catalog](docs/skill-catalog.md)

## What pstack is

pstack is an engineering workflow suite created by Lauren Tan, also known as poteto, for Cursor. Its aim is less unnecessary code and more confidence in the code that ships. It combines skills, engineering principles, playbooks, role prompts, and supporting tools. It is not a model, an application framework, or a replacement for tests.

The main entry point is [poteto-mode](.agents/skills/poteto-mode/SKILL.md). You describe the outcome. The workflow selects the relevant playbook, turns its steps into a visible plan, and brings in investigation, design, implementation, and review skills as needed. A bug fix starts with reproduction. An architecture decision starts with understanding the existing system and exploring alternatives. Shipping requires evidence beyond a green check.

The original Cursor plugin uses Cursor's tools, subagents, model choices, and editor workflows to do that. **This port preserves the engineering method and changes the execution model.** Capy provides the agents, machines, integrations, and lifecycle. capy-pstack tells those agents how to scope work, challenge assumptions, coordinate ownership, and judge results. The [porting record](docs/porting.md) describes the changes.

## What pstack brings

The suite includes **47 ported pstack skills, including 23 principles, and 23 complete playbooks**. Five bundled support skills bring the main catalog to **52**. The separate Benny automation pack contains its own setup, triage, and reproduction workflows.

| Work you need to do | What the workflow adds |
| --- | --- |
| Understand a subsystem or an old decision | [how](.agents/skills/how/SKILL.md) traces behavior. [why](.agents/skills/why/SKILL.md) investigates code history and available external evidence. [teach](.agents/skills/teach/SKILL.md) builds an explanation you can follow rather than handing back a code dump. |
| Design before committing to an implementation | [architect](.agents/skills/architect/SKILL.md) explores structurally different designs. [arena](.agents/skills/arena/SKILL.md) runs competing candidates, waits for an independent cross-judge, selects a base, combines useful parts, and verifies the result. |
| Cover a large surface in parallel | [swarm](.agents/skills/swarm/SKILL.md) partitions coverage or runs explicitly framed races, then combines the evidence into one report. It is distinct from arena's competing solutions to one problem. |
| Fix a bug or build a feature | The [bug-fix](.agents/skills/poteto-mode/playbooks/bug-fix.md), [feature](.agents/skills/poteto-mode/playbooks/feature.md), and [refactoring](.agents/skills/poteto-mode/playbooks/refactoring.md) playbooks require scoped changes and verification. [tdd](.agents/skills/tdd/SKILL.md) establishes a failing test first when an appropriate test path exists. |
| Improve performance or diagnose a runtime symptom | [Performance work](.agents/skills/poteto-mode/playbooks/perf-issue.md) measures a baseline. [hillclimb](.agents/skills/poteto-mode/playbooks/hillclimb.md) repeats measured experiments. Runtime and trace forensics separate evidence-backed diagnosis from a speculative fix. |
| Challenge a change before shipping | [interrogate](.agents/skills/interrogate/SKILL.md) brings independent adversarial reviewers. [blast-radius](.agents/skills/blast-radius/SKILL.md) checks what else a small-looking change could affect. The coordinator evaluates findings rather than applying every review comment mechanically. |
| Prove user-visible behavior | [create-verification-skill](.agents/skills/create-verification-skill/SKILL.md) builds a project-specific verification workflow. [maintain-verification-skill](.agents/skills/maintain-verification-skill/SKILL.md) keeps it aligned with the application. [Visual parity](.agents/skills/poteto-mode/playbooks/visual-parity.md) requires comparison of the rendered result. |
| Get a PR ready, then land it deliberately | [Babysit](.agents/skills/poteto-mode/playbooks/babysit.md) handles conflicts, CI, and review feedback. [Shipping](.agents/skills/poteto-mode/playbooks/shipping.md) separately requires independent review of the current change and lands only the verified bottom-up portion of a stack. |
| Run a migration or a longer program | Autonomous-run, orchestrate, both autopilot playbooks, multi-phase planning, safe pause, and session pickup preserve owners, dependencies, progress, and handoffs. [figure-it-out](.agents/skills/figure-it-out/SKILL.md) designs a task-specific playbook when a bundled one does not fit. |
| Learn from work and communicate it clearly | [recall](.agents/skills/recall/SKILL.md) rebuilds context. [reflect](.agents/skills/reflect/SKILL.md) proposes improvements from observed work. [automate-me](.agents/skills/automate-me/SKILL.md) drafts a personal workflow. [show-me-your-work](.agents/skills/show-me-your-work/SKILL.md) records decisions. Writing and comment-review skills keep explanations and code readable. |

The principles make these workflows more than task checklists. They favor modeling the domain before adding logic, deleting unnecessary structure, making operations idempotent, separating shared state, and proving behavior against real artifacts. See the [complete skill and playbook catalog](docs/skill-catalog.md), including the writing, TypeScript, and principle skills.

## How this port plays to Capy's strengths

The goal is not to rebuild a local IDE inside a cloud VM. It is to make pstack's workflow discipline useful on Capy's native execution model. The platform capabilities below come from Capy; the linked local workflows describe how this port uses them. Environment setup, model configuration, and enabled integrations still matter.

### Isolated work, with explicit ownership

[Capy tasks](https://docs.capy.ai/tasks) have separate conversations and can use shared or fresh machines. The port uses shared machines for read-only exploration and fresh machines for writers. Its [task validator](.agents/skills/poteto-mode/scripts/tasks.py) checks declared scopes and dependencies before work starts, then checks reported stack bases with the results.

Independent production changes need disjoint scopes. Dependent changes start from the accepted predecessor branch. Competing arena candidates are alternatives to evaluate, not changes to merge blindly together. Self-contained task briefs and explicit [file transfers](https://docs.capy.ai/machines#moving-files-between-machines) make inputs and evidence part of the handoff instead of assuming another machine has them.

### PR follow-up that does not depend on an open laptop

[Capy threads](https://docs.capy.ai/threads) live on its servers. Its [PR lifecycle](https://docs.capy.ai/pull-requests) delivers CI results, review feedback, and merge events to the owning thread. The port's babysit, shipping, and autonomous-run playbooks use those events instead of treating a detached polling process as the coordinator.

pstack adds the judgment between events: inspect the failure, send fixes to the existing owner, verify the changed head, and obtain an independent shipping verdict. PR ownership follows the latest pushing thread, so a handoff must preserve the intended event owner. Bot feedback depends on the organization's allowlist; not every bot comment wakes a thread.

An event can resume work; it cannot approve a merge. Installing pstack grants no publication, merge, deployment, or recurring-run authority. Archived threads also do not wake automatically.

### Reproducible machines for real verification

Capy's [dev environment](https://docs.capy.ai/environment) gives each fresh task a shared setup recipe, with snapshots to reuse prepared dependencies. [setup-pstack](.agents/skills/setup-pstack/SKILL.md) directs dependency preparation into `initialize` and `update_after_checkout`, and services that must return after sleep into `startup`.

The bundled [control-cli](.agents/skills/control-cli/SKILL.md) and [control-ui](.agents/skills/control-ui/SKILL.md) skills drive the actual application with available terminal, browser, and desktop tools. Capy's [machines](https://docs.capy.ai/machines) support Docker and a browser desktop, making reproducible service dependencies and UI evidence practical when the application runs there.

This is where setup pays off: candidate implementations and reviewers can use the same test recipe. The port does not enable snapshots, provision every application's dependencies, or make an inaccessible application testable just by being installed.

### Reusable skills and durable evidence, without loading every workflow

Capy's [skill discovery](https://docs.capy.ai/skills) exposes names and descriptions, then loads full instructions when relevant. This repository provides full native `SKILL.md` files, not wrappers around an upstream download. Role prompts and references are read when the workflow needs them.

[Volumes](https://docs.capy.ai/volumes) share skills and retained files within their configured scope. The port's recall, reflection, decision-trail, pause, and pickup workflows use available thread history and explicitly saved run records. They distinguish a durable checkpoint from a note left in `/tmp`. Project repositories version team workflows with code; suitable volumes share workflows across projects without copying them into every application.

### Model roles you can tune to the work

Capy supports a model choice per task. [setup-pstack](.agents/skills/setup-pstack/SKILL.md) and the [model validator](.agents/skills/poteto-mode/scripts/models.py) preserve pstack's distinct implementation, investigation, judgment, and review roles while accepting only account-observed choices.

The default policy is **upstream-faithful**. It restores Grok 4.6 for implementation and exploration, Fable 5.1 for difficult judgment and explanation, GPT-5.6 Sol for reflection tooling, and the four-model Fable/Sol/Grok/Opus design/review panels. Comment Sicko retains its unspecified upstream model. Reasoning effort and priority are separate settings, checked against current account observations before launch. Unsupported settings block rather than silently downgrading. A single-model or custom budget/provider choice is explicit and labelled; billing aliases to the same weights do not add diversity. The arena cross-judge is exactly one independent task selected after all accepted candidates finish.

See the [model policy](.agents/skills/poteto-mode/references/model-policy.md), the [upstream preset](.agents/pstack.model-presets.json), and [requirement-to-evidence map](docs/parity-requirements.md). Saved profiles use version 2. Existing version 1 profiles are preserved and must be migrated explicitly; they are not silently converted into a different spending policy.

Use the [complete example profile](.agents/pstack.models.example.json) to tune roles, panels, and concurrency. More agents are not automatically better; use parallelism where the extra coverage or alternative is worth it.

### Event-driven automation with an explicit operating contract

Capy's [automations](https://docs.capy.ai/automations) support schedules and platform events, with fresh or standing threads. The bundled [capy-automation](.agents/skills/capy-automation/SKILL.md) skill defines authorized setup, identity, durable state, and retry handling.

The [Benny pack](.agents/automations/benny/README.md) applies this to issue-report triage and reproduction. Its workflows separate Slack reports, retain deduplication records, require confirmed reproduction before authoring a fix, and constrain replies to the source thread. [make-bot-ui](.agents/skills/make-bot-ui/SKILL.md) describes a server-side relay to a Capy webhook, keeping its secret out of browser code and distinguishing an accepted request from completed work.

These are included workflows, not already running services. No automation is created or enabled by installation.

## What does not carry over from Cursor

These are execution differences, not a claim that every original workflow becomes impossible. Preserve the outcome when Capy has an appropriate tool; report a blocked step when it does not.

| Cursor assumption or expectation | Capy boundary and the port's response |
| --- | --- |
| Install a Cursor plugin, select its sticky mode, or spawn a registered Cursor subagent type | This port does not register Cursor's manifest, mode UI, or subagent types. `poteto-mode` is a discoverable workflow; role prompts are supplied to native tasks. `pstack.json` is distribution metadata, not an executable Capy plugin SDK. |
| Reuse Cursor model IDs and thinking suffixes | They are not portable model configuration. The port inherits the parent or uses a model observed in the current Capy account. It cannot create model access or guarantee the original provider mix. |
| Read local Cursor chats or rely on everything the parent already knows | There is no automatic import of Cursor history. Recall and reflection use accessible Capy history or supplied evidence. A child starts from its brief, so the coordinator must include the necessary context. |
| Treat worktrees or task machines as one shared disk | Fresh machines do not see the parent's uncommitted changes. Transfer required inputs or use an authorized published branch. A JSON work order does not copy files or reserve paths. |
| Keep a shell loop or dev server alive indefinitely | Processes do not survive machine sleep; unpushed checkout data can be lost when its backing is replaced. Use native wake events or authorized automations, restart services through `startup`, and retain checkpoints in volumes or authorized pushes. |
| Drive a developer's Mac, Xcode simulator, attached device, or private local service | The standard execution environment is a cloud Ubuntu VM, not that workstation. Linux-compatible CLI, web, and container workflows fit. Platform-specific reproduction needs an appropriate accessible environment or supplied captures; otherwise the verification step stays blocked. |
| Inherit Cursor's other plugins or connected services | The port bundles native `create-skill`, `deslop`, `control-cli`, `control-ui`, and `capy-automation` workflows. They implement required outcomes, not the original plugins' APIs. Slack, issue trackers, private docs, and observability still require accessible integrations and permission. |
| Use this repository as a standalone task-dispatch SDK | The [public task API](https://docs.capy.ai/api-reference/overview) is read-only. Native agents create and coordinate tasks. The Python helpers validate plans, model profiles, and result records; they do not start or bill agents. |

**The workflow is not a sandbox.** The validators reject structural mistakes, but cannot authenticate a screenshot, inspect every agent action, or enforce a distributed write lock. Native task nesting is limited to three child levels; the workflow must flatten further work. A task reporting `done`, a test passing, and approval to ship are three different things. See [porting details](docs/porting.md) and the [live smoke checklist](docs/live-smoke.md).

## A workflow that uses the combination

For a cross-package change, give Capy an outcome and acceptance criteria rather than asking it to maximize the number of tasks:

```text
Use poteto-mode on the application repository.
Migrate the export API without changing its observable behavior.
First use how to map the callers and architect to compare the API shapes.
Use shared-machine readers for the audit. Split implementation by disjoint
packages on fresh machines; stack changes that depend on a shared contract.
Give each task its base, writable paths, required inputs, and acceptance tests.
Review actual diffs and evidence before accepting results.
Open PRs and address CI and review feedback. Do not merge them.
```

The intended handoff is an investigation, a design decision, scoped implementation results, and reviewable PRs with evidence. Capy supplies isolation and continuation. pstack supplies the decisions and checks at each transition. A timeout is not a reason to launch a duplicate writer, and a passing test is not a substitute for reviewing the diff.

For a smaller task, start smaller:

```text
Use poteto-mode. Reproduce the export retry bug, fix its root cause,
and verify that two retries still produce each row exactly once.
```

## Get started

### Use the repository directly in Capy

Add `ThewindMom/capy-pstack` alongside your application repository in the [Capy project](https://docs.capy.ai/projects). Its `.agents/skills/` directory is the full catalog. Confirm that the skill repository is available on the machines that need it. Across repositories, the first repository in the project's order owns a duplicate skill name.

```text
Use setup-pstack, then poteto-mode.
Work on the application repository, not capy-pstack.
```

No plugin activation command is needed. Setup can check model choices and the dev environment; it does not activate dormant automations.

### Install into an application repository

The installer needs Python 3.10 or later. After obtaining this repository, installation is offline. A ZIP or tar extraction also works without Git metadata.

```bash
git clone https://github.com/ThewindMom/capy-pstack.git
cd capy-pstack
python3 tools/pstack.py doctor
python3 tools/pstack.py install --target /path/to/application --dry-run
python3 tools/pstack.py install --target /path/to/application
python3 tools/pstack.py doctor --target /path/to/application
```

This copies the full skills, roles, automation sources, licenses, model example, and catalog. A small `.capy/rules/pstack-capy.mdc` rule handles explicit pstack requests. Existing `AGENTS.md`, user model profiles, and unrelated skills are preserved. Collisions or changed managed files stop the update. Commit and push the installed files only with authorization so new task machines can receive them.

### Share through a volume

Choose the actual mounted Personal, Organization, Project, or Project + personal volume. **Automation volumes retain state; they do not provide discoverable skills or instructions.**

```bash
python3 tools/pstack.py install --volume --target /actual/skill-volume --dry-run
python3 tools/pstack.py install --volume --target /actual/skill-volume
python3 tools/pstack.py doctor --volume --target /actual/skill-volume
```

The same files live at `skills/`, `roles/`, and `automations/` in that root. Existing volume instructions remain untouched. Keep one intentional version of each skill in the applicable scope.

## A self-contained distribution

All skill bodies, playbooks, role prompts, Benny sources, references, scripts, script tests, and guide illustrations are committed here. There is no upstream loader, `_upstream` checkout, or Git submodule. Deleting Cursor's pstack repository would not remove this copy or prevent installation.

| Find it here | Contents |
| --- | --- |
| [.agents/skills](.agents/skills/) | 52 full skills, with [23 playbooks](.agents/skills/poteto-mode/playbooks/) under poteto-mode |
| [.agents/roles](.agents/roles/) | Poteto and Comment Sicko role prompts |
| [.agents/automations/benny](.agents/automations/benny/) | Dormant setup, triage, reproduction, templates, and references |
| [scripts](.agents/skills/poteto-mode/scripts/) | Task and model validators, PR watcher, orchestration ledger, and audit tools |
| [guide](docs/guide/README.md) | Ten chapters covering setup through verification and longer runs |
| [provenance](provenance/source.json) | Imported revision and the destination of every original source file |

Self-contained does not mean service-free. Agent execution needs Capy, your application needs its dependencies, and optional Bun tools need Bun and their locked registry packages. External documentation links are references, not runtime source downloads.

## Verification and maintenance

The recorded [standalone-distribution CI run](https://github.com/ThewindMom/capy-pstack/actions/runs/35707180929) passed **58 Python tests, 52 Bun tests, and the TypeScript check**. It used a plain checkout without submodules, checked the catalog and local links, and built both installation layouts. Tests also cover archive-only installation without Git or upstream access. [Current CI runs](https://github.com/ThewindMom/capy-pstack/actions) show subsequent results.

**These are packaging, tool, and workflow-contract tests, not a live Capy certification.** At this documentation update, authenticated Capy task launches, wakeups, machine handoffs, model selection, and browser verification have not been exercised by this project's smoke test. Record those results with the [live smoke checklist](docs/live-smoke.md) before claiming live coverage.

Run the checks from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 tools/catalog.py --check
python3 .agents/skills/poteto-mode/scripts/tasks.py prepare examples/plan.json --structure-only
python3 .agents/skills/poteto-mode/scripts/models.py validate \
  .agents/pstack.models.example.json
```

For changes to the optional Bun tools:

```bash
cd .agents/skills/poteto-mode/scripts
bun install --frozen-lockfile
bun test orch watch-pr
bun run typecheck
```

Native events remain the default continuation mechanism. The bundled watcher supports a one-pass snapshot through `bun watch-pr/cli.ts --status-only`. Set `ORCH_STORE` to a selected volume and run directory for retained ledger records; the ledger is not a distributed lock.

Edit the native files directly. After an intentional bundled-file change, review the diff and run `python3 tools/catalog.py` to refresh hashes, then rerun tests. No upstream regeneration is required.

```bash
python3 tools/pstack.py uninstall --target /path/to/application --dry-run
python3 tools/pstack.py uninstall --target /path/to/application
```

Uninstall removes only intact owned files; add `--volume` for that layout. The installer uses a lock, collision preflight, staged replacement, and exception rollback, not a power-loss transaction. Reconcile older adapter installations and locally edited managed files instead of force-overwriting them.

## Sources and license

This README describes the port based on pstack **0.15.2**, not a promise of automatic parity with future upstream versions. Capy documentation was checked on **September 22, 2026**. Platform behavior, available models, and integrations can change; follow the actual account's capabilities.

The linked local skills are the implementation contract. Capy's official references describe the platform: [welcome](https://docs.capy.ai/welcome), [tasks](https://docs.capy.ai/tasks), [machines](https://docs.capy.ai/machines), [threads](https://docs.capy.ai/threads), [PRs](https://docs.capy.ai/pull-requests), [environment](https://docs.capy.ai/environment), [skills](https://docs.capy.ai/skills), [volumes](https://docs.capy.ai/volumes), and [automations](https://docs.capy.ai/automations).

Original pstack: **Lauren Tan and contributors**. Capy port and native additions: **ThewindMom**. Both are MIT; see [LICENSE](LICENSE), [NOTICE](NOTICE), and the [source inventory](provenance/source.json). This is an independent adaptation, not an official Cursor or Capy integration.

## Fidelity checks and control probes

The restored control-cli and control-ui workflows include detailed terminal/browser harness,
page selection, keyboard/resize, tracing, memory and cleanup recipes. Their original Cursor
MIT notices are included, as is the original deslop checklist. create-skill and capy-automation
implement the required authoring/continuation outcomes using Capy's actual discovery and
lifecycle rather than claiming to copy unavailable editor built-ins.

Normal Python tests cover the model resolver, settings/identity checks, task-plan wiring,
real PTY interaction and safe installation. CI additionally runs the optional real Chromium
scenarios (including a broken-then-fixed UI), with Python Playwright 1.57.0. Enable them in
a prepared local browser environment with `PSTACK_BROWSER_TESTS=1`; they are not prerequisites
for normal installation. Browser dependencies are standard registry packages, not upstream
pstack downloads. The probes test their own fixtures, not an authenticated Capy workspace.

Use `models.py resolve` with current `--observed` capabilities before native task starts.
`tasks.py prepare --structure-only` only validates a dependency/scope graph. Omit that flag
and supply `--observed` for role/settings resolution. No JSON checker authenticates a native
task result; the [live checks](docs/live-smoke.md) still require actual Capy evidence.
