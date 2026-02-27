# Action: connect

## What
Bridge call to PSTN/SIP/Agent endpoints.

## Why
Core action for voice transfer routing and failover patterns.

## Options

| Field | Description | Why |
|---|---|---|
| `params.caller_id` | Caller ID for connect leg. | Required for compliant/expected CLI. |
| `params.strategy` | `sequential` or `simultaneous`. | Controls failover vs parallel dialing. |
| `params.options.*` | Ring timeout, duration, machine detection, recording, waiting music. | Fine control of bridge behavior. |
| `params.metadata` | Custom context values. | Diagnostics and business context. |
| `endpoints` | Target list (`pstn`, `sip`, `agent`). | Defines routing order and targets. |

## Constraints

- Max 2 `agent` endpoints
- Agent endpoints must be at the end
- Endpoint requirements:
  - `pstn` needs `number`
  - `sip` needs `uri`
  - `agent` needs `id`

## Example

```python
from piopiy_voice import connect_action

action = connect_action(
    params={
        "caller_id": "919999999999",
        "strategy": "sequential",
        "options": {
            "ring_timeout_sec": 20,
            "machine_detection": True,
            "recording": {"enabled": True, "channels": "dual", "format": "mp3"},
        },
        "metadata": {"priority": 1},
    },
    endpoints=[
        {"type": "pstn", "number": "918888888887"},
        {"type": "agent", "id": "bdd32bcb-767c-40a5-be4a-5f45eeb348a6"},
        {"type": "agent", "id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2"},
    ],
)
print(action)
```
