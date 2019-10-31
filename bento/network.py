import logging
import os
import platform
import traceback
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.models import Response

from bento.metrics import get_user_uuid

BASE_URL = "https://bento.r2c.dev"
# Add default timeout so that we do not block the user's main thread from exiting
# 1 second value is so that user does not get impatient
TIMEOUT = 1  # sec


PostData = List[Dict[str, Any]]


def _get_version() -> str:
    from bento import __version__

    return __version__


def _get_default_shell() -> str:
    return os.environ.get("SHELL", "")


def _get_default_headers() -> Dict[str, str]:
    """
    Headers for all bento http/s requests
    """
    return {
        "X-R2C-BENTO-User-Platform": f"{platform.platform()}",
        "X-R2C-BENTO-User-Shell": f"{_get_default_shell()}",
        "X-R2C-BENTO-Cli-Version": f"{_get_version()}",
        "Accept": "application/json",
    }


def no_auth_get(
    url: str, params: Dict[str, str] = {}, headers: Dict[str, str] = {}, **kwargs: Any
) -> Response:
    """Perform a requests.get and default headers set"""
    headers = {**_get_default_headers(), **headers}
    r = requests.get(url, headers=headers, params=params, **kwargs, timeout=TIMEOUT)
    return r


def no_auth_post(
    url: str, json: Any = {}, params: Dict[str, str] = {}, headers: Dict[str, str] = {}
) -> Response:
    """Perform a requests.post and default headers set"""
    headers = {**_get_default_headers(), **headers}
    r = requests.post(url, headers=headers, params=params, json=json, timeout=TIMEOUT)
    return r


def _get_base_url() -> str:
    return BASE_URL


def fetch_latest_version() -> Tuple[Optional[str], Optional[str]]:
    try:
        url = f"{_get_base_url()}/bento/api/v1/version"
        r = no_auth_get(url, timeout=0.25)
        response_json = r.json()
        return response_json.get("latest", None), response_json.get("uploadTime", None)
    except Exception:
        return None, None


def post_metrics(data: PostData) -> bool:
    try:
        url = f"{_get_base_url()}/bento/api/v1/metrics/u/{get_user_uuid()}/"
        r = no_auth_post(url, json=data)
        r.raise_for_status()
        return True
    except Exception as e:
        logging.warning(
            f"Exception while posting metrics {e}\n{traceback.format_exc()}"
        )
        return False
