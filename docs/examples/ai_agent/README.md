# AI Agent Docs Index

This folder is split into small docs and single-purpose examples.

## Base Examples

- [01_client_setup.py](../../../example/ai_agent/01_client_setup.py)
- [02_ai_call_minimal.py](../../../example/ai_agent/02_ai_call_minimal.py)
- [03_ai_call_with_options.py](../../../example/ai_agent/03_ai_call_with_options.py)
- [04_ai_call_with_failover.py](../../../example/ai_agent/04_ai_call_with_failover.py)
- [05_ai_transfer_basic.py](../../../example/ai_agent/05_ai_transfer_basic.py)
- [06_ai_transfer_all_actions.py](../../../example/ai_agent/06_ai_transfer_all_actions.py)
- [07_ai_hangup_minimal.py](../../../example/ai_agent/07_ai_hangup_minimal.py)
- [08_ai_hangup_with_reason.py](../../../example/ai_agent/08_ai_hangup_with_reason.py)
- [09_ai_error_handling.py](../../../example/ai_agent/09_ai_error_handling.py)

## Topic Docs (Options + Description)

- [docs/README.md](docs/README.md)
- [docs/01_client_setup.md](docs/01_client_setup.md)
- [docs/02_ai_call.md](docs/02_ai_call.md)
- [docs/03_ai_call_failover.md](docs/03_ai_call_failover.md)
- [docs/04_ai_transfer.md](docs/04_ai_transfer.md)
- [docs/05_ai_hangup.md](docs/05_ai_hangup.md)
- [docs/06_error_handling.md](docs/06_error_handling.md)

## Action-by-Action Files

Each transfer pipeline action is split into its own doc and python file:

- [actions/README.md](actions/README.md)
- [actions/param.md](actions/param.md) / [actions/param.py](../../../example/ai_agent/actions/param.py)
- [actions/play.md](actions/play.md) / [actions/play.py](../../../example/ai_agent/actions/play.py)
- [actions/play_get_input.md](actions/play_get_input.md) / [actions/play_get_input.py](../../../example/ai_agent/actions/play_get_input.py)
- [actions/input.md](actions/input.md) / [actions/input.py](../../../example/ai_agent/actions/input.py)
- [actions/record.md](actions/record.md) / [actions/record.py](../../../example/ai_agent/actions/record.py)
- [actions/connect.md](actions/connect.md) / [actions/connect.py](../../../example/ai_agent/actions/connect.py)
- [actions/hangup.md](actions/hangup.md) / [actions/hangup.py](../../../example/ai_agent/actions/hangup.py)

## Run

```bash
python example/ai_agent/02_ai_call_minimal.py
python example/ai_agent/actions/connect.py
```
