# Error Handling

## What
Use typed SDK exceptions for production-safe handling.

## Why
Separates input errors, API/business errors, and network issues.

## Example

```python
from piopiy_voice import PiopiyAPIError, PiopiyNetworkError, PiopiyValidationError

try:
    response = client.pcmo.call(...)
except PiopiyValidationError as exc:
    print("Validation failed:", exc)
except PiopiyAPIError as exc:
    print("API failed:", exc.status_code, exc.payload)
except PiopiyNetworkError as exc:
    print("Network failed:", exc)
```

## Exception Types

| Exception | Trigger | Action |
|---|---|---|
| `PiopiyValidationError` | Local payload invalid. | Fix request parameters before retry. |
| `PiopiyAPIError` | API returned non-2xx. | Inspect `status_code` + `payload`. |
| `PiopiyNetworkError` | Timeout/connection issue. | Retry with backoff and monitor transport. |
