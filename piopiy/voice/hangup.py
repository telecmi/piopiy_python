"""
Piopiy Hangup Module.

This module provides the `Hangup` class for terminating calls via the Piopiy Voice API.
"""

import requests
from typing import Optional, Dict, Any

# Constants for API Endpoints
API_BASE_URL = "https://rest.piopiy.com/v3"
ENDPOINT_HANGUP = f"{API_BASE_URL}/voice/call/hangup"


class Hangup:
    """
    Hangup handles the termination of calls.
    """

    def __init__(self, token: str):
        """
        Initialize the Hangup client.

        Args:
            token (str): The Bearer token for authentication.
        """
        if not token or not isinstance(token, str):
            raise ValueError("A valid Bearer token is required.")

        self.auth_header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def hangup(self, 
               call_id: str, 
               cause: str = "NORMAL_CLEARING", 
               reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Terminate (hangup) an active call.

        Args:
            call_id (str): The unique identifier of the call to hang up.
            cause (str, optional): The cause for hanging up. Defaults to "NORMAL_CLEARING".
            reason (str, optional): Additional reason description.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        payload = {
            "call_id": call_id,
            "cause": cause
        }

        if reason:
            payload["reason"] = reason

        try:
            response = requests.post(
                ENDPOINT_HANGUP,
                headers=self.auth_header,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise
