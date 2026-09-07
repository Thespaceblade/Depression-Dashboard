"""
Shared ESPN HTTP helpers.

ESPN's site.api.espn.com edge often returns HTTP 403 from datacenter egress
(GitHub Actions, many cloud runners). site.web.api.espn.com serves the same
/apis/site/v2/... routes without that block. Prefer web.api, fall back to api.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

import requests

ESPN_SITE_HOSTS = (
    "https://site.web.api.espn.com",
    "https://site.api.espn.com",
)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DepressionDashboard/1.0)",
    "Accept": "application/json",
    "Referer": "https://www.espn.com/",
}


def espn_headers() -> Dict[str, str]:
    return dict(DEFAULT_HEADERS)


def build_session(session: Optional[requests.Session] = None) -> requests.Session:
    if session is None:
        session = requests.Session()
    session.headers.update(espn_headers())
    return session


def espn_get(
    path: str,
    *,
    session: Optional[requests.Session] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 15,
    retries: int = 2,
) -> Tuple[Optional[requests.Response], Optional[str]]:
    """
    GET an ESPN site API path (must start with /apis/...).

    Returns (response_or_None, host_used_or_None). On total failure returns (None, None).
    Retries transient 5xx; does not retry hard 403 on the same host (switches host instead).
    """
    if not path.startswith("/"):
        path = "/" + path

    sess = build_session(session)
    last_exc: Optional[Exception] = None

    for host in ESPN_SITE_HOSTS:
        url = f"{host}{path}"
        for attempt in range(retries + 1):
            try:
                response = sess.get(url, params=params, timeout=timeout)
                if response.status_code == 200:
                    return response, host
                if response.status_code == 403:
                    print(f"ESPN HTTP 403 from {host} for {path} — trying next host")
                    break  # next host
                if 500 <= response.status_code < 600 and attempt < retries:
                    time.sleep(0.6 * (attempt + 1))
                    continue
                print(f"ESPN HTTP {response.status_code} from {host} for {path}")
                break
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if attempt < retries:
                    time.sleep(0.6 * (attempt + 1))
                    continue
                print(f"ESPN request error from {host} for {path}: {exc}")
                break

    if last_exc:
        print(f"ESPN all hosts failed for {path}: {last_exc}")
    return None, None


def espn_get_json(
    path: str,
    *,
    session: Optional[requests.Session] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 15,
) -> Optional[dict]:
    response, _host = espn_get(path, session=session, params=params, timeout=timeout)
    if response is None:
        return None
    try:
        return response.json()
    except Exception as exc:  # noqa: BLE001
        print(f"ESPN JSON decode error for {path}: {exc}")
        return None
