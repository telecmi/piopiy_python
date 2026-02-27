# PCMO Call

## What
Start an outbound programmable call with `client.pcmo.call(...)`.

## Why
This is the primary endpoint when you want full pipeline control from the first leg.

## Minimal Example

```python
response = client.pcmo.call(
    caller_id="919999999999",
    to_number="918888888888",
    app_id="your_app_id",
    pipeline=[
        {
            "action": "connect",
            "params": {"caller_id": "919999999999"},
            "endpoints": [{"type": "pstn", "number": "918888888888"}],
        }
    ],
)
```

## Full Example

```python
from piopiy_voice import PipelineBuilder

pipeline = (
    PipelineBuilder()
    .param({"customer_id": "CUST-1001", "is_vip": True})
    .play("https://example.com/welcome.wav")
    .connect(
        params={
            "caller_id": "919999999999",
            "strategy": "sequential",
            "options": {"ring_timeout_sec": 20, "machine_detection": True},
        },
        endpoints=[
            {"type": "pstn", "number": "918888888887"},
            {"type": "agent", "id": "bdd32bcb-767c-40a5-be4a-5f45eeb348a6"},
        ],
    )
    .build()
)

response = client.pcmo.call(
    caller_id="919999999999",
    to_number="918888888888",
    app_id="your_app_id",
    pipeline=pipeline,
    options={"max_duration_sec": 900, "record": True, "ring_timeout_sec": 45},
    variables={"campaign": "pcmo", "source": "sdk"},
    agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
)
```

## Parameters

| Parameter | Description | Why | Required | Constraints |
|---|---|---|---|---|
| `caller_id` | Outbound caller ID. | Controls visible number + DID mapping. | Yes | `^[1-9][0-9]{6,15}$` |
| `to_number` | Destination number. | Target for the call. | Yes | `^[1-9][0-9]{6,15}$` |
| `app_id` | Voice app id. | Required for PCMO call path. | Yes | string |
| `pipeline` | Ordered PCMO actions. | Defines complete call behavior. | Yes | valid action list, min 1 |
| `options` | Top-level call options. | Duration/record/ring controls for overall call. | No | same as `ai.call` options |
| `variables` | Context key-values. | Business context for downstream logic. | No | key regex + scalar values |
| `agent_id` | Agent UUID context. | Optional server-side agent association. | No | UUID |

## Action-by-Action Docs

- [connect.md](../actions/connect.md)
- [play.md](../actions/play.md)
- [play_get_input.md](../actions/play_get_input.md)
- [input.md](../actions/input.md)
- [record.md](../actions/record.md)
- [param.md](../actions/param.md)
- [hangup.md](../actions/hangup.md)
