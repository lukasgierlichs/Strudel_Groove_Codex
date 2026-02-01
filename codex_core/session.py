from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime, UTC
import json
import os

@dataclass
class Event:
    timestamp: str           # ISO format
    track: str
    pattern: str
    bpm: Optional[int] = None
    note: Optional[str] = None

@dataclass
class Session:
    session_id: str
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    events: List[Event] = field(default_factory=list)

    def add_event(self, event: Event):
        self.events.append(event)

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "events": [asdict(e) for e in self.events]
        }

    def save(self, directory: str = "sessions"):
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"{self.session_id}.json")
        if os.path.exists(path):
            raise FileExistsError(f"Session {self.session_id} already exists.")
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
