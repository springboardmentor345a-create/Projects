# app.py
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# -----------------------------
# Load models
# -----------------------------
import os
import pickle

BASE_DIR = os.path.dirname(__file__)  # this ensures path relative to app.py

with open(os.path.join(BASE_DIR, "League_winner_model.pkl"), "rb") as f:
    winner_model = pickle.load(f)

with open(os.path.join(BASE_DIR, "Points_model.pkl"), "rb") as f:
    points_model = pickle.load(f)

with open(os.path.join(BASE_DIR, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="EPL Predictor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Navbar */
    .navbar {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        padding: 1.2rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .navbar-brand {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .nav-links {
        display: flex;
        gap: 1rem;
    }
    
    /* Cards */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .card-description {
        color: #718096;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input fields */
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }
    
    /* Results */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stat-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #2d3748;
        font-weight: 600;
    }
    
    /* Success/Info messages */
    .stSuccess, .stInfo {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #48bb78;
    }
    
    .stError {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #f56565;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helper functions
# -----------------------------
def predict_winner(played, won, drawn, lost, gf, ga):
    points = won * 3 + drawn
    gd = gf - ga
    df = pd.DataFrame({
        'played':[played],
        'won':[won],
        'drawn':[drawn],
        'lost':[lost],
        'gf':[gf],
        'ga':[ga],
        'gd':[gd],
        'points':[points]
    })
    df['win_ratio'] = df['won'] / df['played']
    df['points_ratio'] = df['points'] / (df['played']*3)
    df['gd_per_game'] = df['gd'] / df['played']
    df['gd_win_interaction'] = df['gd_per_game'] * df['win_ratio']
    
    feature_cols = ['win_ratio','points_ratio','gd_per_game','gd_win_interaction']
    df_scaled = scaler.transform(df[feature_cols])
    
    pred = winner_model.predict(df_scaled)[0]
    prob = winner_model.predict_proba(df_scaled)[0][1]*100
    return pred, prob, gd, points

def predict_points(gf, ga, team_cols=None):
    gd = gf - ga
    df = pd.DataFrame({
        'gf':[gf],
        'ga':[ga],
        'gd':[gd]
    })
    
    if team_cols is not None:
        for col in team_cols:
            df[col] = 0
    
    pred_points = points_model.predict(df)[0]
    return pred_points, gd

# -----------------------------
# Initialize session state
# -----------------------------
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# -----------------------------
# Navigation
# -----------------------------
def set_page(page_name):
    st.session_state.page = page_name

# Custom Navbar
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    st.markdown('<div class="navbar-brand">⚽ EPL Predictor</div>', unsafe_allow_html=True)
with col2:
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        set_page("Home")
with col3:
    if st.button("🏆 Winner", key="nav_winner", use_container_width=True):
        set_page("League Winner Prediction")
with col4:
    if st.button("📊 Points", key="nav_points", use_container_width=True):
        set_page("Points Prediction")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# Home Page
# -----------------------------
if st.session_state.page == "Home":
    st.markdown("<h1 style='text-align: center; margin-bottom: 3rem;'>⚽ Premier League Prediction Dashboard</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🏆</div>
            <div class="card-title">League Winner Chances</div>
            <div class="card-description">
                Predict the probability of winning the league based on current season statistics including games played, wins, draws, and goal difference.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Winner Chances", key="home_winner", use_container_width=True):
            set_page("League Winner Prediction")
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📊</div>
            <div class="card-title">Points Prediction</div>
            <div class="card-description">
                Predict total points for the season based on offensive and defensive performance metrics like goals scored and conceded.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Predict Points", key="home_points", use_container_width=True):
            set_page("Points Prediction")
            st.rerun()

# -----------------------------
# League Winner Prediction
# -----------------------------
elif st.session_state.page == "League Winner Prediction":
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🏆 League Winner Prediction</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Match Statistics")
        
        played = st.number_input("Games Played", min_value=1, max_value=38, value=19)
        
        won_max = played
        won = st.number_input("Games Won", min_value=0, max_value=won_max, value=min(16, won_max))
        
        lost_max = played - won
        lost = st.number_input("Games Lost", min_value=0, max_value=lost_max, value=min(10, lost_max))
        
        drawn = played - won - lost
        st.markdown(f'<div class="stat-box">Games Drawn: {drawn}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Goal Statistics")
        
        gf = st.number_input("Goals For (GF)", min_value=0, value=50)
        ga = st.number_input("Goals Against (GA)", min_value=0, value=30)
        
        points = won*3 + drawn
        gd = gf - ga
        
        st.markdown(f'<div class="stat-box">Goal Difference: {gd:+d}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-box">Total Points: {points}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔮 Predict Winner Chances", key="winner_btn", use_container_width=True):
            if won+drawn+lost != played:
                st.error("⚠️ Sum of Won + Drawn + Lost does not match Games Played!")
            else:
                pred, prob, gd_calc, points_calc = predict_winner(played, won, drawn, lost, gf, ga)
                
                st.markdown(f"""
                <div class="result-card">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">
                        {'🏆' if pred==1 else '📉'}
                    </div>
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">
                        {'LEAGUE WINNER POTENTIAL' if pred==1 else 'NOT A TITLE CONTENDER'}
                    </div>
                    <div style="font-size: 2rem; font-weight: 700;">
                        {prob:.1f}% Chance
                    </div>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------
# Points Prediction
# -----------------------------
elif st.session_state.page == "Points Prediction":
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>📊 Season Points Prediction</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Goal Statistics")
        
        gf = st.number_input("Goals For (GF)", min_value=0, value=50, key="gf_points")
        ga = st.number_input("Goals Against (GA)", min_value=0, value=30, key="ga_points")
        
        gd = gf - ga
        st.markdown(f'<div class="stat-box">Goal Difference: {gd:+d}</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🎯 Predict Total Points", key="points_btn", use_container_width=True):
            team_cols = points_model.feature_names_in_ if hasattr(points_model, "feature_names_in_") else None
            pred_points, gd_calc = predict_points(gf, ga, team_cols)
            
            st.markdown(f"""
            <div class="result-card">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">
                    🎯
                </div>
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">
                    PREDICTED SEASON TOTAL
                </div>
                <div style="font-size: 3rem; font-weight: 700;">
                    {pred_points:.0f} Points
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)