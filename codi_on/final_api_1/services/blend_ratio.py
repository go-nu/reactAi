from final_api_1.schemas.recommend_schema import (
    RecommendRequest,
    RecommendResponse,
    RecommendResult,
)
from final_api_1.services.bias import apply_bias_and_rerank

from api.services.inference_service import predict_comfort_batch


def run_blend_ratio(req: RecommendRequest) -> RecommendResponse:
    raw_results = predict_comfort_batch(
        context=req.context,
        items=req.items,
    )

    scored_items = [
        {
            "clothingId": r.clothingId,
            "score": r.blendRatioScore,
        }
        for r in raw_results
        if r.blendRatioScore is not None
    ]

    reranked = apply_bias_and_rerank(
        model_type="BLEND_RATIO",
        scored_items=scored_items,
    )

    return RecommendResponse(
        results=[
            RecommendResult(
                clothingId=item["clothingId"],
                blendRatioScore=item["score"],
            )
            for item in reranked
        ]
    )
