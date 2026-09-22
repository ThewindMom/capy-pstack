---
name: setup-pstack
description: Configure Capy pstack role models, panel seats, concurrency and verification. Use for setup-pstack, pstack budget, or changing model choices.
---

# Set up pstack for Capy

This repository already contains the complete skills. No plugin registry, upstream
checkout, model-name translation, or activation command is needed.

## 1. Inspect the installation

Find this SKILL.md in the session skill list. The directory two levels above its
folder is the bundle root: `.agents` in a project, or the selected volume root.
Read its `catalog.json`, `pstack.models.example.json`, and any `pstack.models.json`.
A project `.agents/pstack.models.json` overrides a volume profile for that project.
These JSON files are pstack configuration read by the workflows, not a Capy SDK.

## 2. Observe model availability

Use the actual task-model choices available to the current Capy account. Do not
infer entitlement from a public list. No configuration is required for
`inherit-parent` (or `auto`): omit the native task's model override.
An unavailable configured ID is a visible blocked choice, not permission to invent
another ID or silently change providers. Never ask for an API key in chat.

## 3. Choose the budget and roles

Show the current map and ask for cost/concurrency preferences only when tuning is
requested. Keep all the roles in the example: implementation, difficult judgment,
investigation, reflection, comment review, and design/review panels. Pick cheaper
observed models for mechanical work and stronger observed choices for difficult
judgment according to the user's budget. Do not manufacture reasoning suffixes.

Panel arrays create one task per entry; repeated inherited entries are independent
same-model runs, not a multi-model review. Preserve four seats unless the user chooses
a smaller panel. Architect still requires at least two structurally different designs.
The arena cross-judge pool is a selection pool: start one independent judge after all
candidates finish, preferably from an observed family different from the parent.

## 4. Validate and save

Copy `pstack.models.example.json` to `pstack.models.json` at the chosen bundle root,
or edit the existing profile without touching unrelated instructions. Preserve existing
role choices on reruns. Set confirmed_models from observed account choices; the saved
list is a snapshot and must be rechecked before launching tasks.

Run `python3 skills/poteto-mode/scripts/models.py validate pstack.models.json`
from that bundle root. Show every changed role and panel count before saving a requested
budget change. Write only the selected profile. Never edit a skill to set personal defaults.

## 5. Configure reproducible machines

Inspect the project's existing dev environment and preserve unrelated entries. Python
3.10+ suffices for installation and the task/model validators. Optional PR/ledger tools
use Bun and `bun install --frozen-lockfile` in `skills/poteto-mode/scripts` under this
bundle root. Put dependency setup in initialize/update_after_checkout; services that
must return after sleep belong in startup. Verify setup on the real machine. A snapshot
is a cache of that recipe, not the only copy of it.

## 6. Check the working workflow

Load poteto-mode on a small task. Confirm a child sees the full skill and its references,
not this thread's assumed filesystem. Record the child model and placement. A local
validator passing does not prove a live Capy task was started.

## 7. Offer app verification

Look for a project verify-* skill or a real harness. When absent, offer
create-verification-skill once. On acceptance, build and prove it end to end. A declined
offer does not block setup. No automation is created or enabled by installing this pack.
