---
name: no-comments
description: "Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints."
---

# No comments

Spawn Comment Sicko. Act on accepted findings.

Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Draft a native Capy task with the complete `roles/comment-sicko.md` prompt from this bundle and the exact scoped diff. Use a fresh machine for comment deletions; for report-only review use a shared machine. It never owns application-code changes.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, run `/how` or `/why` on their symbol. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail `/no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `/architect` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.

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

Read the selected role from `pstack.models.json` at the bundle root, then apply an
explicit project `.agents/pstack.models.json` override. Absent configuration means
`inherit-parent`: omit the native model override. Recheck configured IDs against the
current account. Four-seat design/review panels retain four independent seats by
default; report same-model seats honestly rather than claiming model diversity.

Use the native task tools available in this session, not a shell that starts another
agent. Drafts are not running, working/waiting tasks remain live, and idle/stopped is
not completion. Accept a final report only after `done` plus evidence inspection.
Send follow-up fixes to the existing owner. Do not replace a timed-out owner until
its stop or terminal failure and its filesystem/branch have been reconciled.
Independent writers need disjoint paths. A dependent writer starts at its predecessor's
actual accepted branch/head, not just later from main. At three child levels, execute
the next step in the current owner rather than spawning a fourth level.
