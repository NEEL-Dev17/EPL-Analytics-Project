import pandas as pd

df = pd.read_csv("matches_clean.csv", encoding="utf-8")

# 1. Strip whitespace and force to string
df["season"] = df["season"].astype(str).str.strip()

# 2. Diagnose what's actually in the column
print("Unique season values:")
print(sorted(df["season"].unique()))
print(f"\nCount: {df['season'].nunique()} unique seasons")

# 3. Normalize to consistent YYYY/YY format
def normalize(s):
    s = s.strip()
    # Handle "2020-21" → "2020/21"
    s = s.replace("-", "/")
    # Handle "2021" (single year) → "2020/21" if it's meant as a season-end year
    # (only apply if you actually see single-year values)
    if "/" not in s and len(s) == 4:
        y = int(s)
        s = f"{y-1}/{str(y)[-2:]}"
    return s

df["season"] = df["season"].apply(normalize)

# 4. Verify
print("\nAfter normalization:")
print(sorted(df["season"].unique()))

# 5. Save with UTF-8 and no index
df.to_csv("matches_clean.csv", index=False, encoding="utf-8")

print(f"\nSaved. {len(df)} rows, {df['season'].nunique()} seasons.")
