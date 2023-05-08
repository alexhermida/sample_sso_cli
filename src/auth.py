import json
import os
import time
import webbrowser
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path

import requests

_TENANT = os.environ["TENANT"]
_APP_CLIENT_ID = os.environ["APP_CLIENT_ID"]
_AUDIENCE = os.environ["AUDIENCE"]

_CREDENTIALS_FILEPATH = str(Path.home() / ".sso_cli" / "credentials.json")


@dataclass
class DeviceCodeResponse:
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int
    verification_uri_complete: str


@dataclass
class ReceivedCredentials:
    access_token: str
    expires_in: int
    token_type: str


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


class CredentialsError(Exception):
    pass


def request_device_code() -> DeviceCodeResponse:
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = f"client_id={_APP_CLIENT_ID}&audience={_AUDIENCE}"

    response = requests.post(
        f"{_TENANT}/oauth/device/code", headers=headers, data=payload
    )
    response.raise_for_status()

    device_code_info = DeviceCodeResponse(**response.json())

    _user_authorization_flow(device_code_info=device_code_info)

    return device_code_info


def _user_authorization_flow(device_code_info: DeviceCodeResponse):
    opening_msg = (
        f"Attempting to automatically open the SSO authorization page in "
        f"your default browser.\nIf the browser does not open or you wish "
        f"to use a different device to authorize this request,"
        f"please visit the following URL:\n"
        f"\n{device_code_info.verification_uri}\n"
        f"\nThen enter the code:\n"
        f"\n{device_code_info.user_code}\n"
        f"\nAlternatively, you may visit the following URL which will "
        f"autofill the code upon loading:"
        f"\n{device_code_info.verification_uri_complete}\n"
    )
    print(opening_msg)
    webbrowser.open(device_code_info.verification_uri_complete)


def _request_access_token(code: str):
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = (
        f"grant_type=urn:ietf:params:oauth:grant-type:device_code&"
        f"device_code={code}&client_id={_APP_CLIENT_ID}"
    )
    response = requests.post(f"{_TENANT}/oauth/token", headers=headers, data=payload)
    response.raise_for_status()

    return response


def poll_user_verification(code: str) -> ReceivedCredentials | None:
    polling_interval_seconds = 5
    time.sleep(polling_interval_seconds)
    valid_response = False

    while not valid_response:
        try:
            response = _request_access_token(code)
            valid_response = True

            return ReceivedCredentials(**response.json())
        except requests.HTTPError as http_error:
            if http_error.response.status_code == 403:
                print("Retrying device code credentials request")
                time.sleep(polling_interval_seconds)
            else:
                raise http_error


def save_credentials(credentials: ReceivedCredentials):
    os.makedirs(os.path.dirname(_CREDENTIALS_FILEPATH), exist_ok=True)

    with open(_CREDENTIALS_FILEPATH, "w") as credentials_file:
        credentials_file.write(json.dumps(credentials, cls=DataClassJSONEncoder))


def load_credentials():
    try:
        with open(_CREDENTIALS_FILEPATH, "r") as credentials_file:
            return ReceivedCredentials(**json.load(credentials_file))
    except (FileNotFoundError, json.decoder.JSONDecodeError) as error:
        print(f"Error loading credentials file {_CREDENTIALS_FILEPATH}: {error}")
        raise CredentialsError("Error loading credentials file %s: %s ")
