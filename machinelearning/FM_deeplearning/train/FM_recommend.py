import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import torch
from torch import nn
from torch.utils.data import Dataset

# GPU(Windows)/MPS(Mac)/CPU
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Mac OS")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print("CUDA")
else:
    device = torch.device("cpu")
    print("CPU")

def extract_rating(df, custCount=10000, minRating=4.0):
    users = df["user_id"].value_counts().reset_index().iloc[:custCount, :]
    data = df[(df['user_id'].isin(users['user_id'])) & (df['rating']>=minRating)]
    return data

class RatingsDataset(Dataset):
    def __init__(self, users, items, ratings):
        self.users = users
        self.items = items
        self.ratings = ratings

    def __len__(self):
        return len(self.users)

    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.ratings[idx]

class MatrixFactorization(nn.Module):
    def __init__(self, n_users, n_items, embedding_dim):
        super(MatrixFactorization, self).__init__()
        self.users_embedding = nn.Embedding(n_users, embedding_dim)
        self.items_embedding = nn.Embedding(n_items, embedding_dim)

        # uniform_(평균, 분산) 정규화
        self.users_embedding.weight.data.uniform_(0, 0.05)
        self.items_embedding.weight.data.uniform_(0, 0.05)

    # call 함수, 모델 생성 이후 제일 먼저 실행하는 함수
    def forward(self, users, items):
        users_vector = self.users_embedding(users)
        items_vector = self.items_embedding(items)
        # sum(axis)
        ratings = (users_vector * items_vector).sum(1)
        return ratings

def evaluate(model, test_data, device=device):
    model.eval()
    with torch.no_grad():
        test_users = torch.LongTensor(test_data['user_idx'].values).to(device)
        test_items = torch.LongTensor(test_data['item_idx'].values).to(device)
        # forward(call 함수) 실행
        preds_tensor = model(test_users, test_items)
    preds = preds_tensor.detach().cpu().numpy()
    actuals = test_data['rating'].values

    rmse = np.sqrt(mean_squared_error(actuals, preds))
    mae = mean_absolute_error(actuals, preds)
    print(f"RMSE:, {rmse:.4f}", f"MAE:, {mae:.4f}")

if __name__ == "__main__":
    pass
