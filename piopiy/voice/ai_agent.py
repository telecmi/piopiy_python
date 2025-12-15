"""
Piopiy AI Agent Module.

This module provides the `AIAgent` class for interacting with the Piopiy Voice AI API.
It supports initiating AI calls and terminating them.
"""

import requests
import json
from enum import Enum
from typing import Optional, Dict, Any, Union

# Constants for API Endpoints
API_BASE_URL = "https://rest.piopiy.com/v3"
ENDPOINT_AI_CALL = f"{API_BASE_URL}/voice/ai/call"



class AIAgent:
    """
    AIAgent handles interactions with the Piopiy AI Voice API.

    Attributes:
        auth_header (dict): The authorization header with the Bearer token.
    """

    def __init__(self, token: str):
        """
        Initialize the AIAgent client.

        Args:
            token (str): The Bearer token for authentication.

        Raises:
            ValueError: If the token is empty or invalid.
        """
        if not token or not isinstance(token, str):
            raise ValueError("A valid Bearer token is required.")
        
        self.auth_header = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def call(self, 
             caller_id: str, 
             to_number: str, 
             agent_id: str, 
             options: Optional[Dict[str, Any]] = None, 
             variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Initiate an AI Agent call.

        Args:
            caller_id (str): The number calling from (CLI). Must match `^[1-9][0-9]{6,15}$`.
            to_number (str): The destination number. Must match `^[1-9][0-9]{6,15}$`.
            agent_id (str): The UUID of the AI agent to use.
            options (dict, optional): Call options:
                - `max_duration_sec` (int): 30-7200.
                - `record` (bool): generic record flag.
                - `ring_timeout_sec` (int): 5-120.
            variables (dict, optional): Custom variables. keys match `^[A-Za-z_][A-Za-z0-9_]*$`. values: str|int|bool.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        payload = {
            "caller_id": caller_id,
            "to_number": to_number,
            "agent_id": agent_id
        }

        if options:
            payload["options"] = options
        
        if variables:
            payload["variables"] = variables

        try:
            response = requests.post(
                ENDPOINT_AI_CALL,
                headers=self.auth_header,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # In a production SDK, you might want to wrap this in a custom SDK exception
            # For now, we print and re-raise or logging is better.
            # print(f"Error initiating AI call: {e}") 
            raise



