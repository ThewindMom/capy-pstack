### Opening a PR

Invoked at the end of other playbooks only when the user authorized publication. Local-only work ends with verified files and a report, not a PR gate.

**Machine and branch.** Select placement per poteto-mode's Capy task execution contract. Writers use isolated device worktrees on device threads or fresh cloud machines on cloud threads. Explicitly coordinated disjoint shared writers keep one git writer. Transfer required uncommitted inputs explicitly. Preserve unrelated work; never reset or clean another owner's checkout.

**Commits.** Commit, amend, rebase and push only within actual user authorization. Keep commits small, ordered and independently landable. Amend only when authorized and the fix belongs in the just-made commit. Use a new commit when separable. Commit bodies don't restate the subject. Never rewrite a shared branch or publish local-only work because this playbook was read.

**PRs.** Run `/deslop` bundled with this port over the diff before commit and `/no-comments` before review. Write every PR title, description, and commit body with `/technical-writing` (every layer except Diátaxis, and apply the STE vocabulary rules: one word per action, keep articles, a plain verb over `-ing` where one works), then apply `/unslop`.

**Titles.** Conventional Commits `type(scope): subject`, no trailing period. Type such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, or `perf`. Scope is the area, such as `pstack` or `poteto-mode`. Subject is short, imperative, and names a real symbol when one carries the change, for example `fix(pstack): retarget opening-a-pr babysit trigger`.

**Descriptions.** The PR body is a one-minute briefing, not a lab notebook, for a reviewer who has the diff. It says why the change exists, what it leaves out, what it could break, and how you proved it works. Write short, simple sentences with few identifiers, no walls of text. The body becomes the squash commit body, so keep that commit under about 40 lines. Use `##` headings, not bold lead-ins, in this order, and drop a section with nothing to say:

- `## Why`: the problem and approach, one to three short sentences. No SHAs, rebase genealogy, or "based on main" preamble.
- `## What changed`: one to three short bullets. Name a real symbol or path only when it carries the change. Name both sides of a rename or retarget.
- `## Scope`: always. One to three short items on what it covers and what it deliberately leaves out (a follow-up, a known gap). No symbols, paths, or file-by-file essay.
- `## Tradeoffs`: only rejected alternatives a reviewer would otherwise ask about. Skip when there was no real choice.
- `## Blast Radius`: one or two sentences on who or what it touches and why that is safe or risky. If main is red, state the cost of leaving it red.
- `## Verification`: one to three bullets, each a real run path and its outcome. Perf: one primary number with its unit, `before → after`, and a link to the arena or swarm directory for the rest. No sample-size methodology, swarm recitals, or metric tables.

After the sections, attach videos or screenshots when they prove a claim. Full SHAs, swarm or arena lane recitals, lever-correction essays, file-by-file checklists, and "CLEAN" verdicts go in a linked artifact, not the body.

**Publishing.** Use native `pr_create`, which records the PR and commits and pushes the selected changes. Inspect the staged scope before calling it. Verify the returned branch, base, head and URL. Never use `gh pr create` or `origin pr create` instead. Use a CLI only for an authorized operation native tools cannot express. Covered CI and human feedback callbacks reach the owning run. A PR opened elsewhere needs an explicit native subscription before relying on events. Bot comments do not auto-wake this session; read them explicitly when relevant.

**Built-in PR tool.** Create, edit and retarget through the native PR tools. Follow their actual supported operations rather than inventing readiness or subscription calls. For dependent multi-PR work, read the installed gh-stack skill and use its native stack submission workflow when available. Use `pr_create` with an explicit parent base for a single follow-up on an open PR or when gh-stack is absent. The root targets trunk; each child starts at its parent's accepted exact tip. Branch from trunk only for independent work. Prefer narrow independently reviewable PRs.

**Readiness.** Honor the user's requested readiness. For authorized ready publication, set `draft: false` on native `pr_create` and inspect the result. Preserve an explicit draft request. Read actual PR metadata before reporting status.

**Babysit.** Opening a PR does not authorize a babysit program. Follow the actual repository review policy. When a creation or push owes a callback to the owning run, end that turn and resume on the callback. Inspect findings independently. Run the separate babysit playbook when requested. Push back when feedback drifts from intent.

A subagent that opens a PR runs `interrogate`, `/deslop`, and `/no-comments`, and posts the URL. It returns to the parent without babysitting, unless it is an Autopilot-full or Autopilot-stack owner. That owner's brief assigns the babysit loop and is the ask `playbooks/babysit.md` waits for. The owner starts the loop after its code-ready report, reports merge-ready or STACK-READY per its playbook, and is exempt from the rules here and in `playbooks/babysit.md` that hold babysitting until a whole stack is built.
