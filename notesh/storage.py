import uuid
from datetime import datetime
from pathlib import Path
import yaml

from notesh.config import NOTES_DIR
from notesh.models import Note
from datetime import datetime

def _parse_datetime(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    raise TypeError(f"Invalid datetime value: {value!r}")


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


def list_notes() -> list[Note]:
    notes: list[Note] = []

    if not NOTES_DIR.exists():
        return notes

    for path in sorted(NOTES_DIR.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")

            if not text.startswith("---\n"):
                raise ValueError("Missing front-matter")

            parts = text.split("---", 2)
            if len(parts) < 3:
                raise ValueError("Invalid front-matter format")

            fm = parts[1]
            data = yaml.safe_load(fm)

            if not isinstance(data, dict):
                raise ValueError("Front-matter is not a mapping")

            note = Note(
                id=data["id"],
                title=_extract_title(text),
                created=_parse_datetime(data["created"]),
                updated=_parse_datetime(data["updated"]),
            )

            notes.append(note)

        except Exception as e:
            print(f"Skipping {path.name}: {e}")

    return notes




def _extract_title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "(untitled)"