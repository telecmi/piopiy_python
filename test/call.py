from piopiy_voice import PipelineBuilder


def main() -> None:
    pipeline = (
        PipelineBuilder()
        .play("https://example.com/welcome.wav")
        .hangup()
        .build()
    )
    print(pipeline)


if __name__ == "__main__":
    main()
