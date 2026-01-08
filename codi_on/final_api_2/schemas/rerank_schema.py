from pydantic import BaseModel
from typing import List


# ▼▼▼ 입력 ▼▼▼
class RerankItem(BaseModel):
    clothingId: int
    score: float
    itemBias: float

class RerankRequest(BaseModel):
    userBias: float
    items: List[RerankItem]


# ▼▼▼ 결과 ▼▼▼
class RerankResult(BaseModel):
    clothingId: int
    score: float

class RerankResponse(BaseModel):
    results: List[RerankResult]
