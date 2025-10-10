import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os
import base64
import time
from pathlib import Path

st.set_page_config(
    page_title="AI Football Suite",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'match_winner_result' not in st.session_state:
    st.session_state['match_winner_result'] = None

def inject_custom_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    .stApp {
        background: linear-gradient(135deg,#0f0c29 0%,#302b63 50%,#24243e 100%);
        font-family:'Inter',sans-serif;
    }
    #MainMenu, footer, header {visibility:hidden;}
                
    .header-container { display: flex; align-items: center; justify-content: center; gap: 1.5rem; margin-bottom: 1rem; }
                
    .football-icon { font-size: 4.5rem; animation: spin 4s linear infinite; }
                
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                
    h1{ background:linear-gradient(120deg,#667eea 0%,#764ba2 100%); -webkit-background-clip:text;-webkit-text-fill-color:transparent; text-align:center; font-size:4rem!important; font-weight:900; margin-bottom:0; letter-spacing: -1px; }
    h2{ color:#ffffff !important; text-align:center; font-weight:700; font-size: 2.5rem; margin-bottom:2rem; }
    .info-box{ background:rgba(102,126,234,0.2); border-left:5px solid #667eea; padding:1.25rem; border-radius:8px; margin:1.5rem 0; color:#ffffff !important; font-size: 1.1rem; font-weight: 600; }
    .stSelectbox label, .stNumberInput label { color: #ffffff !important; font-weight: 600 !important; font-size: 1.05rem !important; }
    .stSelectbox > div > div, .stNumberInput > div > div > input { background: rgba(255,255,255,0.08) !important; color: #ffffff !important; border: 2px solid rgba(255,255,255,0.2) !important; border-radius: 12px !important; transition: all 0.3s ease; }
    .stSelectbox > div > div:hover, .stNumberInput > div > div > input:hover { border-color: rgba(102,126,234,0.6) !important; }
    .prediction-card{ background:rgba(255,255,255,0.06); border:2px solid rgba(255,255,255,0.15); border-radius:25px; padding:3rem 2.5rem; width: 100%; max-width:480px; backdrop-filter:blur(15px); transition:all .5s; cursor:pointer; text-align: center; margin: 0 auto 1.5rem; }
    .prediction-card:hover{ transform:translateY(-15px) scale(1.02); box-shadow:0 25px 50px rgba(102,126,234,.5); background:rgba(255,255,255,.12); border-color: rgba(102,126,234,0.5); }
    .card-icon { font-size: 4rem; margin-bottom: 1.5rem; }
    .card-title { color: #ffffff; font-size: 1.75rem; font-weight: 700; margin-bottom: 0.75rem; }
    .card-description { color: rgba(255,255,255,0.75); font-size: 1.05rem; margin-bottom: 0; line-height: 1.5; }
    .stButton>button{ background:linear-gradient(135deg,#667eea 0%,#764ba2 100%); color:#fff; border:none; border-radius:35px; padding:1rem 2.5rem; font-weight:700; font-size: 1.1rem; box-shadow:0 8px 25px rgba(102,126,234,.4); transition: all 0.4s; }
    .stButton>button:hover{ transform:translateY(-5px) scale(1.05); box-shadow:0 15px 40px rgba(102,126,234,.6); }
    .prob-bar-container { width: 100%; display: flex; height: 40px; border-radius: 10px; overflow: hidden; font-size: 1em; color: white; font-weight: bold; margin-top: 1rem; border: 1px solid rgba(255,255,255,0.2); }
    .prob-bar-segment { display: flex; align-items: center; justify-content: center; }
    .home-win { background-color: #4CAF50; } .draw { background-color: #FFC107; } .away-win { background-color: #F44336; }
    .team-logo { width: 60px; height: auto; }
    .verdict-badge { display: inline-block; padding: 1rem 2.5rem; border-radius: 30px; font-weight: 700; font-size: 1.25rem; }
    .football-transition { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 12, 41, 0.95); z-index: 9999; display: flex; align-items: center; justify-content: center; }
    .football-flying { font-size: 6rem; animation: flyAcross 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards; }
    @keyframes flyAcross { 0% { transform: translateX(-150vw); } 50% { transform: translateX(0) rotate(720deg); } 100% { transform: translateX(150vw); } }
    </style>""", unsafe_allow_html=True)

inject_custom_css()

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

@st.cache_data
def render_png_as_base64(png_path):
    try:
        full_path = Path(__file__).parent / png_path
        if full_path.exists():
            with open(full_path, "rb") as f:
                return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    except Exception:
        return None
    return None

@st.cache_resource
def load_assets():
    try:
        script_dir = Path(__file__).parent
        with open(script_dir / 'pure_catboost_assets.pkl', 'rb') as f:
            match_winner_assets = pickle.load(f)
        with open(script_dir / 'final_strength_ratings.pkl', 'rb') as f:
            strength_ratings = pickle.load(f)
        df = pd.read_csv(script_dir / 'full_feature_dataset_expanded.csv')
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        return {"match_winner": match_winner_assets}, df.sort_values('Date', ascending=False), strength_ratings
    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: A required file was not found. Please check your asset files. Details: {e}")
        return None, None, None

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

# ------------------------------------------------------
# UI COMPONENTS & TRANSITIONS
# ------------------------------------------------------
def predict_based_on_rank(home_rank, away_rank):
    """Generates a simple probability prediction based only on league rank."""
    rank_diff = abs(home_rank - away_rank)
    DRAW_PROB = 0.25
    win_loss_pool = 1.0 - DRAW_PROB
    
    # Higher-ranked team gets a larger share of the win/loss pool, scaled by rank difference
    better_team_share = 0.5 + (rank_diff / 19) * 0.4
    worse_team_share = 1.0 - better_team_share
    
    better_team_prob = better_team_share * win_loss_pool
    worse_team_prob = worse_team_share * win_loss_pool
    
    if home_rank < away_rank: # Home team is better ranked
        return better_team_prob, DRAW_PROB, worse_team_prob
    else: # Away team is better ranked
        return worse_team_prob, DRAW_PROB, better_team_prob

def show_football_transition():
    placeholder = st.empty()
    placeholder.markdown("<div class='football-transition'><div class='football-flying'>⚽</div></div>", unsafe_allow_html=True)
    time.sleep(1.0)
    placeholder.empty()

def inputs_block_match_winner():
    st.markdown('<div class="info-box">Select the home team, away team, and their current league ranks to predict the match outcome.</div>', unsafe_allow_html=True)
    st.markdown(
    '<div class="info-box">To get the live league rank, click the following link: <a href="https://www.premierleague.com/en/tables/" target="_blank">EPL Live Table</a></div>',unsafe_allow_html=True)
    with st.container():
        c1, c2 = st.columns(2)
        home_team = c1.selectbox('Home Team', options=ALLOWED_TEAMS, index=13) 
        away_team = c2.selectbox('Away Team', options=ALLOWED_TEAMS, index=11)
        home_rank = c1.number_input("Home Team's Current Rank", 1, 20, 10)
        away_rank = c2.number_input("Away Team's Current Rank", 1, 20, 10)
    return {'home_team': home_team, 'away_team': away_team, 'home_rank': home_rank, 'away_rank': away_rank}

def display_results(result):
    home_team, away_team = result['inp']['home_team'], result['inp']['away_team']
    home_p, draw_p, away_p = result['probs']
    
    winner_logo_html = ""
    winner_name = result.get('winner_name')
    if winner_name:
        winner_logo_b64 = render_png_as_base64(TEAM_LOGOS.get(winner_name))
        if winner_logo_b64:
             winner_logo_html = f'<img src="{winner_logo_b64}" style="width: 80px; height: auto; margin-bottom: 1rem;">'
    else:
        winner_logo_html = '<div style="font-size: 5rem; margin-bottom: 1rem;">🤝</div>'

    st.markdown(f"""
    <div class='prediction-card' style='max-width:800px;'>
        <div style='display: flex; justify-content: space-around; align-items: center; margin-bottom: 1.5rem;'>
            <div style='text-align:center;'>
                <img src="{render_png_as_base64(TEAM_LOGOS.get(home_team))}" class="team-logo">
                <h3 style='color:white;'>{home_team}</h3>
            </div>
            <h2 style='color:white; font-size: 2.5rem;'>VS</h2>
            <div style='text-align:center;'>
                <img src="{render_png_as_base64(TEAM_LOGOS.get(away_team))}" class="team-logo">
                <h3 style='color:white;'>{away_team}</h3>
            </div>
        </div>
        <h4 style='color:white; text-align:center;'>Win Probability</h4>
        <div class="prob-bar-container">
            <div class="prob-bar-segment home-win" style="width: {home_p:.2%};">{home_p:.1%}</div>
            <div class="prob-bar-segment draw" style="width: {draw_p:.2%};">{draw_p:.1%}</div>
            <div class="prob-bar-segment away-win" style="width: {away_p:.2%};">{away_p:.1%}</div>
        </div>
        <div style="text-align:center; margin-top: 2rem;">
            {winner_logo_html}
            <div class='verdict-badge' style='background:{result['bg_color']};color:{result['color']};border:2px solid {result['color']};'>
                {result['verdict']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


models, df_final, strength_ratings = load_assets()

st.markdown("<div class='header-container'><div class='football-icon'>⚽</div><h1 style='background: none; -webkit-text-fill-color: white; color: white;'>EPL Match Outcome Predictor</h1></div>", unsafe_allow_html=True)

if st.session_state['page'] == 'home':
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class='prediction-card'>
            <div class='card-icon'>🎯</div>
            <div class='card-title'>Match Winner Prediction</div>
            <div class='card-description'>Predict the outcome (Win, Draw, Loss) of an upcoming EPL match using our CatBoost model.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Predictor", use_container_width=True):
            show_football_transition()
            st.session_state['page'] = 'match_winner_input'
            st.rerun()

elif st.session_state['page'] == 'match_winner_input':
    st.markdown("<h2>⚽ Match Winner Predictor</h2>", unsafe_allow_html=True)
    if models:
        inp = inputs_block_match_winner()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔮 Predict Match Outcome", use_container_width=True):
                if inp['home_team'] == inp['away_team']:
                    st.warning("Please select two different teams.")
                elif inp['home_rank'] == inp['away_rank']:
                    st.warning("Teams cannot have the same rank. Please check the live league table.")
                else:
                    with st.spinner("Running match simulation..."):
                        h_p, d_p, a_p, no_h2h = get_and_predict(df_final, models['match_winner'], **inp, strength_map=strength_ratings)
                        
                        if no_h2h:
                            st.warning("No H2H data found. Using rank-based fallback prediction.")
                            home_p, draw_p, away_p = predict_based_on_rank(inp['home_rank'], inp['away_rank'])
                        else:
                            home_p, draw_p, away_p = h_p, d_p, a_p
                    
                    probs = {'Home Win': home_p, 'Draw': draw_p, 'Away Win': away_p}
                    verdict_key = max(probs, key=probs.get)
                    winner_name = None

                    if verdict_key == 'Home Win':
                        winner_name, verdict_text = inp['home_team'], f"🏆 Likely Winner: {inp['home_team']}"
                        color, bg = "#4CAF50", "rgba(76,175,80,0.2)"
                    elif verdict_key == 'Away Win':
                        winner_name, verdict_text = inp['away_team'], f"🏆 Likely Winner: {inp['away_team']}"
                        color, bg = "#4CAF50", "rgba(76,175,80,0.2)"
                    else:
                        verdict_text = "🤝 Likely Outcome: Draw"
                        color, bg = "#FFC107", "rgba(255,193,7,0.2)"

                    st.session_state['match_winner_result'] = {
                        'inp': inp, 'probs': (home_p, draw_p, away_p), 'verdict': verdict_text,
                        'winner_name': winner_name, 'color': color, 'bg_color': bg
                    }
                    show_football_transition()
                    st.session_state['page'] = 'match_winner_result'
                    st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state['page'] = 'home'
                st.rerun()
    else:
        st.error("Model assets could not be loaded. The application cannot proceed.")

elif st.session_state['page'] == 'match_winner_result':
    result = st.session_state.get('match_winner_result')
    if result:
        st.markdown("<h2>✨ Prediction Result</h2>", unsafe_allow_html=True)
        display_results(result)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Run Another Prediction", use_container_width=True):
                st.session_state['page'] = 'match_winner_input'
                st.rerun()
        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state['page'] = 'home'
                st.rerun()
    else:
        st.warning("No result to display. Please run a prediction first.")
        if st.button("🏠 Back to Home"):
            st.session_state['page'] = 'home'
            st.rerun()

st.markdown("<hr style='border:none; height:1px; background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent); margin:3rem 0;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.7);'>Developed by Arvind K N.</p>", unsafe_allow_html=True)