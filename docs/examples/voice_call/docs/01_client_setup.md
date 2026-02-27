# Client Setup

## What
Initialize `RestClient` for voice convenience operations.

## Why
Centralizes auth, timeout, retry, and base URL config in one place.

## Example

```python
import os
from piopiy_voice import RestClient

client = RestClient(
    token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"),
    base_url=os.getenv("PIOPIY_BASE_URL", "https://rest.piopiy.com/v3"),
    timeout=10,
    max_retries=2,
    backoff_factor=0.4,
)
```

## Parameters

| Parameter | Description | Why |
|---|---|---|
| `token` | Bearer token. | Required for authentication. |
| `base_url` | API base URL. | Useful for prod/UAT/local switching. |
| `timeout` | Request timeout in seconds. | Prevents hanging requests. |
| `max_retries` | Retry count for transient failures. | Better reliability on flaky networks. |
| `backoff_factor` | Retry backoff multiplier. | Reduces retry bursts and API pressure. |
