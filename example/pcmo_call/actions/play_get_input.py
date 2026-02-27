from piopiy_voice import play_get_input_action


def main() -> None:
    action = play_get_input_action(
        prompt={
            "type": "say",
            "say": "Press 1 for sales",
            "language": "en-US",
            "voice_id": "female",
            "speed": 1.0,
        },
        input_modes=["dtmf"],
        dtmf={"max_digits": 1, "first_digit_timeout": 5},
        retries={"max": 1},
        on_result={"type": "url", "url": "https://example.com/input-result"},
    )
    print(action)


if __name__ == "__main__":
    main()
