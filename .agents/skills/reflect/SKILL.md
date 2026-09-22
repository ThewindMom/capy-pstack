---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

Read the active Capy thread and its relevant task messages using the native readers.
Keep their real thread/task IDs, message order and referenced artifact locations. Export
only authorized relevant messages to a per-run file when reviewers need a file, and use
transfer_files across machines. There is no assumed editor transcript directory. If the
full history is unavailable, label the gap and supply a clearly marked session digest.

### 2. Spawn three reviewers in parallel

Draft three read-only native tasks on shared machines for the three lenses below.
Include the scoped transcript or digest and each full template. Read-only scope is an
instruction not a claim that it removes MCP access; use only authorized read tools.

| Lens | `model` | Prompt template |
|---|---|---|
| Judgment | your configured reflect-judgment model (default from the upstream-faithful role preset) | `references/judgment-reviewer.md` |
| Tooling | your configured reflect-tooling model (default from the upstream-faithful role preset) | `references/tooling-reviewer.md` |
| Divergent | your configured reflect-divergent model (default from the upstream-faithful role preset) | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the native task final report.

### 3. Synthesize

Draft one independent native synthesis task using the configured reflect synthesizer model or parent inheritance. Allow authorized read-only citation checks. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

File Backlog items only when tracker writes are authorized; otherwise report them as proposals. Only the Accepted list waits for approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the bundled `create-skill` skill and run its draft / test / iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `create-skill` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `create-skill`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.

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
