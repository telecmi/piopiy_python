import os
import sys
from piopiy import RestClient

# Get token from env or replace with your actual token
token = os.getenv("PIOPIY_TOKEN") or "YOUR_BEARER_TOKEN"

client = RestClient(token=token)

print(f"Terminating call...")

try:
    # Replace with the actual Call UUID you want to hangup
    call_id = "your_active_call_uuid"

    response = client.voice.hangup(
        call_id=call_id,
        cause="NORMAL_CLEARING",
        reason="Consultation done"
    )
    print("Response:", response)
except Exception as e:
    print("Error:", e)
