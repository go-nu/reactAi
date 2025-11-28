import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def visualize_height_weight(df):
    plt.figure(figsize=(5,5))
    plt.scatter(df['Weight(Pounds)'], df['Height(Inches)'])
    plt.xlabel('Weight')
    plt.ylabel('Height')
    plt.xlim(50, 200)
    plt.ylim(50, 200)
    plt.show()

def eigen_values_vectors(df):
    X = df[["Height(Inches)", "Weight(Pounds)"]].to_numpy()
    cov_pivot = np.cov(X.T)

    return np.linalg.eig(cov_pivot)


if __name__ == '__main__':

    list = [1,2,3,4,5,6,7,8,9,10]
    tf = 10 in list
    print(tf)

    exit()


    filename = "data/SOCR-HeightWeight.csv"
    df = pd.read_csv(filename) # DataFrame = table
    # print(df.keys())
    table = df[df["Weight(Pounds)"] >= 150]
    print(table)

    visualize_height_weight(df)
    eigen_values, eigen_vectors = eigen_values_vectors(df)

    print(eigen_values)
    print(eigen_vectors)