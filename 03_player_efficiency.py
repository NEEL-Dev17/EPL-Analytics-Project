import pandas as pd

df = pd.read_csv("player_stats_raw.csv", encoding="utf-8")
df.columns = [c.strip() for c in df.columns]

def find_col(df, candidates):
    for cand in candidates:
        for col in df.columns:
            if col.lower() == cand.lower(): return col
    for cand in candidates:
        for col in df.columns:
            if cand.lower() in col.lower(): return col
    return None

mapping = {
    "Player": find_col(df, ["Player", "Name"]),
    "Pos":    find_col(df, ["Pos", "Position"]),
    "Squad":  find_col(df, ["Squad", "Team", "Club"]),
    "Min":    find_col(df, ["Min", "Minutes"]),
    "Gls":    find_col(df, ["Gls", "Goals"]),
    "Ast":    find_col(df, ["Ast", "Assists"]),
}

df = df[[mapping["Player"], mapping["Pos"], mapping["Squad"],
         mapping["Min"], mapping["Gls"], mapping["Ast"]]].copy()
df.columns = ["Player", "Pos", "Squad", "Min", "Gls", "Ast"]

for c in ["Min", "Gls", "Ast"]:
    df[c] = (df[c].astype(str).str.replace(",", "", regex=False)
                   .replace({"nan": None, "": None}))
    df[c] = pd.to_numeric(df[c], errors="coerce")

df = df.dropna(subset=["Min", "Gls", "Ast"])
df["Pos"] = df["Pos"].astype(str).str.split(",").str[0].str.strip()
df = df[df.Min >= 900].copy()
df["G+A_per90"] = (df.Gls + df.Ast) / (df.Min / 90)
df["rank_in_pos"] = df.groupby("Pos")["G+A_per90"].rank(ascending=False, method="min")

# Exclude goalkeepers from main ranking
df_out = df[df["Pos"] != "GK"].copy()

for pos in sorted(df_out.Pos.unique()):
    top = df_out[df_out.Pos == pos].nsmallest(5, "rank_in_pos")[
        ["Player", "Squad", "Min", "Gls", "Ast", "G+A_per90"]
    ]
    print(f"\n=== {pos} ===")
    print(top.to_string(index=False))

df_out.to_csv("player_clean.csv", index=False)
print(f"\nSaved {len(df_out)} outfield players with 900+ minutes -> player_clean.csv")
