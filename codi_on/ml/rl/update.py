from ml.rl.io import load_policy, save_policy
from ml.rl.reward import compute_reward


def update_policy_from_feedback(
        recommend_clothes,
        selected_cloth_ids,
        feedback,
):
    agent = load_policy()

    rewards = compute_reward(
        recommend_clothes,
        selected_cloth_ids,
        feedback,
    )

    agent.update_from_rewards(rewards)
    save_policy(agent)