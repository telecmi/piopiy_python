"""Request validators mirroring the voice orchestrator API schemas."""

import re
from typing import Any, Dict, Iterable, List, Optional, Set
from uuid import UUID

from .exceptions import PiopiyValidationError

_PHONE_RE = re.compile(r"^[1-9][0-9]{6,15}$")
_VAR_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_HTTP_URL_RE = re.compile(r"^https?://")

_ACTIONS = {
    "connect",
    "play",
    "play_get_input",
    "param",
    "record",
    "hangup",
    "input",
}


def _error(message: str, field: Optional[str] = None) -> None:
    raise PiopiyValidationError(message, field=field)


def _ensure_dict(value: Any, field: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        _error("{0} must be an object.".format(field), field)
    return value


def _ensure_list(value: Any, field: str) -> List[Any]:
    if not isinstance(value, list):
        _error("{0} must be an array.".format(field), field)
    return value


def _validate_required_and_allowed_keys(payload: Dict[str, Any], required: Set[str], allowed: Set[str], field: str) -> None:
    missing = sorted(required.difference(payload.keys()))
    if missing:
        _error("Missing required field(s): {0}".format(", ".join(missing)), field)

    extra = sorted(set(payload.keys()).difference(allowed))
    if extra:
        _error("Unknown field(s): {0}".format(", ".join(extra)), field)


def _ensure_string(value: Any, field: str, min_len: Optional[int] = None, max_len: Optional[int] = None) -> None:
    if not isinstance(value, str):
        _error("{0} must be a string.".format(field), field)

    if min_len is not None and len(value) < min_len:
        _error("{0} must be at least {1} characters long.".format(field, min_len), field)

    if max_len is not None and len(value) > max_len:
        _error("{0} must be at most {1} characters long.".format(field, max_len), field)


def _ensure_bool(value: Any, field: str) -> None:
    if not isinstance(value, bool):
        _error("{0} must be a boolean.".format(field), field)


def _ensure_int(value: Any, field: str, minimum: Optional[int] = None, maximum: Optional[int] = None) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        _error("{0} must be an integer.".format(field), field)

    if minimum is not None and value < minimum:
        _error("{0} must be >= {1}.".format(field, minimum), field)

    if maximum is not None and value > maximum:
        _error("{0} must be <= {1}.".format(field, maximum), field)


def _ensure_number(value: Any, field: str, minimum: Optional[float] = None, maximum: Optional[float] = None) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _error("{0} must be a number.".format(field), field)

    if minimum is not None and value < minimum:
        _error("{0} must be >= {1}.".format(field, minimum), field)

    if maximum is not None and value > maximum:
        _error("{0} must be <= {1}.".format(field, maximum), field)


def _validate_phone(value: Any, field: str) -> None:
    _ensure_string(value, field)
    if not _PHONE_RE.match(value):
        _error("{0} must match ^[1-9][0-9]{{6,15}}$.".format(field), field)


def _validate_uuid(value: Any, field: str) -> None:
    _ensure_string(value, field)
    try:
        UUID(value)
    except (TypeError, ValueError):
        _error("{0} must be a valid UUID string.".format(field), field)


def _validate_variables(value: Any, field: str, max_string_len: Optional[int] = None, max_properties: Optional[int] = None) -> None:
    data = _ensure_dict(value, field)

    if max_properties is not None and len(data) > max_properties:
        _error("{0} supports at most {1} entries.".format(field, max_properties), field)

    for key, item in data.items():
        if not isinstance(key, str) or not _VAR_KEY_RE.match(key):
            _error("{0} has invalid key '{1}'.".format(field, key), field)

        if isinstance(item, str):
            if max_string_len is not None and len(item) > max_string_len:
                _error("{0}.{1} exceeds max string length {2}.".format(field, key, max_string_len), field)
            continue

        if isinstance(item, bool):
            continue

        if isinstance(item, (int, float)):
            continue

        _error("{0}.{1} must be string, number, or boolean.".format(field, key), field)


def _validate_main_options(options: Any, field: str = "options") -> None:
    data = _ensure_dict(options, field)
    allowed = {"max_duration_sec", "record", "ring_timeout_sec"}

    extra = sorted(set(data.keys()).difference(allowed))
    if extra:
        _error("Unknown option(s): {0}".format(", ".join(extra)), field)

    if "max_duration_sec" in data:
        _ensure_int(data["max_duration_sec"], "{0}.max_duration_sec".format(field), minimum=30, maximum=7200)

    if "record" in data:
        _ensure_bool(data["record"], "{0}.record".format(field))

    if "ring_timeout_sec" in data:
        _ensure_int(data["ring_timeout_sec"], "{0}.ring_timeout_sec".format(field), minimum=5, maximum=120)


def _validate_failover_config(failover: Any, primary_agent_id: str, field: str = "failover") -> None:
    data = _ensure_dict(failover, field)
    _validate_required_and_allowed_keys(
        data,
        {"agent_id"},
        {
            "agent_id",
            "strategy",
            "max_duration_sec",
            "ring_timeout_sec",
            "machine_detection",
            "recording",
            "waiting_music",
            "metadata",
        },
        field,
    )

    _validate_uuid(data["agent_id"], "{0}.agent_id".format(field))
    if data["agent_id"] == primary_agent_id:
        _error("{0}.agent_id cannot be same as primary agent_id.".format(field), field)

    if "strategy" in data:
        _ensure_string(data["strategy"], "{0}.strategy".format(field))
        if data["strategy"] not in {"simultaneous", "sequential"}:
            _error("{0}.strategy must be simultaneous or sequential.".format(field), field)

    if "max_duration_sec" in data:
        _ensure_int(data["max_duration_sec"], "{0}.max_duration_sec".format(field), minimum=10, maximum=7200)

    if "ring_timeout_sec" in data:
        _ensure_int(data["ring_timeout_sec"], "{0}.ring_timeout_sec".format(field), minimum=5, maximum=120)

    if "machine_detection" in data:
        _ensure_bool(data["machine_detection"], "{0}.machine_detection".format(field))

    if "waiting_music" in data:
        _ensure_string(data["waiting_music"], "{0}.waiting_music".format(field))

    if "recording" in data:
        recording = _ensure_dict(data["recording"], "{0}.recording".format(field))
        _validate_required_and_allowed_keys(
            recording,
            set(),
            {"enabled", "channels", "format"},
            "{0}.recording".format(field),
        )

        if "enabled" in recording:
            _ensure_bool(recording["enabled"], "{0}.recording.enabled".format(field))

        if "channels" in recording:
            _ensure_string(recording["channels"], "{0}.recording.channels".format(field))
            if recording["channels"] not in {"dual", "single"}:
                _error("{0}.recording.channels must be dual or single.".format(field), field)

        if "format" in recording:
            _ensure_string(recording["format"], "{0}.recording.format".format(field))
            if recording["format"] not in {"mp3", "wav"}:
                _error("{0}.recording.format must be mp3 or wav.".format(field), field)

    if "metadata" in data:
        _validate_variables(data["metadata"], "{0}.metadata".format(field))


def _validate_prompt(prompt: Any, field: str) -> None:
    data = _ensure_dict(prompt, field)
    allowed = {"type", "file_name", "say", "voice_id", "language", "speed"}

    extra = sorted(set(data.keys()).difference(allowed))
    if extra:
        _error("Unknown field(s): {0}".format(", ".join(extra)), field)

    if "type" not in data:
        _error("{0}.type is required.".format(field), field)

    prompt_type = data["type"]
    _ensure_string(prompt_type, "{0}.type".format(field))

    if prompt_type not in {"file", "say"}:
        _error("{0}.type must be one of: file, say.".format(field), field)

    if prompt_type == "file":
        if "file_name" not in data:
            _error("{0}.file_name is required when type is file.".format(field), field)
    elif prompt_type == "say":
        for key in ["say", "language", "voice_id", "speed"]:
            if key not in data:
                _error("{0}.{1} is required when type is say.".format(field, key), field)

    if "file_name" in data:
        _ensure_string(data["file_name"], "{0}.file_name".format(field))

    if "say" in data:
        _ensure_string(data["say"], "{0}.say".format(field))

    if "language" in data:
        _ensure_string(data["language"], "{0}.language".format(field))

    if "voice_id" in data:
        _ensure_string(data["voice_id"], "{0}.voice_id".format(field))

    if "speed" in data:
        _ensure_number(data["speed"], "{0}.speed".format(field), minimum=0.5, maximum=2.0)


def _validate_dtmf(dtmf: Any, field: str) -> None:
    data = _ensure_dict(dtmf, field)
    allowed = {
        "min_digits",
        "max_digits",
        "finish_on_key",
        "first_digit_timeout",
        "inter_digit_timeout",
        "flush_buffer",
    }

    extra = sorted(set(data.keys()).difference(allowed))
    if extra:
        _error("Unknown field(s): {0}".format(", ".join(extra)), field)

    if "min_digits" in data:
        _ensure_int(data["min_digits"], "{0}.min_digits".format(field), minimum=1)

    if "max_digits" in data:
        _ensure_int(data["max_digits"], "{0}.max_digits".format(field), minimum=1)

    if "finish_on_key" in data:
        _ensure_string(data["finish_on_key"], "{0}.finish_on_key".format(field), max_len=1)

    if "first_digit_timeout" in data:
        _ensure_int(data["first_digit_timeout"], "{0}.first_digit_timeout".format(field), minimum=1)

    if "inter_digit_timeout" in data:
        _ensure_int(data["inter_digit_timeout"], "{0}.inter_digit_timeout".format(field), minimum=1)

    if "flush_buffer" in data:
        _ensure_bool(data["flush_buffer"], "{0}.flush_buffer".format(field))


def _validate_on_result(data: Any, field: str) -> None:
    body = _ensure_dict(data, field)
    allowed = {"type", "ref", "url"}
    extra = sorted(set(body.keys()).difference(allowed))
    if extra:
        _error("Unknown field(s): {0}".format(", ".join(extra)), field)

    if "type" not in body:
        _error("{0}.type is required.".format(field), field)

    result_type = body["type"]
    _ensure_string(result_type, "{0}.type".format(field))

    if result_type not in {"pcmo", "url"}:
        _error("{0}.type must be one of: pcmo, url.".format(field), field)

    if result_type == "pcmo" and "ref" not in body:
        _error("{0}.ref is required when type is pcmo.".format(field), field)

    if result_type == "url" and "url" not in body:
        _error("{0}.url is required when type is url.".format(field), field)

    if "ref" in body:
        _ensure_string(body["ref"], "{0}.ref".format(field))

    if "url" in body:
        _ensure_string(body["url"], "{0}.url".format(field))
        if not _HTTP_URL_RE.match(body["url"]):
            _error("{0}.url must start with http:// or https://.".format(field), field)


def _validate_retries(data: Any, field: str) -> None:
    body = _ensure_dict(data, field)
    allowed = {"max", "no_input_prompt", "invalid_prompt"}
    extra = sorted(set(body.keys()).difference(allowed))
    if extra:
        _error("Unknown field(s): {0}".format(", ".join(extra)), field)

    if "max" in body:
        _ensure_int(body["max"], "{0}.max".format(field), minimum=0)

    if "no_input_prompt" in body:
        _validate_prompt(body["no_input_prompt"], "{0}.no_input_prompt".format(field))

    if "invalid_prompt" in body:
        _validate_prompt(body["invalid_prompt"], "{0}.invalid_prompt".format(field))


def _validate_connect_action(action: Dict[str, Any], field: str) -> None:
    _validate_required_and_allowed_keys(action, {"action", "params", "endpoints"}, {"action", "params", "endpoints"}, field)

    params = _ensure_dict(action["params"], "{0}.params".format(field))
    _validate_required_and_allowed_keys(
        params,
        {"caller_id"},
        {"strategy", "caller_id", "options", "metadata"},
        "{0}.params".format(field),
    )

    _validate_phone(params["caller_id"], "{0}.params.caller_id".format(field))

    if "strategy" in params:
        _ensure_string(params["strategy"], "{0}.params.strategy".format(field))
        if params["strategy"] not in {"simultaneous", "sequential"}:
            _error("{0}.params.strategy must be simultaneous or sequential.".format(field), field)

    if "options" in params:
        options = _ensure_dict(params["options"], "{0}.params.options".format(field))
        allowed_options = {"max_duration_sec", "ring_timeout_sec", "machine_detection", "recording", "waiting_music"}
        extra = sorted(set(options.keys()).difference(allowed_options))
        if extra:
            _error("Unknown field(s): {0}".format(", ".join(extra)), "{0}.params.options".format(field))

        if "max_duration_sec" in options:
            _ensure_int(options["max_duration_sec"], "{0}.params.options.max_duration_sec".format(field), minimum=10, maximum=7200)

        if "ring_timeout_sec" in options:
            _ensure_int(options["ring_timeout_sec"], "{0}.params.options.ring_timeout_sec".format(field), minimum=5, maximum=120)

        if "machine_detection" in options:
            _ensure_bool(options["machine_detection"], "{0}.params.options.machine_detection".format(field))

        if "waiting_music" in options:
            _ensure_string(options["waiting_music"], "{0}.params.options.waiting_music".format(field))

        if "recording" in options:
            recording = _ensure_dict(options["recording"], "{0}.params.options.recording".format(field))
            _validate_required_and_allowed_keys(
                recording,
                set(),
                {"enabled", "channels", "format"},
                "{0}.params.options.recording".format(field),
            )

            if "enabled" in recording:
                _ensure_bool(recording["enabled"], "{0}.params.options.recording.enabled".format(field))

            if "channels" in recording:
                _ensure_string(recording["channels"], "{0}.params.options.recording.channels".format(field))
                if recording["channels"] not in {"dual", "single"}:
                    _error("{0}.params.options.recording.channels must be dual or single.".format(field), field)

            if "format" in recording:
                _ensure_string(recording["format"], "{0}.params.options.recording.format".format(field))
                if recording["format"] not in {"mp3", "wav"}:
                    _error("{0}.params.options.recording.format must be mp3 or wav.".format(field), field)

    if "metadata" in params:
        _validate_variables(params["metadata"], "{0}.params.metadata".format(field))

    endpoints = _ensure_list(action["endpoints"], "{0}.endpoints".format(field))
    if len(endpoints) < 1:
        _error("{0}.endpoints must contain at least one endpoint.".format(field), field)

    agent_mode = False
    agent_count = 0

    for idx, endpoint in enumerate(endpoints):
        endpoint_field = "{0}.endpoints[{1}]".format(field, idx)
        endpoint_obj = _ensure_dict(endpoint, endpoint_field)
        _validate_required_and_allowed_keys(endpoint_obj, {"type"}, {"type", "number", "uri", "id", "headers"}, endpoint_field)

        endpoint_type = endpoint_obj["type"]
        _ensure_string(endpoint_type, "{0}.type".format(endpoint_field))
        if endpoint_type not in {"pstn", "sip", "agent"}:
            _error("{0}.type must be one of: pstn, sip, agent.".format(endpoint_field), endpoint_field)

        if endpoint_type == "pstn":
            if "number" not in endpoint_obj:
                _error("{0}.number is required when type is pstn.".format(endpoint_field), endpoint_field)
            _validate_phone(endpoint_obj["number"], "{0}.number".format(endpoint_field))
            if agent_mode:
                _error("Agent endpoints must be at the end of connect.endpoints.", endpoint_field)

        if endpoint_type == "sip":
            if "uri" not in endpoint_obj:
                _error("{0}.uri is required when type is sip.".format(endpoint_field), endpoint_field)
            _ensure_string(endpoint_obj["uri"], "{0}.uri".format(endpoint_field))
            if agent_mode:
                _error("Agent endpoints must be at the end of connect.endpoints.", endpoint_field)

        if endpoint_type == "agent":
            if "id" not in endpoint_obj:
                _error("{0}.id is required when type is agent.".format(endpoint_field), endpoint_field)
            _validate_uuid(endpoint_obj["id"], "{0}.id".format(endpoint_field))
            agent_mode = True
            agent_count += 1
            if agent_count > 2:
                _error("A maximum of two agent endpoints is allowed.", endpoint_field)

        if "headers" in endpoint_obj:
            _ensure_dict(endpoint_obj["headers"], "{0}.headers".format(endpoint_field))


def _validate_play_action(action: Dict[str, Any], field: str) -> None:
    _validate_required_and_allowed_keys(action, {"action", "file_name"}, {"action", "file_name"}, field)
    _ensure_string(action["file_name"], "{0}.file_name".format(field))


def _validate_play_get_input_action(action: Dict[str, Any], field: str) -> None:
    _validate_required_and_allowed_keys(
        action,
        {"action", "prompt", "input", "on_result"},
        {"action", "prompt", "input", "dtmf", "retries", "on_result"},
        field,
    )

    _validate_prompt(action["prompt"], "{0}.prompt".format(field))

    input_modes = _ensure_list(action["input"], "{0}.input".format(field))
    if not input_modes:
        _error("{0}.input must contain at least one item.".format(field), field)

    seen = set()
    for idx, mode in enumerate(input_modes):
        mode_field = "{0}.input[{1}]".format(field, idx)
        _ensure_string(mode, mode_field)
        if mode not in {"dtmf", "speech"}:
            _error("{0} must be dtmf or speech.".format(mode_field), mode_field)
        if mode in seen:
            _error("{0} contains duplicate value '{1}'.".format(field, mode), field)
        seen.add(mode)

    if "dtmf" in action:
        _validate_dtmf(action["dtmf"], "{0}.dtmf".format(field))

    if "retries" in action:
        _validate_retries(action["retries"], "{0}.retries".format(field))

    _validate_on_result(action["on_result"], "{0}.on_result".format(field))


def _validate_param_action(action: Dict[str, Any], field: str) -> None:
    _validate_required_and_allowed_keys(action, {"action", "data"}, {"action", "data"}, field)
    _validate_variables(action["data"], "{0}.data".format(field), max_string_len=256, max_properties=10)


def _validate_record_action(action: Dict[str, Any], field: str) -> None:
    _validate_required_and_allowed_keys(action, {"action"}, {"action", "format", "channels"}, field)

    if "format" in action:
        _ensure_string(action["format"], "{0}.format".format(field))
        if action["format"] not in {"mp3", "wav"}:
            _error("{0}.format must be mp3 or wav.".format(field), field)

    if "channels" in action:
        _ensure_string(action["channels"], "{0}.channels".format(field))
        if action["channels"] not in {"single", "dual"}:
            _error("{0}.channels must be single or dual.".format(field), field)


def _validate_hangup_action(action: Dict[str, Any], field: str) -> None:
    _validate_required_and_allowed_keys(action, {"action"}, {"action"}, field)


def _validate_input_action(action: Dict[str, Any], field: str) -> None:
    _validate_required_and_allowed_keys(action, {"action", "on_result"}, {"action", "dtmf", "on_result"}, field)

    if "dtmf" in action:
        _validate_dtmf(action["dtmf"], "{0}.dtmf".format(field))

    _validate_on_result(action["on_result"], "{0}.on_result".format(field))


def validate_pipeline(pipeline: Any, field: str = "pipeline") -> None:
    items = _ensure_list(pipeline, field)

    if len(items) < 1:
        _error("{0} must contain at least one action.".format(field), field)

    for index, item in enumerate(items):
        action_field = "{0}[{1}]".format(field, index)
        action = _ensure_dict(item, action_field)

        if "action" not in action:
            _error("{0}.action is required.".format(action_field), action_field)

        action_name = action["action"]
        _ensure_string(action_name, "{0}.action".format(action_field))

        if action_name not in _ACTIONS:
            _error("{0}.action must be one of: {1}.".format(action_field, ", ".join(sorted(_ACTIONS))), action_field)

        if action_name == "connect":
            _validate_connect_action(action, action_field)
        elif action_name == "play":
            _validate_play_action(action, action_field)
        elif action_name == "play_get_input":
            _validate_play_get_input_action(action, action_field)
        elif action_name == "param":
            _validate_param_action(action, action_field)
        elif action_name == "record":
            _validate_record_action(action, action_field)
        elif action_name == "hangup":
            _validate_hangup_action(action, action_field)
        elif action_name == "input":
            _validate_input_action(action, action_field)


def validate_ai_call_request(payload: Any) -> None:
    body = _ensure_dict(payload, "body")
    _validate_required_and_allowed_keys(
        body,
        {"caller_id", "to_number", "agent_id"},
        {"caller_id", "to_number", "agent_id", "options", "variables", "app_id", "failover"},
        "body",
    )

    _validate_phone(body["caller_id"], "caller_id")
    _validate_phone(body["to_number"], "to_number")
    _validate_uuid(body["agent_id"], "agent_id")

    if "options" in body:
        _validate_main_options(body["options"], "options")

    if "variables" in body:
        _validate_variables(body["variables"], "variables")

    if "failover" in body:
        if "app_id" not in body:
            _error("app_id is required when failover is provided.", "app_id")
        _ensure_string(body["app_id"], "app_id")
        _validate_failover_config(body["failover"], primary_agent_id=body["agent_id"], field="failover")
    elif "app_id" in body:
        _error("app_id is only supported when failover is provided.", "app_id")


def validate_hangup_request(payload: Any) -> None:
    body = _ensure_dict(payload, "body")
    _validate_required_and_allowed_keys(body, {"call_id"}, {"call_id", "cause", "reason"}, "body")

    _validate_uuid(body["call_id"], "call_id")

    if "cause" in body:
        _ensure_string(body["cause"], "cause", min_len=1, max_len=64)

    if "reason" in body:
        _ensure_string(body["reason"], "reason", min_len=1, max_len=256)


def validate_pcmo_call_request(payload: Any) -> None:
    body = _ensure_dict(payload, "body")
    _validate_required_and_allowed_keys(
        body,
        {"caller_id", "to_number", "pipeline", "app_id"},
        {"caller_id", "to_number", "pipeline", "app_id", "agent_id", "options", "variables"},
        "body",
    )

    _validate_phone(body["caller_id"], "caller_id")
    _validate_phone(body["to_number"], "to_number")
    _ensure_string(body["app_id"], "app_id")
    validate_pipeline(body["pipeline"], "pipeline")

    if "agent_id" in body:
        _validate_uuid(body["agent_id"], "agent_id")

    if "options" in body:
        _validate_main_options(body["options"], "options")

    if "variables" in body:
        _validate_variables(body["variables"], "variables")


def validate_flow_call_request(payload: Any) -> None:
    body = _ensure_dict(payload, "body")
    _validate_required_and_allowed_keys(
        body,
        {"flow_id", "org_id", "caller_id", "to_number", "app_id"},
        {"flow_id", "org_id", "caller_id", "to_number", "app_id", "options", "variables"},
        "body",
    )

    _validate_uuid(body["flow_id"], "flow_id")
    _validate_uuid(body["org_id"], "org_id")
    _validate_phone(body["caller_id"], "caller_id")
    _validate_phone(body["to_number"], "to_number")
    _ensure_string(body["app_id"], "app_id")

    if "options" in body:
        _validate_main_options(body["options"], "options")

    if "variables" in body:
        _validate_variables(body["variables"], "variables")


def validate_transfer_request(payload: Any) -> None:
    body = _ensure_dict(payload, "body")
    _validate_required_and_allowed_keys(body, {"call_id", "pipeline"}, {"call_id", "pipeline"}, "body")

    _validate_uuid(body["call_id"], "call_id")
    validate_pipeline(body["pipeline"], "pipeline")
