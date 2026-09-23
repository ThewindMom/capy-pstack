---
name: setup-pstack
description: Configure faithful pstack model roles, reasoning budgets, panel diversity and Capy machine verification. Use for setup-pstack, configuring pstack models or changing its budget.
---

# Set up pstack for Capy

The complete skills are local files. Default policy is **upstream-faithful**, not repeated
inherited tasks. Read the actual bundled `pstack.model-presets.json` and the model contract
at `../poteto-mode/references/model-policy.md`. Opus 5.5 and Grok 4.7 are required upstream identities, not documented Capy routes in the
public catalog checked on September 23, 2026. Bind them only from an actual account
observation; reasoning/priority also needs live support. Do not invent IDs or entitlements.

## 1. Observe available choices

Find the actual bundle root from this skill's path, not the working directory. Inspect the
native task-model choices in this Capy session and their available reasoning/fast controls.
Record exact route IDs, supported efforts, fast support and actual parent settings in an
observation file with its source reference. For each identity marked
`requires_observed_binding` in the preset, record `bindings[identity]` with its exact
observed `model` route and an identity-observation `source`. An observed route can differ
from the policy identity; never construct it by adding a provider prefix. Recheck before
every launch. A public model
list or previously saved confirmed_models is not proof of account availability. Never ask
for an API key in chat. When a field cannot be set or observed through the current native
schema, block that setting; prose asking the child to think harder is not an implementation.

## 2. Load existing policy

Read bundle `pstack.models.json`, then project `.agents/pstack.models.json` when distinct;
project fields override bundle fields, merging roles/panels by key. No profile means the
bundled upstream-faithful preset. Do not silently convert an old v1 inherited profile:
show its choices, preserve the file, and explicitly migrate to version 2. The presets and
observation format are pstack policy, not a new Capy SDK.

Profiles created before 0.15.3 may explicitly pin the old defaults. A rerun retains any
role, route or panel the user set. Back up the profile; remove only the chosen role/panel
entries to restore bundled defaults, then validate and resolve again. Keep deliberate
older choices under an approved custom profile. Do not erase the whole file or quietly
rewrite a four-seat override to three. A faithful mismatch reports which pin needs review.

## 3. Budget, map and confirm

Preserve the original setup's budget choice: unlimited (keep source efforts), large
(xhigh), medium (high), or small (medium). Explain that the largest budget is not a price
cap. On reruns retain intentional user role, route and panel choices. Show every resolved
role, panel seat, effort, priority request and concurrency before saving a budget change.
Do not silently choose a cheaper route or substitute another family.

The faithful 0.15.3 defaults are Grok 4.7 for implementation/exploration/swarm; Opus 5.5 for
hard judgment, explanation and reflection; GPT-5.6 Sol for reflection tooling; three
distinct Opus/Sol/Grok seats for arena, architect and interrogate. Comment Sicko has no explicit
upstream model and retains parent inheritance. Reflection remains three lenses plus a
synthesizer, not a design/review panel. Architect requires at least two distinct designs.

Single-model operation is an explicitly approved alternative. Use the named `single-model`
preset and record the real approval reference; call its repeated seats same-model runs.
Other changed families/settings/counts use `custom` with an approval reference. An explicit
billing-route alias to the same weights does not increase diversity. Three faithful seats
are three models across three provider families.

## 4. Validate and save only the selected profile

Copy `pstack.models.example.json` at the bundle root to `pstack.models.json` only after
inspecting existing configuration. Run `models.py validate` and `models.py resolve` with
current observations for each required role. An unavailable model or unsupported effort/
fast setting blocks that role. Budget changes never silently approximate an unsupported
effort. Offer supported alternatives and save only the approved change, without editing
skills or overwriting unrelated instructions. Model inheritance omits the native override
only after the expected parent settings are known; record those actual settings for audit.

## 5. Prepare reproducible machines

Inspect the project's dev-environment recipe. Python 3.10+ suffices for validators and
installation. Optional Bun tools use their frozen lockfile. UI probes reuse existing
browser tooling; the bundled Python probe requires installed Playwright. Use initialize
and update_after_checkout for dependencies and idempotent startup for services with health
checks. Preserve unrelated environment configuration and verify the actual commands.

## 6. Verify the working configuration

Run a small task with poteto-mode. Inspect its real reads, returned model/settings and
shared/fresh placement. For arena, retain the resolved candidate order and collect one
record per actual task; `models.py check-run` compares records, not remote authenticity.
Use `select-judge` only after every accepted candidate is done. It selects one judge,
preferably a different family from the observed parent. Transfer its inputs before start.
A missing seat, failed candidate or unsupported setting is visible, never secretly replaced.

## 7. Offer project verification

Find a verify-* skill or real app harness. When absent, offer create-verification-skill
once. On acceptance build and prove it; a declined offer does not block setup. Installing
or configuring pstack never enables Benny or another automation.
