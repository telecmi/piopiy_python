# AI Hangup

## What
Terminate an active call with `client.ai.hangup(...)`.

## Why
Use for immediate stop, timeout workflows, or agent-side end control.

## Minimal

```python
response = client.ai.hangup(call_id="c4d0e5f6-a7b8-12c9-d3e4-f56789012345")
```

## With Cause/Reason

```python
response = client.ai.hangup(
    call_id="c4d0e5f6-a7b8-12c9-d3e4-f56789012345",
    cause="NORMAL_CLEARING",
    reason="Conversation completed",
)
```

## Parameters

| Parameter | Description | Why | Required | Constraints |
|---|---|---|---|---|
| `call_id` | Active call UUID. | Identifies call to terminate. | Yes | UUID |
| `cause` | Hangup cause code. | Structured termination reason. | No | string `1-64` |
| `reason` | Human reason text. | Debug/operations clarity. | No | string `1-256` |
