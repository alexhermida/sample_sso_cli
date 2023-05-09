import typer

from commands import api, sso

__version__ = "0.0.1"


app = typer.Typer(help="CLI sso application")


app.add_typer(sso.app, name="sso", help="Single Sign On log in")
app.add_typer(api.app, name="api")


if __name__ == "__main__":
    app()
