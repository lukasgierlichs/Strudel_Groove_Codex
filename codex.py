# codex.py
import typer
import os
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

@app.command()
def list():
    """
    List all available sessions.
    """
    sessions_dir = "sessions"
    if not os.path.exists(sessions_dir):
        typer.echo("No sessions directory found.")
        return
    
    sessions = [
        f.replace(".json", "")
        for f in os.listdir(sessions_dir)
        if f.endswith(".json")
    ]

    if not sessions:
        typer.echo("No sessions found.")
        return
    
    for session_id in sorted(sessions):
        typer.echo(session_id)

@app.command()
def shoW(session_id: str):
    """
    Show details of a session.
    """
    try:
        session = Session.load(session_id)
    except FileNotFoundError as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)
    
    typer.echo(f"Session: {session.session_id}")
    typer.echo(f"Created: {session.created_at}")
    typer.echo(f"Events: {len(session.events)}\n")

    for event in session.events:
        line = f"[{event.timestamp}] {event.track}  {event.pattern}"
        if event.bpm is not None:
            line += f"  bpm={event.bpm}"
        if event.note is not None:
            line += f"  note={event.note}"
        typer.echo(line)

if __name__ == "__main__":
    app()
