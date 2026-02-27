# Voice Transfer Pipeline Actions (One File Per Action)

Voice transfer uses the same PCMO pipeline action schema.
Each action has:
- a markdown doc (`*.md`) in this folder with options and descriptions
- a python file (`*.py`) under `example/voice_call/actions/` with a standalone example payload

## Files

- [param.md](param.md) / [`example/voice_call/actions/param.py`](../../../../example/voice_call/actions/param.py)
- [play.md](play.md) / [`example/voice_call/actions/play.py`](../../../../example/voice_call/actions/play.py)
- [play_get_input.md](play_get_input.md) / [`example/voice_call/actions/play_get_input.py`](../../../../example/voice_call/actions/play_get_input.py)
- [input.md](input.md) / [`example/voice_call/actions/input.py`](../../../../example/voice_call/actions/input.py)
- [record.md](record.md) / [`example/voice_call/actions/record.py`](../../../../example/voice_call/actions/record.py)
- [connect.md](connect.md) / [`example/voice_call/actions/connect.py`](../../../../example/voice_call/actions/connect.py)
- [hangup.md](hangup.md) / [`example/voice_call/actions/hangup.py`](../../../../example/voice_call/actions/hangup.py)
