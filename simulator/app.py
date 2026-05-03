"""App definition for the memory management simulator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class App:
    """Represents an application that can be loaded into memory."""

    name: str
    memory_usage: int
    load_time: float
    state: str = "unloaded"
    last_accessed: Optional[int] = None

    @property
    def is_loaded(self) -> bool:
        """Return whether the app is currently loaded."""
        return self.state == "loaded"

    def load(self, step: int) -> None:
        """Mark the app as loaded at the given step."""
        self.state = "loaded"
        self.last_accessed = step

    def unload(self) -> None:
        """Mark the app as unloaded."""
        self.state = "unloaded"
        self.last_accessed = None
