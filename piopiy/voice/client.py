from .ai_agent import AIAgent
from .hangup import Hangup
import requests
from typing import Optional, Dict, Any

class RestClient:
    """
    Client for the Piopiy AI Agent API.
    """

    def __init__(self, token):
        """
        Initialize the RestClient.

        Args:
            token (str): The Bearer token for authentication.

        Raises:
            ValueError: If the token is missing.
        """
        if not token:
             raise ValueError('A valid Bearer token is required.')
        
        self.token = token
        self.ai = AIAgent(token)
        self.voice = Hangup(token)
