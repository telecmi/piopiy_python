# Piopiy AI Agent, Voice & WhatsApp SDK - Python

The official Python SDK for **Piopiy** - a complete **Voice AI Agent and CPaaS Platform**.

Easily build intelligent Voice Agents, manage complex call flows (queues, human handoff), execute bulk voice campaigns, and send multi-channel notifications via WhatsApp and SMS.

## Installation

```bash
pip install piopiy
```

## Usage

### 1. Initialize the Client

You strictly need a Bearer token to initialize the client.

```python
from piopiy import RestClient

# Initialize with your Bearer token
client = RestClient(token="your_bearer_token")
```

### 2. Initiate an AI Call

Trigger an outbound call handled by your AI Agent.

```python
try:
    response = client.ai.call(
        caller_id="919999999999",      # The number displayed to the callee
        to_number="918888888888",      # The destination number
        agent_id="bdd32bcb-...",       # Your AI Agent ID
        options={
            "max_duration_sec": 600,   # Optional: Limit call duration (30-7200)
            "record": True,            # Optional: Record the call
            "ring_timeout_sec": 40     # Optional: Ring timeout (5-120)
        },
        variables={
            "customer_name": "John Doe",  # Custom variables for the AI Agent
            "subscription": "premium"
        }
    )
    print("Call Initiated:", response)
except Exception as e:
    print("Error:", e)
```

#### Parameters

| Parameter | Type | Required | constraints | Description |
|-----------|------|----------|-------------|-------------|
| `caller_id` | `string` | **Yes** | `^[1-9][0-9]{6,15}$` | The number calling from. Must start with 1-9 and be 7-16 digits long. |
| `to_number` | `string` | **Yes** | `^[1-9][0-9]{6,15}$` | The destination number. Must start with 1-9 and be 7-16 digits long. |
| `agent_id` | `string` | **Yes** | `uuid` | The unique UUID of the AI agent. |
| `options` | `object` | No | - | Configuration options for the call. |
| `variables` | `object` | No | - | Custom variables to pass to the agent. Keys must match `^[A-Za-z_][A-Za-z0-9_]*$`. Values can be string, number, or boolean. |

#### Options Object

| Key | Type | constraints | Description |
|-----|------|-------------|-------------|
| `max_duration_sec` | `integer` | `30` - `7200` | Maximum duration of the call in seconds. |
| `ring_timeout_sec` | `integer` | `5` - `120` | Time in seconds to wait for the call to be answered. |
| `record` | `boolean` | - | Whether to record the call. |

### 3. Terminate a Call

Hang up an active call programmatically.

```python
try:
    response = client.voice.hangup(
        call_id="bf2d781e-...",        # The Call UUID
        cause="NORMAL_CLEARING",       # Hangup cause
        reason="Consultation done"     # Optional reason
    )
    print("Call Terminated:", response)
except Exception as e:
    print("Error:", e)
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `call_id` | `string` | **Yes** | The unique identifier (UUID) of the call to hang up. |
| `cause` | `string` | No | The cause for hanging up. Defaults to `"NORMAL_CLEARING"`. |
| `reason` | `string` | No | Additional text description or reason for terminating the call. |
