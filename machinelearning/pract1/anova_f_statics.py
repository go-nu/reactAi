import pandas as pd
import numpy as np
import scipy.stats as stats


critical_value = np.array([
        [0.05, 3.841],
        [0.01, 6.635],
        [0.001, 10.828]
    ])

critical_df = pd.DataFrame(critical_value,columns=["유의순준", "임계값"])


if __name__=="__main__":
    df = pd.read_csv("data/amazon_data.csv")
    df = df[["평점", "할인율"]]
    df["할인율"] = df["할인율"].str.replace("%", "", regex=False).astype(float)
    df["평점"] = pd.to_numeric(df["평점"], errors="coerce")

    df["할인율 그룹"] = pd.cut(
        df["할인율"],
        bins = [0, 20, 40, 60, 80, 100],
        labels = ["0~20", "20~40", "40~60", "60~80", "80~100"],
        include_lowest = True
    )
    df.dropna(subset=["평점", "할인율 그룹"], inplace=True)

    #groups = df.groupby("할인율 그룹")
    # for group_name, group_table in groups:
    #     print(group_name, group_table)
    # print(groups)
    # exit()

    # name: 필드, group: 데이터(df) -> df["평점"].values => 행렬 만들기
    dsct_groups = [group["평점"].values
                   for name, group in df.groupby("할인율 그룹", observed=False)]

    # *: 언패킹
    f_stat, p_val = stats.f_oneway(*dsct_groups)

    print(critical_df)
    print("--------------------------------")
    print("f-statistic: ", f_stat)
    print("p-value: ", p_val)