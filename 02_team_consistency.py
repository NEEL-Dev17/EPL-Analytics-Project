import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("matches_clean.csv", encoding="latin-1")

# ---- Build team-season points (union of home + away) ----
home = df[["season","HomeTeam","FTR"]].rename(columns={"HomeTeam":"team"})
home["pts"] = np.where(home.FTR=="H", 3, np.where(home.FTR=="D", 1, 0))

away = df[["season","AwayTeam","FTR"]].rename(columns={"AwayTeam":"team"})
away["pts"] = np.where(away.FTR=="A", 3, np.where(away.FTR=="D", 1, 0))

tsp = (pd.concat([home[["season","team","pts"]], away[["season","team","pts"]]])
         .groupby(["season","team"], as_index=False)["pts"].sum()
         .rename(columns={"pts":"season_points"}))
tsp.to_csv("team_season_points.csv", index=False)

# ---- Team stats across seasons ----
stats_df = (tsp.groupby("team")["season_points"]
              .agg(avg_pts="mean", std_pts="std", seasons="count")
              .reset_index()
              .query("seasons >= 5")
              .sort_values("std_pts"))
stats_df.to_csv("team_consistency.csv", index=False)

print("=== Most consistent (lowest SD, min 5 seasons) ===")
print(stats_df.head(10).to_string(index=False))
print("\n=== Most volatile (highest SD) ===")
print(stats_df.tail(10).to_string(index=False))

# ---- Scatter plot ----
fig, ax = plt.subplots(figsize=(10, 7))
ax.scatter(stats_df.avg_pts, stats_df.std_pts, alpha=0.7)
for _, r in stats_df.iterrows():
    ax.annotate(r.team, (r.avg_pts, r.std_pts), fontsize=8, alpha=0.85)
ax.set_xlabel("Average points per season")
ax.set_ylabel("Std dev of points across seasons")
ax.set_title("Team Consistency (min 5 seasons)")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("team_consistency_scatter.png", dpi=150)
print("\nSaved team_consistency_scatter.png")
