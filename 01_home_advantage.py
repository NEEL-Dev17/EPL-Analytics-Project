import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("matches_clean.csv", encoding="latin-1")
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")

# ---- Match-level points ----
df["home_pts"] = np.where(df.FTR=="H", 3, np.where(df.FTR=="D", 1, 0))
df["away_pts"] = np.where(df.FTR=="A", 3, np.where(df.FTR=="D", 1, 0))

# ---- 2a. Welch's t-test ----
t, p = stats.ttest_ind(df.home_pts, df.away_pts, equal_var=False)
gap = df.home_pts.mean() - df.away_pts.mean()
print("=== T-TEST ===")
print(f"n matches: {len(df)}")
print(f"Home ppg: {df.home_pts.mean():.3f}")
print(f"Away ppg: {df.away_pts.mean():.3f}")
print(f"Gap     : {gap:.3f} ppg")
print(f"t       : {t:.3f}")
print(f"p       : {p:.3e}")

# ---- 2b. Season trend ----
ha = df.groupby("season").apply(lambda g: pd.Series({
    "home_ppg":     g.home_pts.mean(),
    "away_ppg":     g.away_pts.mean(),
    "home_win_pct": (g.FTR=="H").mean(),
    "draw_pct":     (g.FTR=="D").mean(),
    "away_win_pct": (g.FTR=="A").mean(),
}), include_groups=False).reset_index()
ha["gap"] = ha.home_ppg - ha.away_ppg
ha.to_csv("ha_by_season.csv", index=False)
print("\n=== PER-SEASON ===\n", ha.to_string(index=False))

# ---- 2c. COVID comparison ----
covid_season = "2020/21"
normal = ha[ha.season != covid_season]
covid_gap = ha.loc[ha.season==covid_season, "gap"].iloc[0]
print("\n=== COVID ===")
print(f"Normal seasons mean gap: {normal.gap.mean():.3f} (SD {normal.gap.std():.3f})")
print(f"2020/21 gap            : {covid_gap:.3f}")
print(f"Difference             : {covid_gap - normal.gap.mean():.3f} ppg")

# ---- Chart ----
fig, ax = plt.subplots(figsize=(13, 5))
ax.plot(ha.season, ha.home_ppg, marker="o", label="Home ppg")
ax.plot(ha.season, ha.away_ppg, marker="s", label="Away ppg")
covid_idx = ha.index[ha.season==covid_season][0]
ax.axvspan(covid_idx-0.4, covid_idx+0.4, color="red", alpha=0.15, label="2020/21 empty stadiums")
ax.set_ylabel("Points per game")
ax.set_title("Home vs Away PPG by Season (Premier League)")
ax.tick_params(axis="x", rotation=90)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ha_trend.png", dpi=150)
print("\nSaved ha_trend.png")
