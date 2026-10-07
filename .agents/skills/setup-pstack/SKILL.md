---
name: setup-pstack
description: Configure native or strict pstack model roles, reasoning budgets, panel diversity and Capy machine verification. Use for setup-pstack, configuring pstack models or changing its budget.
---

# Set up pstack for Capy

Use this skill to configure role models or reasoning budgets, not to publish changes or enable automation.

The complete skills are local files. With no profile, default policy is `capy-native` for pstack 0.15.15, with a large budget.
Native policy preserves upstream weights and efforts, and labels omission of unsupported fast priority.
Opt-in `upstream-faithful` rejects unavailable priority. Neither policy substitutes models or approximates effort.
Read the actual bundled `pstack.model-presets.json` and `../poteto-mode/references/model-policy.md`.
Opus 5.5 and Grok 4.7 are required upstream identities. The preset does not prove current native route availability.
Bind them only from an actual account observation. Check reasoning and priority support independently. Do not invent IDs or entitlements.

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
schema, block that setting. Native policy can omit only unsupported fast, with a recorded adaptation.
Prose asking the child to think harder is not an implementation.

Advertised controls do not prove that a billing route can execute. Distinguish API credits
from subscription seats and user keys when the session exposes those routes. A native
credit, entitlement, or permission failure blocks that route. Report it once and do not
retry it blindly or claim successful dispatch. Select another policy only through an
explicit user choice; installation never rewrites their model profile to avoid a bill.

## 2. Load existing policy

Read bundle `pstack.models.json`, then project `.agents/pstack.models.json` when distinct;
project fields override bundle fields, merging roles/panels by key. No profile means the
bundled capy-native preset. Existing nonempty profiles without a preset remain upstream-faithful.
Select `capy-native` explicitly to enable priority adaptation in an existing profile. Do not silently convert an old v1 inherited profile:
show its choices, preserve the file, and explicitly migrate to version 2. The presets and
observation format are pstack policy, not a new Capy SDK.

Profiles created before 0.15.15 may explicitly pin the old defaults. A rerun retains any
role, route or panel the user set. Back up the profile; remove only the chosen role/panel
entries to restore bundled defaults, then validate and resolve again. Keep deliberate
older choices under an approved custom profile. Do not erase the whole file or quietly
rewrite a three-seat override to two. A faithful mismatch reports which pin needs review.

## 3. Budget, map and confirm

Offer these budgets. Large is the ordinary default. Existing strict/custom profiles without a budget retain unlimited, so explicit effort pins remain intact.
The choices are unlimited (keep source efforts), large
(xhigh), medium (high), or small (medium). Explain that the largest budget is not a price
cap. On reruns retain intentional user role, route and panel choices. Show every resolved
role, panel seat, effort, priority request and concurrency before saving a budget change.
Do not silently choose a cheaper route or substitute another family.

The 0.15.15 defaults use Grok 4.7 xhigh-fast for implementation, exploration, swarm, and reflection tooling.
Opus 5.5 xhigh handles judgment, explanation, and reflection judgment, divergent, and synthesis roles.
Arena, architect, and interrogate each have two distinct Opus/Grok seats. Sol is not a default role. Comment Sicko has no explicit
upstream model and retains parent inheritance. Reflection remains three lenses plus a
synthesizer, not a design/review panel. Architect requires at least two distinct designs.

Single-model operation is an explicitly approved alternative. Use the named `single-model`
preset and record the real approval reference; call its repeated seats same-model runs.
Other changed families/settings/counts use `custom` with an approval reference. An explicit
billing-route alias to the same weights does not increase diversity. Two upstream seats
are two models across two provider families. Under native policy, a user may explicitly select `auto` or `inherit-parent`.
Both inherit all actual parent settings. Alias seats still run, but do not prove diversity.

## 4. Validate and save only the selected profile

Copy `pstack.models.example.json` at the bundle root to `pstack.models.json` only after
inspecting existing configuration. Run `models.py validate` and `models.py resolve` with
current observations for each required role. An unavailable model or unsupported effort/
fast setting blocks strict policies. Native work orders label omitted unsupported fast.
Unavailable weights or effort block every policy. Budget changes never silently approximate an unsupported
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
shared, device, or fresh placement. Shared uses this runner and checkout. Device uses an isolated sibling worktree on this runner.
Fresh uses an isolated cloud machine. Choose placement independently from model selection and do not claim cloud is local. For arena, retain the resolved candidate order and collect one
record per actual task; `models.py check-run` compares records, not remote authenticity.
Use `select-judge` only after every accepted candidate is done. It selects one judge,
preferably a different family from the observed parent. Transfer its inputs before start.
A missing seat, failed candidate, unsupported setting, or priority adaptation is visible, never secretly replaced.
Report the profile destination, selected policy, adaptations, actual verified settings, and remaining live gaps.

## 7. Offer project verification

Find a verify-* skill or real app harness. When absent, offer create-verification-skill
once. On acceptance build and prove it; a declined offer does not block setup. Installing
or configuring pstack never enables Benny or another automation.
