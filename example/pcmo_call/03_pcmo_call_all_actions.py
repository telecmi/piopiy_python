"""PCMO Example 03: pcmo.call with all pipeline actions."""

import os

from piopiy_voice import PipelineBuilder, RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    pipeline = (
        PipelineBuilder()
        .param({"customer_id": "CUST-1001", "is_vip": True, "score": 97})
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
                    "journey": "pcmo_call",
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
        .build()
    )

    response = client.pcmo.call(
        caller_id="919999999999",
        to_number="918888888888",
        app_id="your_app_id",
        pipeline=pipeline,
        options={
            "max_duration_sec": 600,
            "record": True,
            "ring_timeout_sec": 45,
        },
        variables={
            "source": "sdk",
            "campaign": "pcmo_all_actions",
        },
        agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6",
    )
    print(response)


if __name__ == "__main__":
    main()
