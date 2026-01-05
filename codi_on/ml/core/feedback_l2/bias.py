import math
from datetime import datetime
from typing import List

from ml.core.feedback_l2.config import WINDOW_DAYS, UTCI_RANGE, DECAY_LAMBDA, BIAS_CLAMP
from ml.core.feedback_l2.filters import is_within_window, is_similar_utci
from ml.core.feedback_l2.mapping import FEEDBACK_TO_DELTA
from ml.core.feedback_l2.types import FeedbackLog

def compute_user_insulation_bias(
        logs: List[FeedbackLog],
        today_utci: float,
        now: datetime,
) -> float:
    weighted_sum = 0.0
    weight_total = 0.0

    for log in logs:
        if not is_within_window(log.timestamp, now, WINDOW_DAYS):
            continue

        if not is_similar_utci(log.utci, today_utci, UTCI_RANGE):
            continue

        if log.feedback not in FEEDBACK_TO_DELTA:
            continue

        delta = FEEDBACK_TO_DELTA[log.feedback]

        days_ago = (now - log.timestamp).days
        weight = math.exp(-DECAY_LAMBDA * days_ago)

        weighted_sum += weight * delta
        weight_total += weight

    if weight_total == 0:
        return 0.0

    bias = weighted_sum / weight_total

    return max(-BIAS_CLAMP, min(BIAS_CLAMP, bias))
