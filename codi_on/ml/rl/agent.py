from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any
import random

# 엡실론-그리디
@dataclass
class EpsilonGreedyBandit:
    epsilon: float = 0.1
    seed: int | None = None
    # 옷 추천 횟수
    counts: Dict[int, int] = field(default_factory=dict)
    # 추천 했을 때 평균 reward
    values: Dict[int, float] = field(default_factory=dict)

    def __post_init__(self):
        if self.seed is not None:
            random.seed(self.seed)

    def action(self, state: Dict[str, Any]) -> int:
        candidates: List[Dict[str, Any]] = state["candidates"]
        if not candidates:
            raise ValueError("No candidates found")

        # exploration
        if random.random() < self.epsilon:
            return random.randrange(len(candidates))

        # exploitation
        best_idx = 0
        best_value = float("inf")

        for idx, c in enumerate(candidates):
            cloth_id = c["cloth_id"]
            q = self.values.get(cloth_id, 0.0)

            if q > best_value:
                best_value = q
                best_idx = idx

        return best_idx

    def update(self, selected_cloth_id: int, reward: float) -> None:
        n = self.counts.get(selected_cloth_id, 0) + 1
        q_old = self.values.get(selected_cloth_id, 0.0)

        q_new = q_old + (reward - q_old) / n

        self.counts[selected_cloth_id] = n
        self.values[selected_cloth_id] = q_new

    def get_stats(self) -> Dict[int, Dict[str, float]]:
        out = {}
        for cloth_id in set(list(self.counts.keys()) + list(self.values.keys())):
            out[cloth_id] = {
                "count": float(self.counts.get(cloth_id, 0)),
                "value": float(self.values.get(cloth_id, 0.0)),
            }
        return out