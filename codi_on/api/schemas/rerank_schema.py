from typing import List
from pydantic import BaseModel, Field


class ScoreItem(BaseModel):
    clothingId: int
    blendRatioScore: float = Field(..., ge=0.0, le=1.0)


class RerankRequest(BaseModel):
    blendRatioScores: List[ScoreItem]
    userBias: float


class RerankResponseItem(BaseModel):
    clothingId: int
    blendRatioScore: int