"""Helpers for building PCMO pipeline actions."""

from typing import Any, Dict, Iterable, List, Optional


def connect_action(params: Dict[str, Any], endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "action": "connect",
        "params": params,
        "endpoints": endpoints,
    }


def play_action(file_name: str) -> Dict[str, Any]:
    return {
        "action": "play",
        "file_name": file_name,
    }


def play_get_input_action(
    prompt: Dict[str, Any],
    input_modes: List[str],
    on_result: Dict[str, Any],
    dtmf: Optional[Dict[str, Any]] = None,
    retries: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    action = {
        "action": "play_get_input",
        "prompt": prompt,
        "input": input_modes,
        "on_result": on_result,
    }

    if dtmf is not None:
        action["dtmf"] = dtmf

    if retries is not None:
        action["retries"] = retries

    return action


def param_action(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "action": "param",
        "data": data,
    }


def record_action(fmt: Optional[str] = None, channels: Optional[str] = None) -> Dict[str, Any]:
    action = {"action": "record"}

    if fmt is not None:
        action["format"] = fmt

    if channels is not None:
        action["channels"] = channels

    return action


def hangup_action() -> Dict[str, Any]:
    return {"action": "hangup"}


def input_action(on_result: Dict[str, Any], dtmf: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    action = {
        "action": "input",
        "on_result": on_result,
    }

    if dtmf is not None:
        action["dtmf"] = dtmf

    return action


class PipelineBuilder:
    """Fluent builder for PCMO pipelines."""

    def __init__(self, actions: Optional[Iterable[Dict[str, Any]]] = None):
        self._actions = list(actions or [])

    def connect(self, params: Dict[str, Any], endpoints: List[Dict[str, Any]]) -> "PipelineBuilder":
        self._actions.append(connect_action(params=params, endpoints=endpoints))
        return self

    def play(self, file_name: str) -> "PipelineBuilder":
        self._actions.append(play_action(file_name=file_name))
        return self

    def play_get_input(
        self,
        prompt: Dict[str, Any],
        input_modes: List[str],
        on_result: Dict[str, Any],
        dtmf: Optional[Dict[str, Any]] = None,
        retries: Optional[Dict[str, Any]] = None,
    ) -> "PipelineBuilder":
        self._actions.append(
            play_get_input_action(
                prompt=prompt,
                input_modes=input_modes,
                on_result=on_result,
                dtmf=dtmf,
                retries=retries,
            )
        )
        return self

    def param(self, data: Dict[str, Any]) -> "PipelineBuilder":
        self._actions.append(param_action(data=data))
        return self

    def record(self, fmt: Optional[str] = None, channels: Optional[str] = None) -> "PipelineBuilder":
        self._actions.append(record_action(fmt=fmt, channels=channels))
        return self

    def hangup(self) -> "PipelineBuilder":
        self._actions.append(hangup_action())
        return self

    def input(self, on_result: Dict[str, Any], dtmf: Optional[Dict[str, Any]] = None) -> "PipelineBuilder":
        self._actions.append(input_action(on_result=on_result, dtmf=dtmf))
        return self

    def build(self) -> List[Dict[str, Any]]:
        return list(self._actions)

    def clear(self) -> "PipelineBuilder":
        self._actions = []
        return self
