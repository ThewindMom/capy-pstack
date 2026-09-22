---
name: setup-benny
description: Configure Benny and prepare its triage and repro automations. Use when installing Benny or changing its Slack, tracker, repository, routing, control, model, or budget settings.
---

# Set up Benny

Benny is a complete dormant pack in this repository. Read its operational files directly;
installation never creates jobs. All actions stay within the user's explicit authorization.

## 1. Verify the native pack and its shared skills

Locate the selected project or non-Automation skill volume. Use the offline pstack
installer for project installation, preserving existing files and user configuration.
Verify this setup file, both operational skills, references and templates are present.
Confirm how, why, tdd, unslop and the required principles are discoverable in a fresh
Capy task with the same project/volume. There is no editor settings entry to enable.
Keep user configuration and maps outside the managed pack. Commit project files only
when authorized. A volume installation must use its actual discovered pack path in each
brief; Automation volumes store state and cannot supply discoverable skills.

## 2. Adapt the configuration

Open these copied examples:

- `../../templates/configuration.example.yaml`
- `../reproduce-and-fix-issues/references/feature-map.example.md`

Create user-owned copies outside `.agents/automations/benny/`. These are configuration files, not pack files. Example locations:

- Project config, such as `.capy/benny/configuration.yaml`
- Project feature map, such as `.capy/benny/feature-map.md`
- Project routing map, such as `.capy/benny/routing.md`
- User config, such as `<selected-personal-volume>/benny/configuration.yaml`
- User feature map, such as `<selected-personal-volume>/benny/feature-map.md`

Fill one feature-map section for every user-facing feature the automation may reproduce. Keep it at the user point of view. Do not freeze implementation details or current code paths in the map.

Do not edit the copied examples. Pack refreshes may update source-managed files after conflict review, but they must never touch the user-owned copies.

Prefer committed, secret-free files in the target repository when a fresh automation checkout must read them. Otherwise paraphrase the required values into the live prompt. Reference a repository file only after the native repository and volume checks confirm that the file is committed in the repository where the automation runs.

Use stable repository-relative paths for committed pack and configuration files. Never reference the plugin source directory or a plugin cache path from a live automation.

## 3. Fill the required choices

Ask for or confirm:

- Source Slack channel ID
- Optional operations or status channel ID
- Repository URL and default branch
- Triage identity or Slack user ID
- Issue tracker type, team, project, labels, and intake status
- Tracker adapter skill or MCP actions
- Optional routing map path
- Required control skill name
- Required user-facing feature-map path
- Status emoji strings
- Pull request URL format
- Event-driven deadlines and effort budgets
- Model slug for triage, repro, code work, and media review

Use only model slugs shown as available in the current Capy account's task/automation model choices. Do not guess a slug and do not carry over a private default.

The source channel, triage identity, repository, tracker adapter, control skill, and feature map must be explicit. Fail setup if any required value stays ambiguous.

Use pstack's `unslop` skill on the final automation names, descriptions, and prompt shims before saving them.

## 4. Check integration capabilities

The triage automation needs:

- Read access to the configured source Slack channel and its threads
- Thread-reply access in that channel
- Attachment metadata and file download access when reports include media
- Search, read, create, and update access through the configured issue-tracker adapter

The repro automation needs:

- Read access to the source thread
- Thread-reply access in the source channel
- Optional post and edit access in the configured operations channel
- Repository read and history access
- A pull request action that can open a draft pull request
- The configured control-adapter skill

Prefer authorized Capy Slack tools for reads and posts. The optional `BENNY_SLACK_BOT_TOKEN` may fill a narrow gap such as editing one operations status message or downloading an attachment. Store the value in a secret manager or environment, not in YAML.

Do not use undocumented integration endpoints.

## 5. Prepare the routing map

If the user wants reroutes or owner pings:

1. Copy `../triage-issue-reports/references/routing.example.md` outside `.agents/automations/benny/`.
2. Replace every placeholder with public or organization-local values.
3. Keep owner pings off by default.
4. Allow a ping only for a configured feature owner or a confirmed likely regression author.

If no routing map is configured, triage may classify a report but must not guess a destination or owner.

## 6. Verify the control adapter

Read `../reproduce-and-fix-issues/references/control-adapter.md` and the user's completed feature map.

Confirm that the named skill can:

- Bring up the target app
- Navigate every mapped feature through the real UI
- Exercise mapped states through declared adapter actions
- Inspect state without forcing the result
- Capture screenshots
- Start and stop a recording
- Clean up its processes and temporary data

If any capability is missing, leave the repro automation disabled. It must fail closed rather than claim a reproduction it did not perform.

## 7. Prepare native Capy automations

Use the bundled capy-automation skill and Capy's native automation tools, after explicit
creation/update authorization. Inspect existing automations first and retain their IDs;
do not create duplicates. Read FOR_AGENTS.md and both complete prompt templates. Show
project, source channel, trusted triage identity, repository revision, permitted writes,
model, run cap and trigger filters before saving a requested configuration change.
Create disabled and preserve existing disabled state until thread safety is proven.

Triage: trigger on configured new top-level Slack reports. Normalize each event to the
immutable source channel and root thread_ts. Capy Slack events can arrive as bursts;
process each distinct root report once, and do not combine two reports merely because
they arrived in one burst. Read the full thread, dedupe in the tracker, classify and
trace the evidence, and post exactly one thread-only verdict with the configured
[benny:bug], [benny:performance], or [benny:other] marker. Never post at channel root.

Reproduction: use a filtered event for the trusted triage marker and immutable source
coordinates rather than a detached polling process racing the triager. Resolve the
original report and validate the marker author's exact identity before action. Follow
the full reproduce-and-fix-issues workflow: twice through the mapped real UI, evidence,
verify an existing fix before authoring, bounded optional fix, and draft PR only when
proof and checks pass. No marker, wrong author, or ambiguous coordinates means no action.
A report waiting for triage remains pending in a scoped durable record, not a fake success.
Use the configured time budget to expire it visibly without starting duplicate writers.

Each live prompt reads its exact installed operational file and user configuration.
Save instruction files in the project's committed checkout or a supported skill volume.
Use an Automation volume for pending/processed report receipts, with one owner per root
report. Choose new threads for independent reports or a single queue thread with explicit
per-report isolation. A model is inherited unless an available ID is explicitly selected.
Native tool/API schemas are the source of truth for field names; never invent a backend
endpoint. Keep webhook URLs and tokens out of prompts. Test with a bounded manual run in
a test channel before enabling normal event traffic.

For an existing automation, read its stored prompt, triggers, principal, caps and model,
apply only the requested changes through native tools, and verify the returned state.
No replacement or duplicate is needed merely because a setting changed.

## 8. Test thread safety

Use a test channel or a harmless test report.

Before testing, confirm that the full installed skills, `.agents/automations/benny/`, and every referenced secret-free configuration file are committed on the branch used by the automation checkout. Confirm that both live prompts point at their exact committed operational files. If any check fails, stop. Tell the user that the automation cannot be enabled yet.

Verify:

1. Triage stores the root `thread_ts` and posts exactly one verdict as a reply.
2. The verdict contains one configured marker.
3. Repro accepts the marker only from the configured triage identity.
4. Repro keeps the same immutable source coordinates.
5. No source-channel root message appears.
6. A delegated worker cannot use any Slack write action.
7. Missing coordinates, a deleted parent, or a failed preflight produces no post and no tracker issue.

Enable normal traffic only after all seven checks pass.
