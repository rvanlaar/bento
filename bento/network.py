import logging
import os
import platform
import traceback
from typing import TYPE_CHECKING, Any, Dict

from bento.util import EMPTY_DICT

# Add default timeout so that we do not block the user's main thread from exiting
# 1 second value is so that user does not get impatient
TIMEOUT = 1  # sec

if TYPE_CHECKING:
    # Only import when type checking to avoid loading module when unecessary
    from requests.models import Response  # noqa


def no_auth_post(
    url: str,
    json: Any = EMPTY_DICT,
    params: Dict[str, str] = EMPTY_DICT,
    headers: Dict[str, str] = EMPTY_DICT,
    timeout: float = TIMEOUT,
) -> "Response":
    # import inside def for performance
    import requests

    """Perform a requests.post and default headers set"""
    r = requests.post(url, headers=headers, params=params, json=json, timeout=timeout)
    return r