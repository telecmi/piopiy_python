# PCMO Call Docs Index

This folder is split into small docs and single-purpose examples for `pcmo.call` and `pcmo.transfer`.

## Base Examples

- [01_client_setup.py](../../../example/pcmo_call/01_client_setup.py)
- [02_pcmo_call_minimal.py](../../../example/pcmo_call/02_pcmo_call_minimal.py)
- [03_pcmo_call_all_actions.py](../../../example/pcmo_call/03_pcmo_call_all_actions.py)
- [04_pcmo_transfer_basic.py](../../../example/pcmo_call/04_pcmo_transfer_basic.py)
- [05_pcmo_transfer_all_actions.py](../../../example/pcmo_call/05_pcmo_transfer_all_actions.py)
- [06_pcmo_error_handling.py](../../../example/pcmo_call/06_pcmo_error_handling.py)

## Topic Docs (Options + Description)

- [docs/README.md](docs/README.md)
- [docs/01_client_setup.md](docs/01_client_setup.md)
- [docs/02_pcmo_call.md](docs/02_pcmo_call.md)
- [docs/03_pcmo_transfer.md](docs/03_pcmo_transfer.md)
- [docs/04_error_handling.md](docs/04_error_handling.md)

## Action-by-Action Files

Each PCMO pipeline action is split into its own doc and python file:

- [actions/README.md](actions/README.md)
- [actions/param.md](actions/param.md) / [actions/param.py](../../../example/pcmo_call/actions/param.py)
- [actions/play.md](actions/play.md) / [actions/play.py](../../../example/pcmo_call/actions/play.py)
- [actions/play_get_input.md](actions/play_get_input.md) / [actions/play_get_input.py](../../../example/pcmo_call/actions/play_get_input.py)
- [actions/input.md](actions/input.md) / [actions/input.py](../../../example/pcmo_call/actions/input.py)
- [actions/record.md](actions/record.md) / [actions/record.py](../../../example/pcmo_call/actions/record.py)
- [actions/connect.md](actions/connect.md) / [actions/connect.py](../../../example/pcmo_call/actions/connect.py)
- [actions/hangup.md](actions/hangup.md) / [actions/hangup.py](../../../example/pcmo_call/actions/hangup.py)

## Run

```bash
python example/pcmo_call/02_pcmo_call_minimal.py
python example/pcmo_call/actions/connect.py
```
