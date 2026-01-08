from fastapi import FastAPI
from final_api_2.routers.rerank_router import router as rerank_router

app = FastAPI(
    title="CodiON API2 - Rerank",
    version="1.0.0"
)

app.include_router(rerank_router)
