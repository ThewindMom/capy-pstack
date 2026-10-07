---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

# Swarm

Fan out N parallel native workers on the selected runner. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Set N from the user or derive it from the shape. N is total workers, not the cloud concurrency limit.
4. Pick the worker model from `swarm workers` in `pstack.models.json` at the selected bundle root when present. Resolve the `swarm workers` role through the model policy with current observations. For a model race, name each arm's model up front.
5. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Draft all N workers with independent complete briefs, then start a bounded rolling
window of native Capy tasks. Read-only reports use shared machines. Writers and artifact
candidates use device worktrees on device threads or fresh cloud machines on cloud threads, explicit accepted bases and non-overlapping scopes.
Transfer required files before the child uses them. A required local dependency stays on the device. Unavailable dependencies are explicit blocked gates, not a reason to choose cloud implicitly.
Every brief names goal, scope, slice or race arm, verification and report shape.
Reports use PASS, ISSUES, or BLOCKED with evidence. A worker that can prove a defect reports ISSUES and lists every issue it can prove, not only the first. Only a terminal failed or explicitly
reconciled stopped worker is a dropout; note it when continuing with N-1.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and rerun that worker once with fresh agent context and the complete brief. Reconcile the previous owner before the new attempt. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.

## Capy task execution

Draft each child with its complete goal, exact repository and accepted base, writable
scope, acceptance checks, standing instructions, and full skill/reference paths.
Children do not inherit this conversation. Resolve roles/ and skills/ from the observed
bundle root (.agents in a project, or the selected volume root), not the child directory.
Read-only investigations use `machine: "shared"`. Writers use `machine: "device"` for an
isolated sibling worktree on a device-attached thread, or `machine: "fresh"` for an isolated
cloud machine on a cloud thread. A new agent does not imply a cloud machine. Use coordinated
disjoint shared writing only when explicitly assigned, with one git writer and no concurrent
commits. Verify returned placement and machine ID. Transfer uncommitted inputs and reports
with `transfer_files` when machines differ; a remote path is not an accessible input.

Resolve every role, reasoning budget, alias and panel through
`skills/poteto-mode/references/model-policy.md` at the observed bundle root. Run its
models.py resolver with current account observations before launch, and inspect returned
native settings. The policy owns defaults and unsupported-setting handling. Never silently
substitute models, infer diversity from aliases, or overwrite an existing user profile.

Use native task tools, not a shell that starts agents. Drafts are not running;
working/waiting owners remain live, and idle/stopped is not completion. Accept a final
report only with terminal completion and inspected evidence. Independent new rounds use
fresh agent context with consolidated scope: the original brief, every later directive,
the accepted report, exact head, and transferred inputs. Keep an existing live owner when
callbacks, its local checkout, uncommitted work, or running processes require it. Before a
completed role passes to a new agent, reconcile the filesystem, branch, processes and PR
callback ownership. A timeout never permits a second writer. Stop or reconcile terminal
failure before replacement. A dependent writer starts at its predecessor's accepted head,
not merely later from main. At three child levels, execute rather than spawn a fourth.

Implementation and playbook helpers read the complete poteto-mode skill and
`roles/poteto-agent.md`. Investigation, reflection and adversarial review use their own
full templates. Tier code work by difficulty through the configured policy, including
`hardest tasks` and `judgment and prose`. The parent inspects each diff and writes its own
synthesis. A second opinion uses the same brief against a different resolved model.
