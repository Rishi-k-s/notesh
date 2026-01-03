import typer
from notesh.storage import create_note

app = typer.Typer(help="notesh - A simple note-taking CLI application")


@app.command()
def add(title: str):
    """Add a new note"""
    note = create_note(title)
    typer.echo(f"Note created: [{note.id}] {note.title}")


if __name__ == "__main__":
    app()
