"""AI Agent Example 05: ai.transfer with PCMO-style pipeline builder (basic)."""

import os

from piopiy_voice import RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    pipeline = (
        client.ai.pipeline()
        .play("https://example.com/transfer_notice.wav")
        .connect(
            params={
                "caller_id": "919999999999",
                "strategy": "sequential",
                "options": {"ring_timeout_sec": 20},
            },
            endpoints=[
                {"type": "agent", "id": "bdd32bcb-767c-40a5-be4a-5f45eeb348a6"},
                {"type": "agent", "id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2"},
            ],
        )
    )

    response = client.ai.transfer(
        call_id="c4d0e5f6-a7b8-12c9-d3e4-f56789012345",
        pipeline=pipeline,
    )
    print(response)


if __name__ == "__main__":
    main()
