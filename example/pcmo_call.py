import os

from piopiy_voice import PipelineBuilder, RestClient


def main() -> None:
    token = os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN")
    client = RestClient(token=token)

    pipeline = (
        PipelineBuilder()
        .play("https://example.com/welcome.wav")
        .connect(
            params={
                "caller_id": "919999999999",
                "options": {
                    "ring_timeout_sec": 30,
                    "recording": {
                        "enabled": True,
                        "channels": "dual",
                        "format": "mp3",
                    },
                },
            },
            endpoints=[
                {"type": "pstn", "number": "918888888888"},
            ],
        )
        .build()
    )

    response = client.pcmo.call(
        caller_id="919999999999",
        to_number="918888888888",
        app_id="your_app_id",
        pipeline=pipeline,
        options={"max_duration_sec": 900, "record": True, "ring_timeout_sec": 45},
        variables={"journey": "ivr"},
    )

    print(response)


if __name__ == "__main__":
    main()
