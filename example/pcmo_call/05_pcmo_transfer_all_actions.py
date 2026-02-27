"""PCMO Example 05: pcmo.transfer with all pipeline actions."""

import os

from piopiy_voice import PipelineBuilder, RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    pipeline = (
        PipelineBuilder()
        .param({"transfer_reason": "escalation", "priority": 2, "is_escalation": True})
        .play("https://example.com/transfer_notice.wav")
        .play_get_input(
            prompt={
                "type": "say",
                "say": "Press 1 for billing or 2 for technical support.",
                "language": "en-US",
                "voice_id": "female",
                "speed": 1.0,
            },
            input_modes=["dtmf"],
            dtmf={"min_digits": 1, "max_digits": 1, "first_digit_timeout": 5},
            retries={"max": 1},
            on_result={"type": "url", "url": "https://example.com/transfer-result"},
        )
        .input(
            dtmf={"min_digits": 1, "max_digits": 4, "finish_on_key": "#"},
            on_result={"type": "pcmo", "ref": "branch_after_input"},
        )
        .record(fmt="wav", channels="single")
        .connect(
            params={
                "caller_id": "919999999999",
                "strategy": "sequential",
                "options": {
                    "ring_timeout_sec": 20,
                    "machine_detection": True,
                    "recording": {"enabled": True, "channels": "dual", "format": "mp3"},
                },
                "metadata": {"queue": "support", "attempt": 1},
            },
            endpoints=[
                {"type": "pstn", "number": "918888888887"},
                {"type": "agent", "id": "bdd32bcb-767c-40a5-be4a-5f45eeb348a6"},
            ],
        )
        .hangup()
        .build()
    )

    response = client.pcmo.transfer(
        call_id="c4d0e5f6-a7b8-12c9-d3e4-f56789012345",
        pipeline=pipeline,
    )
    print(response)


if __name__ == "__main__":
    main()
