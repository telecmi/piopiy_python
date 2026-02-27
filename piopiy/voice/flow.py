"""Flow call resource."""

from typing import Any, Dict, Optional

from .http import HTTPClient
from .validators import validate_flow_call_request


class Flow:
    """Resource client for `/voice/flow/call`."""

    def __init__(self, http_client: HTTPClient):
        self._http = http_client

    def call(
        self,
        flow_id: str,
        org_id: str,
        caller_id: str,
        to_number: str,
        app_id: str,
        options: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Initiate a call based on a server-side flow pipeline."""
        payload = {
            "flow_id": flow_id,
            "org_id": org_id,
            "caller_id": caller_id,
            "to_number": to_number,
            "app_id": app_id,
        }

        if options is not None:
            payload["options"] = options

        if variables is not None:
            payload["variables"] = variables

        validate_flow_call_request(payload)
        return self._http.post("/voice/flow/call", payload)
