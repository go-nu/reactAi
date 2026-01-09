import random
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

# =========================
# 0. 설정
# =========================
USER_ID = 1
N_ITEMS = 30
N_DAYS = 30
N_LOGS = utci = random.randint(22, 30)
SEED = 42
ALPHA = 0.1

# random.seed(SEED)

# =========================
# 1. 피드백 정의 (설계 그대로)
# =========================
FEEDBACK_TO_DIR = {
    "HOT": +1.0,
    "OK": 0.0,
    "COLD": -1.0,
}

# =========================
# 2. UTCI weight (Java 로직과 동일)
# =========================
def utci_weight(utci: float) -> float:
    if utci > 46:
        return 0.1
    if utci > 38:
        return 0.2
    if utci > 32:
        return 0.4
    if utci > 26:
        return 0.7
    if utci >= 9:
        return 1.0
    if utci >= 0:
        return 0.7
    if utci >= -13:
        return 0.4
    if utci >= -27:
        return 0.2
    return 0.1

# =========================
# 3. 피드백 로그 구조
# =========================
@dataclass
class FeedbackLog:
    userId: int
    itemId: int
    feedback: str
    utci: float
    created_at: datetime

# =========================
# 4. 피드백 로그 생성 (시뮬레이션)
# =========================
def generate_feedback_logs():
    logs = []
    now = datetime.now()

    for _ in range(N_LOGS):
        itemId = random.randint(1, N_ITEMS)
        day_offset = random.randint(0, N_DAYS - 1)

        feedback = random.choice(["HOT", "OK", "COLD"])
        utci = random.randint(-7, 4)

        logs.append(
            FeedbackLog(
                userId=USER_ID,
                itemId=itemId,
                feedback=feedback,
                utci=utci,
                created_at=now - timedelta(days=day_offset),
            )
        )
    return logs

# =========================
# 5. bias 계산 (공통 로직)
# =========================
def calculate_bias(logs):
    weighted_sum = 0.0
    weight_sum = 0.0

    for log in logs:
        direction = FEEDBACK_TO_DIR[log.feedback]
        weight = utci_weight(log.utci)

        weighted_sum += direction * weight
        weight_sum += weight

    if weight_sum == 0:
        return 0.0

    bias = weighted_sum / weight_sum
    return max(-1.0, min(1.0, bias))

# =========================
# 6. userBias / itemBias 계산
# =========================
def compute_user_bias(logs):
    return calculate_bias(logs)

def compute_item_biases(logs):
    by_item = defaultdict(list)
    for log in logs:
        by_item[log.itemId].append(log)

    return {
        itemId: calculate_bias(item_logs)
        for itemId, item_logs in by_item.items()
    }

# =========================
# 7. Candidate
# =========================
@dataclass
class Candidate:
    itemId: int
    score: float       # API1 결과 흉내 (comfort_score)
    itemBias: float
    rank_score: float = None

# =========================
# 8. Rerank (API2 핵심 로직)
# =========================
def rerank_candidates(candidates, userBias, alpha):
    for c in candidates:
        c.rank_score = c.score + alpha * userBias * c.itemBias

    return sorted(candidates, key=lambda x: x.rank_score, reverse=True)

# =========================
# 9. 실행 (리스트 비교용 출력)
# =========================
if __name__ == "__main__":

    logs = generate_feedback_logs()

    userBias = compute_user_bias(logs)
    itemBiases = compute_item_biases(logs)

    # 후보 생성
    candidates = []
    for itemId in range(1, N_ITEMS + 1):
        score = random.uniform(0.96, 1.0)
        itemBias = itemBiases.get(itemId, 0.0)
        candidates.append(Candidate(itemId, score, itemBias))

    # (1) 기존 score 기준 정렬
    before = sorted(
        candidates,
        key=lambda x: x.score,
        reverse=True,
    )

    before_scores = [
        (c.itemId, round(c.score, 3))
        for c in before
    ]

    # (2) rerank
    ranked = rerank_candidates(candidates, userBias, ALPHA)

    after_scores = [
        (c.itemId, round(c.rank_score, 3))
        for c in ranked
    ]

    # (3) 출력
    print("\n[기존 score 기준 정렬]")
    print(before_scores)

    print("\n[rank_score 기준 정렬]")
    print(after_scores)

    exit()
# =========================
# 9. 실행
# =========================
if __name__ == "__main__":

    # (1) 피드백 로그 생성
    logs = generate_feedback_logs()

    # (2) bias 계산
    userBias = compute_user_bias(logs)
    itemBiases = compute_item_biases(logs)

    print(f"\nUserBias: {userBias:+.3f}")

    # (3) 후보 생성 (API1 결과 흉내)
    candidates = []
    for itemId in range(1, N_ITEMS + 1):
        score = random.uniform(0.96, 1.0)
        itemBias = itemBiases.get(itemId, 0.0)
        candidates.append(Candidate(itemId, score, itemBias))

    # (4) rerank
    ranked = rerank_candidates(candidates, userBias, ALPHA)

    # (5) 결과 출력
    print("\nTop 10 ranked items:")
    for c in ranked[:20]:
        print(
            f"Item {c.itemId:2d} | "
            f"score={c.score:.3f} | "
            # f"itemBias={c.itemBias:+.3f} | "
            f"rank={c.rank_score:.3f}"
        )
