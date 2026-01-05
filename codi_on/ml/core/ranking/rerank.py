def rerank_candidates(
    candidates,
    user_insulation_bias,
    alpha=0.1,
):
    for c in candidates:
        # 옷의 방향: (-) 얇음 ← 0.5 → (+) 두꺼움
        direction = c.insulation_cap - 0.5

        adjustment = - user_insulation_bias * direction

        c.rank_score = c.comfort_score + alpha * adjustment

    return sorted(
        candidates,
        key=lambda x: x.rank_score,
        reverse=True,
    )
