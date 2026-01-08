from fastapi import APIRouter
from final_api_2.schemas.rerank_schema import RerankRequest, RerankResponse
from final_api_2.services.rerank_service import rerank_items

router = APIRouter(
    prefix="/rerank",
    tags=["rerank"]
)

@router.post("", response_model=RerankResponse)
def rerank(req: RerankRequest):
    print(
        f"[DEBUG][API2] rerank endpoint HIT | "
        f"userBias={req.userBias} | items={len(req.items)}"
    )

    results = rerank_items(
        user_bias=req.userBias,
        items=[item.dict() for item in req.items],
    )
    return {"results": results}
