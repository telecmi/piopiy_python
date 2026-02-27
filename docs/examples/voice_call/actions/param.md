# Action: param

## What
Set key/value metadata inside pipeline.

## Why
Carry context across flow steps and callbacks.

## Options

| Field | Description | Why |
|---|---|---|
| `data` | Map of key-value pairs. | Pass contextual values for downstream logic. |

## Constraints

- Max 10 keys
- Key regex: `^[A-Za-z_][A-Za-z0-9_]*$`
- Value types: `string(max 256)`, `number`, `boolean`

## Example

```python
from piopiy_voice import param_action

action = param_action({"customer_id": "CUST-1001", "is_vip": True, "score": 95})
print(action)
```
