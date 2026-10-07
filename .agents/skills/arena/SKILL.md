---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
---

# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. The rubric is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Use `arena runners` from `pstack.models.json` at the selected bundle root when present. Resolve the configured `arena runners` seats through the model policy with current observations. Spawn more when the arena covers multiple design directions. Same model N times when the work is generation-bound rather than judgment-sensitive.
4. Assign output paths. Each candidate writes to its own location (an isolated candidate checkout according to the placement contract below, with its own branch and named artifact directory), per the **separate-before-serializing-shared-state** principle skill.

## Phase B: Fan out

Draft N native Capy candidate tasks and launch within the configured concurrency cap, with placement selected by the contract below, each with the task, the path to the shared grounding, its own output path, and instructions to produce both the artifact and a short rationale.

Each rationale names the alternatives the candidate considered and what it rejected.

Only a terminal failed or reconciled-stopped candidate may be a dropout. Proceed with N-1 and record it; do not treat a live timeout as completion. Transfer all accepted artifacts to the judge machine before starting the judge.

## Phase C: Cross-judge

After all Phase B candidates complete, choose one model from the `arena cross-judge pool` in `pstack.models.json` at the selected bundle root when present. Resolve the `arena cross-judge pool` through the model policy and models.py select-judge after all accepted candidate results exist. Prefer a different model family from the parent's. Draft one read-only native Capy judge task on that model, with the transferred candidate artifacts and exact rubric. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with the parent's reading in Phase D, not with the candidates themselves. Don't spawn the judge while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking.

Score each candidate against the rubric criterion by criterion, not on holistic feel. Compare against the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base on which candidate a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller API when two feel tied, per the Laziness Protocol.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Fold each graft in by hand, per the **redesign-from-first-principles** principle skill. Don't paste mechanically. The result has to remain coherent under one mental model.

Record what was grafted, from which candidate, and what was rejected and why.

When N candidates converge on the same shape, that is a strong agreement signal. Note the convergence in the record and ship the consensus shape. No graft is needed. When N candidates wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

The synthesized artifact has to hold up under the same scrutiny as any other output, per the **prove-it-works** principle skill.

If verification surfaces a problem the arena did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (go back to Phase E). Don't paper over.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.

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