# codex.py

import typer
from codex_core.session import Session

app = typer.Typer()

@app.callback()
def main():
    """
    Strudel Groove Codex CLI.
    """
    pass

@app.command()
def new(session_id: str):
    """
    Create a new Strudel Groove Codex session.
    """
    try:
        session = Session(session_id=session_id)
        session.save()
        typer.echo(f"Session '{session_id}' created.")
    except FileExistsError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
