"""AI Agent Example 09: production-style error handling."""

import os

from piopiy_voice import PiopiyAPIError, PiopiyNetworkError, PiopiyValidationError, RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    try:
        response = client.ai.call(
            caller_id="919999999999",
            to_number="918888888888",
            agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
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
