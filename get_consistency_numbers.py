import os
os.chdir(r"C:\Users\LENOVO\Desktop\EPL_Project")
import pandas as pd

tc = pd.read_csv("team_consistency.csv")

print("=" * 60)
print("MOST CONSISTENT (lowest SD)")
print("=" * 60)
print(tc.sort_values('std_pts').head(5)[['team', 'avg_pts', 'std_pts', 'seasons']].to_string(index=False))

print("\n" + "=" * 60)
print("MOST VOLATILE (highest SD)")
print("=" * 60)
print(tc.sort_values('std_pts', ascending=False).head(5)[['team', 'avg_pts', 'std_pts', 'seasons']].to_string(index=False))
