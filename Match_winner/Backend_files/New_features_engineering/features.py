import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm
import os

print("--- Initiating Unified Data Enrichment Pipeline ---")

try:
    # --- 1. Load Raw Data ---
    print("\n[STEP 1/5] Loading raw merged_dataset.csv...")
    try:
        df = pd.read_csv("merged_dataset.csv", encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv("merged_dataset.csv", encoding='ISO-8859-1')
    
    # --- 2. Initial Cleaning & Time-Series Prep ---
    print("[STEP 2/5] Performing initial cleaning and date sorting...")
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
    df.dropna(subset=['Date', 'HomeTeam', 'AwayTeam', 'FTR'], inplace=True)
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # --- 3. Feature Engineering: Base Features (Odds, Form, H2H) ---
    print("[STEP 3/5] Engineering Base Features (Odds, Form, H2H)...")
    
    # --- Betting Odds ---
    home_odds_cols = [col for col in ['B365H', 'WHH', 'LBH'] if col in df.columns]
    draw_odds_cols = [col for col in ['B365D', 'WHD', 'LBD'] if col in df.columns]
    away_odds_cols = [col for col in ['B365A', 'WHA', 'LBA'] if col in df.columns]
    df['Avg_Odds_H'] = df[home_odds_cols].mean(axis=1)
    df['Avg_Odds_D'] = df[draw_odds_cols].mean(axis=1)
    df['Avg_Odds_A'] = df[away_odds_cols].mean(axis=1)
    # Simple forward-fill for any remaining missing odds
    df[['Avg_Odds_H', 'Avg_Odds_D', 'Avg_Odds_A']] = df[['Avg_Odds_H', 'Avg_Odds_D', 'Avg_Odds_A']].fillna(method='ffill')

    # --- Team Form ---
    stats_cols = ['FTHG', 'FTAG', 'HTHG', 'HTAG' ,'HS', 'AS', 'HF', 'AF', 'HC', 'AC', 'HST', 'AST', 'HY', 'AY', 'HR', 'AR']
    form_feature_names = [f'H_form_{col}' for col in stats_cols] + [f'A_form_{col}' for col in stats_cols]
    
    # This is a more efficient way to calculate rolling averages for form
    for col in stats_cols:
        df[f'H_form_{col}'] = df.groupby('HomeTeam')[col].transform(lambda x: x.shift(1).rolling(5, min_periods=1).mean())
        df[f'A_form_{col}'] = df.groupby('AwayTeam')[col].transform(lambda x: x.shift(1).rolling(5, min_periods=1).mean())
    df.dropna(subset=form_feature_names, inplace=True) # Drop early matches with no form data

    # --- Head-to-Head (H2H) ---
    # This part requires a loop, as it's context-dependent for each match
    h2h_features = []
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Calculating H2H"):
        home_team, away_team, date = row['HomeTeam'], row['AwayTeam'], row['Date']
        h2h_df = df[((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team)) | ((df['HomeTeam'] == away_team) & (df['AwayTeam'] == home_team))]
        past_h2h = h2h_df[h2h_df['Date'] < date]
        if len(past_h2h) == 0:
            h2h_features.append([0, 0, 0])
            continue
        hw = len(past_h2h[(past_h2h['HomeTeam'] == home_team) & (past_h2h['FTR'] == 'H')])
        aw = len(past_h2h[(past_h2h['AwayTeam'] == home_team) & (past_h2h['FTR'] == 'A')])
        home_wins = hw + aw
        draws = len(past_h2h[past_h2h['FTR'] == 'D'])
        total_games = len(past_h2h)
        h2h_features.append([(home_wins / total_games), ((total_games - home_wins - draws) / total_games), (draws / total_games)])
    
    h2h_df = pd.DataFrame(h2h_features, columns=['H_H2H_win_pct', 'A_H2H_win_pct', 'H2H_draw_pct'], index=df.index)
    df = pd.concat([df, h2h_df], axis=1)

    # --- 4. Feature Engineering: Advanced Temporal Features ---
    print("[STEP 4/5] Engineering Advanced Temporal Features (Rank & Strength)...")
    
    # --- Temporal League Rank ---
    def get_season(date):
        return f"{date.year}-{date.year + 1}" if date.month >= 8 else f"{date.year - 1}-{date.year}"
    df['Season'] = df['Date'].apply(get_season)
    ranks_home, ranks_away = [], []
    points_cache = defaultdict(lambda: defaultdict(int))
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Calculating Ranks"):
        season, home, away = row['Season'], row['HomeTeam'], row['AwayTeam']
        season_points = points_cache[season]
        standings = sorted(season_points.items(), key=lambda item: item[1], reverse=True)
        rank_map = {team: r + 1 for r, (team, p) in enumerate(standings)}
        ranks_home.append(rank_map.get(home, 15))
        ranks_away.append(rank_map.get(away, 15))
        if row['FTR'] == 'H': points_cache[season][home] += 3
        elif row['FTR'] == 'A': points_cache[season][away] += 3
        else: points_cache[season][home] += 1; points_cache[season][away] += 1
    df['HomeTeam_League_Rank'] = ranks_home
    df['AwayTeam_League_Rank'] = ranks_away

    # --- Temporal Team Strength (Elo) ---
    strength_home, strength_away = [], []
    strength_cache = defaultdict(lambda: 1500)
    K = 30
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Calculating Strengths"):
        home, away = row['HomeTeam'], row['AwayTeam']
        r_h, r_a = strength_cache[home], strength_cache[away]
        strength_home.append(r_h); strength_away.append(r_a)
        e_h = 1 / (1 + 10**((r_a - r_h) / 400))
        e_a = 1 - e_h
        if row['FTR'] == 'H': s_h, s_a = 1, 0
        elif row['FTR'] == 'A': s_h, s_a = 0, 1
        else: s_h, s_a = 0.5, 0.5
        n_r_h = r_h + K * (s_h - e_h)
        n_r_a = r_a + K * (s_a - e_a)
        strength_cache[home], strength_cache[away] = n_r_h, n_r_a
    df['HomeTeam_Strength'] = strength_home
    df['AwayTeam_Strength'] = strength_away

    # --- 5. Final Save ---
    print("[STEP 5/5] Saving final enriched dataset...")
    output_path = "full_feature_dataset_expanded.csv"
    df.to_csv(output_path, index=False)
    
    print(f"\n--- Pipeline Complete ---")
    print(f"Final dataset shape: {df.shape}")
    print(f"Fully enriched dataset saved to '{output_path}'")

except Exception as e:
    print(f"An error occurred: {e}")
