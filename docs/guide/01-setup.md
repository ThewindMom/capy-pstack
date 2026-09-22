# 1. Set up the full Capy port

Add this repository to the Capy project, or use the [offline installer](../../README.md)
to copy the complete `.agents/skills` catalog into the application repository. A normal
clone has everything. No recursive clone, plugin registration or source download exists.
For shared skills use a supported skill volume, not an Automation volume.

Ask Capy to use [setup-pstack](../../.agents/skills/setup-pstack/SKILL.md). Keep parent
model inheritance unless you want explicit role tuning. The profile's role names and
panel lists are in [.agents/pstack.models.example.json](../../.agents/pstack.models.example.json).
Select only models available to the actual account. Four inherited panel seats are four
independent attempts but not four different model families. Never edit skill text just
to set a personal model preference.

Then use [poteto-mode](../../.agents/skills/poteto-mode/SKILL.md) with a concrete goal and
an observable finish condition. Read-only child tasks may share the current checkout;
writers use fresh machines. Make sure every selected machine has this repository or its
skill volume before starting the task. Transfer required uncommitted files explicitly.

When no project verify-* skill exists, create-verification-skill builds one and proves
it through the real application before handoff. Configure dependencies in the project's
initialize/update_after_checkout phases and restartable services in startup. A snapshot
accelerates that recipe; it never replaces the committed source or durable work record.
