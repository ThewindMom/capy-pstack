# Maintain the upstream adaptation

Use this reference for an explicitly authorized pstack maintenance run. Installing the
bundle does not authorize a schedule or a source update.

The installed `upstream-source.json` is the accepted source inventory, not an assertion
that native workflows are byte-identical to Cursor. `../scripts/upstream-audit.py`
compares a local source snapshot against that inventory without executing source code
or writing either input. It detects content changes even when the version is unchanged.
Its JSON includes added, modified, and removed paths. An unknown destination requires
an explicit mapping before acceptance.

1. Resolve the installed bundle from the current session. Read its inventory and managed
   installation hashes before consulting a remote capy-pstack checkout. Remote main can
   be older than the installed bundle.
2. Fetch upstream into scratch. Record the exact commit and subtree. Verify the snapshot
   against Git, then run the audit against the installed inventory.
3. Review each changed path. Record a native destination and a disposition: ported,
   existing native equivalent, or platform-only. Never replace Capy task or callback
   mechanics with Cursor APIs. Keep permissions and evidence gates.
4. Stage changes outside Drive. Preserve the Personal Drive model policy, budgets,
   explicit overrides, scope instructions, and unrelated skills. Use current native
   account observations with `models.py` before dispatching any role.
5. Run the source repository's required tests, frontmatter and link checks, relevant
   helper tests, and safe installation checks. Migrate release-specific expected values
   only when the release intentionally changes them. Keep behavioral assertions.
6. Preserve previous inventories in the source update record. Accept the new inventory
   only after every changed path has a reviewed disposition. Copy that accepted inventory
   to this reference directory for bundle-only installations.
7. Set staged bundle data files to mode `644` and executable helpers to `755`. The
   catalog and installer require those exact modes. Refresh the catalog, then preflight
   the safe installer against current managed hashes.
   A locally modified managed file or live overlapping owner blocks installation until
   reconciled. Do not remove the lock or silently overwrite customizations.
8. Install only the validated pstack payload. Re-read installed files and rerun the audit.
   Report the installed version and remaining live integration gaps. Leave source changes
   uncommitted unless publication was explicitly requested.

The audit checks content hashes. Source-tree verification also checks Git file modes.
A successful local test does not prove skill triggering, cross-machine handoffs, model
entitlement, PR delivery, or recurring automation execution. Keep those claims separate.
