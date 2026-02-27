"""PCMO call and transfer resources."""

from typing import Any, Dict, List, Optional

from .http import HTTPClient
from .validators import validate_pcmo_call_request, validate_transfer_request


class PCMO:
    """Resource client for `/voice/pcmo/call` and `/voice/pcmo/transfer`."""

    def __init__(self, http_client: HTTPClient):
        self._http = http_client

    def call(
        self,
        caller_id: str,
        to_number: str,
        app_id: str,
        pipeline: List[Dict[str, Any]],
        options: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        agent_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Initiate a PCMO call with a pipeline."""
        payload = {
            "caller_id": caller_id,
            "to_number": to_number,
            "app_id": app_id,
            "pipeline": pipeline,
        }

        if options is not None:
            payload["options"] = options

        if variables is not None:
            payload["variables"] = variables

        if agent_id is not None:
            payload["agent_id"] = agent_id

        validate_pcmo_call_request(payload)
        return self._http.post("/voice/pcmo/call", payload)

    def transfer(self, call_id: str, pipeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Transfer an active call to a new PCMO pipeline."""
        payload = {
            "call_id": call_id,
            "pipeline": pipeline,
        }

        validate_transfer_request(payload)
        return self._http.post("/voice/pcmo/transfer", payload)
