import pandas as pd
import torch
from tqdm import tqdm
import os

from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader

from train.FM_recommend import MatrixFactorization, device, evaluate, extract_rating, RatingsDataset

MODEL_PATH = "../model"

def learning_train(user_ids, item_ids, train_loader, test_data, learning_rate, vector_dim, epochs):
    n_users = len(user_ids)
    n_items = len(item_ids)

    vector_dim = int(vector_dim)

    model = MatrixFactorization(n_users=n_users, n_items=n_items, embedding_dim=vector_dim).to(device)
    loss_fn = torch.nn.MSELoss()
    # backpropagation
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0
        num_samples = 0

        batch_tensor = tqdm(train_loader, desc=f"Epoch {epoch}/{epochs}", leave=False)

        for user, item, rating in batch_tensor:
            user = user.to(device)
            item = item.to(device)
            rating = rating.float().to(device)

            optimizer.zero_grad() # grad = gradient = 미분
            pred = model(user, item)
            loss = loss_fn(pred, rating)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            num_samples += batch_size

            batch_tensor.set_postfix(loss=loss.item())

        avg_loss = total_loss / num_samples
        print(f"Epoch [{epoch+1}/{epochs}] - loss: {avg_loss: .4f}")

    # 평가
    evaluate(model, test_data, device=device)

    # save model
    os.makedirs(MODEL_PATH, exist_ok=True)
    save_path = os.path.join(MODEL_PATH, "fm_model.pt")
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "n_users": n_users,
            "n_items": n_items,
            "embedding_dim": vector_dim,
            "user_idx": user_idx,
            "item_idx": item_idx,
        },
        save_path,
    )
    print(f"모델 저장 완료 -> {save_path}")

if __name__ == "__main__":
    vector_dim = 64
    epochs = 10
    learning_rate = 0.001 # 0.0001
    batch_size = 64

    df = extract_rating(pd.read_pickle("../data/ratings.pkl"))
    user_ids = df["user_id"].unique()
    item_ids = df["movie_id"].unique()

    user_idx = {u: i for i, u in enumerate(user_ids)}
    item_idx = {item: i for i, item in enumerate(item_ids)}
    df["user_idx"] = df["user_id"].map(user_idx)
    df["item_idx"] = df["movie_id"].map(item_idx)

    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

    train_dataset = RatingsDataset(
        torch.LongTensor(train_data["user_idx"].values),
        torch.LongTensor(train_data["item_idx"].values),
        torch.LongTensor(train_data["rating"].values),
    )
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    learning_train(user_ids, item_ids, train_loader, test_data, learning_rate, vector_dim, epochs)