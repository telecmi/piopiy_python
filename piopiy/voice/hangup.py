"""Voice convenience resource."""

from typing import Any, Dict, List, Optional, Union

from .exceptions import PiopiyValidationError
from .http import HTTPClient
from .pipeline import PipelineBuilder
from .validators import validate_hangup_request, validate_pcmo_call_request, validate_transfer_request


class Hangup:
    """Voice resource for direct call, transfer, and hangup APIs.

    `call(...)` is a convenience direct-call API for one-number calling.
    It internally builds a PCMO connect pipeline, so users do not need to
    pass pipeline JSON.
    """

    def __init__(self, http_client: HTTPClient):
        self._http = http_client

    def call(
        self,
        caller_id: str,
        to_number: str,
        app_id: str,
        call_options: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        connect: Optional[Dict[str, Any]] = None,
        # Backward-compatible aliases (deprecated)
        options: Optional[Dict[str, Any]] = None,
        strategy: Optional[str] = None,
        connect_options: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a normal direct call to one number.

        This convenience API internally routes through `/voice/pcmo/call`
        with a generated `connect` pipeline:
        - endpoint type: `pstn`
        - endpoint number: `to_number`

        Preferred input model:
        - `call_options`: top-level call options
        - `connect`: object containing connect leg controls:
          - `strategy`
          - `options`
          - `metadata`
        """
        if call_options is not None and options is not None:
            raise PiopiyValidationError("Use either call_options or options, not both.", field="call_options")

        if connect is not None and not isinstance(connect, dict):
            raise PiopiyValidationError("connect must be an object.", field="connect")

        if connect is not None and any(value is not None for value in [strategy, connect_options, metadata]):
            raise PiopiyValidationError(
                "Use either connect object or legacy strategy/connect_options/metadata arguments, not both.",
                field="connect",
            )

        normalized_call_options = call_options if call_options is not None else options

        normalized_connect: Dict[str, Any] = dict(connect or {})
        if "strategy" not in normalized_connect:
            normalized_connect["strategy"] = strategy if strategy is not None else "sequential"
        if connect_options is not None:
            normalized_connect["options"] = connect_options
        if metadata is not None:
            normalized_connect["metadata"] = metadata

        allowed_connect_keys = {"strategy", "options", "metadata"}
        extra_keys = sorted(set(normalized_connect.keys()).difference(allowed_connect_keys))
        if extra_keys:
            raise PiopiyValidationError(
                "Unknown connect field(s): {0}".format(", ".join(extra_keys)),
                field="connect",
            )

        params: Dict[str, Any] = {
            "caller_id": caller_id,
            "strategy": normalized_connect["strategy"],
        }
        if "options" in normalized_connect:
            params["options"] = normalized_connect["options"]
        if "metadata" in normalized_connect:
            params["metadata"] = normalized_connect["metadata"]

        payload: Dict[str, Any] = {
            "caller_id": caller_id,
            "to_number": to_number,
            "app_id": app_id,
            "pipeline": [
                {
                    "action": "connect",
                    "params": params,
                    "endpoints": [
                        {
                            "type": "pstn",
                            "number": to_number,
                        }
                    ],
                }
            ],
        }

        if normalized_call_options is not None:
            payload["options"] = normalized_call_options
        if variables is not None:
            payload["variables"] = variables

        validate_pcmo_call_request(payload)
        return self._http.post("/voice/pcmo/call", payload)

    def transfer(
        self,
        call_id: str,
        pipeline: Union[List[Dict[str, Any]], PipelineBuilder],
    ) -> Dict[str, Any]:
        """Transfer an active call.

        This is a convenience alias over `/voice/pcmo/transfer`.
        `pipeline` accepts either:
        - `list[dict]` PCMO actions
        - `PipelineBuilder`
        """
        if isinstance(pipeline, PipelineBuilder):
            pipeline = pipeline.build()

        payload = {
            "call_id": call_id,
            "pipeline": pipeline,
        }
        validate_transfer_request(payload)
        return self._http.post("/voice/pcmo/transfer", payload)

    @staticmethod
    def pipeline() -> PipelineBuilder:
        """Create a PCMO pipeline builder for voice transfer/call scenarios."""
        return PipelineBuilder()

    def hangup(self, call_id: str, cause: str = "NORMAL_CLEARING", reason: Optional[str] = None) -> Dict[str, Any]:
        """Terminate an active call."""
        payload = {
            "call_id": call_id,
            "cause": cause,
        }

        if reason is not None:
            payload["reason"] = reason

        validate_hangup_request(payload)
        return self._http.post("/voice/call/hangup", payload)
