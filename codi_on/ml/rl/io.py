import pickle
from pathlib import Path

from ml.rl.agent import EpsilonGreedyBandit

POLICY_PATH = Path("ml/artifacts/rl_policy.pkl")

def load_policy():
    if POLICY_PATH.exists():
        with open(POLICY_PATH, "rb") as f:
            return pickle.load(f)
    return EpsilonGreedyBandit(epsilon=0.1)

def save_policy(agent: EpsilonGreedyBandit) -> None:
    POLICY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(POLICY_PATH, "wb") as f:
        pickle.dump(agent, f)