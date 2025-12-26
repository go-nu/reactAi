from typing import Dict, List, Any
import random

from ml.rl.agent import EpsilonGreedyBandit
from ml.rl.env import ClothingRecommendEnv
from ml.rl.reward import feedback_to_reward


def run_bandit_episode(
        env: ClothingRecommendEnv,
        agent: EpsilonGreedyBandit,
        feedback: str,
):
    state = env.reset()

    action = agent.action(state)

    selected_cloth_id = state["candidates"][action]["cloth_id"]

    reward = feedback_to_reward(feedback)

    _, r, done, info = env.step(action, reward)

    agent.update(selected_cloth_id, r)

    return {
        "action": action,
        "cloth_id": selected_cloth_id,
        "reward": r,
        "done": done,
    }

if __name__ == "__main__":
    weather_context = {
        "UTCI": 5.0,
        "temp_range": 7.0,
        "weather_type": "clear"
    }

    candidate_clothes = [
        {"cloth_id": 1, "cloth_props": {"R_ct": 0.05, "R_et": 12.0, "AP": 70}},  # 얇고 통기 좋음
        {"cloth_id": 2, "cloth_props": {"R_ct": 0.07, "R_et": 10.0, "AP": 60}},
        {"cloth_id": 3, "cloth_props": {"R_ct": 0.09, "R_et": 9.0,  "AP": 55}},
        {"cloth_id": 4, "cloth_props": {"R_ct": 0.10, "R_et": 8.5,  "AP": 50}},
        {"cloth_id": 5, "cloth_props": {"R_ct": 0.11, "R_et": 8.0,  "AP": 45}},

        {"cloth_id": 6, "cloth_props": {"R_ct": 0.12, "R_et": 7.5,  "AP": 40}},
        {"cloth_id": 7, "cloth_props": {"R_ct": 0.13, "R_et": 7.0,  "AP": 35}},
        {"cloth_id": 8, "cloth_props": {"R_ct": 0.14, "R_et": 6.5,  "AP": 30}},
        {"cloth_id": 9, "cloth_props": {"R_ct": 0.15, "R_et": 6.0,  "AP": 25}},  # 두껍고 통기 낮음
        {"cloth_id":10, "cloth_props": {"R_ct": 0.16, "R_et": 5.5,  "AP": 20}},
    ]

    env = ClothingRecommendEnv(weather_context, candidate_clothes)

    agent = EpsilonGreedyBandit(epsilon=0.4)

    fake_feedbacks = ["like", "neutral", "dislike"]

    for episode in range(50):
        feedback = random.choice(fake_feedbacks)

        result = run_bandit_episode(env, agent, feedback)

        print("\n"
            f"[Episode {episode+1}] "
            f"cloth={result['cloth_id']} "
            f"reward={result['reward']}"
        )

        print("=== Agent Stats ===")
        for cloth_id, stats in agent.get_stats().items():
            print(f"cloth {cloth_id}: {stats}")