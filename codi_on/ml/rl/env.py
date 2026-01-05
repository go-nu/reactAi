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

    def build_state(self) -> Dict[str, Any]:
        return {
            "candidates": [
                {
                    "cloth_id": c["cloth_id"],
                    "blendRatioScore": c["blendRatioScore"],
                }
                for c in self.candidates
            ]
        }
