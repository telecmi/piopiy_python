"""PCMO Example 01: client setup."""

import os

from piopiy_voice import RestClient


def get_client() -> RestClient:
    return RestClient(
        token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"),
        base_url=os.getenv("PIOPIY_BASE_URL", "https://rest.piopiy.com/v3"),
        timeout=10,
        max_retries=2,
        backoff_factor=0.4,
    )


def main() -> None:
    client = get_client()
    print(client)


if __name__ == "__main__":
    main()
