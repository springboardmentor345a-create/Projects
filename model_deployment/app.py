import streamlit as st
import pandas as pd
import numpy as np
import pickle
import joblib
import time
from pathlib import Path

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="EPL Prediction Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------
# CSS & Styling (you can reuse from your existing code)
# ------------------------------------------------------
st.markdown("""
<style>
/* put your custom CSS here (backgrounds, fonts, etc) */
body {
    background: #f0f2f6;
}
h1, h2 {
    color: #333 !important;
}
/* etc… */
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# Load Models & Preprocessors
# ------------------------------------------------------
@st.cache_resource
def load_models():
    models_dir = Path("models")
    # League / Season-level models
    winner_model = None
    points_model = None
    scaler = None
    # Match-level model
    match_model = None

    # Try loading league winner, points, scaler
    if models_dir.exists():
        wpath = models_dir / "League_winner_model.pkl"
        ppath = models_dir / "Points_model.pkl"
        spath = models_dir / "scaler.pkl"
        if wpath.exists():
            with open(wpath, "rb") as f:
                winner_model = pickle.load(f)
        if ppath.exists():
            with open(ppath, "rb") as f:
                points_model = pickle.load(f)
        if spath.exists():
            with open(spath, "rb") as f:
                scaler = pickle.load(f)

        # Try match winner model (joblib or pickle)
        mpath = models_dir / "match_winner_model.pkl"
        if mpath.exists():
            try:
                match_model = joblib.load(mpath)
            except Exception:
                with open(mpath, "rb") as f:
                    match_model = pickle.load(f)

    return winner_model, points_model, scaler, match_model

winner_model, points_model, scaler, match_model = load_models()

# ------------------------------------------------------
# Constants & Mappings
# ------------------------------------------------------
EPL_TEAMS = [
    'Arsenal','Aston Villa','Bournemouth','Brentford','Brighton',
    'Chelsea','Crystal Palace','Everton','Fulham','Leicester City',
    'Liverpool','Manchester City','Manchester United','Newcastle United',
    'Nottingham Forest','Southampton','Tottenham Hotspur','West Ham United',
    'Wolverhampton Wanderers','Leeds United'
]

# For match-level: mapping from team name to numeric encoding (if needed)
team_to_id = {team: idx for idx, team in enumerate(EPL_TEAMS)}
id_to_team = {idx: team for team, idx in team_to_id.items()}

half_time_result_map = {"Draw": 0, "Home Win": 1, "Away Win": 2}

# ------------------------------------------------------
# Helper Functions
# ------------------------------------------------------
def prep_league_features(inp: dict):
    """
    Prepare features for the league winner / points model
    inp must contain keys: team, played, wins, draws, losses
    """
    df = pd.DataFrame([{
        'team': inp['team'],
        'played': inp['played'],
        'wins': inp['wins'],
        'draws': inp['draws'],
        'losses': inp['losses'],
        'points': inp['wins'] * 3 + inp['draws'],
        'win_rate': inp['wins'] / max(1, inp['played']),
        'draw_rate': inp['draws'] / max(1, inp['played']),
        'loss_rate': inp['losses'] / max(1, inp['played']),
        'team_encoded': team_to_id.get(inp['team'], 0)
    }])
    X = df[['played','wins','draws','losses','points','win_rate','draw_rate','loss_rate','team_encoded']]
    if scaler is not None:
        try:
            X = scaler.transform(X)
        except Exception:
            pass
    return X

def match_input_df(inputs: dict):
    """
    Prepare a DataFrame for match prediction model from user inputs dict.
    The dict should include all features your model expects, e.g.:
    HomeTeam, AwayTeam, HalfTimeHomeGoals, HalfTimeAwayGoals, HalfTimeResult,
    HomeShots, AwayShots, HomeShotsOnTarget, AwayShotsOnTarget, HomeCorners, AwayCorners,
    HomeFouls, AwayFouls, HomeRedCards, AwayRedCards, HomeYellowCards, AwayYellowCards
    """
    df = pd.DataFrame([inputs])
    # If your match_model expects features in a specific order, enforce it:
    if hasattr(match_model, "feature_names_in_"):
        df = df[match_model.feature_names_in_]
    return df

def animate_number(target, placeholder, fmt="{:.1f}", duration=1.0):
    steps = 30
    for i in range(steps + 1):
        val = target * (i / steps)
        with placeholder.container():
            st.markdown(f"<div style='font-size:3rem; font-weight:900;'>{fmt.format(val)}</div>", unsafe_allow_html=True)
        time.sleep(duration / steps)

# ------------------------------------------------------
# Main UI / Navigation
# ------------------------------------------------------
st.title("⚽ EPL Prediction Hub")

st.sidebar.title("Navigate")
page = st.sidebar.radio("Choose a prediction type:",
                        ["League Winner & Points", "Match Winner Prediction"])

if page == "League Winner & Points":
    st.header("📊 League / Season Prediction")
    st.markdown("Predict the probability a team will win the league, and estimate total season points.")

    # Input block
    col1, col2 = st.columns(2)
    with col1:
        team = st.selectbox("Team", EPL_TEAMS)
        played = st.number_input("Matches Played", min_value=1, max_value=38, value=10)
        wins = st.number_input("Wins", min_value=0, max_value=38, value=5)
        draws = st.number_input("Draws", min_value=0, max_value=38, value=2)
    # Losses auto-calculated
    losses = played - (wins + draws)
    if wins + draws > played:
        st.error("Wins + Draws exceed total matches played!")
        losses = 0
    else:
        st.write(f"Losses (auto): {losses}")

    if st.button("🔮 Predict League Outcomes"):
        X = prep_league_features({
            'team': team,
            'played': played,
            'wins': wins,
            'draws': draws,
            'losses': losses
        })

        # 1. Predict league win prob
        win_prob = None
        if winner_model is not None:
            try:
                win_prob = float(winner_model.predict_proba(X)[0][1]) * 100
            except Exception as e:
                st.warning(f"Could not compute win probability: {e}")

        # If no model or error, fallback heuristic
        if win_prob is None:
            win_prob = (wins / max(1, played)) * 50 + 5

        # 2. Predict total points
        pts = None
        if points_model is not None:
            try:
                pts = float(points_model.predict(X)[0])
            except Exception as e:
                st.warning(f"Could not compute points prediction: {e}")

        if pts is None:
            pts = (wins * 3 + draws) / max(1, played) * 38

        # Show results
        placeholder1 = st.empty()
        animate_number(win_prob, placeholder1, fmt="{:.1f}%", duration=1.2)

        st.write("---")
        st.subheader(f"Estimated Season Points: **{round(pts)} pts**")

        # Sentiment / zone
        if win_prob > 50:
            st.success("🟩 High Championship Contender")
        elif win_prob >= 20:
            st.info("🟨 Top‑6 Possibility")
        else:
            st.error("🟥 Unlikely to Win")

elif page == "Match Winner Prediction":
    st.header("🏆 Match Result Predictor")
    st.markdown("Predict which team wins (or draw) based on in‑match statistics.")

    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        home = st.selectbox("Home Team", EPL_TEAMS, key="home_team_select")
        home_ht_goals = st.number_input("Half-Time Home Goals", min_value=0, key="home_htg")
        home_shots = st.number_input("Home Shots", min_value=0, key="home_shots")
        home_shots_ot = st.number_input("Home Shots on Target", min_value=0, key="home_shots_ot")
        home_corners = st.number_input("Home Corners", min_value=0, key="home_corners")
        home_fouls = st.number_input("Home Fouls", min_value=0, key="home_fouls")
        home_red = st.number_input("Home Red Cards", min_value=0, key="home_red")
        home_yellow = st.number_input("Home Yellow Cards", min_value=0, key="home_yellow")
    with col2:
        away = st.selectbox("Away Team", EPL_TEAMS, key="away_team_select")
        away_ht_goals = st.number_input("Half-Time Away Goals", min_value=0, key="away_htg")
        ht_result = st.selectbox("Half-Time Result", list(half_time_result_map.keys()), key="ht_result_select")
        away_shots = st.number_input("Away Shots", min_value=0, key="away_shots")
        away_shots_ot = st.number_input("Away Shots on Target", min_value=0, key="away_shots_ot")
        away_corners = st.number_input("Away Corners", min_value=0, key="away_corners")
        away_fouls = st.number_input("Away Fouls", min_value=0, key="away_fouls")
        away_red = st.number_input("Away Red Cards", min_value=0, key="away_red")
        away_yellow = st.number_input("Away Yellow Cards", min_value=0, key="away_yellow")

    if st.button("⚡ Predict Match Result"):
        if match_model is None:
            st.error("Match prediction model not loaded.")
        else:
            # Build input dict
            inp = {
                'HomeTeam': team_to_id[home],
                'AwayTeam': team_to_id[away],
                'HalfTimeHomeGoals': home_ht_goals,
                'HalfTimeAwayGoals': away_ht_goals,
                'HalfTimeResult': half_time_result_map[ht_result],
                'HomeShots': home_shots,
                'AwayShots': away_shots,
                'HomeShotsOnTarget': home_shots_ot,
                'AwayShotsOnTarget': away_shots_ot,
                'HomeCorners': home_corners,
                'AwayCorners': away_corners,
                'HomeFouls': home_fouls,
                'AwayFouls': away_fouls,
                'HomeRedCards': home_red,
                'AwayRedCards': away_red,
                'HomeYellowCards': home_yellow,
                'AwayYellowCards': away_yellow
            }
            input_df = match_input_df(inp)
            try:
                pred = match_model.predict(input_df)[0]
                # Map predictions: you need to know what your model's labels are
                # Suppose: 0 = Away Win, 1 = Draw, 2 = Home Win
                mapping = {0: "Away Win", 1: "Draw", 2: "Home Win"}
                result_label = mapping.get(pred, "Unknown")
                if pred == 2:
                    winner_team = home
                elif pred == 0:
                    winner_team = away
                else:
                    winner_team = "No one — Draw"

                st.success(f"🏁 Predicted: **{result_label}** (Winner: {winner_team})")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

# ------------------------------------------------------
# Footer / Info
# ------------------------------------------------------
st.markdown("---")
st.markdown("EPL Prediction Hub — Combine league‑level and match‑level predictions")
