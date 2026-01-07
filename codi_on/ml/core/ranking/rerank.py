def rerank_candidates(
    candidates,
    user_insulation_bias,  # == userBias
    alpha=0.1,
):
    for c in candidates:
        # itemBias: [-1, +1]
        adjustment = user_insulation_bias * c.itemBias

        c.rank_score = c.comfort_score + alpha * adjustment

    return sorted(
        candidates,
        key=lambda x: x.rank_score,
        reverse=True,
    )
