from fastapi import FastAPI
from final_api_1.routers.recommend_router import router as recommend_router

app = FastAPI(
    title="CodiON API1 - Comfort Score",
    version="1.0.0"
)

# 외부 노출 엔드포인트
app.include_router(recommend_router)
