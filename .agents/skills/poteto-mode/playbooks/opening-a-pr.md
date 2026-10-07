### Opening a PR

Invoked at the end of other playbooks only when the user authorized publication. Local-only work ends with verified files and a report, not a PR gate.

**Machine and branch.** Select placement per poteto-mode's Capy task execution contract. Writers use isolated device worktrees on device threads or fresh cloud machines on cloud threads. Explicitly coordinated disjoint shared writers keep one git writer. Transfer required uncommitted inputs explicitly. Preserve unrelated work; never reset or clean another owner's checkout.

**Commits.** Commit, amend, rebase and push only within actual user authorization. Keep commits small, ordered and independently landable. Amend only when authorized and the fix belongs in the just-made commit. Use a new commit when separable. Never rewrite a shared branch or publish local-only work because this playbook was read.

**PRs.** Run `/deslop` bundled with this port over the diff before commit. Run `/no-comments` before review. Write every PR title, PR description, and commit body with `/technical-writing`, then apply `/unslop`. Apply every technical-writing layer except Diátaxis. Use one word for each action, keep articles, and avoid `-ing` when a plain verb works.

**Titles.** Use Conventional Commits in the form `type(scope): subject`. Use `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf` as the type. Use the changed area, such as `pstack` or `poteto-mode`, as the scope. Keep the subject short and imperative. Name a real symbol when one carries the change. For example, `fix(pstack): retarget opening-a-pr babysit trigger`. Do not add a trailing period.

**Descriptions.** The PR body is a briefing, not the lab notebook. A reviewer who has the diff should learn why the change exists, what it leaves out, what it could break, and how you proved it works, in under a minute. Write short, simple sentences with few identifiers. Do not write walls of text. The squash commit body is the PR body. If the body would make the squash commit longer than about 40 lines, cut the body.

Put each section under a `##` heading, not a bold lead-in, so the sections stand apart. Use these sections in order. Drop a section when it has nothing to say.

- `## Why` gives the problem and the approach in one to three short sentences. Do not list SHAs or rebase genealogy. Do not add a "based on main" preamble.
- `## What changed` has one to three short bullets. Name a real symbol or path only when it carries the change. Name both sides of a rename or retarget.
- `## Scope` always names what the PR covers and what it deliberately leaves out, for example a related follow-up or a known gap. Use one to three short items. Do not list symbols or paths, and do not write a file-by-file essay.
- `## Tradeoffs` names only rejected alternatives that a reviewer would otherwise ask about. Skip this section when there was no real choice.
- `## Blast Radius` gives one or two sentences on who or what the change touches and why that is safe or risky. If main is red, state the cost of leaving it red.
- `## Verification` has one to three bullets. Each bullet names a real run path and its outcome. For a performance change, report one primary number with its unit in `before → after` form. Link the arena or swarm directory for the remaining evidence. Do not include sample-size methodology, swarm recitals, or metric tables.

After these sections, attach videos or screenshots when they prove a claim. Do not paste full SHAs, swarm or arena lane recitals, lever-correction essays, file-by-file checklists, or "CLEAN" verdicts. Put these details in a linked artifact. A commit body does not restate its subject.

**Publishing.** Use native `pr_create`, which records the PR and commits and pushes the selected changes. Inspect the staged scope before calling it. Verify the returned branch, base, head and URL. Never use `gh pr create` or `origin pr create` instead. Use a CLI only for an authorized operation native tools cannot express. Covered CI and human feedback callbacks reach the owning run. A PR opened elsewhere needs an explicit native subscription before relying on events. Bot comments do not auto-wake this session; read them explicitly when relevant.

**Built-in PR tool.** Create, edit and retarget through the native PR tools. Follow their actual supported operations rather than inventing readiness or subscription calls. For dependent multi-PR work, read the installed gh-stack skill and use its native stack submission workflow when available. Use `pr_create` with an explicit parent base for a single follow-up on an open PR or when gh-stack is absent. The root targets trunk; each child starts at its parent's accepted exact tip. Branch from trunk only for independent work. Prefer narrow independently reviewable PRs.

**Readiness.** Honor the user's requested readiness. For authorized ready publication, set `draft: false` on native `pr_create` and inspect the result. Preserve an explicit draft request. Read actual PR metadata before reporting status.

**Babysit.** Opening a PR does not authorize a babysit program. Follow the actual repository review policy. When a creation or push owes a callback to the owning run, end that turn and resume on the callback. Inspect findings independently. Run the separate babysit playbook when requested. Push back when feedback drifts from intent.

A subagent that opens a PR runs `interrogate`, `/deslop`, and `/no-comments`, and posts the URL. Then it returns to the parent without babysitting, unless it is an Autopilot-full or Autopilot-stack owner. That owner's brief assigns the babysit loop and is the ask `playbooks/babysit.md` waits for. The owner starts the loop after its code-ready report and reports merge-ready or STACK-READY as its playbook says. The rules here and in `playbooks/babysit.md` that hold babysitting until a whole stack is built do not apply to that owner.
