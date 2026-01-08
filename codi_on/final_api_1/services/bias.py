from final_api_1.services.rerank_client import rerank_with_api2
# from api.services.feedback_client import fetch_feedback_logs  # Step 4에서 사용

def apply_bias_and_rerank(model_type: str, scored_items: list):
    """
    지금 단계: bias 없음(콜드스타트)
    """
    user_bias = 0.0
    item_bias_map = {}  # clothingId -> bias

    return rerank_with_api2(
        scored_items=scored_items,
        user_bias=user_bias,
        item_bias_map=item_bias_map,
    )
