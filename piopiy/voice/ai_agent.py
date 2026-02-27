"""AI agent voice call resource."""

from typing import Any, Dict, List, Optional, Union

from .http import HTTPClient
from .pipeline import PipelineBuilder
from .validators import (
    validate_ai_call_request,
    validate_hangup_request,
    validate_pcmo_call_request,
    validate_transfer_request,
)


class AIAgent:
    """Resource client for `/voice/ai/call`."""

    def __init__(self, http_client: HTTPClient):
        self._http = http_client

    def call(
        self,
        caller_id: str,
        to_number: str,
        agent_id: str,
        options: Optional[Dict[str, Any]] = None,
        variables: Optional[Dict[str, Any]] = None,
        app_id: Optional[str] = None,
        failover: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Initiate an AI agent call.

        Behavior:
        - Standard path (no `failover`): calls `/voice/ai/call`.
        - Failover path (`failover` provided): internally generates a PCMO
          connect pipeline and calls `/voice/pcmo/call`.
        """
        payload = {
            "caller_id": caller_id,
            "to_number": to_number,
            "agent_id": agent_id,
        }

        if options is not None:
            payload["options"] = options

        if variables is not None:
            payload["variables"] = variables

        if app_id is not None:
            payload["app_id"] = app_id

        if failover is not None:
            payload["failover"] = failover

        validate_ai_call_request(payload)

        if failover is None:
            api_payload = {
                "caller_id": caller_id,
                "to_number": to_number,
                "agent_id": agent_id,
            }
            if options is not None:
                api_payload["options"] = options
            if variables is not None:
                api_payload["variables"] = variables
            return self._http.post("/voice/ai/call", api_payload)

        pipeline = self._build_failover_pipeline(
            caller_id=caller_id,
            primary_agent_id=agent_id,
            failover=failover,
        )

        pcmo_payload = {
            "caller_id": caller_id,
            "to_number": to_number,
            "app_id": app_id,
            "pipeline": pipeline,
        }
        if options is not None:
            pcmo_payload["options"] = options
        if variables is not None:
            pcmo_payload["variables"] = variables

        validate_pcmo_call_request(pcmo_payload)
        return self._http.post("/voice/pcmo/call", pcmo_payload)

    def transfer(
        self,
        call_id: str,
        pipeline: Union[List[Dict[str, Any]], PipelineBuilder],
    ) -> Dict[str, Any]:
        """Transfer an active call.

        Use the same PCMO pipeline structure. `pipeline` accepts:
        - `list[dict]` PCMO actions
        - `PipelineBuilder` for non-raw JSON construction
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
        """Create a PCMO pipeline builder for AI transfer/call scenarios."""
        return PipelineBuilder()

    def hangup(self, call_id: str, cause: str = "NORMAL_CLEARING", reason: Optional[str] = None) -> Dict[str, Any]:
        """Hang up an active call.

        This is a convenience wrapper over `/voice/call/hangup`.
        """
        payload = {
            "call_id": call_id,
            "cause": cause,
        }
        if reason is not None:
            payload["reason"] = reason

        validate_hangup_request(payload)
        return self._http.post("/voice/call/hangup", payload)

    @staticmethod
    def _build_failover_pipeline(
        caller_id: str,
        primary_agent_id: str,
        failover: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        params: Dict[str, Any] = {"caller_id": caller_id}

        if "strategy" in failover:
            params["strategy"] = failover["strategy"]

        connect_options: Dict[str, Any] = {}
        for key in ["max_duration_sec", "ring_timeout_sec", "machine_detection", "recording", "waiting_music"]:
            if key in failover:
                connect_options[key] = failover[key]
        if connect_options:
            params["options"] = connect_options

        if "metadata" in failover:
            params["metadata"] = failover["metadata"]

        endpoints = [
            {"type": "agent", "id": primary_agent_id},
            {"type": "agent", "id": failover["agent_id"]},
        ]

        return [
            {
                "action": "connect",
                "params": params,
                "endpoints": endpoints,
            }
        ]
