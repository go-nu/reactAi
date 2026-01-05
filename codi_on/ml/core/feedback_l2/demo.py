# ml/core/feedback_l2/demo.py

from datetime import datetime, timedelta
import random

from ml.core.feedback_l2.types import FeedbackLog
from ml.core.feedback_l2.bias import compute_user_insulation_bias
from ml.core.feedback_l2.config import (
    WINDOW_DAYS,
    UTCI_RANGE,
    DECAY_LAMBDA,
    BIAS_CLAMP,
)

# ---------------------------
# 유틸: 더미 로그 생성기
# ---------------------------

def generate_dummy_logs(
    pattern: str,
    today_utci: float,
    now: datetime,
    n: int = 20
):
    """
    pattern:
      - 'always_cold'
      - 'always_hot'
      - 'mixed'
      - 'recent_hot'
    """
    logs = []

    for i in range(n):
        days_ago = random.randint(0, 40)
        ts = now - timedelta(days=days_ago)

        # 비슷한 날씨 위주로 생성 (±4℃)
        utci = today_utci + random.uniform(-4.0, 4.0)

        if pattern == "always_cold":
            feedback = "cold"

        elif pattern == "always_hot":
            feedback = "hot"

        elif pattern == "mixed":
            feedback = random.choice(["cold", "neutral", "good", "hot"])

        elif pattern == "recent_hot":
            # 최근엔 덥다, 과거엔 보통/춥다
            if days_ago <= 7:
                feedback = "hot"
            else:
                feedback = random.choice(["neutral", "cold"])

        else:
            raise ValueError(f"Unknown pattern: {pattern}")

        logs.append(
            FeedbackLog(
                utci=utci,
                feedback=feedback,
                timestamp=ts,
            )
        )

    return logs


# ---------------------------
# 실험 실행
# ---------------------------

def run_experiment():
    now = datetime.now()
    today_utci = 18.0

    scenarios = [
        "always_cold",
        "always_hot",
        "mixed",
        "recent_hot",
    ]

    print("=== Layer 2 Dummy Experiment ===")
    print(f"WINDOW_DAYS={WINDOW_DAYS}, UTCI_RANGE=±{UTCI_RANGE}, "
          f"DECAY_LAMBDA={DECAY_LAMBDA}, BIAS_CLAMP=±{BIAS_CLAMP}\n")

    for scenario in scenarios:
        logs = generate_dummy_logs(
            pattern=scenario,
            today_utci=today_utci,
            now=now,
            n=30,
        )

        bias = compute_user_insulation_bias(
            logs=logs,
            today_utci=today_utci,
            now=now,
        )

        print(f"[{scenario:>12}] user_insulation_bias = {bias:+.3f}")


if __name__ == "__main__":
    run_experiment()
