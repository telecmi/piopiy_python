from piopiy_voice import param_action


def main() -> None:
    action = param_action({"customer_id": "CUST-1001", "is_vip": True, "score": 95})
    print(action)


if __name__ == "__main__":
    main()
