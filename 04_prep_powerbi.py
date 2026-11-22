import pandas as pd
import numpy as np

df = pd.read_csv("matches_clean.csv", encoding="latin-1")

# Home perspective
home = df[["season","HomeTeam","FTHG","FTAG","FTR"]].copy()
home.columns = ["season","team","GF","GA","FTR"]
home["pts"] = np.where(home.FTR=="H", 3, np.where(home.FTR=="D", 1, 0))
home["win"] = (home.FTR=="H").astype(int)
home["draw"] = (home.FTR=="D").astype(int)
home["loss"] = (home.FTR=="A").astype(int)

# Away perspective
away = df[["season","AwayTeam","FTAG","FTHG","FTR"]].copy()
away.columns = ["season","team","GF","GA","FTR"]
away["pts"] = np.where(away.FTR=="A", 3, np.where(away.FTR=="D", 1, 0))
away["win"] = (away.FTR=="A").astype(int)
away["draw"] = (away.FTR=="D").astype(int)
away["loss"] = (away.FTR=="H").astype(int)

summary = (pd.concat([home, away])
             .groupby(["season","team"], as_index=False)
             .agg(played=("pts","count"), points=("pts","sum"),
                  GF=("GF","sum"), GA=("GA","sum"),
                  wins=("win","sum"), draws=("draw","sum"), losses=("loss","sum")))
summary["GD"] = summary["GF"] - summary["GA"]

summary.to_csv("team_season_summary.csv", index=False)
print(f"Saved {len(summary)} team-seasons -> team_season_summary.csv")
print(summary.head().to_string(index=False))
