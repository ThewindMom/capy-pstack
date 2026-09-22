### Pause safely

**Leave a checkpoint a cold-start Capy task can resume.** This playbook is explicit
only. "Going to bed, keep going" is not a pause request.

1. Stop at an atomic boundary. Start no new work. Send targeted stop/hold messages to
   owned children and confirm none remain writing before releasing their scopes.
2. Take no new irreversible action just to pause. Preserve existing push/PR authorization;
   no force-push, merge or new publication is implied. Disable this run's owned periodic
   automation when a stop requires it; leave unrelated jobs intact.
3. Make a scoped WIP commit when authorized and report a broken tree honestly. A local
   commit is not durable against VM replacement: push only with authorization, or save
   a patch plus required untracked files to the selected persistent volume. Verify the
   saved artifacts. Never put credentials or unrelated project data into a public branch.
4. Save intent, actual repository/base/head, task/machine IDs, scope owners, verification,
   blockers, next steps, key paths and gotchas to the selected run record. Point to an
   existing decision trail rather than duplicating it. A /tmp note alone is not durability.

**Reply:** loop position, held/stopped tasks, saved artifact locations and commit IDs,
what is still ephemeral, whether the tree is clean, and the first resume action.
