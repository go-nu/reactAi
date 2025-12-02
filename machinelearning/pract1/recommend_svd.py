import pickle
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

def extract_data(df, minRating=4.0, custCount=100):
    users = df["user_id"].value_counts().reset_index().iloc[:custCount, :]
    movies = df["movie_id"].value_counts().reset_index().iloc[:, :]
    data = df[(df['user_id'].isin(users['user_id'])) & (df['rating']>=minRating)]
    return data

def svd_predict_model(users, degree=50):
    index = users['user_id'].unique()
    columns = users['movie_id'].unique()
    pivot_df = users.pivot_table(
        index='user_id',
        columns='movie_id',
        values='rating',
        fill_value=None
    )
    means = pivot_df.mean(axis=0)
    pivot_df.fillna(means, inplace=True)

    svd = TruncatedSVD(n_components=degree, random_state=42)
    user_svd = svd.fit_transform(pivot_df)
    matrix = svd.components_
    ratings_predict = user_svd@matrix
    df = pd.DataFrame(data=ratings_predict, columns=columns, index=index)

    unpivot_df = df.stack().reset_index()
    unpivot_df.columns = ['user_id', 'movie_id', 'rating']
    return unpivot_df

# 성능 지표
def performance_metics(data):
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    predict_df = svd_predict_model(train_data)

    comparison_df = pd.merge(predict_df, test_data, on=['user_id', 'movie_id'], how='inner')

    actual_rating = comparison_df['rating_y']
    predicted_rating = comparison_df['rating_x']

    rmse = np.sqrt(mean_squared_error(actual_rating, predicted_rating))
    mae = mean_absolute_error(actual_rating, predicted_rating)

    return rmse, mae


if __name__ == '__main__':
    df = pd.read_pickle('data/ratings.pkl')
    data = extract_data(df)

    performance_metics(data)

    rmse, mae = performance_metics(data)
    print(rmse, mae)