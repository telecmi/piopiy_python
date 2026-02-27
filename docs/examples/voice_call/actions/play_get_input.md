# Action: play_get_input

## What
Play prompt and collect DTMF/speech input.

## Why
Build IVR decisioning inside voice transfer pipeline.

## Options

| Field | Description | Why |
|---|---|---|
| `prompt` | Prompt config (`file` or `say`). | Defines what user hears. |
| `input` | Allowed input modes (`dtmf`, `speech`). | Defines accepted input channel(s). |
| `dtmf` | DTMF capture settings. | Control digit collection behavior. |
| `retries` | No-input/invalid retry config. | Improve completion rate. |
| `on_result` | `url` or `pcmo` route target. | Route based on collected input. |

## Example

```python
from piopiy_voice import play_get_input_action

action = play_get_input_action(
    prompt={"type": "say", "say": "Press 1 for sales", "language": "en-US", "voice_id": "female", "speed": 1.0},
    input_modes=["dtmf"],
    dtmf={"max_digits": 1, "first_digit_timeout": 5},
    retries={"max": 1},
    on_result={"type": "url", "url": "https://example.com/input-result"},
)
print(action)
```
