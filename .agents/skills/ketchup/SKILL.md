---
name: ketchup
description: "Catch the user up on this Capy thread since their last message, in plain words. Give each action item an executive summary with enough context to decide. Use for /ketchup."
---

# Ketchup

Catch the user up on this thread since the last message they wrote before `/ketchup`. Agent reports, subagent completions, and wakes that are not a person writing are not their messages. Write in the plain voice of [`/bro`](../bro/SKILL.md), and skip its restating step. Assume they remember that message and nothing after it. Call each PR, branch, or task by a name they would recognize, such as the PR title or the words they used. Do not invent a label during the catch-up.

This skill covers only the current thread. Rebuilding context across other threads is [`/recall`](../recall/SKILL.md). Resuming one prior chat or branch is the Session pickup playbook.

## Gather what changed

Keep this turn read-only, except for visuals you make for the reply from artifacts you already have. Do not change code, start an app or a job, post a comment, merge, or send a message to another thread.

The cutoff applies to new work, not to decisions still waiting on them. Read this thread with `thread.get` transcript pages. Page only this thread. Collect your own work since their last message, reports from subagents, and messages from anyone else in this thread. Use `subagent.get` for each task this thread spawned, and `pr.getOverview` plus `pr.getChecks` for each PR it touched. Say which are still running and which you could not check. A missing check is a gap, not a guess. Read earlier history only when you need it to reconcile an outstanding user decision. Do not retell work they already saw.

An action item is a decision or step only the user can take, such as a product choice, an approval, an irreversible action, or access you lack. Include any still waiting on them, even one raised before their last message. Work you can still do yourself is not an action item.

## Write the reply

Open with one sentence that says how many action items there are, or that there are none. If nothing happened and nothing waits on the user, say so and stop.

Then say what happened, most important first. Give each result and what it means for them. Skip steps that changed nothing. Name in one line any work left that you can do yourself.

Then give each action item a short executive summary. Cover the decision to make, why it matters now, the options and what each costs, your recommendation, and what happens if they do not answer. If you do not know a part, say so instead of guessing. Link to the detail when there is one, and write the summary so they can decide without opening it.

Show each action item as a before and after, side by side. For a choice, put the current state beside each option, or the options alone when there is no current state. Use a screenshot or video you already captured when the change is visible. Otherwise use another real artifact, such as a table of numbers, a diff, or a diagram. If no visual exists yet and you can make one from data you already have, make that. If you cannot, say plainly that none exists. Never invent a number. Never draw or generate a picture of a screen you did not capture. Link only artifacts that exist.

Prefer a table, a Mermaid diagram, or a chart to dense prose.
