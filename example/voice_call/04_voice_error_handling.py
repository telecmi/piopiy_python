"""Voice Call Example 04: production-style error handling."""

import os

from piopiy_voice import PiopiyAPIError, PiopiyNetworkError, PiopiyValidationError, RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    try:
        response = client.voice.call(
            caller_id="919999999999",
            to_number="918888888888",
            app_id="your_app_id",
            connect={"strategy": "invalid_strategy"},
        )
        print(response)
    except PiopiyValidationError as exc:
        print("Validation failed:", exc)
    except PiopiyAPIError as exc:
        print("API failed:", exc.status_code, exc.payload)
    except PiopiyNetworkError as exc:
        print("Network failed:", exc)


if __name__ == "__main__":
    main()
