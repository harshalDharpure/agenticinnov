"""Context prediction models for next-app usage."""
from __future__ import annotations

from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np


class MarkovPredictor:
    """Simple Markov-chain predictor for next app usage."""

    def __init__(self, app_names: Sequence[str], smoothing: float = 1.0) -> None:
        self.app_names = list(app_names)
        self.index = {name: idx for idx, name in enumerate(self.app_names)}
        self.smoothing = smoothing
        n = len(self.app_names)
        self.counts = np.full((n, n), smoothing, dtype=float)

    def update(self, previous_app: str, next_app: str) -> None:
        """Update transition counts with an observed transition."""
        if previous_app not in self.index or next_app not in self.index:
            return
        i = self.index[previous_app]
        j = self.index[next_app]
        self.counts[i, j] += 1.0

    def predict(self, previous_app: str | None) -> Dict[str, float]:
        """Predict the next app distribution based on the previous app."""
        if previous_app is None or previous_app not in self.index:
            return self._uniform_distribution()
        row = self.counts[self.index[previous_app]]
        probs = row / row.sum()
        return {name: float(probs[idx]) for idx, name in enumerate(self.app_names)}

    def predict_top_k(self, previous_app: str | None, k: int) -> List[Tuple[str, float]]:
        """Return the top-k predicted apps."""
        distribution = self.predict(previous_app)
        return sorted(distribution.items(), key=lambda item: item[1], reverse=True)[:k]

    def _uniform_distribution(self) -> Dict[str, float]:
        """Return a uniform distribution over apps."""
        n = len(self.app_names)
        if n == 0:
            return {}
        prob = 1.0 / n
        return {name: prob for name in self.app_names}
