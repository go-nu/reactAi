from ml.rl.env import ClothingRecommendEnv
from ml.rl.io import load_policy

def split_strata(
        candidates: list,
        ratio: float = 0.3,
) -> dict:
    if not candidates:
        return {"high": [], "mid": [], "low": []}

    items = sorted(
        candidates,
        key=lambda x: x["blendRatioScore"],
        reverse=True,
    )

    n = len(items)
    k = max(1, int(ratio * n))
    high = items[:k]
    mid = items[-k:]
    low = items[k:-k] if n > 2 * k else []

    return {"high": high, "mid": mid, "low": low}

def recommend(candidates, weather, user_context):
    agent = load_policy()

    env = ClothingRecommendEnv(
        weather_context=weather,
        candidate_clothes=candidates,
    )
    state = env.build_state()

    strata = split_strata(candidates)

    results = []
    for level in ["high", "mid", "low"]:
        group = strata[level]

        if not group:
            continue

        state = {
            "candidates": [
                {
                    "cloth_id": c["cloth_id"],
                    "blendRatioScore": c["blendRatioScore"],
                }
                for c in group
            ]
        }

        idx = agent.action(state)
        results.append(group[idx])
    return results