import os
import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import time

from pipeline.preprocess import build_feature_vector
from core.models.comfort_mlp import ComfortMLP
from pipeline.config import TRAIN_CONFIG

DATA_PATH = "../artifacts"


class ComfortDataset(Dataset):
    def __init__(self, csv_path: str, use_ap: bool):
        self.df = pd.read_csv(csv_path)
        self.use_ap = use_ap

        self.X = []
        self.y = []

        for _, row in self.df.iterrows():
            features = build_feature_vector(
                c_ratio=row["C_ratio"],
                Ta=row["Ta"],
                RH=row["RH"],
                Va=row["Va"],
                cloud=row["cloud"],
                use_ap=self.use_ap,
            )

            self.X.append(features)
            self.y.append(row["comfort_score"])

        self.X = torch.tensor(self.X, dtype=torch.float32)
        self.y = torch.tensor(self.y, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

def get_loss_function(cfg):
    if cfg["loss"] == "mse":
        return nn.MSELoss()
    else:
        raise ValueError(f"Unsupported loss: {cfg['loss']}")


def get_optimizer(model, cfg):
    opt_name = cfg["optimizer"].lower()
    lr = cfg["learning_rate"]
    wd = cfg.get("weight_decay", 0.0)

    if opt_name == "adam":
        return torch.optim.Adam(
            model.parameters(),
            lr=lr,
            weight_decay=wd
        )

    elif opt_name == "adamw":
        return torch.optim.AdamW(
            model.parameters(),
            lr=lr,
            weight_decay=wd
        )

    elif opt_name == "sgd":
        return torch.optim.SGD(
            model.parameters(),
            lr=lr,
            momentum=cfg.get("momentum", 0.0),
            weight_decay=wd
        )

    elif opt_name == "rmsprop":
        return torch.optim.RMSprop(
            model.parameters(),
            lr=lr,
            weight_decay=wd,
            momentum=cfg.get("momentum", 0.0)
        )

    else:
        raise ValueError(
            f"Unsupported optimizer '{cfg['optimizer']}'. "
            f"Choose from: adam | adamw | sgd | rmsprop"
        )


def regression_accuracy(pred, target, eps=0.05):
    return (torch.abs(pred - target) <= eps).float().mean().item()


class EarlyStopping:
    def __init__(self, patience=10, min_delta=0.0, mode="min"):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode

        self.best = None
        self.counter = 0
        self.should_stop = False

    def step(self, value):
        if self.best is None:
            self.best = value
            return False

        improved = (
            value < self.best - self.min_delta
            if self.mode == "min"
            else value > self.best + self.min_delta
        )

        if improved:
            self.best = value
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True

        return self.should_stop


def train():
    start_time = time.time()

    cfg = TRAIN_CONFIG
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    es = None
    if cfg.get("early_stopping", False):
        mode = "min" if cfg["es_monitor"] == "loss" else "max"
        es = EarlyStopping(
            patience=cfg["es_patience"],
            min_delta=cfg["es_min_delta"],
            mode=mode
        )

    dataset = ComfortDataset(
        csv_path=os.path.join(DATA_PATH, "dataset.csv"),
        use_ap=cfg["use_ap"]
    )

    loader = DataLoader(
        dataset,
        batch_size=cfg["batch_size"],
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )

    model = ComfortMLP(
        input_dim=cfg["input_dim"],
        hidden_dims=cfg["hidden_dims"],
        activation=cfg["activation"],
        dropout=cfg["dropout"],
    ).to(device)

    loss_fn = get_loss_function(cfg)
    optimizer = get_optimizer(model, cfg)

    loss_history = []
    acc_history = []

    LOG_INTERVAL = max(1, cfg["epochs"] // 20)
    ACC_EPS = 0.05   # ← 추후 config로 빼도 됨

    for epoch in range(cfg["epochs"]):
        epoch_loss = 0.0
        epoch_acc = 0.0

        for x, y in loader:
            x = x.to(device)
            y = y.to(device)

            pred = model(x)
            loss = loss_fn(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            epoch_acc += regression_accuracy(pred, y, ACC_EPS)

        epoch_loss /= len(loader)
        epoch_acc /= len(loader)

        loss_history.append(epoch_loss)
        acc_history.append(epoch_acc)

        if epoch % LOG_INTERVAL == 0 or epoch == cfg["epochs"] - 1:
            print(
                f"[{epoch+1}/{cfg['epochs']}] "
                f"loss={epoch_loss:.4f} | acc={epoch_acc:.4f}"
            )
        monitor_value = (
            epoch_loss if cfg["es_monitor"] == "loss"
            else epoch_acc
        )

        if es and es.step(monitor_value):
            print(
                f"🛑 Early stopping at epoch {epoch} "
                f"(best {cfg['es_monitor']}={es.best:.4f})"
            )
            break

    # 시간 측정
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"⏱️ Total training time: {elapsed:.2f} seconds")

    # 모델 저장
    os.makedirs("artifacts", exist_ok=True)
    torch.save(model.state_dict(), "artifacts/model.pt")

    # 📊 Plot (왼쪽 accuracy, 오른쪽 loss)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(acc_history)
    axes[0].set_title("Accuracy (|pred - gt| ≤ ε)")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Accuracy")
    axes[0].grid(True)

    axes[1].plot(loss_history)
    axes[1].set_title("MSE Loss")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Loss")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    train()
