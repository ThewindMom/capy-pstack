---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Resolve every role through the installed model policy. A rejected native route is blocked,
not permission to substitute a default or another model from the same family.

## Step 1. Assess Complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. One explainer explores and explains in a single pass. Go to Step 2b.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): spawn parallel explorers first, then hand off to the explainer. Go to Step 2a.

When in doubt, take the simple path.

## Step 2a. Explore (complex questions only)

Decompose the question into 2 to 4 exploration angles, each a distinct slice of the subsystem. Spawn all explorers in a single message:

- `model`: your configured how-explorer model (resolved through the model policy)
- Read-only scope on a shared Capy machine; return the report as a task message.

Each explorer gets the prompt in `references/explorer-prompt.md` with its angle filled in. Then go to Step 3.

## Step 2b. Direct Explain (simple questions)

Spawn one native Capy task that explores and explains in one pass:

- `model`: your configured how-explainer model (resolved through the model policy)
- Read-only scope on a shared Capy machine; return the report as a task message.

Build its prompt from `references/explainer-prompt.md` without the explorer-findings section. Go to Step 4.

## Step 3. Synthesize (complex questions only)

Once all explorers have returned, spawn one native Capy task to synthesize their findings into one explanation:

- `model`: your configured how-explainer model (resolved through the model policy)
- Read-only scope on a shared Capy machine; return the report as a task message.

Build its prompt from `references/explainer-prompt.md` with every explorer's findings filled in.

## Step 4. Present

Present the explainer's output to the user. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output Format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.

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
