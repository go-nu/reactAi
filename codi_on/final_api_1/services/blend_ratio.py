from final_api_1.schemas.recommend_schema import RecommendRequest
from final_api_1.services.inference_service import predict_comfort_batch


def run_blend_ratio(req: RecommendRequest):
    raw_results = predict_comfort_batch(
        context=req.context,
        items=req.items,
    )

    return [
        {
            "clothingId": r.clothingId,
            "score": r.blendRatioScore,
        }
        for r in raw_results
        if r.blendRatioScore is not None
    ]
