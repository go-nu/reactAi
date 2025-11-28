import pandas as pd
import numpy as np


if __name__ == "__main__":
    df = pd.read_csv("./data/amazon.csv")

    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df["user_name"] = df["user_name"].astype(str).str.split(",")
    df_explode = df.explode("user_name")
    df_explode = df_explode.dropna(subset=["rating", 'user_name'])
    # df_explode.info()

    # exit()

    pivot_table = pd.pivot_table(
        df_explode,
        values="rating",
        index="user_name",
        columns="product_name",
        aggfunc="mean",
        fill_value= np.nan
    )
    means = pivot_table.mean(axis=0)
    pivot_table.fillna(means, inplace=True)

    print(pivot_table.iloc[0, :3].tolist())
