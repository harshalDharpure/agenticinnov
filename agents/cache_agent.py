"""Cache agent tracking recency for eviction decisions."""
from __future__ import annotations

from collections import OrderedDict
from typing import Iterable, Optional


class CacheAgent:
    """Tracks app recency for cache management."""

    def __init__(self) -> None:
        self.recency: "OrderedDict[str, None]" = OrderedDict()

    def touch(self, app_name: str) -> None:
        """Mark an app as recently accessed."""
        if app_name in self.recency:
            self.recency.move_to_end(app_name)
        else:
            self.recency[app_name] = None

    def remove(self, app_name: str) -> None:
        """Remove an app from recency tracking."""
        self.recency.pop(app_name, None)

    def least_recently_used(self, protected: Iterable[str]) -> Optional[str]:
        """Return the least recently used app not in the protected set."""
        protected_set = set(protected)
        for app_name in self.recency.keys():
            if app_name not in protected_set:
                return app_name
        return None
