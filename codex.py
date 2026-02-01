# codex.py
import typer
from datetime import datetime, UTC
from codex_core.session import Session, Event

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

@app.command()
def add(
    session_id: str,
    track: str = typer.Option(..., help="Track name"),
    pattern: str = typer.Option(..., help="Strudel pattern text"),
    bpm: int = typer.Option(None, help="Tempo in BPM"),
    note: str = typer.Option(None, help="Optional note"),
):
    """
    Add an event to an existing session.
    """
    try:
        session = Session.load(session_id)
        event = Event(
            timestamp=datetime.now(UTC).isoformat(),
            track=track,
            pattern=pattern,
            bpm=bpm,
            note=note,
        )
        session.add_event(event)
        session.save_overwrite()
        typer.echo(f"Added event to session '{session_id}'.")
    except FileNotFoundError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
