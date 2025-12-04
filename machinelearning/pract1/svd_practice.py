import numpy as np
import pandas as pd
import pickle
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds

# df = pd.read_csv('data/ratings.dat', sep='::', engine='python')
# df.columns = ['user_id', 'movie_id', 'rating', 'timestamp']
# df.drop(columns=['timestamp'], inplace=True)
# df.to_pickle('data/ratings.pkl')
#
# df = pd.read_pickle('data/ratings.pkl')
# users = df['user_id'].value_counts().index[:200]
# # users = df['user_id'].value_counts().reset_index().iloc[:200, :]
# # users = df['user_id'].value_counts().reset_index().loc[:199, :]
# movies = df['movie_id'].value_counts().reset_index().iloc[:]
# data = df[(df['user_id'].isin(users)) & (df['rating'] >= 4.0)]
# pivot_df = pd.pivot_table(df, index='user_id', columns='movie_id', values='rating', aggfunc='mean')
# pivot_df.to_pickle('data/ratings_pivot.pkl')
#
# df = pd.read_pickle('data/ratings_pivot.pkl')
# means = df.mean(axis=0)
# df.fillna(means, inplace=True)
# df.to_pickle('data/ratings_pivot_means.pkl')

if __name__ == '__main__':
    X = pd.read_pickle('data/ratings_pivot_means.pkl').values
    # U, S, VT = np.linalg.svd(df, full_matrices=False)

    # svd = TruncatedSVD(n_components=2)
    # A_reduced = svd.fit_transform(X) # 차원축소
    # print(A_reduced.shape)

    U, S, VT = svds(X, k=5)
    D = np.diag(S)

    X_new_rating = U@D@VT
    print(X_new_rating)