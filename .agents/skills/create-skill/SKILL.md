---
name: create-skill
description: Author, update and test a complete Capy SKILL.md with local references.
---

# Create a Capy skill

1. Name the user outcome, trigger examples, non-triggers, permitted effects, and evidence.
2. Choose `.agents/skills/<kebab-name>/SKILL.md` in the target project or
   `skills/<kebab-name>/SKILL.md` on the selected non-Automation volume. Preserve an
   existing skill and unrelated instructions; inspect conflicts before editing.
3. Write YAML frontmatter with name and a single-scalar description naming the trigger.
   Write executable steps, failure paths, acceptance checks, and a bounded output contract.
   Put long material in relative references, helpers in scripts, and fixtures in assets.
   Use ordinary read-based discovery, not a plugin manifest, mode flag, or slash registration.
4. Test at least one positive trigger, one negative trigger, and one failure case. Drive
   a real representative task. Record expected versus observed behavior; do not merely
   check whether the document contains required words. Refine and rerun failed cases.
5. Optimize a misleading description with explicit trigger/non-trigger examples and
   check it again in a fresh task. Apply unslop to agent-facing prose.
6. Validate every local reference and run repository checks. Commit or publish only when
   authorized. Report runtime evidence and remaining unavailable tools. A missing platform
   permission is blocked, not a reason to invent an endpoint.
