### Worktree and machine cleanup

**Own the disk and the safety gate.** Capy machines are disposable execution environments;
that does not make unpushed user work disposable.

1. Snapshot `df -h /` on the machine being inspected. Run `scripts/worktree-audit.sh`
   from this skill's directory. It reports real Git worktrees read-only and never deletes.
   List native tasks/machines separately and map their IDs to branches and artifact paths.
2. Treat every audit row as a candidate, not permission. A working/waiting task, held
   scope, retained user thread, unpushed commit or untracked evidence blocks cleanup.
   Inspect actual native state; a shell cannot infer it from a transcript directory.
3. For uncertain candidates, assign read-only investigations on the relevant machine.
   Preserve needed diffs and artifacts with transfer_files and the selected durable
   volume, and verify the destination. Do not delete any other machine through local paths.
4. Show WIP and untracked files before destructive cleanup. Obtain the necessary
   authorization for the exact confirmed paths. Never assume untracked means throwaway.
5. Remove only the confirmed clean unused worktrees through `git worktree remove` without
   force; an unexpected refusal requires inspection, not `rm -rf`. Prune stale metadata
   only after verifying the candidate set. Keep branch refs holding unrecovered work.
6. Inspect project-owned caches/processes or Docker resources on this Ubuntu machine
   when further space is needed. Delete only approved unused resources. Do not run local
   macOS simulator or editor-state cleanup in Capy, and do not delete machine identities
   merely to reclaim disk. Use native lifecycle controls only when requested.

**Reply:** before/after disk use, exactly what was removed, evidence retained, and each
held item with its task/branch or uncommitted-work reason.
