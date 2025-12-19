from fastapi import FastAPI

from api.config import MODEL_PATH
from api.dependencies.model_loader import get_model
from api.routers import predict

app = FastAPI()
app.include_router(predict.router)

# if __name__ == "__main__":
    # model = get_model()
    # print(model)
