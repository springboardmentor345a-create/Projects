import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os
import base64
import requests
from bs4 import BeautifulSoup
import joblib

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Football Suite", page_icon="⚽", layout="wide")

# --- DEFINITIVE, FOCUSED TEAM LIST & LOCAL ASSET PATHS ---
ALLOWED_TEAMS = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley", "Chelsea", 
    "Crystal Palace", "Everton", "Fulham", "Leeds", "Liverpool", "Man City", 
    "Man United", "Newcastle", "Nottingham", "Sunderland", "Tottenham", 
    "West Ham", "Wolverhampton"
]
PLAYER_POSITIONS = ['Forward', 'Midfielder', 'Attacking Midfielder', 'Winger', 'Defender']

TEAM_LOGOS = { 
    "Arsenal": "assets/Arsenal.png", "Aston Villa": "assets/Aston_Villa.png", "Bournemouth": "assets/Bournemouth.png", 
    "Brentford": "assets/Brentford.png", "Brighton": "assets/Brighton.png", "Burnley": "assets/Burnley.png",
    "Chelsea": "assets/Chelsea.png", "Crystal Palace": "assets/Crystal_Palace.png", "Everton": "assets/Everton.png", 
    "Fulham": "assets/Fulham.png", "Leeds": "assets/Leeds.png", "Liverpool": "assets/Liverpool.png", 
    "Man City": "assets/Manchester_City.png", "Man United": "assets/Manchester_United.png", "Newcastle": "assets/Newcastle.png", 
    "Nottingham": "assets/Nottingham.png", "Sunderland": "assets/Sunderland.png", "Tottenham": "assets/Tottenham.png", 
    "West Ham": "assets/West_Ham.png", "Wolverhampton": "assets/Wolverhampton.png"
}

# --- DEFINITIVE PNG Rendering Engine ---
@st.cache_data
def render_png_as_base64(png_path):
    """Renders a local PNG file as a Base64 encoded URI."""
    try:
        full_path = os.path.join(os.path.dirname(__file__), png_path)
        if os.path.exists(full_path):
            with open(full_path, "rb") as f:
                png_bytes = f.read()
                b64 = base64.b64encode(png_bytes).decode("utf-8")
                return f"data:image/png;base64,{b64}"
    except Exception:
        return None
    return None

# --- ASSET LOADING (DUAL MODEL) ---
@st.cache_resource
def load_assets():
    """Load both AI expert toolkits and all data assets."""
    try:
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir, 'pure_catboost_assets.pkl'), 'rb') as f:
            match_winner_assets = pickle.load(f)
        with open(os.path.join(script_dir, 'final_strength_ratings.pkl'), 'rb') as f:
            strength_ratings = pickle.load(f)
        df = pd.read_csv(os.path.join(script_dir, 'full_feature_dataset_expanded.csv'))
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values('Date', ascending=False).reset_index(drop=True)
        
        models = {
            "match_winner": match_winner_assets
        }
        return models, df, strength_ratings
    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: {e}. Ensure all .pkl and .csv files are in the same directory as app.py.")
        return None, None, None
# --- PREDICTION LOGIC (MODIFIED) ---
def get_and_predict(df, catboost_assets, home_team, away_team, strength_map, home_rank, away_rank):
    relevant_matches = df[((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team))]
    if relevant_matches.empty:
        return None, None, None, True 

    last_5_encounters = relevant_matches.head(5)
    most_recent_encounter = relevant_matches.iloc[0]

    odds_features = last_5_encounters[[c for c in df.columns if 'Avg_Odds' in c]].mean().to_dict()
    h2h_features = last_5_encounters[[c for c in df.columns if 'H2H' in c]].mean().to_dict()
    form_features = most_recent_encounter[[c for c in df.columns if 'form' in c]].to_dict()
    raw_stats_list = ['HTHG', 'HTAG', 'HS', 'AS', 'AST', 'HST', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'HF', 'AF']
    raw_stats_features = most_recent_encounter[raw_stats_list].to_dict()

    home_strength = strength_map.get(home_team, 1500)
    away_strength = strength_map.get(away_team, 1500)
    
    # --- MODIFIED: Simplified the rank logic to use user input directly ---
    st.success(f"Using Ranks: {home_team} (Rank {home_rank} - Live), {away_team} (Rank {away_rank} - Live)")

    features_dict = {
        'HomeTeam': home_team, 'AwayTeam': away_team, 'Season': '2023-2024',
        'HomeTeam_League_Rank': home_rank, 
        'AwayTeam_League_Rank': away_rank,
        'HomeTeam_Strength': home_strength, 'AwayTeam_Strength': away_strength,
        **h2h_features, **odds_features, **form_features, **raw_stats_features
    }
    features_df = pd.DataFrame([features_dict])

    model = catboost_assets['model']
    target_encoder = catboost_assets['target_encoder']
    
    features_df = features_df[model.feature_names_]
    all_probs = model.predict_proba(features_df)[0]
    
    draw_idx = list(target_encoder.classes_).index('D')
    home_idx = list(target_encoder.classes_).index('H')
    away_idx = list(target_encoder.classes_).index('A')
    
    return all_probs[home_idx], all_probs[draw_idx], all_probs[away_idx], False
# --- UI Functions (No Changes Here) ---
def display_professional_results(home_team, away_team, home_p, draw_p, away_p):
    """Renders the detailed prediction results with probabilities."""
    home_logo_path = TEAM_LOGOS.get(home_team)
    away_logo_path = TEAM_LOGOS.get(away_team)
    home_svg = render_png_as_base64(home_logo_path)
    away_svg = render_png_as_base64(away_logo_path)
    
    st.markdown("""
    <style>
        .team { font-size: 1.5em; font-weight: bold; }
        .team-logo { width: 80px; height: auto; }
        .prob-bar-container { width: 100%; display: flex; height: 40px; border-radius: 10px; overflow: hidden; font-size: 1em; color: white; font-weight: bold; }
        .prob-bar-segment { display: flex; align-items: center; justify-content: center; }
        .home-win { background-color: #4CAF50; }
        .draw { background-color: #FFC107; }
        .away-win { background-color: #F44336; }
    </style>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        if home_svg: st.markdown(f'<div style="text-align: right;"><img src="{home_svg}" class="team-logo"></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="team" style="text-align: right;">{home_team}</p>', unsafe_allow_html=True)
    with c2: 
        st.markdown('<div style="text-align: center; font-size: 2.5em; font-weight: bold; margin-top: 40px;">VS</div>', unsafe_allow_html=True)
    with c3:
        if away_svg: st.markdown(f'<div style="text-align: left;"><img src="{away_svg}" class="team-logo"></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="team" style="text-align: left;">{away_team}</p>', unsafe_allow_html=True)
        
    st.subheader("Win Probability", anchor=False)
    st.markdown(f"""
    <div class="prob-bar-container">
        <div class="prob-bar-segment home-win" style="width: {home_p:.2%};">{home_p:.1%}</div>
        <div class="prob-bar-segment draw" style="width: {draw_p:.2%};">{draw_p:.1%}</div>
        <div class="prob-bar-segment away-win" style="width: {away_p:.2%};">{away_p:.1%}</div>
    </div>
    """, unsafe_allow_html=True)
    
    outcomes = {'Home Win': home_p, 'Draw': draw_p, 'Away Win': away_p}
    final_call = max(outcomes, key=outcomes.get)
    st.divider()
    st.subheader('Final Verdict', anchor=False)
    
    winner_team = home_team if final_call == 'Home Win' else away_team if final_call == 'Away Win' else None
    
    if winner_team:
        st.snow()
        winner_logo_path = TEAM_LOGOS.get(winner_team)
        winner_svg = render_png_as_base64(winner_logo_path)
        _, center_col, _ = st.columns([1, 1, 1])
        with center_col:
            if winner_svg:
                st.markdown(f'<div style="text-align: center;"><img src="{winner_svg}" width=150></div>', unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: green;'>WINNER: {winner_team.upper()}</h2>", unsafe_allow_html=True)
    else: # Draw
        _, center_col, _ = st.columns([1, 1, 1])
        with center_col:
            st.markdown("<h1 style='text-align: center; font-size: 80px;'>🤝</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #D39C00;'>DRAW</h2>", unsafe_allow_html=True)

def predict_with_strength_only(strength_map, home_team, away_team):
    """Provides a simplified prediction if no historical H2H data is available."""
    st.warning("⚠️ No historical H2H data found. A simplified prediction will be made based on the teams' inherent Strength Rating.")
    home_strength = strength_map.get(home_team, 1500)
    away_strength = strength_map.get(away_team, 1500)
    strength_difference = abs(home_strength - away_strength)
    DRAW_THRESHOLD = 75 
    
    st.subheader('Final Verdict (Strength-Based)', anchor=False)
    winner = None
    if strength_difference > DRAW_THRESHOLD:
        winner = home_team if home_strength > away_strength else away_team
        
    if winner:
        st.snow()
        _, center_col, _ = st.columns([1, 1, 1])
        with center_col:
            logo_path = TEAM_LOGOS.get(winner)
            winner_svg = render_png_as_base64(logo_path)
            if winner_svg:
                st.markdown(f'<div style="text-align: center;"><img src="{winner_svg}" width=120></div>', unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: green;'>LIKELY WINNER: {winner.upper()}</h2>", unsafe_allow_html=True)
    else:
        _, center_col, _ = st.columns([1, 1, 1])
        with center_col:
            st.markdown("<h1 style='text-align: center; font-size: 80px;'>🤝</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #D39C00;'>DRAW</h2>", unsafe_allow_html=True)

# --- MAIN APP LOGIC ---
st.image("https://images.pexels.com/photos/270085/pexels-photo-270085.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", use_container_width=True)
st.markdown(f"""<style> .main-title{{font-size: 3em; font-weight:bold;text-align: centre;margin-bottom:0rem;}}</style>""", unsafe_allow_html=True)
st.markdown('<h1 class="main-title">EPL Match outcome predictor</h1>', unsafe_allow_html=True)

if 'view' not in st.session_state:
    st.session_state.view = 'menu'

with st.spinner('Loading AI Expert Systems...'):
    models, df_final, strength_ratings = load_assets()

if models:
    # --- MENU VIEW ---
    if st.session_state.view == 'menu':
        st.header("Analysis Tool")
        with st.container(border=True):
            st.markdown("### ⚽ Match Winner Predictor")
            st.write("Predict the outcome (Home Win, Draw, Away Win) of an upcoming match using our champion CatBoost model, powered by deep historical data.")
            if st.button("Launch Predictor", use_container_width=True, type="primary"):
                st.session_state.view = 'match_winner'
                st.rerun()

    # --- MATCH WINNER PREDICTOR VIEW ---
    elif st.session_state.view == 'match_winner':
        st.header("Match Winner Predictor")
        if st.button("⬅️ Back to Menu"):
            st.session_state.view = 'menu'
            st.rerun()
        
        st.info("This tool predicts the outcome of an upcoming match. Please select the teams and enter their current league rank.")
        st.info("To get the live league rank click the link [premier_league_live](https://www.premierleague.com/en/tables)")
        
        with st.container(border=True):
            c1, c2 = st.columns(2)
            home_team = c1.selectbox('Home Team', options=ALLOWED_TEAMS, index=13) 
            away_team = c2.selectbox('Away Team', options=ALLOWED_TEAMS, index=11)

            home_rank = c1.number_input("Enter Home Team's Current Rank", min_value=1, max_value=20, value=10)
            away_rank = c2.number_input("Enter Away Team's Current Rank", min_value=1, max_value=20, value=10)
        
        if st.button('🔮 Predict Match Outcome', use_container_width=True, type="primary"):
            if home_team == away_team:
                st.warning("Please select two different teams.")
            else:
                with st.spinner("Running match simulation..."):
                    home_p, draw_p, away_p, no_h2h = get_and_predict(df_final, models['match_winner'], home_team, away_team, strength_ratings, home_rank, away_rank)
                
                if no_h2h:
                    predict_with_strength_only(strength_ratings, home_team, away_team)
                elif home_p is not None:
                    display_professional_results(home_team, away_team, home_p, draw_p, away_p)
else:
    st.error('Failed to load critical application assets.')

# --- Footer ---
st.divider()
st.markdown("<p style='text-align: center;'>Developed by Arvind K N.</p>", unsafe_allow_html=True)