import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import numpy as np
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import os
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Live Football Match Predictor", page_icon="⚽", layout="wide")

# --- DEFINITIVE, FOCUSED TEAM LIST & LOCAL ASSET PATHS ---
ALLOWED_TEAMS = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton", "Burnley", "Chelsea", 
    "Crystal Palace", "Everton", "Fulham", "Leeds", "Liverpool", "Man City", 
    "Man United", "Newcastle", "Nottingham", "Sunderland", "Tottenham", 
    "West Ham", "Wolverhampton"
]
# --- DEFINITIVE LOCAL PNG PATHS ---
TEAM_LOGOS = { 
    "Arsenal": "assets/Arsenal.png", "Aston Villa": "assets/Aston_Villa.png", "Bournemouth": "assets/Bournemouth.png", 
    "Brentford": "assets/Brentford.png", "Brighton": "assets/Brighton.png", "Burnley": "assets/Burnley.png",
    "Chelsea": "assets/Chelsea.png", "Crystal Palace": "assets/Crystal_Palace.png", "Everton": "assets/Everton.png", 
    "Fulham": "assets/Fulham.png", "Leeds": "assets/Leeds.png", "Liverpool": "assets/Liverpool.png", 
    "Man City": "assets/Manchester_City.png", "Man United": "assets/Manchester_United.png", "Newcastle": "assets/Newcastle.png", 
    "Nottingham": "assets/Nottingham.png", "Sunderland": "assets/Sunderland.png", "Tottenham": "assets/Tottenham.png", 
    "West Ham": "assets/West_Ham.png", "Wolverhampton": "assets/Wolverhampton.png"
}
logo_aliases = { 
    "Brighton and Hove Albion": "Brighton", "Manchester City": "Man City", "Manchester United": "Man United", 
    "Newcastle United": "Newcastle", "Nottingham Forest": "Nottingham", "Nott'm Forest": "Nottingham", 
    "Tottenham Hotspur": "Tottenham", "West Ham United": "West Ham", "Wolverhampton Wanderers": "Wolverhampton",
    "Leeds United": "Leeds"
}

# --- DEFINITIVE PNG Rendering Engine ---
@st.cache_data
def render_png_as_base64(png_path):
    """Renders a local PNG file as a Base64 encoded URI."""
    full_path = os.path.join(os.path.dirname(__file__), png_path)
    if os.path.exists(full_path):
        with open(full_path, "rb") as f:
            png_bytes = f.read()
            b64 = base64.b64encode(png_bytes).decode("utf-8")
            return f"data:image/png;base64,{b64}"
    return None


# --- ASSET LOADING ---
@st.cache_resource
def load_assets():
    """Load all AI experts and data assets."""
    try:
        script_dir = os.path.dirname(__file__)
        with open(os.path.join(script_dir, 'win_lose_model_historian.pkl'), 'rb') as f: win_lose_historian = pickle.load(f)
        with open(os.path.join(script_dir, 'draw_model_historian.pkl'), 'rb') as f: draw_historian = pickle.load(f)
        with open(os.path.join(script_dir, 'win_lose_model_strategist.pkl'), 'rb') as f: win_lose_strategist = pickle.load(f)
        with open(os.path.join(script_dir, 'draw_model_strategist.pkl'), 'rb') as f: draw_strategist = pickle.load(f)
        with open(os.path.join(script_dir, 'win_loss_encoders.pkl'), 'rb') as f: win_loss_encoders = pickle.load(f)
        with open(os.path.join(script_dir, 'draw_encoders.pkl'), 'rb') as f: draw_encoders = pickle.load(f)
        with open(os.path.join(script_dir, 'final_strength_ratings.pkl'), 'rb') as f: strength_ratings = pickle.load(f)
        df = pd.read_csv(os.path.join(script_dir, 'full_feature_dataset_expanded.csv'))
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values('Date', ascending=False).reset_index(drop=True)
        
        models = {
            "historian": {"win_loss": win_lose_historian, "draw": draw_historian},
            "strategist": {"win_loss": win_lose_strategist, "draw": draw_strategist}
        }
        return models, win_loss_encoders, draw_encoders, df, strength_ratings
    except FileNotFoundError as e:
        st.error(f"Error loading asset file: {e}. Please ensure all four training scripts have been run and the .pkl files are in the repository.")
        return (None,) * 5

# --- LIVE DATA ENGINE ---
@st.cache_data(ttl=3600)
def fetch_live_epl_table():
    try:
        url = "https://www.espn.com/soccer/table/_/league/ENG.1"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers); response.raise_for_status()
        tables = pd.read_html(response.content)
        if len(tables) < 2: return None
        df_table = pd.concat([tables[0], tables[1]])
        df_table = df_table.rename(columns={df_table.columns[0]: 'Team'})
        df_table.dropna(subset=['Team'], inplace=True)
        df_table['Team'] = df_table['Team'].astype(str)
        def clean_espn_team_name(name):
            for i, char in enumerate(name):
                if char.isupper(): return name[i:]
            return name
        df_table['Team'] = df_table['Team'].apply(clean_espn_team_name)
        df_table.reset_index(drop=True, inplace=True)
        rank_map = {row['Team']: idx + 1 for idx, row in df_table.iterrows()}
        name_corrections = { "Manchester United": "Man United", "Manchester City": "Man City", "Tottenham Hotspur": "Tottenham", "Wolverhampton Wanderers": "Wolverhampton", "Nottingham Forest": "Nottingham", "West Ham United": "West Ham", "Newcastle United": "Newcastle", "Brighton & Hove Albion": "Brighton" }
        return {name_corrections.get(team, team): rank for team, rank in rank_map.items()}
    except Exception as e:
        st.warning(f"Could not fetch live league table. Predictions may be less accurate. Error: {e}")
        return None

# --- DYNAMIC FEATURE & PREDICTION LOGIC ---
def get_and_predict(df, models, home_team, away_team, strength_map, mode, live_rank_map=None, hypothetical_strengths=None):
    if mode == "Future":
        st.info("Consulting the 'Strategist' AI expert (Context-Agnostic) for this simulation.")
        draw_model, win_lose_model = models["strategist"]["draw"], models["strategist"]["win_loss"]
        home_strength, away_strength = hypothetical_strengths['home'], hypothetical_strengths['away']
        final_features = {'HomeTeam_Strength': home_strength, 'AwayTeam_Strength': away_strength}
        input_df = pd.DataFrame([final_features])
    else: # Current Season
        draw_model, win_lose_model = models["historian"]["draw"], models["historian"]["win_loss"]
        relevant_matches = df[((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team))]
        if relevant_matches.empty: return None, None, None, True
        odds_features = relevant_matches.head(5)[[c for c in df.columns if 'Avg_Odds' in c]].mean().to_dict()
        h2h_features = relevant_matches.head(5)[[c for c in df.columns if 'H2H' in c]].mean().to_dict()
        form_diff_features = relevant_matches.iloc[0][[c for c in df.columns if 'form' in c and 'diff' in c]].to_dict()
        home_strength, away_strength = strength_map.get(home_team, 1500), strength_map.get(away_team, 1500)
        home_rank, away_rank = (live_rank_map.get(home_team, 10), live_rank_map.get(away_team, 11)) if live_rank_map else (10, 11)
        home_form_features, away_form_features = {}, {}
        home_matches = df[(df['HomeTeam'] == home_team) | (df['AwayTeam'] == away_team)]
        if not home_matches.empty:
            latest = home_matches.iloc[0]
            prefix = 'H_form_' if latest['HomeTeam'] == home_team else 'A_form_'
            for col in [c for c in df.columns if c.startswith(prefix)]: home_form_features['H_form_' + col[len(prefix):]] = latest[col]
        away_matches = df[(df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team)]
        if not away_matches.empty:
            latest = away_matches.iloc[0]
            prefix = 'H_form_' if latest['HomeTeam'] == away_team else 'A_form_'
            for col in [c for c in df.columns if c.startswith(prefix)]: away_form_features['A_form_' + col[len(prefix):]] = latest[col]
        final_features = {**home_form_features, **away_form_features, **form_diff_features, **h2h_features, **odds_features, 'HomeTeam_League_Rank': home_rank, 'AwayTeam_League_Rank': away_rank, 'HomeTeam_Strength': home_strength, 'AwayTeam_Strength': away_strength, 'HomeTeam': home_team, 'AwayTeam': away_team}
        input_df = pd.DataFrame([final_features])
    try:
        input_df_draw, input_df_win_loss = input_df.copy(), input_df.copy()
        if mode == "Current Season":
            input_df_draw['HomeTeam'] = draw_encoders['home_team'].transform(input_df_draw['HomeTeam'])
            input_df_draw['AwayTeam'] = draw_encoders['away_team'].transform(input_df_draw['AwayTeam'])
            input_df_win_loss['HomeTeam'] = win_loss_encoders['home_team'].transform(input_df_win_loss['HomeTeam'])
            input_df_win_loss['AwayTeam'] = win_loss_encoders['away_team'].transform(input_df_win_loss['AwayTeam'])
        draw_model_features = draw_model.get_booster().feature_names
        win_loss_model_features = win_lose_model.get_booster().feature_names
        input_df_draw = input_df_draw[draw_model_features]
        input_df_win_loss = input_df_win_loss[win_loss_model_features]
    except Exception as e:
        st.error(f"Error preparing data for models: {e}"); return None, None, None, False
    draw_proba = draw_model.predict_proba(input_df_draw)[0][1]
    win_loss_probs = win_lose_model.predict_proba(input_df_win_loss)[0]
    away_idx = np.where(win_loss_encoders['y_encoder_wl'].classes_ == 'A')[0][0]
    home_idx = np.where(win_loss_encoders['y_encoder_wl'].classes_ == 'H')[0][0]
    away_cond, home_cond = win_loss_probs[away_idx], win_loss_probs[home_idx]
    away_win, home_win = away_cond * (1 - draw_proba), home_cond * (1 - draw_proba)
    total = home_win + away_win + draw_proba
    if total > 0: home_win, away_win, draw_proba = home_win/total, away_win/total, draw_proba/total
    no_h2h_flag = (mode == "Current Season" and 'relevant_matches' in locals() and relevant_matches.empty)
    return home_win, draw_proba, away_win, no_h2h_flag

# --- UI Functions ---
def display_professional_results(home_team, away_team, home_p, draw_p, away_p):
    """The definitive, polished results display function with local assets."""
    home_logo_path = TEAM_LOGOS.get(home_team, TEAM_LOGOS.get(logo_aliases.get(home_team)))
    away_logo_path = TEAM_LOGOS.get(away_team, TEAM_LOGOS.get(logo_aliases.get(away_team)))
    home_svg = render_png_as_base64(home_logo_path)
    away_svg = render_png_as_base64(away_logo_path)
    
    st.markdown("""<style> .team { font-size: 1.5em; font-weight: bold; } .team-logo { width: 80px; height: auto; } .prob-bar-container { width: 100%; display: flex; height: 40px; border-radius: 10px; overflow: hidden; font-size: 1em; color: white; font-weight: bold; } .prob-bar-segment { display: flex; align-items: center; justify-content: center; } .home-win { background-color: #4CAF50; } .draw { background-color: #FFC107; } .away-win { background-color: #F44336; } </style>""", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        if home_svg: st.markdown(f'<div style="text-align: right;"><img src="{home_svg}" class="team-logo"></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="team" style="text-align: right;">{home_team}</p>', unsafe_allow_html=True)
    with c2: st.markdown('<div style="text-align: center; font-size: 2.5em; font-weight: bold; margin-top: 40px;">VS</div>', unsafe_allow_html=True)
    with c3:
        if away_svg: st.markdown(f'<div style="text-align: left;"><img src="{away_svg}" class="team-logo"></div>', unsafe_allow_html=True)
        st.markdown(f'<p class="team" style="text-align: left;">{away_team}</p>', unsafe_allow_html=True)

    st.subheader("Win Probability", anchor=False)
    st.markdown(f"""<div class="prob-bar-container"> <div class="prob-bar-segment home-win" style="width: {home_p:.2%};">{home_p:.1%}</div> <div class="prob-bar-segment draw" style="width: {draw_p:.2%};">{draw_p:.1%}</div> <div class="prob-bar-segment away-win" style="width: {away_p:.2%};">{away_p:.1%}</div> </div>""", unsafe_allow_html=True)
    outcomes = {'Home Win': home_p, 'Draw': draw_p, 'Away Win': away_p}; final_call = max(outcomes, key=outcomes.get)
    st.divider()
    
    st.subheader('Final Verdict', anchor=False)
    
    winner_team = home_team if final_call == 'Home Win' else away_team if final_call == 'Away Win' else None
    
    if winner_team:
        st.snow()
        winner_logo_path = TEAM_LOGOS.get(winner_team, TEAM_LOGOS.get(logo_aliases.get(winner_team)))
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
    """A robust fallback using Team Strength Rating."""
    st.warning("⚠️ No historical H2H data found. A simplified prediction will be made based on the teams' inherent Strength Rating.")
    home_strength, away_strength = strength_map.get(home_team, 1500), strength_map.get(away_team, 1500)
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
            logo_path = TEAM_LOGOS.get(winner, TEAM_LOGOS.get(logo_aliases.get(winner)))
            winner_svg = render_png_as_base64(logo_path)
            if winner_svg:
                st.markdown(f'<div style="text-align: center;"><img src="{winner_svg}" width=120></div>', unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: green;'>LIKELY WINNER: {winner.upper()}</h2>", unsafe_allow_html=True)
    else:
        _, center_col, _ = st.columns([1, 1, 1])
        with center_col:
            st.markdown("<h1 style='text-align: center; font-size: 80px;'>🤝</h1>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align: center; color: #D39C00;'>DRAW</h2>", unsafe_allow_html=True)

# --- UI & APP LOGIC ---
with st.spinner('Loading all AI experts and data...'):
    assets = load_assets()

st.image("https://images.pexels.com/photos/270085/pexels-photo-270085.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", use_container_width=True)
st.title('AI Football Match Predictor')

if 'view' not in st.session_state: st.session_state.view = 'menu'

if all(a is not None for a in assets):
    models, win_loss_encoders, draw_encoders, df_final, strength_ratings = assets
    live_ranks = fetch_live_epl_table()
    all_teams = ALLOWED_TEAMS

    RATING_MAP = { 1: 1300, 2: 1350, 3: 1400, 4: 1450, 5: 1500, 6: 1550, 7: 1600, 8: 1650, 9: 1700, 10: 1750 }
    REVERSE_RATING_MAP = {v: k for k, v in RATING_MAP.items()}

    if st.session_state.view == 'menu':
        st.subheader("Choose a Prediction Mode")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("### 📊 Current Season Prediction"); st.write("Predict a near-future match using the **'Historian'** AI expert for maximum contextual accuracy.")
                if st.button("Start Current Prediction", use_container_width=True, type="primary"):
                    st.session_state.view = 'current_season'; st.rerun()
        with c2:
            with st.container(border=True):
                st.markdown("### 🔮 Future Scenario Simulator"); st.write("Predict a hypothetical match using the **'Strategist'** AI expert, which ignores team identities and focuses purely on strength.")
                if st.button("Start Future Scenario", use_container_width=True):
                    st.session_state.view = 'future_match'; st.rerun()
        st.divider()
        with st.expander("🔬 What's the difference between the two AI experts?"):
            st.markdown("""
            This application is powered by two distinct AI models, each with a specialized purpose:
            - **The 'Historian' (Current Season):** This AI is like an expert sports historian. It has studied every team's specific rivalries, biases, and historical patterns. It uses this deep, context-rich knowledge, along with live league tables, to make the most accurate predictions for matches happening **now**.
            - **The 'Strategist' (Future Simulator):** This AI is a pure theorist. It was trained without ever knowing team names, so it has no biases. It has learned the fundamental physics of football—how a team with a certain strength rating performs against another. It is used to simulate hypothetical "what-if" scenarios for the **future**, where its judgment is based purely on the ratings you provide.
            """)

    elif st.session_state.view == 'current_season':
        st.subheader("Predict a Current Season Match")
        if st.button("⬅️ Back to Menu"): st.session_state.view = 'menu'; st.rerun()
        with st.container(border=True):
            c1, c2 = st.columns(2)
            home_team = c1.selectbox('Home Team', options=all_teams, key='home_c', index=all_teams.index("Man United") if "Man United" in all_teams else 0)
            away_team = c2.selectbox('Away Team', options=all_teams, key='away_c', index=all_teams.index("Liverpool") if "Liverpool" in all_teams else 1)
        if st.button('🔮 Predict Outcome', use_container_width=True, key='predict_c', type="primary"):
            if home_team == away_team: st.warning("Please select two different teams.")
            else:
                with st.spinner("Consulting the 'Historian' AI expert..."):
                    home_p, draw_p, away_p, no_h2h = get_and_predict(df_final, models, home_team, away_team, strength_ratings, "Current Season", live_rank_map=live_ranks)
                if no_h2h:
                    predict_with_strength_only(strength_ratings, home_team, away_team)
                else: 
                    display_professional_results(home_team, away_team, home_p, draw_p, away_p)

    elif st.session_state.view == 'future_match':
        st.subheader("Simulate a Future / Hypothetical Match")
        if st.button("⬅️ Back to Menu"): st.session_state.view = 'menu'; st.rerun()
        
        # <<< --- NEW USER GUIDE SECTION --- >>>
        with st.expander("💡 How to Use the Strength Simulator", expanded=True):
            st.markdown("""
            This tool lets you ask "what-if" questions based on a team's long-term strength. The **Team Rating (1-10)** is a simplified score derived from a complex **Elo-style rating system**, which analyzes historical performance.
            
            - **10**: A historically dominant, title-winning team (e.g., peak Man City).
            - **5**: A solid mid-table team.
            - **1**: A team struggling against relegation.
            
            Use the table below as a baseline for your simulation. To get a feel for a team's current form, you can also check the [official Premier League table](https://www.premierleague.com/tables).
            """)
            
            # Calculate and display the scaled strength index
            min_rating = min(strength_ratings.values())
            max_rating = max(strength_ratings.values())
            
            strength_data = []
            for team in all_teams:
                rating = strength_ratings.get(team, 1500) # Default to 1500 if team not in ratings
                # Min-Max scaling formula
                scaled_strength = 1 + 9 * ((rating - min_rating) / (max_rating - min_rating))
                strength_data.append({"Team": team, "Calculated Strength (1-10)": f"{scaled_strength:.1f}"})
            
            df_strength = pd.DataFrame(strength_data)
            st.dataframe(df_strength, use_container_width=True, hide_index=True)
        # <<< --- END OF NEW SECTION --- >>>

        with st.container(border=True):
            c1, c2 = st.columns(2)
            home_team_selection = c1.selectbox('Home Team', options=all_teams, key='home_f', index=all_teams.index("Chelsea") if "Chelsea" in all_teams else 0)
            away_team_selection = c2.selectbox('Away Team', options=all_teams, key='away_f', index=all_teams.index("Arsenal") if "Arsenal" in all_teams else 1)
            
            st.markdown("---")
            st.markdown("**Set the Hypothetical Team Rating (1-10) for your scenario:**")
            
            default_home_strength = strength_ratings.get(home_team_selection, 1500)
            default_away_strength = strength_ratings.get(away_team_selection, 1500)
            
            # Find the closest key in our simple RATING_MAP to the team's actual strength
            default_home_rating_key = min(REVERSE_RATING_MAP.keys(), key=lambda k:abs(k-default_home_strength))
            default_away_rating_key = min(REVERSE_RATING_MAP.keys(), key=lambda k:abs(k-default_away_strength))

            c3, c4 = st.columns(2)
            home_rating_input = c3.slider("Home Team Rating", 1, 10, REVERSE_RATING_MAP[default_home_rating_key], 1)
            away_rating_input = c4.slider("Away Team Rating", 1, 10, REVERSE_RATING_MAP[default_away_rating_key], 1)

        if st.button('🔮 Simulate Outcome', use_container_width=True, key='predict_f', type="primary"):
            if home_team_selection == away_team_selection: st.warning("Please select two different teams.")
            else:
                hypothetical_strengths = { 'home': RATING_MAP[home_rating_input], 'away': RATING_MAP[away_rating_input] }
                with st.spinner("Consulting the 'Strategist' AI expert..."):
                    home_p, draw_p, away_p, _ = get_and_predict(df_final, models, home_team_selection, away_team_selection, strength_ratings, "Future", hypothetical_strengths=hypothetical_strengths)
                display_professional_results(home_team_selection, away_team_selection, home_p, draw_p, away_p)
else:
    st.error('Failed to load critical application assets. Please check the logs.')

# --- Footer Credit Section ---
st.divider()
st.markdown("<p style='text-align: center;'>Developed by Arvind K N as a part of the Infosys Internship program.</p>", unsafe_allow_html=True)