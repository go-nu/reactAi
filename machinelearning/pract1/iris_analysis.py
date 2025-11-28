import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

# 함수, 클래스, 전역변수



# 실행 코드
# 'data', 'target', 'target_names', 'feature_names'
if __name__ == "__main__":
    iris = load_iris()
    X = iris.data
    Cov = X.T @ X
    print(Cov)
