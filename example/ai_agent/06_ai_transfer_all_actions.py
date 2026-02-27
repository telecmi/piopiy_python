"""AI Agent Example 06: ai.transfer pipeline with all supported PCMO actions."""

import os

from piopiy_voice import RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    pipeline = (
        client.ai.pipeline()
        .param({"customer_id": "CUST-1001", "case_open": True, "risk_score": 71})
        .play("https://example.com/welcome.wav")
        .play_get_input(
            prompt={
                "type": "say",
                "say": "Press 1 for sales or 2 for support.",
                "language": "en-US",
                "voice_id": "female",
                "speed": 1.0,
            },
            input_modes=["dtmf", "speech"],
            dtmf={
                "min_digits": 1,
                "max_digits": 1,
                "finish_on_key": "#",
                "first_digit_timeout": 5,
                "inter_digit_timeout": 2,
                "flush_buffer": True,
            },
            retries={
                "max": 2,
                "no_input_prompt": {
                    "type": "say",
                    "say": "I did not get your input.",
                    "language": "en-US",
                    "voice_id": "female",
                    "speed": 1.0,
                },
                "invalid_prompt": {
                    "type": "file",
                    "file_name": "https://example.com/invalid.wav",
                },
            },
            on_result={"type": "url", "url": "https://example.com/input-result"},
        )
        .input(
            dtmf={
                "min_digits": 1,
                "max_digits": 4,
                "finish_on_key": "#",
                "first_digit_timeout": 5,
                "inter_digit_timeout": 2,
                "flush_buffer": True,
            },
            on_result={"type": "pcmo", "ref": "next_step_pipeline_ref"},
        )
        .record(fmt="mp3", channels="dual")
        .connect(
            params={
                "strategy": "sequential",
                "caller_id": "919999999999",
                "options": {
                    "max_duration_sec": 120,
                    "ring_timeout_sec": 20,
                    "machine_detection": True,
                    "recording": {
                        "enabled": True,
                        "channels": "dual",
                        "format": "mp3",
                    },
                    "waiting_music": "https://example.com/hold.wav",
                },
                "metadata": {
                    "segment": "priority",
                    "attempt": 1,
                    "is_callback": False,
                },
            },
            endpoints=[
                {"type": "pstn", "number": "918888888887"},
                {"type": "sip", "uri": "sip:agent@example.com", "headers": {"X-Tenant": "acme"}},
                {"type": "agent", "id": "bdd32bcb-767c-40a5-be4a-5f45eeb348a6"},
                {"type": "agent", "id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2"},
            ],
        )
        .hangup()
    )

    response = client.ai.transfer(
        call_id="c4d0e5f6-a7b8-12c9-d3e4-f56789012345",
        pipeline=pipeline,
    )
    print(response)


if __name__ == "__main__":
    main()
