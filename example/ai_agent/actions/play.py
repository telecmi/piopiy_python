from piopiy_voice import play_action


def main() -> None:
    action = play_action("https://example.com/welcome.wav")
    print(action)


if __name__ == "__main__":
    main()
