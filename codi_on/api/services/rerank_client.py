import requests

API2_BASE_URL = "http://127.0.0.1:8001"

def call_rerank_api(model: str, payload: dict):
    url = f"{API2_BASE_URL}/rerank/{model}"
    resp = requests.post(url, json=payload, timeout=1.0)
    resp.raise_for_status()
    return resp.json()
