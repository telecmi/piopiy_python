# Action: input

## What
Collect input without playing prompt.

## Why
Useful when prompt already played or silent capture is needed.

## Options

| Field | Description | Why |
|---|---|---|
| `dtmf` | DTMF capture settings. | Tune digit capture behavior. |
| `on_result` | `url` or `pcmo` route target. | Route control after input. |

## Example

```python
from piopiy_voice import input_action

action = input_action(
    dtmf={"min_digits": 1, "max_digits": 4, "finish_on_key": "#"},
    on_result={"type": "pcmo", "ref": "next_pipeline_ref"},
)
print(action)
```
