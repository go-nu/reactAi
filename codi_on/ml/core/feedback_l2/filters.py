from datetime import datetime

def is_within_window(
        timestamp: datetime,
        now: datetime,
        window_days: int
) -> bool:
    return (now - timestamp).days <= window_days

def is_similar_utci(
        past_utci: float,
        current_utci: float,
        utci_range: float
) -> bool:
    return abs(past_utci - current_utci) <= utci_range