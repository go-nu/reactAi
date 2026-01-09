import os
import requests

JAVA_BACKEND_URL = os.getenv(
    "JAVA_BACKEND_URL",
    "http://127.0.0.1:8080"
)

def fetch_feedback_logs(user_id: int, model_type: str) -> list:
    resp = requests.get(
        f"{JAVA_BACKEND_URL}/api/feedback/logs", # java api
        params={
            "userId": user_id,
            "modelType": model_type,
            "days": 30,
        },
        timeout=3,
    )
    resp.raise_for_status()
    return resp.json()
