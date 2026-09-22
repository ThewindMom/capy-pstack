---
name: deslop
description: Remove AI-generated code slop and clean up the scoped branch diff without broad rewrites or unrelated behavior changes.
---

# Remove AI code slop

Adapted from Cursor's MIT-licensed deslop. Check the diff against main (or the actual PR
base) and remove AI-generated slop introduced in the branch. Include scoped working-tree
changes when they are the requested deliverable. Read the surrounding code before deletion.

## Focus areas

- Extra comments that are unnecessary or inconsistent with local style.
- Defensive checks or try/catch blocks abnormal for trusted code paths.
- Casts to `any` used only to bypass type issues.
- Deeply nested code that should use early returns.
- Other patterns inconsistent with the file and surrounding codebase.

Keep behavior unchanged unless fixing a clear bug. A clear bug fix still needs reproduction
and the bug-fix workflow; do not smuggle it into cleanup. Prefer minimal focused edits over
broad rewrites. Keep the final summary concise, one to three sentences.

## Capy execution

Inspect the actual checkout and base/head on the implementation owner's machine. Give
follow-up edits to that owner; do not write concurrently from a second shared task.
Preserve public contracts, legal headers, boundary validation, intended constraints and
regression coverage. Use no-comments for its independent comment review, not as a substitute
for whole-change correctness review. Remove demonstrated redundancy, rerun relevant tests,
and keep accepted evidence before machine cleanup. Do not weaken a test to get green.
See `LICENSE` for the retained upstream notice.
