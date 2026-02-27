# Action: play

## What
Play an audio file.

## Why
Announcements or prompts before connect/input.

## Options

| Field | Description | Why |
|---|---|---|
| `file_name` | Audio URL or file name. | Audio to be played to the participant. |

## Example

```python
from piopiy_voice import play_action

action = play_action("https://example.com/welcome.wav")
print(action)
```
