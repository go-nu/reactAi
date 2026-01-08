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

    def rank_key(item: dict) -> float:
        rank_score = item["score"] + ALPHA * user_bias * item["itemBias"]
        print(
            f"[DEBUG][API2] rank_score "
            f"(id={item['clothingId']}): {rank_score}"
        )
        return rank_score

    sorted_items = sorted(items, key=rank_key, reverse=True)

    print("[DEBUG][API2] items (sorted order):")
    for it in sorted_items:
        print(f"  - id={it['clothingId']} score={it['score']}")

    print("[DEBUG][API2] ===== Rerank End =====\n")

    return [
        {
            "clothingId": it["clothingId"],
            "score": it["score"],
        }
        for it in sorted_items
    ]