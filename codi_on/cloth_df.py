import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

if __name__ == '__main__':
    data = {
        "C_ratio": [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0],
        "P_ratio": [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        "R_ct":    [0.072, np.nan, 0.069, 0.066, np.nan, 0.060, np.nan, 0.056, np.nan, np.nan, 0.052],
        "R_et":    [np.nan, 9.7, 9.6, 9.1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        "AP":      [np.nan, 77, 83, 101, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    }

    df = pd.DataFrame(data)

    result_df = df.copy()

    # R_ct interpolation
    result_df["R_ct"] = result_df["R_ct"].interpolate(
        method="linear",
        limit_area="inside"
    )

    # R_et extrapolation
    mask_ret = df["R_et"].notna()

    f_ret = interp1d(
        df.loc[mask_ret, "C_ratio"],
        df.loc[mask_ret, "R_et"],
        kind="linear",
        fill_value="extrapolate"
    )

    result_df["R_et"] = f_ret(result_df["C_ratio"])

    # AP extrapolation
    mask_ap = df["AP"].notna()

    f_ap = interp1d(
        df.loc[mask_ap, "C_ratio"],
        df.loc[mask_ap, "AP"],
        kind="linear",
        fill_value="extrapolate"
    )

    result_df["AP"] = f_ap(result_df["C_ratio"])

    print(result_df)
