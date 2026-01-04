import typer
from notesh.storage import create_note, list_notes

app = typer.Typer(help="A simple note-taking CLI")


@app.command()
def add(title: str):
    """Add a new note"""
    note = create_note(title)
    typer.echo(f"Note created: [{note.id}] {note.title}")



@app.command()
def list():
    """List all notes"""
    notes = list_notes()

    if not notes:
        typer.echo("No notes found.")
        return

    for note in notes:
        date = note.created.date()
        typer.echo(f"[{date}] {note.title}  ({note.id})")




@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")
if __name__ == "__main__":
    app()
