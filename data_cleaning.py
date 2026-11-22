import pandas as pd
import numpy as np

RAW = "epl_final.csv"
OUT = "matches_clean.csv"

# ---- Load ----
df = pd.read_csv(RAW, encoding="latin-1")

# ---- Rename to project schema ----
df = df.rename(columns={
    "Season": "season", "MatchDate": "Date",
    "FullTimeHomeGoals": "FTHG", "FullTimeAwayGoals": "FTAG",
    "FullTimeResult": "FTR",
    "HalfTimeHomeGoals": "HTHG", "HalfTimeAwayGoals": "HTAG",
    "HalfTimeResult": "HTR",
    "HomeShots": "HS", "AwayShots": "AS",
    "HomeShotsOnTarget": "HST", "AwayShotsOnTarget": "AST",
    "HomeCorners": "HC", "AwayCorners": "AC",
    "HomeFouls": "HF", "AwayFouls": "AF",
    "HomeYellowCards": "HY", "AwayYellowCards": "AY",
    "HomeRedCards": "HR", "AwayRedCards": "AR",
})

# ---- Date parsing (US format M/D/YYYY — confirmed from data) ----
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")
assert df["Date"].isna().sum() == 0, "Unparsed dates found"

# ---- Drop seasons with known source gaps ----
EXCLUDE = ["2003/04", "2004/05"]
df = df[~df["season"].isin(EXCLUDE)].copy()

# ---- Type safety ----
for c in ["FTHG","FTAG","HS","AS","HST","AST"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# ---- Drop any rows still missing goals (should be zero) ----
df = df.dropna(subset=["FTHG","FTAG","FTR"])

# ---- Sanity check: FTR matches goals ----
bad = df[((df.FTHG > df.FTAG) & (df.FTR != "H")) |
         ((df.FTHG < df.FTAG) & (df.FTR != "A")) |
         ((df.FTHG == df.FTAG) & (df.FTR != "D"))]
assert len(bad) == 0, f"{len(bad)} rows have inconsistent FTR"
print(f"OK: {len(bad)} FTR inconsistencies")

# ---- Save ----
df.to_csv(OUT, index=False)
print(f"Saved {OUT}: shape={df.shape}, seasons={df.season.nunique()}")
print(df.groupby("season").size().to_string())
