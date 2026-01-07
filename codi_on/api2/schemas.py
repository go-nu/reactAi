from pydantic import BaseModel, Field
from typing import List

class RerankItem(BaseModel):
    clothingId: int
    score: float = Field(ge=0.0, le=1.0)
    itemBias: float = Field(ge=-1.0, le=1.0)

class RerankRequest(BaseModel):
    userBias: float = Field(ge=-1.0, le=1.0)
    items: List[RerankItem]

class RerankResultItem(BaseModel):
    clothingId: int
    rankScore: int

class RerankResponse(BaseModel):
    results: List[RerankResultItem]

