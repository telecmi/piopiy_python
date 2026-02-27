from piopiy_voice import record_action


def main() -> None:
    action = record_action(fmt="mp3", channels="dual")
    print(action)


if __name__ == "__main__":
    main()
