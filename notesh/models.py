from dataclasses import dataclass
from datetime import datetime

@dataclass
class Note:
    id: str
    title: str
    created: datetime
    updated: datetime
