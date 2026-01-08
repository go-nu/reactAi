# ml/tests/run_recommend_demo.py
from collections import defaultdict
import random

from ml.pipeline.recommend import recommend
from ml.rl.io import load_policy, save_policy
from ml.rl.reward import compute_reward

# -------------------------
# 1. 더미 환경
# -------------------------
environment = {
    "UTCI": 12.0,
    "temp_range": 8.0,
    "sky": "clear",
}

# -------------------------
# 2. 더미 의복 후보 (이미 comfort 계산 전 단계)
# -------------------------
clothes = [
    {"cloth_id": 1, "blendRatioScore": 0.82},
    {"cloth_id": 2, "blendRatioScore": 0.77},
    {"cloth_id": 3, "blendRatioScore": 0.73},
    {"cloth_id": 4, "blendRatioScore": 0.65},
    {"cloth_id": 5, "blendRatioScore": 0.60},
    {"cloth_id": 6, "blendRatioScore": 0.55},
    {"cloth_id": 7, "blendRatioScore": 0.48},
    {"cloth_id": 8, "blendRatioScore": 0.42},
    {"cloth_id": 9, "blendRatioScore": 0.38},
    {"cloth_id": 10, "blendRatioScore": 0.31},
]

user_context = {
    "user_id": 1001,
}

# -------------------------
# 3. 추천 실행
# -------------------------
if __name__ == "__main__":
    agent = load_policy()
    total_rewards = defaultdict(float)

    for step in range(10):
        print(f"\n=== STEP {step+1} ===")

        recommended = recommend(
            candidates=clothes,
            weather=environment,
            user_context=user_context,
        )

        print("Recommended:")
        for c in recommended:
            print(c)

        # -------------------------
        # 4. 사용자 피드백 가정
        # -------------------------
        selected_ids = [recommended[0]["cloth_id"], recommended[1]["cloth_id"]]
        feedback = random.choice([-1, 0, 1])

        rewards = compute_reward(
            recommend_clothes=recommended,
            selected_cloth_ids=selected_ids,
            feedback=feedback,
        )

        print("\nRewards:", rewards)

        for cloth_id, r in rewards.items():
            total_rewards[cloth_id] += r
        # -------------------------
        # 5. RL policy 업데이트
        # -------------------------
        agent.update_from_rewards(rewards)
    save_policy(agent)

    print("\nPolicy updated and saved")
    for cloth_id, r in sorted(total_rewards.items()):
        print(f"cloth_id={cloth_id}: total_reward={r:.2f}")