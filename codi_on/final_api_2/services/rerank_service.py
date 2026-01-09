from final_api_2.config import ALPHA

def rerank_items(user_bias: float, items: list[dict]) -> list[dict]:
    print("\n[DEBUG][API2] ===== Rerank Start =====")
    print("[DEBUG][API2] userBias:", user_bias)
    print("[DEBUG][API2] alpha:", ALPHA)
    print("[DEBUG][API2] items (input):")

    for it in items:
        print(
            f"  - id={it['clothingId']} "
            f"score={it['score']} "
            f"itemBias={it['itemBias']}"
        )

    for it in items:
        rank_score = it["score"] + ALPHA * user_bias * it["itemBias"]
        print(
            f"[DEBUG][API2] rank_score "
            f"(id={it['clothingId']}): {rank_score}"
    )

    print("[DEBUG][API2] ===== Rerank End =====\n")

    return [
        {
            "clothingId": it["clothingId"],
            "score": it["score"],
        }
        for it in items
    ]
