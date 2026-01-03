import uuid
from datetime import datetime
from pathlib import Path

from notesh.config import NOTES_DIR
from notesh.models import Note


def ensure_notes_dir():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

def generate_id() -> str:
    return uuid.uuid4().hex[:6]


def create_note(title: str) -> Note:
    ensure_notes_dir()

    note_id = generate_id()
    now = datetime.now()

    filename = f"{now.date()}-{note_id}.md"
    path = NOTES_DIR / filename

    content = f"""---
id: {note_id}
created: {now.isoformat()}
updated: {now.isoformat()}
tags: []
---

# {title}

"""

    path.write_text(content)

    return Note(
        id=note_id,
        title=title,
        created=now,
        updated=now,
    )