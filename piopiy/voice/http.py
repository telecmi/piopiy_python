"""Shared HTTP transport for Piopiy API resources."""

from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import PiopiyAPIError, PiopiyNetworkError, PiopiyValidationError


class HTTPClient:
    """Simple authenticated HTTP client with retries and error mapping."""

    def __init__(
        self,
        token: str,
        base_url: str,
        timeout: int = 10,
        max_retries: int = 2,
        backoff_factor: float = 0.4,
        session: Optional[requests.Session] = None,
    ):
        if not token or not isinstance(token, str):
            raise PiopiyValidationError("A valid Bearer token is required.", field="token")

        if not base_url or not isinstance(base_url, str):
            raise PiopiyValidationError("A valid base_url is required.", field="base_url")

        if timeout <= 0:
            raise PiopiyValidationError("timeout must be greater than 0.", field="timeout")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()
        self._configure_session(token, max_retries, backoff_factor)

    def _configure_session(self, token: str, max_retries: int, backoff_factor: float) -> None:
        retry = Retry(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["POST"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        self._session.headers.update(
            {
                "Authorization": "Bearer {0}".format(token),
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not path.startswith("/"):
            path = "/{0}".format(path)

        url = "{0}{1}".format(self.base_url, path)

        try:
            response = self._session.post(url, json=payload, timeout=self.timeout)
        except requests.Timeout as exc:
            raise PiopiyNetworkError("Request timed out.", original_exception=exc)
        except requests.RequestException as exc:
            raise PiopiyNetworkError("Network error while calling Piopiy API.", original_exception=exc)

        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        status_code = response.status_code

        if 200 <= status_code < 300:
            if not response.content:
                return {}

            try:
                return response.json()
            except ValueError:
                return {"raw_response": response.text}

        payload = self._extract_error_payload(response)
        message = payload.get("error") or payload.get("message") or "Piopiy API request failed."
        raise PiopiyAPIError(message=message, status_code=status_code, payload=payload)

    @staticmethod
    def _extract_error_payload(response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
            if isinstance(data, dict):
                return data
            return {"message": str(data)}
        except ValueError:
            text = (response.text or "").strip()
            if not text:
                text = "Unknown API error"
            return {"message": text}
