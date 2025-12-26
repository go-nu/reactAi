from typing import List, Dict, Any
import random

from ml.core.scoring.compute_comfort import compute_comfort_score


class ClothingRecommendEnv:
    # env 세팅
    def __init__(self,
                 weather_context: Dict[str, Any],
                 candidate_clothes: List[Dict[str, Any]],
    ):
        self.weather = weather_context # 추천에 기준이 되는 날씨 정보
        self.candidates = candidate_clothes # 체크리스트에서 필터링된 추천 후보(옷)

        self.state = None

    # state 반환
    def reset(self) -> Dict[str, Any]:
        self.state = self._build_state()
        return self.state

    # bandit 구조
    # 다음 상태 없이 한번 실행 = 하나의 보상
    def step(self, action: int, reward: float):
        done = True # one-shot decision
        info = {
            "selected_cloth": self.state["candidates"][action]
        }
        return self.state, reward, done, info

    # state 구성
    # 고정된 날씨에서 후보들의 comfort score를 계산하여
    # dict 구조에 담음
    def _build_state(self) -> Dict[str, Any]:
        candidate_states = []

        for cloth in self.candidates:
            comfort = compute_comfort_score(
                environment_context = self.weather,
                clothing_response = cloth["cloth_props"],
            )

            candidate_states.append({
                "cloth_id": cloth["cloth_id"],
                "comfort_score": comfort,
            })

        return {
            "environment": self.weather,
            "candidates": candidate_states,
        }