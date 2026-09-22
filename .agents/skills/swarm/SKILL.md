---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
---

# Swarm

Fan out N parallel cloud workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

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
4. Pick the worker model from `swarm workers` in `pstack.models.json` at the selected bundle root when present. Otherwise use `inherit-parent`. For a model race, name each arm's model up front.
5. Give each worker its own writable output when it writes.

## Phase B: Fan out

Draft all N workers with independent complete briefs, then start a bounded rolling
window of native Capy tasks. Read-only reports use shared machines. Writers and artifact
candidates use fresh machines, explicit accepted bases and non-overlapping scopes.
Transfer required files before the child uses them. A machine-only dependency unavailable
in Capy is blocked, not a reason to invent a local-computer execution mode.
Every brief names goal, scope, slice or race arm, verification and report shape.
Reports use PASS, ISSUES, or BLOCKED with evidence. Only a terminal failed or explicitly
reconciled stopped worker is a dropout; note it when continuing with N-1.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.

## Capy task execution

Draft each child with its complete goal, exact repository and base commit, writable
scope, acceptance checks, standing instructions, and the skill/reference paths to read.
Children do not inherit this conversation. Resolve roles/ and skills/ from the observed
bundle root (.agents in a project, or the selected volume root), never the child
working directory. Select a shared machine for a read-only
investigation of this checkout, or a fresh machine for any writer or candidate artifact.
A report returned in the task message is not a filesystem write. Verify the placement
and machine ID returned at start. Use `transfer_files` for inputs and reports crossing
machines; a path on another machine is not an accessible input.

Read the selected role from `pstack.models.json` at the bundle root, then apply an
explicit project `.agents/pstack.models.json` override. Absent configuration means
`inherit-parent`: omit the native model override. Recheck configured IDs against the
current account. Four-seat design/review panels retain four independent seats by
default; report same-model seats honestly rather than claiming model diversity.

Use the native task tools available in this session, not a shell that starts another
agent. Drafts are not running, working/waiting tasks remain live, and idle/stopped is
not completion. Accept a final report only after `done` plus evidence inspection.
Send follow-up fixes to the existing owner. Do not replace a timed-out owner until
its stop or terminal failure and its filesystem/branch have been reconciled.
Independent writers need disjoint paths. A dependent writer starts at its predecessor's
actual accepted branch/head, not just later from main. At three child levels, execute
the next step in the current owner rather than spawning a fourth level.
