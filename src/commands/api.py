import requests
import typer
from rich import print

from auth import CredentialsError, load_credentials

app = typer.Typer()


@app.command()
def call_api_with_credentials(ctx: typer.Context):
    access_token = ctx.obj["access_token"]

    print("Calling fake API https://httpbin.org/bearer")
    response = requests.get(
        "https://httpbin.org/bearer",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    result = response.json()

    print("Authenticated: ", result["authenticated"])


@app.callback()
def main(ctx: typer.Context):
    """
    Call a fake API with the access token
    """
    ctx.ensure_object(dict)
    try:
        credentials = load_credentials()
        ctx.obj["access_token"] = credentials.access_token
    except CredentialsError:
        print("Credentials not available, you might need to log in.")
        raise typer.Exit()
