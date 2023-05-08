import os
from dataclasses import dataclass

import requests

_TENANT = os.environ["TENANT"]
_APP_CLIENT_ID = os.environ["APP_CLIENT_ID"]
_AUDIENCE = os.environ["AUDIENCE"]


@dataclass
class DeviceCodeResponse:
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int
    verification_uri_complete: str


def request_device_code() -> DeviceCodeResponse:
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = f"client_id={_APP_CLIENT_ID}&audience={_AUDIENCE}"

    response = requests.post(
        f"{_TENANT}/oauth/device/code", headers=headers, data=payload
    )
    response.raise_for_status()

    return DeviceCodeResponse(**response.json())
