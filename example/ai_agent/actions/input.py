from piopiy_voice import input_action


def main() -> None:
    action = input_action(
        dtmf={"min_digits": 1, "max_digits": 4, "finish_on_key": "#"},
        on_result={"type": "pcmo", "ref": "next_pipeline_ref"},
    )
    print(action)


if __name__ == "__main__":
    main()
