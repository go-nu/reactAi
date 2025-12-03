import torch
from fastapi import FastAPI, HTTPException
from train.FM_recommend import MatrixFactorization

app = FastAPI()

# ----------------------------
# 서버 시작 시 모델 + 매핑 로드
# ----------------------------
checkpoint = torch.load("./model/fm_model.pt", map_location="cpu")

n_users = checkpoint["n_users"]
n_items = checkpoint["n_items"]
embedding_dim = checkpoint["embedding_dim"]

user_idx = checkpoint["user_idx"]
item_idx = checkpoint["item_idx"]

# 역매핑: internal_item_index -> real_movie_id
idx_to_item = {v: k for k, v in item_idx.items()}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = MatrixFactorization(n_users, n_items, embedding_dim)
model.load_state_dict(checkpoint["model_state_dict"])
model.eval()
model.to(device)

@app.get("/recommend/{user_id}")
async def recommend(user_id: int, top_k: int = 10):
    # 1) 유저 ID가 학습 데이터에 있는지 확인
    if user_id not in user_idx:
        raise HTTPException(status_code=404, detail=f"user_id {user_id} not found in training data")

    # real user_id -> 내부 인덱스 (0 ~ n_users-1)
    u_index = user_idx[user_id]

    # 2) 모든 아이템 인덱스 텐서 생성: 0,1,2,...,n_items-1
    movie_indices = torch.arange(n_items, dtype=torch.long, device=device)   # (n_items,)

    # 3) 해당 유저 인덱스를 영화 개수만큼 복제
    user_indices = torch.full((n_items,), int(u_index), dtype=torch.long, device=device)  # (n_items,)

    # 4) 모델로 예측
    with torch.no_grad():
        preds = model(user_indices, movie_indices)   # (n_items,)
        preds = preds.detach().cpu()

    # 5) 상위 top_k 아이템 뽑기
    top_k = min(top_k, n_items)
    values, indices = torch.topk(preds, k=top_k)  # values: 예측 점수, indices: 내부 item 인덱스

    top_movies = []
    for rank, (internal_item_idx, score) in enumerate(zip(indices.tolist(), values.tolist()), start=1):
        # internal_item_idx -> 실제 movie_id
        real_movie_id = idx_to_item[internal_item_idx]

        top_movies.append(
            {
                "rank": int(rank),
                "movie_id": int(real_movie_id),   # numpy.int64 방지
                "score": float(score),            # numpy.float 방지
            }
        )

    return {
        "user_id": int(user_id),
        "top_k": int(top_k),
        "recommendations": top_movies,
    }
