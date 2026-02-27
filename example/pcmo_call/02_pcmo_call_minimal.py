"""PCMO Example 02: minimal pcmo.call."""

import os

from piopiy_voice import PipelineBuilder, RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    pipeline = (
        PipelineBuilder()
        .connect(
            params={"caller_id": "919999999999"},
            endpoints=[{"type": "pstn", "number": "918888888888"}],
        )
        .build()
    )

    response = client.pcmo.call(
        caller_id="919999999999",
        to_number="918888888888",
        app_id="your_app_id",
        pipeline=pipeline,
    )
    print(response)


if __name__ == "__main__":
    main()
