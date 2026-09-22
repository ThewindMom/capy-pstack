---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
---

# Interrogate

Spawn one reviewer per configured model to adversarially review code changes. Each model gets the same prompt and rubric. The adversarial signal comes from model diversity, not assigned personas.

The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Determine Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset
- If the user's message references recent work, gather the relevant files

Package the diff (or file contents) plus any surrounding context files the reviewers need to understand the code.

## Step 2, State the Intent

Before spawning reviewers, state the intent explicitly. Derive this from:

- The user's message
- Commit messages
- PR description if one exists
- The code itself

Write one clear paragraph. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Draft independent read-only Capy review tasks with the same exact diff, intent and rubric.
Resolve `interrogate reviewers` through models.py using the active profile and current
account observations. Without an override, use the four upstream-faithful seats. A repeated
same-model panel requires an explicitly approved single-model/custom profile, not fallback.
Choose shared machines for a stable current checkout or fresh machines pinned to the PR
head for an independent checkout. Wait for all final reports; a timeout is still pending.
An unavailable model blocks that seat until an authorized replacement is selected.
Do not silently substitute providers or count the implementer as independent review.

Read `references/reviewer-prompt.md` and fill in the template with:
1. The stated intent
2. The diff or file contents
3. The review rubric from `references/rubric.md`
4. The code-quality lens from `references/code-quality-review.md`

The same filled template goes to all reviewers, so every model applies the code-quality lens.

## Step 4, Synthesize

As results come back, build a unified picture:

1. **Parse all findings** from the reviewers
2. **Identify consensus**. Findings raised by 2+ models independently are highest signal.
3. **Identify lone-model findings**. Still worth reading, but weight accordingly.
4. **Deduplicate**. Different models may describe the same issue differently. Merge these and note which models raised it.
5. **Note disagreements**. If one model flags something and another explicitly says the opposite, that's useful context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator.

Read `references/lead-judgment.md` for the full framework.

Categorize every finding using these buckets:

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. These would block a real PR.
- **Consider**. Legitimate points, but you're not sure they outweigh the cost of addressing them right now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact given the current stage.
- **Dismissed**. Wrong, nitpicky, or missing context. Brief explanation why.

For each finding, include:
- Which model(s) raised it
- The category (act on / consider / noted / dismissed)
- A one-line rationale for the categorization

## Output Format

Present the verdict in this structure:

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On
[Findings that should be addressed. For each: description, which models raised it, why it matters.]

### Consider
[Findings worth thinking about. For each: description, which models raised it, tradeoff involved.]

### Noted
[Valid but low-priority. Brief list.]

### Dismissed
[Rejected findings with brief rationale.]

### Agreement Map
[Where did models agree, where did they diverge, and what does the pattern of agreement/disagreement tell us?]

## Capy task execution

Draft each child with its complete goal, exact repository and base commit, writable
scope, acceptance checks, standing instructions, and the skill/reference paths to read.
Children do not inherit this conversation. Resolve roles/ and skills/ from the observed
bundle root (.agents in a project, or the selected volume root), never the child
working directory. Select a shared machine for a read-only
investigation of this checkout, or a fresh machine for any writer or candidate artifact.
A report returned in the task message is not a filesystem write. Verify the placement
and machine ID returned at start. Use `transfer_files` for inputs and reports crossing
machines; a path on another machine is not an accessible input.

Read the selected role from `pstack.models.json` at the bundle root, with the project
profile overriding matching fields. Absent configuration uses `upstream-faithful` from
`pstack.model-presets.json`. Follow `skills/poteto-mode/references/model-policy.md` at
that root and run its models.py resolver with current account observations before launch.
Preserve the role-specific model, reasoning effort, priority and panel count. Unsupported
settings block the affected seat; never silently inherit or substitute. Same-model/custom
profiles require an explicit user-approved difference. Four faithful seats are four models
across three families. Inspect returned native settings, not only the requested prompt.

Use the native task tools available in this session, not a shell that starts another
agent. Drafts are not running, working/waiting tasks remain live, and idle/stopped is
not completion. Accept a final report only after `done` plus evidence inspection.
Send follow-up fixes to the existing owner. Do not replace a timed-out owner until
its stop or terminal failure and its filesystem/branch have been reconciled.
Independent writers need disjoint paths. A dependent writer starts at its predecessor's
actual accepted branch/head, not just later from main. At three child levels, execute
the next step in the current owner rather than spawning a fourth level.
