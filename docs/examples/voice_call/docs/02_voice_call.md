# Voice Direct Call

## What
Call one number directly with `client.voice.call(...)`.

## Why
Keeps normal call usage simple without requiring raw PCMO pipeline JSON.

Internally, SDK builds a single `connect` action pipeline and posts to `/voice/pcmo/call`.

## Example

```python
response = client.voice.call(
    caller_id="919999999999",
    to_number="918888888888",
    app_id="your_app_id",
    call_options={"max_duration_sec": 600, "record": True, "ring_timeout_sec": 40},
    variables={"customer_name": "Kumar", "source": "voice_call_api"},
    connect={
        "strategy": "sequential",
        "options": {
            "ring_timeout_sec": 20,
            "machine_detection": True,
            "recording": {"enabled": True, "channels": "dual", "format": "mp3"},
            "waiting_music": "https://example.com/waiting_music.wav",
        },
        "metadata": {"campaign": "normal_outbound", "priority": 1, "is_callback": False},
    },
)
```

## Parameters

| Parameter | Description | Why | Required | Constraints |
|---|---|---|---|---|
| `caller_id` | Outbound caller ID. | Displayed number + DID mapping checks. | Yes | phone regex |
| `to_number` | Destination number. | Number to dial directly. | Yes | phone regex |
| `app_id` | Voice app id. | Required for PCMO call path. | Yes | string |
| `call_options` | Top-level call options. | Duration/record/ring controls for overall call. | No | same as `ai.call` options |
| `variables` | Custom context map. | Business context for downstream use. | No | key regex + scalar values |
| `connect.strategy` | Connect dial strategy. | Ordered or parallel dialing. | No | `simultaneous|sequential` |
| `connect.options` | Connect leg options. | Fine control of bridge leg behavior. | No | PCMO connect options |
| `connect.metadata` | Connect metadata map. | Observability and business tags. | No | key regex + scalar values |

## Important Rules

- Use `call_options` for call-level options.
- Use `connect` for connect-leg controls (`strategy`, `options`, `metadata`).
- Legacy args are supported for compatibility: `options`, `strategy`, `connect_options`, `metadata`.
- Do not mix models:
  - `call_options` with `options` is invalid.
  - `connect` with legacy connect args is invalid.

## File

- `example/voice_call/01_voice_call_direct.py`
