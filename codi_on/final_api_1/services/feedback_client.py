# api/services/feedback_client.py

def fetch_feedback_logs(model_type: str):
    # 피드백 api 받는 코드

    return []

'''
import requests

JAVA_FEEDBACK_API = "http://backend/internal/feedback/logs"

def fetch_feedback_logs(model_type: str, user_id: int):
    resp = requests.get(
        JAVA_FEEDBACK_API,
        params={
            "userId": user_id,
            "modelType": model_type,
            "days": 30
        }
    )
    resp.raise_for_status()
    return resp.json()["logs"]
'''