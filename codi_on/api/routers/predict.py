from fastapi import APIRouter
from api.schemas.predict_schema import ComfortBatchRequest, ComfortBatchResult
from api.services.inference_service import predict_comfort_batch
from api.services.rerank_client import call_rerank_api

router = APIRouter(prefix="/recommend/blend-ratio", tags=["comfort"])

@router.get("/health")
def comfort_health():
    return {"status": "ok"}

@router.post("", response_model=ComfortBatchResult)
def comfort_batch(req: ComfortBatchRequest):
    # batch는 “응답 200 유지”가 목표
    results = predict_comfort_batch(req.context, req.items)
    return ComfortBatchResult(results=results or [])

@router.post("/test/rerank-ml1")
def test_rerank_ml1():
    payload = {
        "userBias": 0.25,
        "items": [
            { "clothingId": 1,  "score": 0.98, "itemBias": 0.10 },
            { "clothingId": 2,  "score": 0.97, "itemBias": -0.05 },
            { "clothingId": 3,  "score": 0.96, "itemBias": -0.20 },
            { "clothingId": 4,  "score": 0.95, "itemBias": 0.30 },
            { "clothingId": 5,  "score": 0.93, "itemBias": 0.10 },
            { "clothingId": 6,  "score": 0.92, "itemBias": 0.00 },
            { "clothingId": 7,  "score": 0.90, "itemBias": -0.35 },
            { "clothingId": 8,  "score": 0.88, "itemBias": 0.15 },
            { "clothingId": 9,  "score": 0.86, "itemBias": 0.25 },
            { "clothingId": 10, "score": 0.84, "itemBias": -0.15 }
        ]
    }

    return call_rerank_api("ml1", payload)