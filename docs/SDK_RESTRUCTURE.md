# Piopiy Python SDK Restructure (Aligned to `piopiyai_voice_orchestrator` `development`)

## Scope

This SDK restructure aligns `piopiy_python` with the API contracts implemented in:

- Repository: `https://github.com/telecmi/piopiyai_voice_orchestrator`
- Branch: `development`
- Router registration source: `server.js`

Recommended import path for voice SDK consumers:

- `from piopiy_voice import ...`

## Endpoint Mapping

| API Endpoint | Server Route | SDK Method |
|---|---|---|
| AI Agent call | `POST /v3/voice/ai/call` | `client.ai.call(...)` |
| Voice direct call (convenience) | `POST /v3/voice/pcmo/call` | `client.voice.call(...)` |
| Voice direct transfer (convenience) | `POST /v3/voice/pcmo/transfer` | `client.voice.transfer(...)` |
| Hangup call | `POST /v3/voice/call/hangup` | `client.voice.hangup(...)` |
| PCMO call | `POST /v3/voice/pcmo/call` | `client.pcmo.call(...)` |
| PCMO transfer | `POST /v3/voice/pcmo/transfer` | `client.pcmo.transfer(...)` |
| Flow call | `POST /v3/voice/flow/call` | `client.flow.call(...)` |

## New SDK Package Structure

```text
piopiy/
  __init__.py
  voice/
    __init__.py
    client.py          # RestClient and resource wiring
    http.py            # shared HTTP session, retries, error mapping
    exceptions.py      # SDK exception types
    validators.py      # client-side schema validation
    ai_agent.py        # /voice/ai/call
    hangup.py          # /voice/call/hangup
    pcmo.py            # /voice/pcmo/call + /voice/pcmo/transfer
    flow.py            # /voice/flow/call
    pipeline.py        # pipeline action helpers + fluent builder
```

## Client Surface

```python
client = RestClient(token="...")

client.ai.call(...)
client.ai.transfer(...)
client.ai.hangup(...)
client.voice.call(...)
client.voice.transfer(...)
client.voice.hangup(...)
client.pcmo.call(...)
client.pcmo.transfer(...)
client.flow.call(...)
```

### AI Convenience Failover

`client.ai.call(...)` now supports optional failover fields:

- `app_id` (required when failover enabled)
- `failover` object

When `failover` is passed, SDK internally:

1. Generates a PCMO `connect` pipeline with primary `agent_id` + failover agent.
2. Sends request to `/voice/pcmo/call`.

When `failover` is not passed, SDK uses `/voice/ai/call` as normal.

Additional AI convenience aliases:

- `client.ai.transfer(...)` -> internally calls `/voice/pcmo/transfer`
- `client.ai.hangup(...)` -> internally calls `/voice/call/hangup`

`client.ai.transfer(...)` uses the same PCMO pipeline structure as `client.pcmo.transfer(...)`.
It accepts:

1. `pipeline` as `list[dict]`.
2. `pipeline` as `PipelineBuilder` (recommended to avoid raw JSON).

### Voice Convenience Surface

`client.voice` exposes a direct convenience layer similar to `client.ai`:

- `client.voice.call(...)` -> internally posts to `/voice/pcmo/call`
- `client.voice.transfer(...)` -> internally posts to `/voice/pcmo/transfer`
- `client.voice.hangup(...)` -> internally posts to `/voice/call/hangup`

`client.voice.transfer(...)` accepts `pipeline` as either `list[dict]` or `PipelineBuilder`.

`client.voice.call(...)` supports two input styles:

1. Preferred:
   - `call_options`
   - `connect = {strategy, options, metadata}`
2. Backward-compatible legacy:
   - `options`, `strategy`, `connect_options`, `metadata`

Important compatibility rules:

- `call_options` and `options` cannot be used together.
- `connect` cannot be combined with legacy `strategy/connect_options/metadata`.
- Unknown keys in `connect` are rejected.

## Request Validation Coverage

Validation mirrors the server Ajv schemas and endpoint constraints.

### Common Types

- E.164-like phone regex: `^[1-9][0-9]{6,15}$`
- UUID fields validated for RFC-4122 format.
- `variables` / `metadata` key regex: `^[A-Za-z_][A-Za-z0-9_]*$`
- URL callback pattern: `^https?://`

### AI Call (`/voice/ai/call`)

Required fields:

- `caller_id: string (phone)`
- `to_number: string (phone)`
- `agent_id: string (uuid)`

Optional:

- `options.max_duration_sec: int [30, 7200]`
- `options.record: bool`
- `options.ring_timeout_sec: int [5, 120]`
- `variables: object<string, string|number|boolean>`

AI convenience failover inputs:

- `app_id: string` (required with failover)
- `failover.agent_id: string` (failover agent uuid)
- `failover.strategy: simultaneous|sequential`
- `failover.max_duration_sec: int [10, 7200]`
- `failover.ring_timeout_sec: int [5, 120]`
- `failover.machine_detection: bool`
- `failover.recording.enabled: bool`
- `failover.recording.channels: dual|single`
- `failover.recording.format: mp3|wav`
- `failover.waiting_music: string`
- `failover.metadata: object<string, string|number|boolean>`

### Voice Direct Call Convenience (`client.voice.call` -> `/voice/pcmo/call`)

Required inputs:

- `caller_id: string (phone)`
- `to_number: string (phone)`
- `app_id: string`

Optional preferred inputs:

- `call_options.max_duration_sec: int [30, 7200]`
- `call_options.record: bool`
- `call_options.ring_timeout_sec: int [5, 120]`
- `variables: object<string, string|number|boolean>`
- `connect.strategy: simultaneous|sequential`
- `connect.options`: same shape as PCMO `connect.params.options`
- `connect.metadata: object<string, string|number|boolean>`

Optional legacy-compatible inputs:

- `options` (same as `call_options`)
- `strategy`
- `connect_options`
- `metadata`

Conflict checks:

- `call_options` + `options` is invalid.
- `connect` + (`strategy` or `connect_options` or `metadata`) is invalid.

### Hangup (`/voice/call/hangup`)

Required:

- `call_id: string (uuid)`

Optional:

- `cause: string (1-64)`
- `reason: string (1-256)`

### PCMO Call (`/voice/pcmo/call`)

Required:

- `caller_id: string (phone)`
- `to_number: string (phone)`
- `app_id: string`
- `pipeline: action[] (min 1)`

Optional:

- `agent_id: string (uuid)`
- `options` (same as AI call)
- `variables` (same as AI call)

### Flow Call (`/voice/flow/call`)

Required:

- `flow_id: string (uuid)`
- `org_id: string (uuid)`
- `caller_id: string (phone)`
- `to_number: string (phone)`
- `app_id: string`

Optional:

- `options` (same as AI call)
- `variables` (same as AI call)

### PCMO Transfer (`/voice/pcmo/transfer`)

Required:

- `call_id: string (uuid)`
- `pipeline: action[] (min 1)`

### Voice Direct Transfer Convenience (`client.voice.transfer` -> `/voice/pcmo/transfer`)

Required:

- `call_id: string (uuid)`
- `pipeline: action[] (min 1)` or `PipelineBuilder`

## Pipeline Action Coverage

All validated actions from `development` branch schemas are supported.

### `connect`

Required:

- `action: "connect"`
- `params.caller_id`
- `endpoints[]`

Supported params:

- `strategy: "simultaneous" | "sequential"`
- `caller_id: phone`
- `options.max_duration_sec: int [10, 7200]`
- `options.ring_timeout_sec: int [5, 120]`
- `options.machine_detection: bool`
- `options.recording.enabled: bool`
- `options.recording.channels: "dual" | "single"`
- `options.recording.format: "mp3" | "wav"`
- `options.waiting_music: string`
- `metadata: object<string, string|number|boolean>`

Endpoint variants:

- `type=pstn` requires `number`
- `type=sip` requires `uri`
- `type=agent` requires `id (uuid)`

Business rules mirrored from server handlers:

- Maximum 2 agent endpoints.
- Agent endpoints must be at the end of the endpoint list.

### `play`

- `action: "play"`
- `file_name: string`

### `play_get_input`

Required:

- `action: "play_get_input"`
- `prompt`
- `input` (`dtmf`, `speech`, or both; unique)
- `on_result`

Prompt:

- `type=file` requires `file_name`
- `type=say` requires `say`, `language`, `voice_id`, `speed[0.5,2.0]`

Optional blocks:

- `dtmf` (min/max digits, finish key, timeouts, flush)
- `retries.max`
- `retries.no_input_prompt`
- `retries.invalid_prompt`

On-result:

- `type=url` requires `url`
- `type=pcmo` requires `ref`

### `input`

- `action: "input"`
- optional `dtmf`
- required `on_result` (`url` or `pcmo`)

### `param`

- `action: "param"`
- `data` max 10 keys
- key regex: `^[A-Za-z_][A-Za-z0-9_]*$`
- value type: `string(max 256)` | `number` | `boolean`

### `record`

- `action: "record"`
- optional `format: mp3|wav`
- optional `channels: single|dual`

### `hangup`

- `action: "hangup"`

## Error Model

SDK raises structured exceptions:

- `PiopiyValidationError`: client payload invalid before network call
- `PiopiyNetworkError`: timeout / transport failures
- `PiopiyAPIError`: API returned non-2xx (`status_code`, `payload` available)

## Reliability

- Shared `requests.Session`
- Retry-enabled POST transport for transient failures (429/5xx)
- Configurable `base_url`, `timeout`, `max_retries`, `backoff_factor`

## Builder Helpers

`piopiy.voice.pipeline` provides:

- `PipelineBuilder`
- `connect_action`, `play_action`, `play_get_input_action`, `param_action`, `record_action`, `hangup_action`, `input_action`

These helpers create schema-aligned payload objects and can be combined with SDK validation for safe request construction.
