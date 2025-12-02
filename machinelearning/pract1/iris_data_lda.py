import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler


if __name__ == '__main__':
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 정규화()
    X_normalized = StandardScaler().fit_transform(X)

    # LDA
    lda = LDA(n_components=2) # 성분
    X_lda = lda.fit_transform(X_normalized, y)

    plt.figure(figsize=(5, 5))
    plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y, cmap='viridis', edgecolor='k', s=100)
    plt.xlabel('First Linear Discriminant Component')
    plt.ylabel('Second Linear Discriminant Component')
    plt.title('LDA on iris dataset')
    plt.show()