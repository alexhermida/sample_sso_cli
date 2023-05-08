import typer

app = typer.Typer()


@app.command()
def public(name: str):
    print(f"Hello {name}")


@app.command()
def secure(name: str):
    print(f"Hello secure {name}")


if __name__ == "__main__":
    app()
