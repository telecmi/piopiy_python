import os

from piopiy_voice import RestClient


def main() -> None:
    token = os.getenv("PIOPIY_TOKEN", "YOUR_BEARER_TOKEN")
    client = RestClient(token=token)

    response = client.flow.call(
        flow_id="7f4d89c7-3485-45c5-9016-f45a47cd885c",
        org_id="f89dd77d-c226-4ff2-b88c-6d7e4f5a88e2",
        caller_id="919999999999",
        to_number="918888888888",
        app_id="your_app_id",
    )

    print(response)


if __name__ == "__main__":
    main()
