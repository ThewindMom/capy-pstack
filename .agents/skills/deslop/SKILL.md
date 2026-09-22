---
name: deslop
description: Remove unnecessary code and prose from a scoped diff before commit.
---

# Deslop

Read the full scoped diff and nearby code. Identify dead code, speculative compatibility,
redundant wrappers, needless guards, narration, unsafe casts, and unrelated edits. Trace
behavior before deleting it. Preserve public contracts, legal headers, real boundary
validation, and regression coverage. Use no-comments for comment review; do not confuse
it with an independent correctness review. Remove only demonstrated redundancy, run the
real targeted tests plus the relevant broader checks, and report what changed. Do not
sneak a behavior change into a cleanup or weaken a test to get green.
