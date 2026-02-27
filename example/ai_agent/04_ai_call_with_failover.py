"""AI Agent Example 04: ai.call with failover (internally routed to PCMO call)."""

import os

from piopiy_voice import RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    response = client.ai.call(
        caller_id="919999999999",
        to_number="918888888888",
        agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",  # primary agent
        app_id="your_app_id",  # required when failover is passed
        failover={
            "agent_id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2",  # failover agent
            "strategy": "sequential",
            "max_duration_sec": 120,
            "ring_timeout_sec": 20,
            "machine_detection": True,
            "recording": {
                "enabled": True,
                "channels": "dual",
                "format": "mp3",
            },
            "waiting_music": "https://example.com/waiting_music.wav",
            "metadata": {
                "transfer_reason": "agent_busy",
                "priority": 2,
                "is_escalation": True,
            },
        },
        options={
            "max_duration_sec": 600,
            "record": True,
            "ring_timeout_sec": 45,
        },
        variables={
            "journey": "voice_assist",
            "source": "sdk",
        },
    )
    print(response)


if __name__ == "__main__":
    main()
