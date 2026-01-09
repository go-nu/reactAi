from fastapi import APIRouter
from final_api_1.schemas.recommend_schema import (
    RecommendRequest,
    RecommendResponse,
    RecommendResult,
)
from final_api_1.services.blend_ratio import run_blend_ratio
from final_api_1.services.feedback_recommend import run_feedback_recommend

router = APIRouter(
    prefix="/recommend",
    tags=["recommend"]
)

@router.post("/blend-ratio", response_model=RecommendResponse)
def recommend_blend_ratio(req: RecommendRequest):

    scored_items = run_blend_ratio(req)

    return RecommendResponse(
        results=[
            RecommendResult(
                clothingId=item["clothingId"],
                blendRatioScore=round(item["score"] * 100),
            )
            for item in scored_items
        ]
    )


@router.post("/yesterday-feedback", response_model=RecommendResponse)
def recommend_with_feedback(req: RecommendRequest):

    result = run_feedback_recommend(req)  # dict 반환

    return RecommendResponse(
        date=result["date"],
        results=[
            RecommendResult(
                clothingId=item["clothingId"],
                blendRatioScore=round(item["score"] * 100),
            )
            for item in result["results"]
        ]
    )

# @router.post("/material-ratio", response_model=RecommendResponse)
# def recommend_material_ratio(req: RecommendRequest):
#     return run_material_ratio(req)
