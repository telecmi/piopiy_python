# Voice Call Docs Index

This folder is split into small docs and single-purpose examples for the voice convenience surface:

- `client.voice.call(...)`
- `client.voice.transfer(...)`
- `client.voice.hangup(...)`

## Base Examples

- [01_voice_call_direct.py](../../../example/voice_call/01_voice_call_direct.py)
- [02_voice_transfer_direct.py](../../../example/voice_call/02_voice_transfer_direct.py)
- [03_voice_hangup_direct.py](../../../example/voice_call/03_voice_hangup_direct.py)
- [04_voice_error_handling.py](../../../example/voice_call/04_voice_error_handling.py)

## Topic Docs (Options + Description)

- [docs/README.md](docs/README.md)
- [docs/01_client_setup.md](docs/01_client_setup.md)
- [docs/02_voice_call.md](docs/02_voice_call.md)
- [docs/03_voice_transfer.md](docs/03_voice_transfer.md)
- [docs/04_voice_hangup.md](docs/04_voice_hangup.md)
- [docs/05_error_handling.md](docs/05_error_handling.md)

## Action-by-Action Files

Voice transfer uses the same PCMO pipeline action schema. Each action has a dedicated doc and python example:

- [actions/README.md](actions/README.md)
- [actions/param.md](actions/param.md) / [actions/param.py](../../../example/voice_call/actions/param.py)
- [actions/play.md](actions/play.md) / [actions/play.py](../../../example/voice_call/actions/play.py)
- [actions/play_get_input.md](actions/play_get_input.md) / [actions/play_get_input.py](../../../example/voice_call/actions/play_get_input.py)
- [actions/input.md](actions/input.md) / [actions/input.py](../../../example/voice_call/actions/input.py)
- [actions/record.md](actions/record.md) / [actions/record.py](../../../example/voice_call/actions/record.py)
- [actions/connect.md](actions/connect.md) / [actions/connect.py](../../../example/voice_call/actions/connect.py)
- [actions/hangup.md](actions/hangup.md) / [actions/hangup.py](../../../example/voice_call/actions/hangup.py)

## Run

```bash
python example/voice_call/01_voice_call_direct.py
python example/voice_call/02_voice_transfer_direct.py
python example/voice_call/actions/connect.py
```
