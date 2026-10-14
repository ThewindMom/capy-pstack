---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge changes from independent angles."
---

# Interrogate

Spawn one reviewer per configured model to adversarially review code changes. The adversarial signal comes from model diversity, not assigned personas. The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files or a diff, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the code. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Draft independent read-only Capy review tasks with the same exact diff, intent and rubric.
Resolve `interrogate reviewers` through models.py using the active profile and current
account observations. Use the configured panel from the model policy, whose default has two independent model families. A repeated
same-model panel requires an explicitly approved single-model/custom profile, not fallback.
Choose shared machines for a stable current checkout or isolated device worktrees on device threads and fresh cloud machines on cloud threads, pinned to the PR
head for an independent checkout. Wait for all final reports; a timeout is still pending.
An unavailable model blocks that seat until an authorized replacement is selected.
Do not silently substitute providers or count the implementer as independent review.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the stated intent, the diff or file contents, the rubric from `references/rubric.md`, and the code-quality lens from `references/code-quality-review.md`.

## Step 4, Synthesize

As results come back, build a unified picture. Parse every reviewer's findings. Merge findings that describe the same issue differently, and note which models raised each one. Findings two or more models raised independently are the highest signal. Read a lone model's finding, but weight it accordingly. Note disagreements. If one model flags something and another explicitly says the opposite, that is context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Put every finding in one of four buckets, with the model(s) that raised it and a one-line rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. They would block a real PR.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On
[Each: description, which models raised it, why it matters.]

### Consider
[Each: description, which models raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where models agreed and diverged, and what that pattern tells us.]

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