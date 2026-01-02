from typing import Optional

def compute_reward(
        recommend_clothes: list,
        selected_cloth_ids: list,
        feedback: float,
):
    rewards = {}
    for cloth in recommend_clothes:
        rewards[cloth["cloth_id"]] = feedback * 0.3
    for cloth_id in selected_cloth_ids:
        rewards[cloth_id] += 1.0

    return rewards