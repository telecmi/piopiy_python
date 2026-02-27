# Action: record

## What
Record call audio in pipeline.

## Why
Compliance, QA, and audit trails.

## Options

| Field | Description | Why |
|---|---|---|
| `format` | Output format (`mp3` or `wav`). | Storage/quality tradeoff. |
| `channels` | `single` or `dual`. | Mono/stereo recording mode. |

## Example

```python
from piopiy_voice import record_action

action = record_action(fmt="mp3", channels="dual")
print(action)
```
