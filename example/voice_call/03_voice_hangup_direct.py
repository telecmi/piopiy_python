"""Voice Call Example 03: direct hangup API from client.voice."""

import os

from piopiy_voice import RestClient


def main() -> None:
    client = RestClient(token=os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN"))

    response = client.voice.hangup(
        call_id="c4d0e5f6-a7b8-12c9-d3e4-f56789012345",
        cause="NORMAL_CLEARING",
        reason="completed",
    )
    print(response)


if __name__ == "__main__":
    main()
