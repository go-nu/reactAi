from fastapi import APIRouter
from final_api_1.schemas.recommend_schema import (
    RecommendRequest,
    RecommendResponse
)
from final_api_1.services.blend_ratio import run_blend_ratio
# from api.services.material_ratio import run_material_ratio

router = APIRouter(
    prefix="/recommend",
    tags=["recommend"]
)

@router.post("/blend-ratio", response_model=RecommendResponse)
def recommend_blend_ratio(req: RecommendRequest):
    return run_blend_ratio(req)

# @router.post("/material-ratio", response_model=RecommendResponse)
# def recommend_material_ratio(req: RecommendRequest):
#     return run_material_ratio(req)
