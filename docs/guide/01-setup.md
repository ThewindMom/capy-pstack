# 1. Set up the full Capy port

Add this repository to the Capy project, or use the [offline installer](../../README.md)
to copy the complete `.agents/skills` catalog into the application repository. A normal
clone has everything. No recursive clone, plugin registration or source download is needed.
For shared skills use a supported skill volume, not an Automation volume.

Ask Capy to use [setup-pstack](../../.agents/skills/setup-pstack/SKILL.md). The default is
`capy-native` for pstack 0.15.15. Its two-model panels use Opus 5.5 and Grok 4.7.
Implementation, exploration and reflection tooling use Grok; judgment and explanation use
Opus. Reflection still has three lenses and a later
synthesizer; Comment Sicko keeps its unspecified upstream model by inheriting the parent.
The [example profile](../../.agents/pstack.models.example.json) uses version 2 policy.

The [model contract](../../.agents/skills/poteto-mode/references/model-policy.md) separates
required identities from actual Capy routes. Observe the exact route and model identity in
your account and record its binding, supported reasoning and fast settings. The native
policy records unsupported fast priority as an adaptation without changing the model.
Choose `upstream-faithful` when exact priority is required; that policy blocks unsupported
settings. Missing models or reasoning controls stay blocked in either policy.

## Upgrade an existing profile

A profile written before 0.15.15 can pin old default models or panel lengths. Setup
preserves explicit role and panel choices on reruns. Back up the file, then remove only
the role/panel entries you intend to reset; absent entries use the new bundled defaults.
Retain intentional different choices under an explicitly approved `custom` profile.
Never delete unrelated settings or silently rewrite a version 1 profile into version 2.
Run `models.py validate` and then `resolve` with current account observations before use.

A named `single-model` profile is an explicitly approved alternative. Repeated inherited
seats are independent attempts, not different models. No personal preference requires
editing skill text. Budget and concurrency do not silently change model identity or seats.

## Verify the installation

Use [poteto-mode](../../.agents/skills/poteto-mode/SKILL.md) with a concrete goal and an
observable finish condition. Read-only child tasks may share the current checkout;
writers normally use isolated worktrees. On a device-attached thread, `device` placement
creates a sibling worktree on the same computer. On a cloud thread, `fresh` placement
creates a cloud machine. `shared` placement uses this runner and checkout; disjoint writers
need explicit coordination and no concurrent git writes. A fresh agent need not use cloud.
Every selected machine needs the bundle before starting. Transfer uncommitted inputs.

Accept the offer to create a project verification skill when none exists. Without a real
application check, neither model setup nor a successful task launch proves the outcome.
Choose a budget and concurrency cap before large runs. More workers spend more tokens and
do not remove dependency ordering.

When no project verify-* skill exists, create-verification-skill builds one and proves it
through the real application before handoff. Configure dependencies in initialize and
update_after_checkout and restartable services in startup. A snapshot accelerates that
recipe; it never replaces committed source or durable work records. A local validator
passing does not prove a native Capy task launched with the requested model.
