"""Compatibility import path for the voice SDK.

Recommended import path:
    from piopiy_voice import RestClient
"""

from piopiy import (
    PipelineBuilder,
    PiopiyAPIError,
    PiopiyError,
    PiopiyNetworkError,
    PiopiyValidationError,
    RestClient,
    connect_action,
    hangup_action,
    input_action,
    param_action,
    play_action,
    play_get_input_action,
    record_action,
)

__all__ = [
    "RestClient",
    "PiopiyError",
    "PiopiyValidationError",
    "PiopiyNetworkError",
    "PiopiyAPIError",
    "PipelineBuilder",
    "connect_action",
    "play_action",
    "play_get_input_action",
    "param_action",
    "record_action",
    "hangup_action",
    "input_action",
]
