---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and queries each evidence category (source control, issue tracker, long-form docs, real-time chat, infrastructure observability, error tracking, product analytics warehouse) in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
---

# Why

Investigate the motivation and intent behind code. The companion `how` skill answers what the code does and how it works. `why` answers what forces led to its shape.

Resolve every role through the installed model policy. A rejected native route is blocked, not permission to substitute a default or another model from the same family.

Every investigator and the synthesizer is a native Capy task with the complete role brief. Read-only scope is an instruction to not write to evidence sources. It is not a claim that a scope flag removes MCP access. Use only authorized connected reads.

## Operating Posture

Operate as a **careful, cautious, and precise investigator**. Be honest about what you know vs what you're inferring. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the Target and the Question

The **target** is usually a chunk of code, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, or a broad history sweep.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from conversation context (open files, recent edits, the referenced file and line, what was just discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the Code Anchor

Before spawning investigators, build the seed context inline: file paths and line ranges, key symbols (functions, classes, constants), the last few commits touching the target, PR numbers from merge commits (pattern `(#1234)` in the subject line), and any linked ticket IDs. Run `git blame -L <start>,<end> <file>` for last-touch commits, `git log --follow -p -- <file>` for full history with patches through renames, `git log --oneline -20 -- <file>` for recent commits with PR numbers visible, and `git log -1 --format=%B <commit>` to extract PR numbers. Then pull the PR bodies and discussion for any substantive commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`. This anchor goes to every investigator and to the synthesizer.

## Step 3. Spawn Parallel Investigators

**Default to the full parallel investigation.** The goal is a complete coverage map, not a minimal one. Document the null, don't skip the search.

### Discovery

Inspect the actual integrations and MCP tools exposed to this Capy session. Map only authorized readable sources. No local editor configuration directory is assumed. A missing source is an explicit coverage gap.

Map each available MCP to one evidence category:

1. Source control history
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Infrastructure observability
6. Error / exception tracking
7. Product analytics warehouse

Source control is always available through git and `gh`. For the other six, classify using the MCP name, server instructions, tool names, and resource descriptors. If an MCP could fit more than one category, choose the one matching its primary evidence. Record ambiguous cases in the coverage map.

Spawn one investigator per category that has a matching MCP, all in a single message so they run concurrently, each owning exactly one tool or MCP. Don't ask one agent to cover multiple MCPs. `model`: your configured why-investigators model, resolved through the model policy. Place each investigator read-only on a shared machine.

Each investigator's prompt is `references/investigator-prompt.md` filled in, plus:

- the category playbook `references/sources/<source>.md` for the selected MCP, adapted from the examples in `references/source-playbook.md`
- `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, retry logic, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
- the code anchor and the user's original question

### Investigator roster, one per available evidence category

Each category below is uniquely positioned to surface one shape of "why", shown after "Best at". Use it to know what to expect back, to name a gap when a category returns empty, and, only in the rare provably-irrelevant case, to justify a skip.

1. **Source control** (git history, `gh` for PRs, code comments, tests). Always spawn, the only guaranteed source. Best at *implementation-time rationale captured during review*.
2. **Issue / ticket tracker** (e.g. Linear, Jira, GitHub Issues, Plane, Shortcut MCP). Best at *the product or business forcing function*. Strongest when the why is external to engineering.
3. **Long-form documents** (e.g. Notion, Confluence, Google Docs, Coda MCP). Best at *long-form design rationale*, written out before it becomes code.
4. **Real-time team chat** (e.g. Slack, Discord, Microsoft Teams, Mattermost MCP). Best at *real-time deliberation that never reached a doc*. Especially important when the source control, ticket, and doc paper trail is thin.
5. **Infrastructure observability** (e.g. Datadog, New Relic, Honeycomb, Grafana, Splunk MCP). Best at *infrastructure and runtime reality that motivated the code*. Strongest when the target reacts to an infra signal (timeouts, retries, rate limits, circuit breakers).
6. **Error / exception tracking** (e.g. Sentry, Rollbar, Bugsnag, Airbrake MCP). Best at *the specific exceptions and error trajectories that motivated defensive or corrective code*. Strongest for catch blocks, null guards, type checks, retries, and other defenses.
7. **Product analytics warehouse** (e.g. Databricks, Snowflake, BigQuery, ClickHouse, dbt, Redshift MCP). Best at *product and data reality that shaped the code*. Strongest for flag-gated code, experiment-driven ships, data migrations, and "where did this number come from" questions.

### When to skip an investigator

Only with an **explicit, written justification** that goes in the final Sources Consulted. Two valid reasons:

- **No MCP is available for that category** in this environment. Flag it as a gap, not a choice: "Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable."
- **The source is provably irrelevant**, not just "probably irrelevant." A high bar: "Error / exception tracking skipped. Target is a build-time script with no runtime code path."

If your scope assessment suggests a single-commit trivial target where the PR description already contains the complete answer, you may answer inline **only after** confirming all seven available category searches would be redundant. Say so explicitly. This should be rare.

## Step 4. Synthesize

Spawn one synthesizer. `model`: your configured why-synthesizer model, resolved through the model policy. Read-only native synthesis scope on a shared machine, with authorized connected reads to spot-check citations. Do not write to source systems. It gets:

1. The investigator findings, including any null results and any categories skipped with justification
2. The code anchor
3. The user's original question
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Present the synthesizer's output to the user. You may lightly edit for clarity or add context from the conversation, but **do not rewrite the confidence language**.

## Output Format

The structure is the one in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt as needed, but keep the confidence separation intact, and keep Sources Consulted as one line per investigator, including the ones that returned nothing or were skipped, with the reason.

After Sources Consulted, if the user's `why` question is a precursor to changing this code, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set for planning the change.

## Common Failure Modes to Avoid

- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.

## Capy task execution

Before dispatch, size reasoning and speed through the [poteto-mode subagent policy](../poteto-mode/SKILL.md#capy-task-execution). Preserve explicit user settings and resolve against current account observations.

Draft each child with its complete goal, exact repository and accepted base, writable
scope, acceptance checks, standing instructions, and full skill/reference paths.
Children do not inherit this conversation. Resolve roles/ and skills/ from the observed
bundle root (.agents in a project, or the selected volume root), not the child directory.
Read-only investigations use `machine: "shared"`. Writers use `machine: "device"` for an
isolated sibling worktree on a device-attached thread, or `machine: "fresh"` for an isolated
cloud machine on a cloud thread. A new agent does not imply a cloud machine. Use coordinated
disjoint shared writing only when explicitly assigned, with one git writer and no concurrent
commits. Verify returned placement and machine ID. Transfer uncommitted inputs and reports
with `transfer_files` when machines differ; a remote path is not an accessible input.

Resolve every role, reasoning budget, alias and panel through
`skills/poteto-mode/references/model-policy.md` at the observed bundle root. Run its
models.py resolver with current account observations before launch, and inspect returned
native settings. The policy owns defaults and unsupported-setting handling. Never silently
substitute models, infer diversity from aliases, or overwrite an existing user profile.

Use native task tools, not a shell that starts agents. Drafts are not running;
working/waiting owners remain live, and idle/stopped is not completion. Accept a final
report only with terminal completion and inspected evidence. Independent new rounds use
fresh agent context with consolidated scope: the original brief, every later directive,
the accepted report, exact head, and transferred inputs. Keep an existing live owner when
callbacks, its local checkout, uncommitted work, or running processes require it. Before a
completed role passes to a new agent, reconcile the filesystem, branch, processes and PR
callback ownership. A timeout never permits a second writer. Stop or reconcile terminal
failure before replacement. A dependent writer starts at its predecessor's accepted head,
not merely later from main. At three child levels, execute rather than spawn a fourth.

Implementation and playbook helpers read the complete poteto-mode skill and
`roles/poteto-agent.md`. Investigation, reflection and adversarial review use their own
full templates. Tier code work by difficulty through the configured policy, including
`hardest tasks` and `judgment and prose`. The parent inspects each diff and writes its own
synthesis. A second opinion uses the same brief against a different resolved model.
