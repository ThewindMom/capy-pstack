---
name: create-skill
description: Author, revise and evaluate a complete Capy skill. Use when a workflow should become a reusable SKILL.md, when its trigger is wrong or when a skill needs maintenance.
---

# Create a Capy skill

Deliver a reusable workflow with observable acceptance criteria, not a motivational prompt.
This is a Capy implementation of the authoring capability pstack requires, not a copy of
an unavailable Cursor built-in. Read the authoring-a-skill playbook in poteto-mode and use
its full steps. Preserve the caller's scope and the existing skill's requirements.

## 1. Define the contract

Name the outcome, consumer, inputs, permitted writes, prerequisites, triggers and explicit
non-triggers. Collect a real example task, a nearby task that should not trigger it, and
an unavailable-prerequisite case. Capture the failure that motivated an edit before changing
it. Check whether an existing skill can be improved instead of adding a duplicate.

## 2. Choose the installation scope

Find the actual project and skill paths in this session. Repository skills live at
`.agents/skills/<kebab-name>/SKILL.md`; volume skills at `skills/<kebab-name>/SKILL.md` in an
explicit non-Automation volume. Personal/Organization share across projects; Project and
Project + personal restrict scope. Automation volumes are state, not discoverable skills.
Inspect name collisions and multi-repository order. Preserve AGENTS.md and unrelated skills.
A standing always-needed rule belongs in instructions, not a huge on-demand skill.

## 3. Write the complete workflow

Frontmatter must contain `name` and a scalar `description` with the actual trigger words.
Include when to use/not use, input inspection, concrete steps, branch decisions, failure
paths, permissions, acceptance checks and a bounded output contract. Put long material in
relative references, executable helpers in scripts and fixtures in assets. Every helper
must have explicit inputs and failure behavior. Do not hide mandatory gates in optional
reference material. Preserve the same steps in direct invocation and delegated execution.

Use progressive loading: the description is what Capy sees before reading the skill body.
There is no plugin activation flag or synthetic mode registration. Avoid duplicate prose
that consumes the shared instructions/skill-list budget. Resolve references relative to
the skill file, never an assumed task working directory. Child tasks receive self-contained
briefs, skill paths and required transferred inputs, not the parent's conversation.

## 4. Verify static structure and executable helpers

Parse the frontmatter with the project's YAML tooling, check the name matches its intended
catalog identity, and resolve every local link from the file that contains it. Run helper
unit/CLI tests, malformed-input cases, timeout/failure paths and the relevant project checks.
Installation tests prove file discovery structure only. They do not prove the skill triggers
or that a model executes the workflow correctly. Never count word length as behavioral proof.

## 5. Evaluate the skill in actual tasks

Use the eval playbook. Run the positive, negative and blocked cases in fresh Capy tasks
with the intended model and scope. Record exact prompt, expected behavior, actual skill
reads, tool actions, artifact and verdict. For a change compare the old and new versions on
the same cases; blind the evaluator where feasible. Include at least one holdout case not
used to tune the description. Do not grade an agent solely on its own completion summary.
A false trigger needs description repair; a missed mandatory action needs workflow repair.
Refine, replay the failure and rerun the holdout. Missing live access stays explicitly untested.

## 6. Publish deliberately

Apply unslop and technical-writing. Report the requirement changes and evaluation evidence.
Skill edits from reflect require its explicit approval gate; this authoring workflow does
not bypass it. Commit/publish only within the caller's authorization. Refresh the bundle
catalog after reviewed changes, and run installation/link checks for repository and volume
layouts. Report the destination, actual version, tested cases and remaining platform gaps.

Capy discovery and frontmatter contract: https://docs.capy.ai/skills
Scope and persistence contract: https://docs.capy.ai/volumes
