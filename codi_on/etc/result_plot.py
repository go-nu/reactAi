import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. CSV 로드
df = pd.read_csv('../ml/artifacts/test_predict.csv')

# 2. error 사용 (안전하게 절대값 보장)
errors = df['error'].abs()
# 또는 더 안전하게:
# errors = (df['gt'] - df['pred']).abs()

# 3. bin 설정 (tolerance = 0.02)
tolerance = 0.02
max_error = errors.max()
bins = np.arange(0, max_error + tolerance, tolerance)

# 4. 히스토그램 (비율 기준)
plt.figure(figsize=(7, 5))
plt.hist(
    errors,
    bins=bins,
    weights=[1 / len(errors)] * len(errors),
    color='lightgray',
    edgecolor='black'
)

# 5. tolerance 기준선
plt.axvline(
    tolerance,
    color='red',
    linestyle='--',
    linewidth=2,
    label='Tolerance = 0.02'
)

plt.xlabel('|y − ŷ|')
plt.ylabel('Ratio')
plt.title('Prediction Error Distribution (Bin width = 0.02)')
plt.legend()

plt.tight_layout()
plt.show()
