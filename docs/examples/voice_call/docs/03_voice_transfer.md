# Voice Direct Transfer

## What
Transfer an active call with `client.voice.transfer(call_id, pipeline)`.

## Why
Gives the same convenience style as AI transfer under `client.voice`.

Internally, SDK posts to `/voice/pcmo/transfer`.

## Recommended Pattern
Use `client.voice.pipeline()` or `PipelineBuilder` to avoid manual JSON.

```python
transfer_pipeline = (
    client.voice.pipeline()
    .play("https://example.com/transfer_notice.wav")
    .connect(
        params={"caller_id": "919999999999", "strategy": "sequential"},
        endpoints=[
            {"type": "agent", "id": "PRIMARY_AGENT_UUID"},
            {"type": "agent", "id": "SECOND_AGENT_UUID"},
        ],
    )
    .hangup()
)

response = client.voice.transfer(
    call_id="c4d0e5f6-a7b8-12c9-d3e4-f56789012345",
    pipeline=transfer_pipeline,
)
```

## Parameters

| Parameter | Description | Why | Required | Constraints |
|---|---|---|---|---|
| `call_id` | Active call UUID. | Identifies which call to modify. | Yes | UUID |
| `pipeline` | New pipeline actions. | Defines transfer behavior. | Yes | valid PCMO action list |

## Action-by-Action Docs

- [connect.md](../actions/connect.md)
- [play.md](../actions/play.md)
- [play_get_input.md](../actions/play_get_input.md)
- [input.md](../actions/input.md)
- [record.md](../actions/record.md)
- [param.md](../actions/param.md)
- [hangup.md](../actions/hangup.md)

## File

- `example/voice_call/02_voice_transfer_direct.py`
