from fastapi import APIRouter
from api.schemas.rerank_schema import (
    RerankRequest,
    RerankResponseItem,
)
from api.services.rerank_service import rerank

router = APIRouter(
    prefix="/rerank",
    tags=["rerank"]
)

# 임시 insulation lookup (실서비스에서는 캐시/메모리)
INSULATION_LOOKUP = {
    12: 0.8,
    34: 0.3,
    56: 0.5,
}


@router.post("", response_model=list[RerankResponseItem])
def rerank_endpoint(req: RerankRequest):
    result = rerank(
        scores=[s.dict() for s in req.scores],
        user_bias=req.userBias,
        insulation_lookup=INSULATION_LOOKUP,
    )
    return result
