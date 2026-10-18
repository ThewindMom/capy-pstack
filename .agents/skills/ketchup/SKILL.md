---
name: ketchup
description: "Catch the user up on changes in this Capy thread since their last message, in plain words and small visuals. List every item waiting on them with what they need to decide it from the reply alone. Use for /ketchup."
---

# Ketchup

Catch the user up on this thread since the last message they wrote before `/ketchup`, and help them understand each change, not only where it stands. Then lay out every call waiting on them so they can make it from your reply alone. Agent reports, subagent completions, and wakes that are not a person writing are not their messages. Write in the plain voice of [`/bro`](../bro/SKILL.md), and skip its restating step. Assume they remember that message and nothing after it. Call each PR, branch, or task by a name they would recognize, such as the PR title or the words they used. Do not invent a label during the catch-up.

This skill covers only the current thread. Rebuilding context across other threads is [`/recall`](../recall/SKILL.md). Resuming one prior chat or branch is the Session pickup playbook.

## Gather what changed

Keep this turn read-only, except for visuals you make for the reply from artifacts you already have. Do not change code, start an app or a job, post a comment, merge, or send a message to another thread.

The cutoff applies to new work, not to decisions still waiting on them. Read this thread with `thread.get` transcript pages. Page only this thread. Collect your own work since their last message, reports from subagents, and messages from anyone else in this thread. Use `subagent.get` for each task this thread spawned, and `pr.getOverview` plus `pr.getChecks` for each PR it touched. Say which are still running and which you could not check. A missing check is a gap, not a guess. Read earlier history only when you need it to reconcile an outstanding user decision. Do not retell work they already saw.

An action item is a call or step only the user can take, such as a product choice, an approval, an irreversible action, or access you lack. Include any still waiting on them, even one raised before their last message. Work you can still do yourself is not an action item. Never make up a call to fill the reply. A step the user did not ask for and the work does not need is not an action item, unless it is irreversible and waiting on them: give it one line and no visual.

One call can cover many items, such as each PR in a set awaiting merge. For each item, collect its link, what it changes for users, the evidence behind your pick, its risk, and your pick. Write "unknown" for a fact the call needs that you could not check. Leave out a link you do not have.

## Write the reply

Spend words on the calls, not on the story. Keep what happened under 100 words, not counting visuals, and shorter when less happened. Leave out work that changed nothing for the user. Give each item about 30 words. The reply grows with the number of items: two items need well under 150 words in all, not counting visuals, and thirty need far more. Never cut items or shrink them to stay under a word count: no count in place of a list, and no link in place of an item. A link can add depth, but the reply alone must be enough to decide.

Open with one short sentence that names what waits on the user, or says nothing does. The action items give the detail. If nothing happened and nothing waits on the user, say so and stop.

Show what happened, pictures first. Embed screenshots and videos the work produced, then any diagram that explains a change. Sum up in one short bullet per requested outcome, saying what came of it and whether it is done, still running, failed, or not checked. Write each line in plain spoken words. Name bugs found and fixed on the way. Each line must stay true alone. Never mark work done that still needs the user, and leave out anything the action items say. Below the summary, give at most three short lines that change what the user knows or must do. Name work left that you can do yourself in one line.

Then list the action items. Ask only for the call the user owns, such as merge, approve, or pick, and give your pick. A step you would take first goes in your pick. So do prerequisites and anything that cannot be undone. Give the number or link of each PR, issue, or task a call is about, also in a call between options.

Fit the shape to the call. A call about one item is one bullet: the call, your pick, what it changes for users, the evidence behind your pick, and its risk, with the item named once. When items share a call, write the call and your pick once, then give each item its own bullet, riskiest first: its link and name, what it changes for users, the evidence behind your pick, and its risk. Name an item's pick only where it differs from the call's. Give each item's risk even when it is low, such as "Low risk: only the colors change." Say what waiting costs only when it is more than a delay, such as a deadline or lost data.

For a call between options, give every option the work weighed, each with what it gets the user and what it costs, and the current state when one exists. Those costs are the call's risk, so add no separate risk line. When screenshots above show the options, write each option's gain and cost under its screenshot.

## Visuals

A visual is a screenshot, video, Mermaid diagram, chart, or generated image. A Markdown table is not a visual. Use available native tools or a local renderer instead of assuming an upstream `/visualize` command exists.

Draw a picture when it explains a design or system, a PR stack or dependency chain with each PR's state, a before and after of a fix, or options side by side more clearly than sentences. Never draw a status list, a list of action items, or boxes with nothing connecting them. Never repeat a fact in text or across visuals.

Keep each visual readable at a glance, with at most six boxes and eight words per box. Write labels as plain words, not status tags. Keep longer facts in the prose.

Embed already captured screenshots or videos inline for visible changes, not only as links. If none exists, mark its summary line "No screenshot yet" and say there what changed on screen. Do not start an app to capture one during this read-only turn. Make diagrams from observed connections or charts from actual numbers. Never invent a number or generate a picture of an uncaptured screen. Link only existing artifacts. Attach any produced image or file in the user-facing message. Place inline images with Markdown referencing the matching attachment's file ID or exact path. If you cannot produce the visual, state the gap plainly.
