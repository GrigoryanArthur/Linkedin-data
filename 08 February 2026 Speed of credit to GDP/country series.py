import pandas as pd
import numpy as np

# ---- settings you change ----
file_path = "C:\\Users\\Arthur\\OneDrive\\Documents\\Linkedin data\\08 February 2026 Speed of credit to GDP\\"
credit_df = pd.read_excel(file_path+'Credit to GDP worldbank.xlsx', sheet_name='Final')
threshold_df = pd.read_excel(file_path+'time_to_threshold_results.xlsx', sheet_name='Final')

# ---- 1) reshape master credit data to long ----
credit_long = credit_df.melt(
    id_vars="Country Code",
    var_name="year",
    value_name="credit_to_gdp"
)

credit_long["year"] = pd.to_numeric(credit_long["year"], errors="coerce")

# ---- 2) merge thresholds ----
m = credit_long.merge(
    threshold_df[["Country Code", "year_thr1", "year_thr2"]],
    on="Country Code",
    how="inner"
)

# ---- 3) keep only the path from 50% to 100% ----
path_df = m[
    (m["year"] >= m["year_thr1"]) &
    (m["year"] <= m["year_thr2"])
].dropna(subset=["credit_to_gdp"])

# ---- 4) sort nicely ----
path_df = path_df.sort_values(["Country Code", "year"])

# ---- 5) export ----
path_df.to_excel("credit_paths_50_to_100.xlsx", index=False)





