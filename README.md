# EPL Performance Intelligence — Premier League Analytics & Business Intelligence

An end-to-end analytics project analyzing **23 seasons of English Premier League data (2000/01–2024/25)** to answer three business questions using Python, statistics, and an interactive Power BI dashboard.

## Project Background
This project analyzes **8,710 Premier League matches** to answer three questions relevant to club performance and recruitment:
1. **Home Advantage:** Is the home-field effect statistically significant, and how did the COVID-19 empty-stadium season (2020/21) affect it?
2. **Team Consistency:** Which clubs show the most stable vs. most volatile season-to-season performance?
3. **Player Efficiency:** Who are the most efficient attacking players per position (goals + assists per 90 minutes) in the 2023/24 season?

## Data Sources
- **Kaggle — Combined EPL Match Dataset:** 9,380 match-level rows × 22 columns (results, goals, shots, cards, corners).
- **Kaggle — EPL Player Stats 2023/24:** Player-level minutes, goals, assists, and positions.

## Tools Used
- **Python 3.11** (Pandas, SciPy, Matplotlib): Data cleaning, statistical testing, and visualization.
- **Power BI:** Interactive 3-page dashboard.
- **Excel / CSV:** Data exploration and validation.
- **Git/GitHub:** Version control and project delivery.

## Key Findings

### 1. Home Advantage is Real — But Disappeared in COVID Season
Across 8,710 matches:
- **Home mean points per game:** 1.621
- **Away mean points per game:** 1.135
- **Gap:** +0.486
- **t-statistic (Welch's):** 24.70
- **p-value:** < 0.001

**Conclusion:** Home advantage is statistically significant. Home teams earn roughly 0.49 more points per game than away teams. 
**COVID Anomaly:** In the 2020/21 empty-stadium season, the home–away gap collapsed to **-0.071**, compared to a **+0.511** average across all other seasons. This strongly suggests that home advantage is driven substantially by crowd support.

### 2. Team Consistency (Teams with 5+ seasons)
**Most Consistent (Lowest SD):**
- **Crystal Palace:** 45.3 Avg Pts | 2.71 SD (12 seasons)
- **Hull:** 34.2 Avg Pts | 2.59 SD (5 seasons)
- **Wigan:** 41.4 Avg Pts | 5.07 SD (8 seasons)

**Most Volatile (Highest SD):**
- **Man City:** 72.3 Avg Pts | 19.47 SD (22 seasons)
- **Leicester:** 48.0 Avg Pts | 16.60 SD (12 seasons)
- **Leeds:** 51.5 Avg Pts | 15.24 SD (6 seasons)

**Insight:** Consistency isn't always a virtue — Hull and Wigan were consistently poor. Crystal Palace is the most interesting case: a stable mid-table club earning ~45 points every season for over a decade.

### 3. Player Efficiency — Top Attackers per Position (2023/24)
Filtered to players with 900+ minutes. Metric: `(Goals + Assists) / (Minutes / 90)`.

**Forwards (Top 3):**
1. **Cole Palmer** (Chelsea) — 1.139 G+A/90
2. **Michael Olise** (Crystal Palace) — 1.129 G+A/90
3. **Erling Haaland** (Man City) — 1.129 G+A/90

**Midfielders (Top 3):**
1. **Kevin De Bruyne** (Man City) — 1.032 G+A/90
2. **Leon Bailey** (Aston Villa) — 0.827 G+A/90
3. **Kai Havertz** (Arsenal) — 0.683 G+A/90

**Defenders (Top 3):**
1. **Kieran Trippier** (Newcastle) — 0.443 G+A/90
2. **Jakub Kiwior** (Arsenal) — 0.381 G+A/90
3. **Pervis Estupiñán** (Brighton) — 0.362 G+A/90

**Insight:** Cole Palmer, Michael Olise, and Erling Haaland posted nearly identical efficiency (1.13–1.14 G+A/90). However, per-90 metrics must be paired with minutes played for recruitment decisions (e.g., Olise only played 1,275 minutes due to injury).

## Limitations
- **2003/04 and 2004/05 excluded** — Kaggle source has corrupted season boundaries.
- **2024/25 is partial** (350 matches) — kept in data but excluded from trend visualizations.
- **No expected goals (xG) data** — finishing efficiency vs. chance quality cannot be separated.
- **Player data covers only 2023/24.**
- **Per-90 metrics overstate part-time players.**
- **Standard deviation understates "yo-yo" clubs** that are promoted/relegated.

## Dashboard
The Power BI report (`dashboard.pbix`) contains three pages:
1. **League Overview:** KPI cards, goals per season, and the Home vs. Away PPG line chart highlighting the COVID anomaly.
2. **Team Comparison:** Interactive team slicer, season-by-season table, trend line, and Avg/SD cards.
3. **Player Scatter:** Minutes played vs. G+A/90, colored by position, with an annotation highlighting elite players.

## How to Run
1. Install Python dependencies: `pip install pandas scipy matplotlib sqlalchemy`
2. Run the scripts in order:
   - `data_cleaning.py`
   - `01_home_advantage.py`
   - `02_team_consistency.py`
   - `03_player_efficiency.py`
3. Open `dashboard.pbix` in Power BI Desktop to view the interactive dashboard.