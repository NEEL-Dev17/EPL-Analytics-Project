import os
os.chdir(r"C:\Users\LENOVO\Desktop\EPL_Project")
import pandas as pd
from scipy import stats

df = pd.read_csv("matches_clean.csv", encoding="utf-8", dtype={"season": str})
df['home_pts'] = df['FTR'].map({'H': 3, 'D': 1, 'A': 0})
df['away_pts'] = df['FTR'].map({'A': 3, 'D': 1, 'H': 0})

t_stat, p_value = stats.ttest_ind(df['home_pts'], df['away_pts'], equal_var=False)

print("=" * 60)
print("HOME ADVANTAGE — README NUMBERS")
print("=" * 60)
print(f"Total matches:  {len(df)}")
print(f"Home mean PPG:  {df['home_pts'].mean():.4f}")
print(f"Away mean PPG:  {df['away_pts'].mean():.4f}")
print(f"Gap:            {df['home_pts'].mean() - df['away_pts'].mean():.4f}")
print(f"t-statistic:    {t_stat:.4f}")
print(f"p-value:        {p_value:.10f}")

ha = df.groupby('season').agg(
    home_ppg=('home_pts', 'mean'),
    away_ppg=('away_pts', 'mean')
).reset_index()
ha['gap'] = ha['home_ppg'] - ha['away_ppg']

print("\n" + "=" * 60)
print("COVID COMPARISON")
print("=" * 60)
covid_gap = ha.loc[ha['season'] == '2020/21', 'gap'].values[0]
other_gaps = ha.loc[ha['season'] != '2020/21', 'gap']
print(f"2020/21 gap:            {covid_gap:.4f}")
print(f"Other seasons mean gap: {other_gaps.mean():.4f}")
print(f"Difference:             {covid_gap - other_gaps.mean():.4f}")
