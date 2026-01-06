def rerank(scores, user_bias, alpha=0.15):
    values = [s["blendRatioScore"] for s in scores]
    mu = sum(values) / len(values)

    ranked = sorted(
        scores,
        key=lambda x: (
            x["blendRatioScore"]
            + alpha * user_bias * (x["blendRatioScore"] - mu)
        ),
        reverse=True
    )

    return ranked
