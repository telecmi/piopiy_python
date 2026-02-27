"""Top-level Piopiy REST client."""

from .ai_agent import AIAgent
from .flow import Flow
from .hangup import Hangup
from .http import HTTPClient
from .pcmo import PCMO

DEFAULT_BASE_URL = "https://rest.piopiy.com/v3"


class RestClient:
    """Production-ready Piopiy SDK client.

    Attributes:
        ai: AI Agent calls resource.
        voice: Voice convenience resource (`call`, `transfer`, `hangup`).
        pcmo: PCMO resources (`call`, `transfer`).
        flow: Flow resource (`call`).
    """

    def __init__(
        self,
        token: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 10,
        max_retries: int = 2,
        backoff_factor: float = 0.4,
    ):
        self.token = token
        self.base_url = base_url

        self._http = HTTPClient(
            token=token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
        )

        self.ai = AIAgent(self._http)
        self.voice = Hangup(self._http)
        self.pcmo = PCMO(self._http)
        self.flow = Flow(self._http)
