from api2.schemas import RerankRequest, RerankResponse, RerankResultItem
from api2.config import RERANK_ALPHA

def score_0_1_to_0_100(score: float) -> int:
    score = max(0.0, min(1.0, score))
    return int(round(score * 100))

def rerank(req: RerankRequest) -> RerankResponse:
    results = []

    for item in req.items:
        rank_score = (
            item.score
            + RERANK_ALPHA * req.userBias * item.itemBias
        )
        output_score = score_0_1_to_0_100(rank_score)

        results.append(
            RerankResultItem(
                clothingId=item.clothingId,
                rankScore=output_score
            )
        )

    results.sort(key=lambda x: x.rankScore, reverse=True)
    return RerankResponse(results=results)
