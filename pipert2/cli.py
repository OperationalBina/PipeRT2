import typer

app = typer.Typer()


@app.command()
def hello():
    typer.echo(f"Hello PipeRT2 User!")


@app.command()
def goodbye():
    typer.echo(f"Goodbye PipeRT2 User! Have a good day.")


if __name__ == "__main__":
    app()
