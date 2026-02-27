# Piopiy Python SDK

Production-ready Python SDK for Piopiy Voice Orchestrator APIs. Easily build AI voice agents, manage programmable voice calls, and orchestrate complex call flows directly from your Python applications.

## Prerequisites

- Python 3.7 or higher
- A Piopiy account and API token (Get yours from the [Piopiy Dashboard](https://piopiy.com))

## Installation

```bash
pip install piopiy
```

## Quick Start

Initialize the client using your API token. We recommend storing your token in an environment variable securely.

```python
import os
from piopiy_voice import RestClient

client = RestClient(token=os.environ.get("PIOPIY_API_TOKEN"))
```

## Main Examples

### 1) AI Single Call

```python
response = client.ai.call(
    caller_id="919999999999",
    to_number="918888888888",
    agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
)
print(response)
```

Example code: [`example/ai_agent/02_ai_call_minimal.py`](example/ai_agent/02_ai_call_minimal.py)

### 2) AI Call With Failover

```python
response = client.ai.call(
    caller_id="919999999999",
    to_number="918888888888",
    agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",  # primary agent
    app_id="your_app_id",
    failover={
        "agent_id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2",  # failover agent
        "strategy": "sequential",
        "ring_timeout_sec": 20,
        "machine_detection": True,
    },
)
print(response)
```

Failover rules:
- `app_id` is required when `failover` is used.
- `failover.agent_id` is required (single failover agent).
- Failover agent must be different from primary `agent_id`.

Example code: [`example/ai_agent/04_ai_call_with_failover.py`](example/ai_agent/04_ai_call_with_failover.py)

### 3) Voice Direct Call

```python
response = client.voice.call(
    caller_id="919999999999",
    to_number="918888888888",
    app_id="your_app_id",
)
print(response)
```

Example code: [`example/voice_call/01_voice_call_direct.py`](example/voice_call/01_voice_call_direct.py)

### 4) PCMO Simple Call

```python
from piopiy_voice import PipelineBuilder

pipeline = (
    PipelineBuilder()
    .connect(
        params={"caller_id": "919999999999"},
        endpoints=[{"type": "pstn", "number": "918888888888"}],
    )
    .build()
)

response = client.pcmo.call(
    caller_id="919999999999",
    to_number="918888888888",
    app_id="your_app_id",
    pipeline=pipeline,
)
print(response)
```

Example code: [`example/pcmo_call/02_pcmo_call_minimal.py`](example/pcmo_call/02_pcmo_call_minimal.py)

## Other Actions And Full Docs

- AI transfer/hangup + all AI docs: [`docs/examples/ai_agent/README.md`](docs/examples/ai_agent/README.md)
- Voice transfer/hangup + full voice convenience docs: [`docs/examples/voice_call/README.md`](docs/examples/voice_call/README.md)
- PCMO transfer + all pipeline actions: [`docs/examples/pcmo_call/README.md`](docs/examples/pcmo_call/README.md)
- Flow connect (minimal): [`docs/examples/flow_call/README.md`](docs/examples/flow_call/README.md)
- Full SDK contract/validation details: [`docs/SDK_RESTRUCTURE.md`](docs/SDK_RESTRUCTURE.md)

## Extra Example Code Indexes

- AI examples folder: [`example/ai_agent`](example/ai_agent)
- Voice examples folder: [`example/voice_call`](example/voice_call)
- PCMO examples folder: [`example/pcmo_call`](example/pcmo_call)
