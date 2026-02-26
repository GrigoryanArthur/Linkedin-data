import pandas as pd
import numpy as np

# ---- settings you change ----
file_path = r"C:\Users\Arthur\OneDrive\Documents\Linkedin data\08 February 2026 Speed of credit to GDP\Credit to GDP worldbank.xlsx"
sheet_name = "Final"          # change if needed
country_col = "Country Code"   # or whatever your first column name is
thr1 = 0.5
thr2 = 1.0

# if True: if first observed value is already >= thr2, return NaN (no observable transition)
require_transition = True
# ----------------------------

df = pd.read_excel(file_path, sheet_name=sheet_name)

# Identify year columns (works if they are like 1960, 1961, ... as ints or strings)
year_cols = [c for c in df.columns if str(c).isdigit()]
year_cols_sorted = sorted(year_cols, key=lambda x: int(x))

def time_to_threshold(row, thr1, thr2, require_transition=True):
    s = row[year_cols_sorted]

    # coerce to numeric, keep years where value is present
    v = pd.to_numeric(s, errors="coerce")
    if v.notna().sum() == 0:
        return pd.Series({"year_thr1": np.nan, "year_thr2": np.nan, "years_diff": np.nan})

    first_year = v.first_valid_index()
    if require_transition and v.loc[first_year] >= thr2:
        return pd.Series({"year_thr1": np.nan, "year_thr2": np.nan, "years_diff": np.nan})

    # year when >= thr1 (chronological)
    hit1 = v[v >= thr1]
    if hit1.empty:
        return pd.Series({"year_thr1": np.nan, "val_thr1": np.nan,
                  "year_thr2": np.nan, "val_thr2": np.nan,
                  "years_diff": np.nan})

    y1 = hit1.index[0]

    # year when >= thr2 after y1
    v_after = v.loc[y1:]
    hit2 = v_after[v_after >= thr2]
    if hit2.empty:
        return pd.Series({"year_thr1": y1, "val_thr1": float(v.loc[y1]),
                  "year_thr2": np.nan, "val_thr2": np.nan,
                  "years_diff": np.nan})

    y2 = hit2.index[0]

    v1 = float(v.loc[y1])
    v2 = float(v.loc[y2])


    return pd.Series({
    "year_thr1": y1,
    "val_thr1": v1,
    "year_thr2": y2,
    "val_thr2": v2,
    "years_diff": int(y2) - int(y1)})


out = df.apply(time_to_threshold, axis=1, thr1=thr1, thr2=thr2, require_transition=require_transition)
result = pd.concat([df[[country_col]], out], axis=1)

# Save results
result.to_excel("time_to_threshold_results.xlsx", index=False)

print(result.head(10))
