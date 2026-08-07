# GLUON Agy supervisor/worker connection check

- Execution Domain: `DESKTOP_DRY_RUN`
- Date: 2026-08-04
- Policy Checkpoint SHA256 or ONNX Hash: N/A (agent CLI connection check)
- Evidence Status: `PASS` for plan-mode CLI connectivity; code-edit worker remains `NOT_TESTED`

## Scope

Verify that Codex can invoke the locally installed Agy CLI as a bounded,
read-only planning worker before defining the implementation loop. No source
file edits, Isaac Sim process, ROS process, SDK connection, or robot command
were delegated to Agy.

## Evidence

Local executable:

```text
/home/cocel/.local/bin/agy
```

`agy models` returned model slugs including:

```text
claude-sonnet-4-6
claude-opus-4-6-thinking
gemini-3.1-pro-high
```

`agy agents` did not list a custom agent. An early invocation incorrectly used
`--agent claude-sonnet-4-6`; the detailed CLI log reported `Agent not found,
falling back to default`, and selected Gemini 3.6 Flash High. Those early calls
prove generic Agy connectivity, not Claude routing.

Minimal text-output plan-mode call returned exit code 0 and:

```text
AGY_PLAN_CONNECTION_READY
```

Minimal JSON-output plan-mode call returned:

```json
{
  "conversation_id": "915bab14-f6db-4b2d-a692-025215dc0e1a",
  "status": "SUCCESS",
  "response": "JSON_MODE_READY\n",
  "num_turns": 1
}
```

The same conversation was then resumed explicitly with
`--conversation 915bab14-f6db-4b2d-a692-025215dc0e1a`. It returned exit code 0
and:

```json
{
  "conversation_id": "915bab14-f6db-4b2d-a692-025215dc0e1a",
  "status": "SUCCESS",
  "response": "AGY_CONVERSATION_RESUME_READY\n",
  "num_turns": 2
}
```

A corrected model-selection call used `--model claude-sonnet-4-6`. The detailed
log showed:

```text
Resolving model claude-sonnet-4-6
Propagating selected model override to backend: label="Claude Sonnet 4.6 (Thinking)"
```

The terminal JSON result was:

```json
{
  "conversation_id": "c3e0e524-6245-4950-b011-b6b58587c98b",
  "status": "SUCCESS",
  "response": "AGY_CLAUDE_MODEL_READY\n",
  "num_turns": 1
}
```

## Result and limits

- Codex-to-Agy subprocess invocation: `PASS`
- Plan-mode text response: `PASS`
- Plan-mode JSON/conversation ID response: `PASS`
- Explicit conversation resume: `PASS`
- Claude Sonnet routing through `--model`: `PASS`
- Claude slug supplied through `--agent`: `FAIL` with default-model fallback;
  this invocation form is forbidden in the implementation loop
- Claude long-form plan review with final `json`: `FAIL`; conversation was left
  without a terminal result, and explicit resume reported an unexpected
  `GENERATING` planner-step status
- Claude `stream-json` probe: `PASS` for `init.model`, conversation ID, and
  step/tool visibility; terminal result remained `FAIL` after a headless
  `run_command` permission/tool step
- Failure-driven code correction iteration: `NOT_TESTED`
- `accept-edits` source modification: `NOT_TESTED`
- Independent diff/test supervision of an Agy edit: `NOT_TESTED`

The implementation workflow will use one writer at a time in the shared dirty
worktree. Agy will perform bounded edits only after Codex defines allowed files
and acceptance commands. Hardware operations remain explicitly forbidden.

For non-trivial workers, the supervisor will use `stream-json`, verify the
requested model in the init event, inspect every tool call, and require a
terminal result. Missing terminal results and active tool steps at process exit
are failures, not partial successes. A conversation stuck in a generating step
is abandoned and replaced with a fresh, smaller-scope conversation rather than
resumed indefinitely.
