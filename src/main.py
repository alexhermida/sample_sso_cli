import typer
from auth import load_credentials

from commands import sso

__version__ = "0.0.1"


app = typer.Typer(help="CLI sso application")


app.add_typer(sso.app, name="sso")


@app.command()
def call_api_with_credentials():
    credentials = load_credentials()
    access_token = credentials.access_token
    if access_token:
        print(f"Calling API with token {access_token}")


if __name__ == "__main__":
    app()
