# PCMO Transfer

## What
Transfer an active call with `client.pcmo.transfer(call_id, pipeline)`.

## Why
Allows full runtime control over an existing call using the same PCMO pipeline format.

## Recommended Pattern
Use `PipelineBuilder` to avoid manual JSON.

```python
from piopiy_voice import PipelineBuilder

pipeline = (
    PipelineBuilder()
    .play("https://example.com/transfer_notice.wav")
    .connect(
        params={"caller_id": "919999999999", "strategy": "sequential"},
        endpoints=[
            {"type": "agent", "id": "PRIMARY_AGENT_UUID"},
            {"type": "agent", "id": "SECOND_AGENT_UUID"},
        ],
    )
)

response = client.pcmo.transfer(call_id="CALL_UUID", pipeline=pipeline)
```

## Parameters

| Parameter | Description | Why | Required | Constraints |
|---|---|---|---|---|
| `call_id` | Active call UUID. | Identifies which call to modify. | Yes | UUID |
| `pipeline` | New pipeline actions. | Defines transfer behavior. | Yes | valid PCMO action list |

## Action-by-Action Docs

Each action has its own file (description + standalone example):

- [connect.md](../actions/connect.md)
- [play.md](../actions/play.md)
- [play_get_input.md](../actions/play_get_input.md)
- [input.md](../actions/input.md)
- [record.md](../actions/record.md)
- [param.md](../actions/param.md)
- [hangup.md](../actions/hangup.md)

## Validation Rules

| Rule | Reason |
|---|---|
| Max 2 `agent` endpoints per `connect`. | Server-side limit. |
| If `agent` endpoints exist, they must be at the end. | Deterministic routing behavior. |
| All actions validated before request is sent. | Early error detection. |
