# capy-pstack

**The complete pstack workflow suite, ported to Capy and committed in this repository.**
This is not a loader for Cursor's plugin. A normal clone contains the full skills,
playbooks, principles, role prompts, scripts, reference material, guide and Benny pack.
There are no Git submodules and installation never contacts an upstream repository.
Deleting the original pstack repository does not remove this port's source or workflows.

Based on Lauren Tan's MIT-licensed pstack 0.15.2. The source inventory and revision are
recorded in [provenance/source.json](provenance/source.json). The original MIT license
is retained. This is an independent Capy adaptation, not an official integration.

## What is in the repository

| Component | Actual committed files |
| --- | --- |
| 47 ported pstack skills and 5 native support skills | [.agents/skills](.agents/skills/) |
| 23 complete engineering playbooks | [poteto-mode/playbooks](.agents/skills/poteto-mode/playbooks/) |
| 23 engineering principles | [Skill catalog](docs/skill-catalog.md) |
| Poteto and Comment Sicko role prompts | [.agents/roles](.agents/roles/) |
| Full dormant Benny automation pack | [.agents/automations/benny](.agents/automations/benny/) |
| PR watcher, orchestration ledger, validators and audit scripts | [scripts](.agents/skills/poteto-mode/scripts/) |
| Ten-chapter guide and original illustrations | [Guide](docs/guide/README.md) |
| Safe offline installer and integrity checks | [tools](tools/) |

Open [poteto-mode/SKILL.md](.agents/skills/poteto-mode/SKILL.md) or
[how/SKILL.md](.agents/skills/how/SKILL.md): each contains its real workflow, not an
instruction to load a preserved Cursor file elsewhere. Edit these native files directly.
The [porting record](docs/porting.md) explains semantic changes and remaining limits.

## Use directly in Capy

Add `ThewindMom/capy-pstack` as a repository in the Capy project alongside the application
repository. Capy discovers the complete `.agents/skills/<name>/SKILL.md` catalog from
this checkout. A fresh task must have this repository selected or the installed skill
volume attached. In multi-repository projects, check repository order when skill names
conflict. There is no plugin activation command or special mode registration.

```text
Use setup-pstack, then poteto-mode.
Work on the application repository, not capy-pstack.
Reproduce the bug, fix its cause, and verify the real user-visible result.
Use native Capy tasks for independent work.
```

## Copy into one project, completely offline

Only Python 3.10+ is needed. A ZIP/tar extraction works too; Git metadata is not required.

```bash
git clone https://github.com/ThewindMom/capy-pstack.git
cd capy-pstack
python3 tools/pstack.py doctor
python3 tools/pstack.py install --target /path/to/application --dry-run
python3 tools/pstack.py install --target /path/to/application
python3 tools/pstack.py doctor --target /path/to/application
```

The installer copies full `.agents/skills`, `.agents/roles`, `.agents/automations`,
licenses, model example and catalog. It never downloads or generates the skill bodies.
It also adds a small `.capy/rules/pstack-capy.mdc` rule for explicit pstack requests.
It does not overwrite `AGENTS.md`, user model settings or unrelated skills. A collision
or locally changed managed file stops the update before any managed write. Commit the
installed project files when authorized so fresh machines receive them.

## Share through a Capy volume

Choose the actual mounted Personal, Organization, Project or Project + personal volume.
**Automation volumes hold state, not discoverable instructions/skills.**

```bash
python3 tools/pstack.py install --volume --target /actual/skill-volume --dry-run
python3 tools/pstack.py install --volume --target /actual/skill-volume
python3 tools/pstack.py doctor --volume --target /actual/skill-volume
```

The same complete files install at `skills/`, `roles/` and `automations/` in that root.
Relative skill references work in both layouts. Volume instructions and personal files
remain untouched. Use only one intentional copy of a same-named skill in a given scope.

## Native Capy behavior

Read-only investigations share the current machine; writers and candidate artifacts use
fresh machines at explicit bases. Task prompts carry their own context. `transfer_files`
moves required inputs/evidence, and dependent writers inherit the accepted branch/head.
Task completion and PR/CI/review events wake the owner. Periodic programs use explicitly
authorized Capy automations and durable volume records, never detached VM sleepers.

Models inherit the parent by default. The complete per-role example is
[.agents/pstack.models.example.json](.agents/pstack.models.example.json). Configure only
IDs observed in the actual account. Panel arrays preserve four seats by default; repeated
inherited seats are not misrepresented as multi-model diversity. No provider IDs or
reasoning suffixes are guessed. The native support skills `create-skill`, `deslop`,
`control-cli`, `control-ui` and `capy-automation` replace editor-only dependencies.

Benny's complete triage and reproduction workflows are included but remain dormant.
Its setup normalizes Slack bursts into independent root reports and uses trusted triage
marker events for reproduction, with durable deduplication and thread-only posting.
Creating or enabling an automation is a separate authorized action.

## Tools and development

```bash
python3 -m unittest discover -s tests -v
python3 tools/catalog.py --check
python3 .agents/skills/poteto-mode/scripts/tasks.py prepare examples/plan.json
python3 .agents/skills/poteto-mode/scripts/models.py validate \
  .agents/pstack.models.example.json
```

Optional Bun tools keep the complete original implementation and tests, adapted where
platform behavior differs. They depend on Bun and the locked registry packages, **not**
on Cursor's repository:

```bash
cd .agents/skills/poteto-mode/scripts
bun install --frozen-lockfile
bun test orch watch-pr
bun run typecheck
```

Native Capy events are the default wake path. Use `bun watch-pr/cli.ts --status-only`
for a one-pass GitHub snapshot. The ledger is local bookkeeping; set `ORCH_STORE` to an
explicit selected volume/run directory. It is not a distributed ownership lock.

After editing bundled files, inspect the diff and run `python3 tools/catalog.py` to
refresh hashes, then tests. The [catalog](docs/skill-catalog.md) links every full skill.
The installer uses a lock, collision preflight, staged replacement and exception rollback;
it is not a power-loss transaction or a defense against another malicious same-user process.

```bash
python3 tools/pstack.py uninstall --target /path/to/application --dry-run
python3 tools/pstack.py uninstall --target /path/to/application
```

Uninstall removes only intact owned files. Add `--volume` for a volume installation.
Older adapter installations use a different ownership manifest; reconcile those files
rather than force-overwriting them. No installer removes unrelated work.

## Verification boundary

CI checks the full direct-file catalog, local links, forbidden editor runtime mechanics,
all source-file destinations, task/model validation, safe installation and offline
source-free packaging. It also runs the bundled Bun tests and typecheck. These are not
claims that an authenticated Capy session has executed every workflow. Follow the
[live smoke checklist](docs/live-smoke.md) to record actual task/machine IDs, wakeups,
model choices, browser proof and volume behavior. Missing platform capabilities remain
explicitly blocked. Instruction text and structural validators are not a sandbox.

## References and license

Capy contracts checked on 2026-09-22: [skills](https://docs.capy.ai/skills),
[tasks](https://docs.capy.ai/tasks), [machines](https://docs.capy.ai/machines),
[volumes](https://docs.capy.ai/volumes), [instructions](https://docs.capy.ai/instructions),
[environment](https://docs.capy.ai/environment), [pull requests](https://docs.capy.ai/pull-requests),
and [automations](https://docs.capy.ai/automations). These links are documentation,
not runtime dependencies. Original work: Lauren Tan and contributors. Native additions:
ThewindMom. Both are MIT; see [LICENSE](LICENSE) and [NOTICE](NOTICE).
