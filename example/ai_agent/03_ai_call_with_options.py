"""AI Agent Example 03: ai.call with options and variables."""

import os

from piopiy_voice import RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    response = client.ai.call(
        caller_id="919999999999",
        to_number="918888888888",
        agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
        options={
            "max_duration_sec": 600,
            "record": True,
            "ring_timeout_sec": 40,
        },
        variables={
            "customer_name": "Kumar",
            "ticket_id": "TCK-1001",
            "score": 97,
            "is_vip": True,
        },
    )
    print(response)


if __name__ == "__main__":
    main()
