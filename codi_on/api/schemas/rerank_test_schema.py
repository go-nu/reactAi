from pydantic import BaseModel, Field
from typing import List

class CandidateItem(BaseModel):
    clothingId: int
    score: float = Field(ge=0.0, le=1.0)
    itemBias: float = Field(ge=-1.0, le=1.0)

class RerankTestRequest(BaseModel):
    userBias: float = Field(ge=-1.0, le=1.0)
    candidates: List[CandidateItem]
