import typer
from rich import print
from typing_extensions import Annotated

from auth import (
    DeviceCodeResponse,
    ReceivedCredentials,
    poll_user_verification,
    request_device_code,
    save_credentials,
)

app = typer.Typer()


@app.command()
def login(profile: Annotated[str, typer.Argument()] = "default"):
    """
    Single Sign-On login
    """
    print(f"Log in with profile {profile}")

    device_code_info: DeviceCodeResponse = request_device_code()

    credentials: ReceivedCredentials | None = poll_user_verification(
        device_code_info.device_code,
        device_code_info.interval,
    )

    if credentials is not None:
        save_credentials(credentials)

        print("Authentication successful")
