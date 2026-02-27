# AI Call With Failover

## What
Use `ai.call` with `failover` to keep customer API simple while SDK handles PCMO routing internally.

## Why
You get backup-agent routing without forcing users to send raw PCMO pipeline JSON.

## Example

```python
response = client.ai.call(
    caller_id="919999999999",
    to_number="918888888888",
    agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
    app_id="your_app_id",
    failover={
        "agent_id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2",
        "strategy": "sequential",
        "max_duration_sec": 120,
        "ring_timeout_sec": 20,
        "machine_detection": True,
        "recording": {"enabled": True, "channels": "dual", "format": "mp3"},
        "waiting_music": "https://example.com/waiting_music.wav",
        "metadata": {"priority": 2, "is_escalation": True},
    },
    options={"max_duration_sec": 600, "record": True, "ring_timeout_sec": 45},
)
```

## Parameters

| Parameter | Description | Why | Required | Constraints |
|---|---|---|---|---|
| `app_id` | Voice app id. | Required for internal PCMO call path. | Yes (when failover used) | string |
| `failover.agent_id` | Failover agent ID. | Defines fallback destination. | Yes | valid UUID |
| `failover.strategy` | Dial strategy. | `sequential` for true failover. | No | `simultaneous|sequential` |
| `failover.max_duration_sec` | Max bridge duration. | Controls transfer leg duration. | No | `10-7200` |
| `failover.ring_timeout_sec` | Ring timeout per attempt. | Controls failover speed. | No | `5-120` |
| `failover.machine_detection` | AMD flag. | Reduces voicemail connection. | No | bool |
| `failover.recording` | Recording config for connect leg. | Capture post-transfer segment. | No | `enabled/channels/format` |
| `failover.waiting_music` | Waiting media URL. | Better caller experience while bridging. | No | string |
| `failover.metadata` | Custom metadata. | Traceability and business context. | No | key regex + scalar values |

## Rules

| Rule | Reason |
|---|---|
| `app_id` required with `failover`. | Internal route is PCMO call. |
| failover agent must differ from primary `agent_id`. | Prevent invalid loops. |
| max two total agent endpoints (primary + failover). | Fixed one-failover-agent design. |
