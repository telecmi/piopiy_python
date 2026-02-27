# AI Call

## What
Start an outbound AI-agent call with `client.ai.call(...)`.

## Why
This is the simplest way to start an AI conversation.

## Minimal Example

```python
response = client.ai.call(
    caller_id="919999999999",
    to_number="918888888888",
    agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
)
```

## Full Standard Example

```python
response = client.ai.call(
    caller_id="919999999999",
    to_number="918888888888",
    agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
    options={"max_duration_sec": 600, "record": True, "ring_timeout_sec": 40},
    variables={"customer_name": "Kumar", "score": 97, "is_vip": True},
)
```

## Parameters

| Parameter | Description | Why | Required | Constraints |
|---|---|---|---|---|
| `caller_id` | Outbound caller ID. | Controls visible number + DID mapping. | Yes | `^[1-9][0-9]{6,15}$` |
| `to_number` | Destination number. | Target for the call. | Yes | `^[1-9][0-9]{6,15}$` |
| `agent_id` | Primary agent UUID. | Chooses which agent handles the call. | Yes | UUID |
| `options.max_duration_sec` | Max call length. | Controls cost and timeout behavior. | No | `30-7200` |
| `options.record` | Enable recording. | QA/compliance. | No | bool |
| `options.ring_timeout_sec` | Ring timeout. | Controls no-answer behavior. | No | `5-120` |
| `variables` | Context key-values. | Personalization and routing context. | No | key regex + scalar values |
