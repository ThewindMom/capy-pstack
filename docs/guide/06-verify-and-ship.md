# Verify the result and open a PR

"It compiles" is not evidence. The [Prove It Works principle](../../.agents/skills/principle-prove-it-works/SKILL.md) makes the agent check the real artifact before it reports success, and your job is to make "the real artifact" checkable. This page covers stating a finish condition, generating a verification skill for your app, formally verifying a property tests rarely reach, opening the PR, and driving it to merged.

![A prototype plane flies a real test course while she times it with a stopwatch and robots film and checklist the run; the terminal reads verify: pass, evidence: captured.](images/verification.jpg)

## State the finish condition up front

Put what done means in the first prompt, in whatever words fit:

```text
/poteto-mode add json output to this command. text output stays byte-identical, the json parses, both run against the sample project. show me the evidence.
```

Now the agent has three checks it can run, not a mood to satisfy. When the reply comes back, it should carry the exact commands and outputs. If a check couldn't run, a good reply says "inconclusive". A confident reply without evidence is a warning sign.

Match the check to the change:

- A CLI change runs the real command.
- A UI change walks the changed flow in the running app.
- A parser or migration replays a saved input.
- A perf change compares before and after profiles.
- A storage change reads back the written value.

For a small diff you don't fully trust, [`/blast-radius`](../../.agents/skills/blast-radius/SKILL.md) finds what it could break elsewhere. It finds the one fact that makes the change safe and proves that fact by running code, not by arguing for it.

## Create a project verification skill

The UI bullet above hides a real requirement. The agent needs a scripted way to drive your app. If your project has one, great. If not, run:

```text
/create-verification-skill
```

[`/create-verification-skill`](../../.agents/skills/create-verification-skill/SKILL.md) interviews the repository, not you. It works out what a user touches, how the app launches locally, what can drive it (an existing harness first, otherwise browser and CDP, a PTY, or plain HTTP), what evidence proves behavior, and whether two instances can run side by side. It asks you only what the code can't answer.

It writes `.agents/skills/verify-<app>/`, agent-facing instructions with exact Launch, Doctor, Drive, Evidence, and Cleanup sections, a Helpers section for any script it ships, plus a feature map under `features/` that indexes what the app does and what result proves each feature works. The skill ships a [worked feature-map example](../../.agents/skills/create-verification-skill/references/feature-map-example) with a README index and one file per feature using the four required H2s. Before handing it over, the generator proves the skill once end to end: launch, doctor check, drive one feature, capture evidence, clean up, then confirm the evidence survived the cleanup. If that proof fails, don't use the output.

From then on, "verify it in the app" is a step any agent can execute, in this repo, with no setup conversation.

Once the verify skill works, a [`/swarm`](../../.agents/skills/swarm/SKILL.md) can split a full pass by feature-map entry and aggregate the results.

## Keep the verification skill honest

Apps change, and feature maps go out of date. When yours drifts, run:

```text
/maintain-verification-skill
```

[`/maintain-verification-skill`](../../.agents/skills/maintain-verification-skill/SKILL.md) audits the generated skill: one read-only source reader per feature in parallel, then one live pass that drives every mapped feature. It ends in exactly one of three outcomes. `clean` means full coverage and nothing to ship. `changed` means one PR of proven corrections, confined to the verification skill's own directory. `blocked` names the blocker. It never edits product code. If the live pass catches a product regression, it reports the regression instead of hiding it with a doc edit.

## Prove a property with a formal verification skill

A verification skill proves the paths you drive. Some bugs live on paths nobody drives: two retries that overlap, a lock that expires mid-write, a state change that arrives out of order. Tests rarely reach those cases. For code where such a bug is costly, run:

```text
/create-formal-verification-skill
```

[`/create-formal-verification-skill`](../../.agents/skills/create-formal-verification-skill/SKILL.md) picks the target from the code: a promise the code makes, where a break harms users and tests rarely reach the case that breaks it. It picks the strongest target, not the easiest to verify. Name an area or a bug to start there instead:

```text
/create-formal-verification-skill the job lease and retry logic. a job must never run twice at once.
```

The question picks the tool. Whether events can happen in a bad order suits a model checker over a small model of the design, and TLA+ is the default for that in any language. Whether the code behaves for every input suits a verifier that runs on the code. If no verifier runs on your language, the agent says so and tests the real code with generated inputs, not a hand-written model of the function. A property that must hold at every size can need a proof. The agent tells you which tool it chose and why, and installs it on the Capy machine without editing the project's Setup as a side effect.

It verifies one property and shows that property failing on a broken variant of the code, because a check you've never seen fail proves nothing. When the current code already breaks the property, you get the counterexample as a short sequence of steps in your code's terms. The property stays as stated, so the finding stays a finding. Product code doesn't change unless you ask.

It writes `.agents/skills/verify-<area>/`, a project-local skill that tells the next agent whether a change touches the verified code, how to run the check with one command, and how to tell a real bug from a modeling error. Before handing it over, the generator follows that skill once on a scratch change that breaks the property, and the check must catch it. The handoff says what was verified, with which tool and bounds, what the check found, and what it doesn't cover. A pass covers the model or the bound, not the whole system.

The skill also records which code each check covers and the commit where the check last matched it. Merges and refactors that skip the skill can leave the check passing on a description of code that's gone. After them, run [`/maintain-formal-verification-skill`](../../.agents/skills/maintain-formal-verification-skill/SKILL.md). It updates the verification from the code, reruns it, shows that each updated check can still fail, and tells you whether each failure is drift in the verification or a bug in the code.

## Open the PR

```text
/poteto-mode open the pr. small ordered commits, evidence in the description.
```

The [Opening a PR playbook](../../.agents/skills/poteto-mode/playbooks/opening-a-pr.md) cleans
the diff, verifies it, and publishes only when requested. Otherwise it leaves the changes
uncommitted for you. Native PR creation records ownership and delivers callbacks. Use the
installed gh-stack workflow for a dependent multi-PR stack. Amendment and rebasing still
need their own authorization; updating a skill does not grant it.

## Drive the PR to merge-ready with Babysit

An open PR starts collecting blockers immediately. Checks fail, reviewers comment, trunk moves. Hand that churn to the [Babysit playbook](../../.agents/skills/poteto-mode/playbooks/babysit.md):

```text
/poteto-mode babysit this pr. get it green.
```

Babysit uses native PR events and takes blockers in order, conflicts, review threads, then
CI. A bundled status-only watcher can provide a snapshot, not durable continuation. Bot
comments need an explicit read because they do not automatically wake this thread. Every
known fix batches into one push. The lead checks findings against the actual diff before
fixing or dismissing them. When all you want is status, ask for a single pass:

```text
/poteto-mode check on pr 123. anything outstanding?
```

Babysit stops at merge-ready. It never merges, even with everything green, because merging is a different decision.

## Land the stack with Shipping

Green is not the same as safe. When you're ready to land, say so:

```text
/poteto-mode land the stack.
```

The [Shipping playbook](../../.agents/skills/poteto-mode/playbooks/shipping.md) verifies each PR independently before it arms anything. One fresh agent per PR proves the behavior live, and the agent that judges a change is never the one that wrote it. Then Shipping lands only the contiguous verified run from the bottom, one PR at a time through GitHub by default or Origin when its CLI is available, and reports the first PR that breaks the chain. A verified PR sitting above an unverified one waits, because merging it would pull the gap in underneath.

## Review the proof before trusting the result

Open the screenshot, inspect the recording, read the output, and check the exact tested
head. A confident agent summary is not an artifact. Repeat the user flow through the
project's verification skill, and maintain that skill as the application changes.

Before reporting a measured speedup or regression, run
[benchmark-checklist](../../.agents/skills/benchmark-checklist/SKILL.md). Ask what limits the
number and whether the experiment measured the same work in both versions. Regular
verification maintenance requires an explicitly authorized automation.

Next: [Run work while you sleep](07-overnight.md).
