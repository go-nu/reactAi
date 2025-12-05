import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from visualization.pca_visualization import font_prop
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA


Base_path = os.path.dirname(os.path.dirname(__file__))

def lda(df):
    X = np.vstack(df["synopsis_vectors"].values)
    y = df["labels"].values
    lda = LDA(n_components=2)
    lda_results = lda.fit_transform(X, y)
    df['lda_x'] = list(lda_results[:, 0])
    df['lda_y'] = list(lda_results[:, 1])

    plt.figure(figsize=(10, 10))
    sns.scatterplot(x='lda_x', y='lda_y', hue='labels', data=df, palette="viridis", s=50, alpha=.8)
    plt.title("LDA synopsis visualization cluster: 4", fontproperties=font_prop, fontsize=20)
    plt.xlabel("LDA Component 1", fontproperties=font_prop, fontsize=12)
    plt.ylabel("LDA Component 2", fontproperties=font_prop, fontsize=12)
    plt.grid(True)
    save_path = os.path.join(Base_path, 'data/LDA_synopsis_visualization.png')
    plt.savefig(save_path)
    plt.show()