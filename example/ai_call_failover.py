import os

from piopiy_voice import RestClient


def main() -> None:
    token = os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN")
    client = RestClient(token=token)

    response = client.ai.call(
        caller_id="919999999999",
        to_number="918888888888",
        agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
        app_id="your_app_id",
        failover={
            "agent_id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2",
            "strategy": "sequential",
            "ring_timeout_sec": 20,
            "machine_detection": True,
        },
        options={
            "max_duration_sec": 600,
            "record": True,
            "ring_timeout_sec": 40,
        },
    )

    print(response)


if __name__ == "__main__":
    main()
