"""Voice Call Example 01: normal direct call API (no pipeline input required)."""

import os

from piopiy_voice import RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    response = client.voice.call(
        caller_id="919999999999",
        to_number="918888888888",
        app_id="your_app_id",
        call_options={
            "max_duration_sec": 600,
            "record": True,
            "ring_timeout_sec": 40,
        },
        variables={
            "customer_name": "Kumar",
            "source": "direct_call_api",
        },
        connect={
            "strategy": "sequential",
            "options": {
                "ring_timeout_sec": 20,
                "machine_detection": True,
                "recording": {
                    "enabled": True,
                    "channels": "dual",
                    "format": "mp3",
                },
                "waiting_music": "https://example.com/waiting_music.wav",
            },
            "metadata": {
                "campaign": "normal_outbound",
                "priority": 1,
                "is_callback": False,
            },
        },
    )

    print(response)


if __name__ == "__main__":
    main()
