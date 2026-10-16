---
name: ketchup
description: "Catch the user up on changes in this Capy thread since their last message, with plain sentences and small visuals that help them decide. Use for /ketchup."
---

# Ketchup

Catch the user up on this thread since the last message they wrote before `/ketchup`, and help them understand each change, not only where it stands. Agent reports, subagent completions, and wakes that are not a person writing are not their messages. Write in the plain voice of [`/bro`](../bro/SKILL.md), and skip its restating step. Assume they remember that message and nothing after it. Call each PR, branch, or task by a name they would recognize, such as the PR title or the words they used. Do not invent a label during the catch-up.

This skill covers only the current thread. Rebuilding context across other threads is [`/recall`](../recall/SKILL.md). Resuming one prior chat or branch is the Session pickup playbook.

## Gather what changed

Keep this turn read-only, except for visuals you make for the reply from artifacts you already have. Do not change code, start an app or a job, post a comment, merge, or send a message to another thread.

The cutoff applies to new work, not to decisions still waiting on them. Read this thread with `thread.get` transcript pages. Page only this thread. Collect your own work since their last message, reports from subagents, and messages from anyone else in this thread. Use `subagent.get` for each task this thread spawned, and `pr.getOverview` plus `pr.getChecks` for each PR it touched. Say which are still running and which you could not check. A missing check is a gap, not a guess. Read earlier history only when you need it to reconcile an outstanding user decision. Do not retell work they already saw.

An action item is a decision or step only the user can take, such as a product choice, an approval, an irreversible action, or access you lack. Include any still waiting on them, even one raised before their last message. Work you can still do yourself is not an action item.

## Write the reply

Keep the whole reply well under 150 words, not counting visuals. Draw a picture when it explains a design, a dependency chain, a fix, or options more clearly than sentences. Never draw a status list or boxes with nothing connecting them. Never repeat a fact in text or across visuals. Leave out work that changed nothing for the user. Cut what happened before cutting action items.

Open with one sentence that says how many things need the user, or that nothing does. If nothing happened and nothing waits on the user, say so and stop.

Show what happened, pictures first. Embed screenshots and videos the work produced, then any diagram that explains a change. Sum up in one short bullet per requested outcome, saying what came of it and whether it is done, still running, failed, or not checked. Write each line in plain spoken words. Name bugs found and fixed on the way. Each line must stay true alone. Never mark work done that still needs the user, and leave out anything the action items say. Below the summary, give at most three short lines that change what the user knows or must do. Name work left that you can do yourself in one line.

List action items as plain bullets, never as a diagram or box. Give each two lines, or one for an unasked irreversible step. State the decision, your recommendation and why, then what happens without an answer. Ask only for the call the user owns. Include prerequisites and irreversible consequences in the recommendation. Say "unknown" for what you could not check, and link to existing detail.

Show a choice after the list. If screenshots above already show its options, write each option's gain and cost under its screenshot instead of drawing another visual. Otherwise compare every option considered side by side, with the current state when one exists. Keep gains and costs out of the rest of the text.

## Visuals

A visual is a screenshot, video, Mermaid diagram, chart, or generated image. A Markdown table is not a visual. Use available native tools or a local renderer instead of assuming an upstream `/visualize` command exists.

Keep each visual readable at a glance, with at most six boxes and eight words per box. Write labels as plain words, not status tags. Keep longer facts in the prose.

Embed already captured screenshots or videos inline for visible changes, not only as links. If none exists, mark its summary line "No screenshot yet" and say there what changed on screen. Do not start an app to capture one during this read-only turn. Make diagrams from observed connections or charts from actual numbers. Never invent a number or generate a picture of an uncaptured screen. Link only existing artifacts. Attach any produced image or file in the user-facing message. Place inline images with Markdown referencing the matching attachment's file ID or exact path. If you cannot produce the visual, state the gap plainly.
