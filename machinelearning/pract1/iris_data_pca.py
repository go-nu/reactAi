import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


if __name__ == '__main__':
    iris = load_iris()
    X = iris.data
    y = iris.target
    # print(X)

    # 정규화(통계적 거리, 마할라노비스 거리)
    X_normalized = StandardScaler().fit_transform(X)
    # print(X_normalized)

    # PCA
    pca = PCA(n_components=2) # 성분
    X_pca = pca.fit_transform(X_normalized)
    # print(X_pca)

    plt.figure(figsize=(5, 5))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis', edgecolor='k', s=100)
    plt.xlabel('First Principal Component')
    plt.ylabel('Second Principal Component')
    plt.title('PCA on iris dataset')
    plt.show()