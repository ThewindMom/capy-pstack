# Benny for Capy

Two coordinated native Capy automation workflows for Slack issue reports: triage, then
reproduce and optionally prepare a bounded draft fix. The entire pack is here, including
setup, operational skills, reference maps and prompt templates. It is dormant until
explicitly configured and authorized.

Read [FOR_AGENTS.md](FOR_AGENTS.md), then [setup](skills/setup-benny/SKILL.md).
Keep user configuration outside the managed pack, e.g. `.capy/benny/`. Use project or
supported skill volumes for instructions and Automation volumes only for state. The
triage run normalizes Slack bursts to separate root reports; repro accepts only trusted
marker events. Never publish a source-channel root message. Test all thread-safety gates
before enabling real traffic. No upstream repository or editor plugin is required.
