from dataclasses import dataclass
from datetime import datetime

@dataclass
class FeedbackLog:
    utci: float
    feedback: str
    timestamp: datetime