"""AI Agent Example 01: SDK client setup.

Use this as the base for all other examples.
"""

import os

from piopiy_voice import RestClient


def build_client() -> RestClient:
    return RestClient(
        token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"),
        base_url=os.getenv("PIOPIY_BASE_URL", "https://rest.piopiy.com/v3"),
        timeout=10,
        max_retries=2,
        backoff_factor=0.4,
    )


def main() -> None:
    client = build_client()
    print("Client initialized:", type(client).__name__)


if __name__ == "__main__":
    main()
