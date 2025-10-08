# app.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="EPL Predictor Hub",
    page_icon="⚽",
    layout="centered"
)

# ---------------------------
# Load Models (replace with your trained models)
# ---------------------------
# For demo purposes, I’m using dummy models (replace with your own joblib files)
try:
    league_model = joblib.load("league_winner_model.joblib")
    assists_model = joblib.load("player_assists_model.joblib")
except:
    league_model = None
    assists_model = None

# ---------------------------
# Homepage
# ---------------------------
def home():
    st.title("⚽ EPL PREDICTOR HUB")
    st.markdown("### Choose Your Prediction Model")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🏆 League Winner Predictor")
        st.write("Analyze team performance metrics including wins, goals, and points to predict championship probability.")
        if st.button("🚀 Launch League Winner Predictor"):
            st.session_state.page = "league"

    with col2:
        st.markdown("#### 🎯 Player Assists Predictor")
        st.write("Forecast individual player assist totals based on key stats. Perfect for fantasy football and analysts.")
        if st.button("🚀 Launch Assists Predictor"):
            st.session_state.page = "assists"

    st.markdown("---")
    st.subheader("Why Use Our Platform?")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.write("📊 **Data-Driven**")
        st.caption("Powered by advanced ML algorithms")
    with col4:
        st.write("⚡ **Instant Results**")
        st.caption("Get predictions in seconds")
    with col5:
        st.write("🎯 **Accurate**")
        st.caption("Trained on historical EPL data")

# ---------------------------
# League Winner Predictor Page
# ---------------------------
def league_winner_predictor():
    st.title("🏆 League Winner Predictor")
    st.caption("Enter team statistics to predict championship probability")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        matches_played = st.number_input("Matches Played", min_value=0, max_value=38, value=38)
        wins = st.number_input("Wins", min_value=0, max_value=38, value=25)
    with col2:
        draws = st.number_input("Draws", min_value=0, max_value=38, value=8)
        losses = st.number_input("Losses", min_value=0, max_value=38, value=5)
    with col3:
        goals_for = st.number_input("Goals For", min_value=0, value=80)
        goals_against = st.number_input("Goals Against", min_value=0, value=30)
    with col4:
        goal_diff = st.number_input("Goal Difference", value=50)
        points = st.number_input("Points", value=90)

    if st.button("🔮 Predict Championship Probability"):
        features = np.array([[matches_played, wins, draws, losses, goals_for, goals_against, goal_diff, points]])
        if league_model:
            prediction = league_model.predict_proba(features)[0][1] * 100
        else:
            prediction = np.random.uniform(30, 95)  # demo random output
        st.success(f"🏆 Championship Probability: **{prediction:.2f}%**")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

# ---------------------------
# Player Assists Predictor Page
# ---------------------------
def player_assists_predictor():
    st.title("🎯 Player Assists Predictor")
    st.caption("Enter player statistics to forecast season assists")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        season = st.text_input("Season", value="19/20")
        minutes_played = st.number_input("Minutes Played", value=2000)
        key_passes = st.number_input("Key Passes", value=50)
        club_total_goals = st.number_input("Club Total Goals", value=60)
    with col2:
        set_piece = st.selectbox("Set Piece Taken?", ["Yes", "No"])
        expected_assists = st.number_input("Expected Assists (xA)", value=5.0)
        club_position = st.number_input("Club League Position", value=5)
        dribbles = st.number_input("Dribbles Completed", value=40)
    with col3:
        age = st.number_input("Age", value=25)
        prev_assists = st.number_input("Previous Season Assists", value=5)
        shots_assisted = st.number_input("Shots Assisted", value=20)
        big_club = st.selectbox("Big 6 Club?", ["Yes", "No"])

    col4, col5 = st.columns(2)
    with col4:
        position = st.selectbox("Position", ["Forward", "Midfielder", "Defender"])
        prev_goals = st.number_input("Previous Season Goals", value=3)
    with col5:
        attack_share = st.number_input("Player’s Attack Share", value=0.5)
        club_xg = st.number_input("Club Expected Goals (xG)", value=50.0)

    if st.button("🔮 Predict Season Assists"):
        features = np.array([[minutes_played, key_passes, club_total_goals,
                              1 if set_piece == "Yes" else 0, expected_assists,
                              club_position, dribbles, age, prev_assists,
                              shots_assisted, 1 if big_club == "Yes" else 0,
                              1 if position == "Forward" else 2 if position == "Midfielder" else 3,
                              prev_goals, attack_share, club_xg]])
        if assists_model:
            prediction = assists_model.predict(features)[0]
        else:
            prediction = np.random.randint(5, 15)  # demo random output
        st.success(f"🎯 Predicted Season Assists: **{prediction}**")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

# ---------------------------
# App Navigation
# ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home()
elif st.session_state.page == "league":
    league_winner_predictor()
elif st.session_state.page == "assists":
    player_assists_predictor()
