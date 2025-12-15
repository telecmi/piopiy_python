import os
import sys
from piopiy import RestClient

# Get token from env or replace with your actual token
token = os.getenv("PIOPIY_TOKEN") or "YOUR_BEARER_TOKEN"

if token == "YOUR_BEARER_TOKEN":
    print("Warning: Using placeholder token. Set PIOPIY_TOKEN env var or update script.")

client = RestClient(token=token)

print(f"Initiating call...")

try:
    response = client.ai.call(
        caller_id="919999999999",      # Your Piopiy Number
        to_number="918888888888",      # Destination Number
        agent_id="bdd32bcb-767c-40a5-be4a-5f45eeb348a6", # Your AI Agent UUID
        options={
            "max_duration_sec": 600,
            "record": True,
            "ring_timeout_sec": 40
        },
        variables={
            "customer_id": "CUST_1001",
            "campaign": "summer_sale_2025"
        }
    )
    print("Response:", response)
except Exception as e:
    print("Error:", e)
