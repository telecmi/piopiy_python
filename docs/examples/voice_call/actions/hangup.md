# Action: hangup

## What
Terminate call inside pipeline.

## Why
Ends flow cleanly after announcements or routing steps.

## Options

No additional fields.

## Example

```python
from piopiy_voice import hangup_action

action = hangup_action()
print(action)
```
