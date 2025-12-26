# 사용자 피드백을 점수로 바꾸는 로직
# 실제 로직에 맞춰 추후 수정
def feedback_to_reward(feedback: str) -> float:
    if feedback == "like":
        return 1.0
    elif feedback == "neutral":
        return 0.0
    elif feedback == "dislike":
        return -1.0
    else:
        raise Exception(f"Unknown feedback: {feedback}")