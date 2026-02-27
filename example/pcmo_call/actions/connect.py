from piopiy_voice import connect_action


def main() -> None:
    action = connect_action(
        params={
            "caller_id": "919999999999",
            "strategy": "sequential",
            "options": {
                "ring_timeout_sec": 20,
                "machine_detection": True,
                "recording": {"enabled": True, "channels": "dual", "format": "mp3"},
            },
            "metadata": {"priority": 1},
        },
        endpoints=[
            {"type": "pstn", "number": "918888888887"},
            {"type": "agent", "id": "bdd32bcb-767c-40a5-be4a-5f45eeb348a6"},
            {"type": "agent", "id": "2f2ae3ad-7ff6-4011-b10e-9ca1f8f8d1a2"},
        ],
    )
    print(action)


if __name__ == "__main__":
    main()
