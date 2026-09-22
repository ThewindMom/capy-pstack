# Triage automation prompt

> Complete template for a native Capy automation. Configure only after explicit authorization; install the full skills in its project or supported skill volume first. Read setup-benny for disabled creation and a bounded live test.

Read and follow `.agents/automations/benny/skills/triage-issue-reports/SKILL.md` for this run.

Configuration source. Include this repository-relative path only when it is committed in the same target repository. Otherwise paraphrase the configured values. For a volume installation use its actual installed skill path instead of a repository-relative guess. Never use an inaccessible machine-local path:

```text
{{BENNY_CONFIG_PATH}}
```

Trigger:

```json
{
	"source_channel_id": "{{SLACK_CHANNEL_ID}}",
	"message_ts": "{{SLACK_MESSAGE_TS}}",
	"thread_ts": "{{SLACK_THREAD_TS_OR_EMPTY}}"
}
```

The creation intent should describe this as a new top-level report in the configured source Slack channel.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting or writing to the issue tracker.

The committed operational file owns classification, attachment review, cause tracing, routing, dedupe, tracker writes, and the final verdict. Post no progress messages. Never post a root message in the source channel.

The coordinator is the only Slack poster. Any delegated worker must be read-only, return findings only, and receive an explicit ban on every Slack write action.

End the single verdict with exactly one configured marker:

```text
[benny:bug]
[benny:performance]
[benny:other]
```

A bug or performance marker may add `tracker=<URL>`.

Capy Slack burst handling: process each distinct top-level root report separately with immutable coordinates. Do not combine reports. Persist the actual posted-marker receipt and reconcile it on retry before another post. Native run output is not a Slack reply; use the explicit authorized thread-post action.
