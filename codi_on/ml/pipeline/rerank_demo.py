import pandas as pd
import numpy as np
import random

from ml.core.ranking.rerank import rerank_candidates


# ---------------------------
# 데모용 Candidate 구조
# ---------------------------
class Candidate:
    def __init__(self, idx, comfort_score, insulation_cap):
        self.idx = idx
        self.comfort_score = comfort_score
        self.insulation_cap = insulation_cap
        self.rank_score = comfort_score  # 초기값


# ---------------------------
# 데모 실행
# ---------------------------
def run_demo(
    csv_path="../artifacts/test_predict.csv",
    sample_size=30,
    user_insulation_bias=+0.25, # 피드백 바탕으로 계산되는 값, 더위(+) ~ 추위(-)
    alpha=0.15, # 피드백의 영향력 0.05 ~ 0.15 / 0.15 ~ 0.25 / 0.3 이상
    # seed=0,
):
    # random.seed(seed)
    # np.random.seed(seed)

    df = pd.read_csv(csv_path)

    if "pred" not in df.columns:
        raise ValueError("test_predict.csv must contain 'pred' column")

    # sampled = df.sample(n=sample_size, random_state=seed).reset_index()
    sampled = df.sample(n=sample_size).reset_index()

    candidates = []
    for i, row in sampled.iterrows():
        candidates.append(
            Candidate(
                idx=i,
                comfort_score=float(row["pred"]),
                insulation_cap=float(np.random.uniform(0.0, 1.0)),  # 데모용
            )
        )

    before = sorted(
        candidates,
        key=lambda x: x.comfort_score,
        reverse=True,
    )

    after = rerank_candidates(
        candidates=candidates,
        user_insulation_bias=user_insulation_bias,
        alpha=alpha,
    )

    print("\n==============================")
    print(" Layer 2 Rerank Demo")
    print("==============================")
    print(f"user_insulation_bias = {user_insulation_bias:+.2f}")
    print(f"alpha = {alpha}\n")

    print("---- Before (comfort_score) ----")
    for c in before[:10]:
        print(
            f"id={c.idx:4d} | "
            f"comfort={c.comfort_score:.3f} | "
            f"insul={c.insulation_cap:.2f}"
        )

    print("\n---- After (rank_score) ----")
    for c in after[:10]:
        print(
            f"id={c.idx:4d} | "
            f"comfort={c.comfort_score * 100:6.1f} | "
            f"rank={c.rank_score * 100:6.1f} | "
            f"insul={c.insulation_cap:.2f}"
        )


if __name__ == "__main__":
    run_demo()