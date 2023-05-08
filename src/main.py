import typer

from auth import CredentialsError, load_credentials
from commands import sso

__version__ = "0.0.1"


app = typer.Typer(help="CLI sso application")


app.add_typer(sso.app, name="sso")


@app.command()
def call_api_with_credentials(ctx: typer.Context):
    access_token = ctx.obj.get("access_token")
    if access_token:
        print(f"Calling API with token {access_token}")


@app.callback()
def main(ctx: typer.Context):
    """
    Load credentials for the main app state
    """
    ctx.ensure_object(dict)
    try:
        credentials = load_credentials()
        ctx.obj["access_token"] = credentials.access_token
    except CredentialsError:
        print("Credentials not available, you might need to log in.")


if __name__ == "__main__":
    app()
