# Flow Call (`client.flow.call`)

## What
Connect a customer call into an existing server-side flow.

## Why
Flow contains the routing/pipeline on server side, so SDK call should stay minimal.

## Minimal Example (Required Fields Only)

```python
response = client.flow.call(
    flow_id="7f4d89c7-3485-45c5-9016-f45a47cd885c",
    org_id="f89dd77d-c226-4ff2-b88c-6d7e4f5a88e2",
    caller_id="919999999999",
    to_number="918888888888",
    app_id="your_app_id",
)
```

## Parameters

| Parameter | Description | Required | Constraints |
|---|---|---|---|
| `flow_id` | Flow UUID to execute. | Yes | UUID |
| `org_id` | Organization UUID. | Yes | UUID |
| `caller_id` | Outbound caller ID. | Yes | `^[1-9][0-9]{6,15}$` |
| `to_number` | Destination number. | Yes | `^[1-9][0-9]{6,15}$` |
| `app_id` | Voice app id. | Yes | string |

## Important Note

For flow calls, keep usage minimal in examples/docs: only connect to flow using required fields.

## File

- `example/flow_call.py`
