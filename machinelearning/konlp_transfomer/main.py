import pickle
import ast
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
import torch
import warnings

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

warnings.filterwarnings("ignore")
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from visualization.pca_visualization import font_prop, visualizations_tsne, visualizations_umap
from sklearn.svm import SVC


def preprocessing_embedding(df):
    device = torch.device("cuda" if torch.cuda.is_available() else "mps"
                          if torch.backends.mps.is_available() else "cpu")

    df["genre"] = df["genre"].apply(lambda row: ast.literal_eval(row))
    # embedding
    embedder = SentenceTransformer("sentence-transformers/xlm-r-base-en-ko-nli-ststb", device=device)
    X_embeddings = embedder.encode(df["synopsis"].tolist(),
                                   convert_to_tensor=False, show_progress_bar=True)
    # normalization
    X_embeddings = normalize(X_embeddings)
    df['synopsis_vectors'] = list(X_embeddings)

    df.to_pickle("data/synopsis_embedding_df.pkl")

def put_label_max_count_genre(df):
    genre_series = df.groupby("labels")["genre"].sum().apply(Counter)
    genre_rank_series = genre_series.apply(lambda row: dict(row.most_common()))
    df["genre_rank_series"] = df["labels"].map(genre_rank_series)

    df.to_pickle("data/synopsis_rank_genre_embedding_label_df.pkl")

# df = pd.read_excel("data/NAVER-Webtoon_OSMU.xlsx")[["synopsis", "genre"]]
# preprocessing_embedding(df)
# pca_kmeans()
if __name__ == '__main__':
    df = pd.read_pickle("data/synopsis_embedding_label.pkl")
    X = np.vstack(df["synopsis_vectors"].values)
    y = np.vstack(df["labels"].values)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
    svm_model = SVC(kernel="rbf", C=1.0, random_state=42, probability=True)
    svm_model.fit(X_train, y_train)

    y_pred = svm_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("acc", accuracy)
