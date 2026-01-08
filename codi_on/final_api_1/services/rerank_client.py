import os
import requests

# 로컬 / 도커 겸용
API2_BASE_URL = os.getenv("API2_BASE_URL", "http://127.0.0.1:8001")

def rerank_with_api2(scored_items: list, user_bias: float, item_bias_map: dict):
    payload = {
        "userBias": user_bias,
        "items": [
            {
                "clothingId": it["clothingId"],
                # API2는 float score 사용 (정렬용), 값은 그대로
                "score": it["score"] / 100.0,
                "itemBias": item_bias_map.get(it["clothingId"], 0.0),
            }
            for it in scored_items
        ],
    }

    resp = requests.post(f"{API2_BASE_URL}/rerank", json=payload, timeout=3)
    resp.raise_for_status()

    # API2는 정렬된 id+score(float) 반환
    ordered = resp.json()["results"]

    # API1 외부 계약 유지: id + score(int) 그대로 반환
    score_map = {it["clothingId"]: it["score"] for it in scored_items}
    return [
        {
            "clothingId": r["clothingId"],
            "score": score_map[r["clothingId"]],
        }
        for r in ordered
    ]
