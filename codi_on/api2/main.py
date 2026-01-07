from fastapi import APIRouter, FastAPI
from api2.schemas import RerankRequest, RerankResponse
from api2.rerank_service import rerank

app = FastAPI(title="CodiON API2 - Rerank")

router = APIRouter(
    prefix="/rerank",
    tags=["rerank"]
)

@router.post("/ml1", response_model=RerankResponse)
def rerank_ml1(req: RerankRequest):
    return rerank(req)

@router.post("/ml2", response_model=RerankResponse)
def rerank_ml2(req: RerankRequest):
    return rerank(req)

app.include_router(router)
