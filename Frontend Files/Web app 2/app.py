import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
from pathlib import Path

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="EPL ScoreSight",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------
# ENSURE SESSION STATE KEYS
# ------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Keys to hold results
if 'assists_result' not in st.session_state:
    st.session_state['assists_result'] = None
if 'goals_result' not in st.session_state:
    st.session_state['goals_result'] = None

# ------------------------------------------------------
# ENHANCED CUSTOM CSS
# ------------------------------------------------------
def inject_custom_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg,#0f0c29 0%,#302b63 50%,#24243e 100%);
        font-family:'Inter',sans-serif;
    }
    
    #MainMenu, footer, header {visibility:hidden;}
    
    /* Enhanced Header with Football Icon */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        margin-bottom: 1rem;
        animation: titleFloat 3s ease-in-out infinite;
    }
    
    .football-icon {
        font-size: 4.5rem;
        animation: spin 4s linear infinite, float 3s ease-in-out infinite;
        filter: drop_shadow(0 5px 20px rgba(102,126,234,0.6));
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    h1{
        background:linear-gradient(120deg,#667eea 0%,#764ba2 100%);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        text-align:center;
        font-size:4rem!important;
        font-weight:900;
        margin-bottom:0;
        letter-spacing: -1px;
        position: relative;
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    h2{
        color:#ffffff !important;
        text-align:center;
        font-weight:700;
        font-size: 2.5rem;
        margin-bottom:2rem;
        animation: fadeInDown 0.6s ease-out;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Info box enhancement for better visibility */
    .info-box{
        background:rgba(102,126,234,0.2);
        border-left:5px solid #667eea;
        padding:1.25rem;
        border-radius:8px;
        margin:1.5rem 0;
        color:#ffffff !important;
        font-size: 1.1rem;
        font-weight: 600;
        animation: slideInLeft 0.6s ease-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .info-box * {
        color: #ffffff !important;
    }
    
    /* Fix label visibility */
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    .stNumberInput label {
        color: rgba(255,255,255,0.85) !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }
    
    /* Enhanced Input fields */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stSelectbox > div > div:hover, .stNumberInput > div > div > input:hover {
        border-color: rgba(102,126,234,0.6) !important;
        background: rgba(255,255,255,0.12) !important;
        box-shadow: 0 0 20px rgba(102,126,234,0.3);
    }
    
    .stSelectbox > div > div:focus-within, .stNumberInput > div > div:focus-within {
        border-color: rgba(102,126,234,0.8) !important;
        background: rgba(255,255,255,0.15) !important;
        box-shadow: 0 0 25px rgba(102,126,234,0.5);
    }
    
    /* Enhanced Prediction cards */
    .prediction-card{
        background:rgba(255,255,255,0.06);
        border:2px solid rgba(255,255,255,0.15);
        border-radius:25px;
        padding:3rem 2.5rem;
        width: 100%;
        max-width:480px;
        backdrop-filter:blur(15px);
        transition:all .5s cubic-bezier(.4,0,.2,1);
        cursor:pointer;
        text-align: center;
        margin: 0 auto 1.5rem;
        position: relative;
        overflow: hidden;
        animation: cardFadeIn 0.8s ease-out;
    }
    
    @keyframes cardFadeIn {
        from { opacity: 0; transform: scale(0.9) translateY(20px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    .prediction-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .prediction-card:hover::before {
        left: 100%;
    }
    
    .prediction-card:hover{
        transform:translateY(-15px) scale(1.02);
        box-shadow:0 25px 50px rgba(102,126,234,.5), 0 0 50px rgba(118,75,162,0.3);
        background:rgba(255,255,255,.12);
        border-color: rgba(102,126,234,0.5);
    }
    
    .card-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        animation: float 3s ease-in-out infinite;
        filter: drop-shadow(0 5px 15px rgba(102,126,234,0.5));
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(-5deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
    }
    
    .card-title {
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        letter-spacing: 0.5px;
    }
    
    .card-description {
        color: rgba(255,255,255,0.75);
        font-size: 1.05rem;
        margin-bottom: 0;
        line-height: 1.5;
    }
    
    /* Enhanced Button styling with perfect positioning */
    .stButton {
        display: flex;
        justify-content: center;
        margin: 2rem auto;
        width: 100%;
    }
    
    .stButton>button{
        background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        color:#fff;
        border:none;
        border-radius:35px;
        padding:1.2rem 3.5rem;
        font-weight:700;
        font-size: 1.15rem;
        letter-spacing: 0.5px;
        box-shadow:0 8px 25px rgba(102,126,234,.4);
        width: 100%;
        max-width: 450px;
        margin: 0 auto;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 400px;
        height: 400px;
    }
    
    .stButton>button:hover{
        transform:translateY(-5px) scale(1.05);
        box-shadow:0 15px 40px rgba(102,126,234,.6), 0 0 30px rgba(118,75,162,0.4);
        background:linear-gradient(135deg,#764ba2 0%,#667eea 100%);
    }
    
    .stButton>button:active {
        transform:translateY(-2px) scale(1.02);
    }
    
    /* Enhanced Result display with celebration */
    .result-display{
        background:rgba(102,126,234,.18);
        border:3px solid rgba(102,126,234,.5);
        border-radius:25px;
        padding:2.5rem;
        margin:2.5rem auto;
        text-align:center;
        max-width:550px;
        animation: resultPopIn 0.8s cubic-bezier(.68,-0.55,.265,1.55), shimmer 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .result-display:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 50px rgba(102,126,234,.6), 0 0 40px rgba(118,75,162,0.4);
    }
    
    @keyframes resultPopIn {
        0% { 
            opacity: 0; 
            transform: scale(0.5); 
        }
        60% {
            transform: scale(1.1);
        }
        100% { 
            opacity: 1; 
            transform: scale(1); 
        }
    }
    
    .result-display::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(255, 255, 255, 0.15) 50%,
            transparent 70%
        );
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    @keyframes shimmer {
        0%, 100% { 
            box-shadow: 0 0 30px rgba(102,126,234,.4), 0 0 60px rgba(118,75,162,.2); 
            border-color: rgba(102,126,234,.5);
        }
        50% { 
            box-shadow: 0 0 50px rgba(102,126,234,.7), 0 0 80px rgba(118,75,162,.5); 
            border-color: rgba(102,126,234,.8);
        }
    }
    
    .result-number{
        font-size:5rem;
        font-weight:900;
        background:linear-gradient(120deg,#667eea 0%,#764ba2 50%, #f093fb 100%);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        animation: pulse 2s ease-in-out infinite, numberPop 0.8s cubic-bezier(.68,-0.55,.265,1.55);
        position: relative;
        z-index: 1;
        letter-spacing: -2px;
        filter: drop_shadow(0 5px 20px rgba(102,126,234,0.5));
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.08); }
    }
    
    @keyframes numberPop {
        0% { 
            transform: scale(0); 
            opacity: 0; 
        }
        60% { 
            transform: scale(1.15); 
        }
        100% { 
            transform: scale(1); 
            opacity: 1; 
        }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Alert boxes */
    .stAlert {
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        border-left: 4px solid #f87171 !important;
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    hr{
        border:none;
        height:2px;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);
        margin:4rem 0;
    }
    
    .caption{
        text-align:center;
        color:rgba(255,255,255,.6);
        font-size:.95rem;
        margin-top:2rem;
        font-weight: 500;
    }
    
    /* Enhanced Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
        animation: progressGlow 2s ease-in-out infinite, progressMove 2s linear infinite;
        box-shadow: 0 0 20px rgba(102,126,234,.6);
    }
    
    @keyframes progressGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(102,126,234,.5); }
        50% { box-shadow: 0 0 30px rgba(102,126,234,.9); }
    }
    
    @keyframes progressMove {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    
    /* Enhanced Sentiment badge */
    .sentiment-badge {
        display: inline-block;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        margin-top: 2rem;
        font-weight: 700;
        font-size: 1.25rem;
        animation: badgeExplode 1s cubic-bezier(.68,-0.55,.265,1.55);
        position: relative;
        letter-spacing: 0.5px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    @keyframes badgeExplode {
        0% { 
            transform: scale(0) rotate(-180deg);
            opacity: 0;
        }
        70% {
            transform: scale(1.2) rotate(10deg);
        }
        100% { 
            transform: scale(1) rotate(0deg);
            opacity: 1;
        }
    }
    
    .sentiment-badge::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 100%;
        height: 100%;
        border-radius: 30px;
        animation: ripple 1.5s ease-out infinite;
        z-index: -1;
    }
    
    @keyframes ripple {
        0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.6;
        }
        100% {
            transform: translate(-50%, -50%) scale(1.8);
            opacity: 0;
        }
    }
    
    /* Enhanced subtitle */
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.8);
        font-size: 1.3rem;
        margin-bottom: 2rem;
        font-weight: 500;
        animation: fadeIn 1s ease-out 0.3s backwards;
        letter-spacing: 0.5px;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Loss display enhancement */
    .loss-display {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.75rem;
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        margin-top: 1rem;
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Football transition overlay */
    .football-transition {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 12, 41, 0.95);
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: fadeInOverlay 0.3s ease-out;
    }
    
    @keyframes fadeInOverlay {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .football-flying {
        font-size: 6rem;
        animation: flyAcross 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
        filter: drop-shadow(0 0 30px rgba(102,126,234,0.8));
    }
    
    @keyframes flyAcross {
        0% {
            transform: translateX(-150vw) rotate(0deg) scale(0.5);
            opacity: 0;
        }
        50% {
            transform: translateX(0) rotate(720deg) scale(1.5);
            opacity: 1;
        }
        100% {
            transform: translateX(150vw) rotate(1440deg) scale(0.5);
            opacity: 0;
        }
    }
    
    </style>""", unsafe_allow_html=True)

inject_custom_css()

# ------------------------------------------------------
# LOAD MODELS (.pkl)
# ------------------------------------------------------
@st.cache_resource
def load_models():
    models_dir = Path("models")
    # Only loading Assists and Goals models
    assists_model = None
    assists_label_encoder = None
    assists_imputer = None
    goals_model = None

    def load_pkl(path):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading {path.name}: {e}")
            return None

    if models_dir.exists():
        assists_model_path = models_dir / "top_assist_model.pkl"
        assists_le_path = models_dir / "label_encoder.pkl"
        assists_imputer_path = models_dir / "imputer.pkl"
        goals_model_path = models_dir / "top_goals_model.pkl"

        if assists_model_path.exists():
            assists_model = load_pkl(assists_model_path)
        if assists_le_path.exists():
            assists_label_encoder = load_pkl(assists_le_path)
        if assists_imputer_path.exists():
            assists_imputer = load_pkl(assists_imputer_path)
        if goals_model_path.exists():
            goals_model = load_pkl(goals_model_path)

    # Updated return statement
    return assists_model, assists_label_encoder, assists_imputer, goals_model


assists_model, assists_label_encoder, assists_imputer, goals_model = load_models()

# ------------------------------------------------------
# HELPERS
# ------------------------------------------------------
POSITIONS = ['Forward', 'Midfielder', 'Defender']
SET_PIECE_OPTIONS = ['Yes', 'No']
BIG6_OPTIONS = ['Yes', 'No']

def prep_features_assists(inp):
    """Prepare features for Top Assists prediction"""
    # Calculate derived features
    assists_per_90 = inp['assists'] / (inp['minutes_played'] / 90) if inp['minutes_played'] > 0 else 0
    goals_per_90 = inp['goals_prev_season'] / (inp['minutes_played'] / 90) if inp['minutes_played'] > 0 else 0
    contribution_ratio = (inp['assists'] + inp['goals_prev_season']) / inp['club_total_goals'] if inp['club_total_goals'] > 0 else 0
    dribbles_per_90 = inp['dribbles_completed'] / (inp['minutes_played'] / 90) if inp['minutes_played'] > 0 else 0
    shots_assisted_per_90 = inp['shots_assisted'] / (inp['minutes_played'] / 90) if inp['minutes_played'] > 0 else 0
    
    # Encode categorical features
    position_encoded = POSITIONS.index(inp['position']) if inp['position'] in POSITIONS else 0
    set_piece_encoded = 1 if inp['set_piece_involvement'] == 'Yes' else 0
    big6_encoded = 1 if inp['big6_club'] == 'Yes' else 0
    
    df = pd.DataFrame([{
        'Position': position_encoded,
        'Minutes_Played': inp['minutes_played'],
        'Goals_prev_season': inp['goals_prev_season'],
        'Dribbles_Completed': inp['dribbles_completed'],
        'Shots_Assisted': inp['shots_assisted'],
        'Key_Passes': inp['key_passes'],
        'xA': inp['xa'],
        'Club_Total_Goals': inp['club_total_goals'],
        'Set_Piece_Involvement': set_piece_encoded,
        'Big6_Club_Feature': big6_encoded,
        'Assists_per_90': assists_per_90,
        'Goals_per_90': goals_per_90,
        'Contribution_Ratio': contribution_ratio,
        'Dribbles_per_90': dribbles_per_90,
        'Shots_Assisted_per_90': shots_assisted_per_90
    }])
    
    return df

def prep_features_goals(inp):
    """Prepare features for Top Goals prediction"""
    # Encode position
    position_encoded = POSITIONS.index(inp['position']) if inp['position'] in POSITIONS else 0
    
    # Calculate derived features
    goals_per_90 = inp['goals_prev_season'] / (inp['minutes_played'] / 90) if inp['minutes_played'] > 0 else 0
    
    df = pd.DataFrame([{
        'Position': position_encoded,
        'Age': inp['age'],
        'Appearances': inp['appearances'],
        'Minutes_Played': inp['minutes_played'],
        'Goals_prev_season': inp['goals_prev_season'],
        'Assists': inp['assists'],
        'Goals_per_90': goals_per_90,
        'League_Goals_per_Match': inp['league_goals_per_match'],
        'Goals_last_3_seasons_avg': inp['goals_last_3_avg']
    }])
    
    return df

def animate_number(target, placeholder, fmt="{:.1f}", duration=1.0):
    steps = 40
    for i in range(steps + 1):
        val = target * (i / steps)
        with placeholder.container():
            st.markdown(f"<div class='result-display'><div class='result-number'>{fmt.format(val)}</div></div>", unsafe_allow_html=True)
        time.sleep(duration / steps)

# ------------------------------------------------------
# INPUT BLOCKS 
# ------------------------------------------------------

def inputs_block_assists(prefix='assists'):
    """Input block for Top Assists Prediction"""
    col1, col2 = st.columns(2)
    with col1:
        position = st.selectbox("👤 Position", POSITIONS, key=f'{prefix}_position')
        minutes_played = st.number_input("⏱️ Minutes Played", min_value=1, max_value=5000, value=1260, key=f'{prefix}_mins')
        assists = st.number_input("🎯 Current Assists", min_value=0, max_value=50, value=5, key=f'{prefix}_assists')
        goals_prev_season = st.number_input("⚽ Goals (Previous Season)", min_value=0, max_value=50, value=8, key=f'{prefix}_goals_prev')
        dribbles_completed = st.number_input("🏃 Dribbles Completed", min_value=0, max_value=200, value=25, key=f'{prefix}_dribbles')
        shots_assisted = st.number_input("🎯 Shots Assisted", min_value=0, max_value=200, value=30, key=f'{prefix}_shots_assisted')
    with col2:
        key_passes = st.number_input("🔑 Key Passes", min_value=0, max_value=200, value=35, key=f'{prefix}_key_passes')
        xa = st.number_input("📊 Expected Assists (xA)", min_value=0.0, max_value=30.0, value=6.5, step=0.1, key=f'{prefix}_xa')
        club_total_goals = st.number_input("🏆 Club Total Goals", min_value=1, max_value=200, value=60, key=f'{prefix}_club_goals')
        set_piece_involvement = st.selectbox("🎯 Set Piece Involvement", SET_PIECE_OPTIONS, key=f'{prefix}_set_piece')
        big6_club = st.selectbox("⭐ Big 6 Club", BIG6_OPTIONS, key=f'{prefix}_big6')
    
    return {
        'position': position,
        'minutes_played': minutes_played,
        'assists': assists,
        'goals_prev_season': goals_prev_season,
        'dribbles_completed': dribbles_completed,
        'shots_assisted': shots_assisted,
        'key_passes': key_passes,
        'xa': xa,
        'club_total_goals': club_total_goals,
        'set_piece_involvement': set_piece_involvement,
        'big6_club': big6_club
    }

def inputs_block_goals(prefix='goals'):
    """Input block for Top Goals Prediction"""
    col1, col2 = st.columns(2)
    with col1:
        position = st.selectbox("👤 Position", POSITIONS, key=f'{prefix}_position')
        age = st.number_input("🎂 Age", min_value=16, max_value=45, value=25, key=f'{prefix}_age')
        appearances = st.number_input("📊 Appearances", min_value=1, max_value=50, value=14, key=f'{prefix}_appearances')
        minutes_played = st.number_input("⏱️ Minutes Played", min_value=1, max_value=5000, value=1260, key=f'{prefix}_mins')
        goals_prev_season = st.number_input("⚽ Goals (Previous Season)", min_value=0, max_value=50, value=12, key=f'{prefix}_goals_prev')
    with col2:
        assists = st.number_input("🎯 Assists", min_value=0, max_value=50, value=3, key=f'{prefix}_assists')
        league_goals_per_match = st.number_input("📈 League Goals per Match", min_value=0.0, max_value=10.0, value=2.8, step=0.1, key=f'{prefix}_league_gpm')
        goals_last_3_avg = st.number_input("📊 Goals Last 3 Seasons (Avg)", min_value=0.0, max_value=50.0, value=10.5, step=0.1, key=f'{prefix}_goals_3avg')
    
    return {
        'position': position,
        'age': age,
        'appearances': appearances,
        'minutes_played': minutes_played,
        'goals_prev_season': goals_prev_season,
        'assists': assists,
        'league_goals_per_match': league_goals_per_match,
        'goals_last_3_avg': goals_last_3_avg
    }

# ------------------------------------------------------
# TRANSITION
# ------------------------------------------------------
def show_football_transition():
    """Display flying football transition effect"""
    transition_placeholder = st.empty()
    transition_placeholder.markdown("""
    <div class='football-transition'>
        <div class='football-flying'>⚽</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1.0)
    transition_placeholder.empty()

# ------------------------------------------------------
# APP PAGES
# ------------------------------------------------------

# Header with football icon
st.markdown("""
<div class='header-container'>
    <div class='football-icon'>⚽</div>
    <h1 style='margin: 0;'>EPL ScoreSight</h1>
</div>
""", unsafe_allow_html=True)

# -------------------
# HOME PAGE
# -------------------
if st.session_state['page'] == 'home':
    st.markdown("<p class='subtitle'>AI-Powered Premier League Predictions</p>", unsafe_allow_html=True)
    
    # Prediction cards in a single row (2 columns)
    col1, col2 = st.columns(2, gap="large")
    
    # ASSISTS CARD
    with col1:
        st.markdown("""
        <div class='prediction-card'>
            <div class='card-icon'>🎯</div>
            <div class='card-title'>Top Assists Prediction</div>
            <div class='card-description'>Predict season assists for a player</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([0.5, 2, 0.5])
        with btn_col2:
            if st.button("🚀 Open Assists Prediction", key="assists", use_container_width=True): 
                show_football_transition()
                st.session_state['page']='assists'
                st.rerun()
    
    # GOALS CARD
    with col2:
        st.markdown("""
        <div class='prediction-card'>
            <div class='card-icon'>⚽</div>
            <div class='card-title'>Top Goals Prediction</div>
            <div class='card-description'>Predict season goals for a player</div>
        </div>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2, btn_col3 = st.columns([0.5, 2, 0.5])
        with btn_col2:
            if st.button("🚀 Open Goals Prediction", key="goals", use_container_width=True): 
                show_football_transition()
                st.session_state['page']='goals'
                st.rerun()

# -------------------
# ASSISTS INPUT PAGE
# -------------------
elif st.session_state['page'] == 'assists':
    st.markdown("<h2>🎯 Top Assists Prediction</h2>", unsafe_allow_html=True)
    st.markdown('<div class="info-box">📋 Enter player statistics to predict season assists</div>', unsafe_allow_html=True)
    inp = inputs_block_assists('assists')
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🎯 Predict Season Assists", use_container_width=True):
            X = prep_features_assists(inp)
            assists_pred = None
            if assists_model is not None:
                try:
                    assists_pred = float(assists_model.predict(X)[0])
                except Exception:
                    assists_pred = None
            if assists_pred is None:
                # Fallback calculation if model fails
                assists_pred = inp['assists'] * (3420 / max(1, inp['minutes_played']))
            
            if assists_pred >= 10:
                category = "🌟 Elite Playmaker"
                color = "#4ade80"
                bg_color = "rgba(74, 222, 128, 0.15)"
            elif assists_pred >= 5:
                category = "⚡ Quality Creator"
                color = "#facc15"
                bg_color = "rgba(250, 204, 21, 0.15)"
            else:
                category = "📊 Developing Player"
                color = "#f87171"
                bg_color = "rgba(248, 113, 113, 0.15)"
            
            st.session_state['assists_result'] = {
                'input': inp,
                'assists': assists_pred,
                'category': category,
                'color': color,
                'bg_color': bg_color
            }
            
            show_football_transition()
            st.session_state['page'] = 'assists_result'
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state['page']='home'
            st.rerun()

# -------------------
# GOALS INPUT PAGE
# -------------------
elif st.session_state['page'] == 'goals':
    st.markdown("<h2>⚽ Top Goals Prediction</h2>", unsafe_allow_html=True)
    st.markdown('<div class="info-box">📋 Enter player statistics to predict season goals</div>', unsafe_allow_html=True)
    inp = inputs_block_goals('goals')
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🎯 Predict Season Goals", use_container_width=True):
            X = prep_features_goals(inp)
            goals_pred = None
            if goals_model is not None:
                try:
                    goals_pred = float(goals_model.predict(X)[0])
                except Exception:
                    goals_pred = None
            if goals_pred is None:
                # Fallback calculation if model fails
                goals_pred = inp['goals_prev_season'] * 1.1
            
            if goals_pred >= 20:
                category = "🔥 Golden Boot Contender"
                color = "#4ade80"
                bg_color = "rgba(74, 222, 128, 0.15)"
            elif goals_pred >= 10:
                category = "⚡ Solid Scorer"
                color = "#facc15"
                bg_color = "rgba(250, 204, 21, 0.15)"
            else:
                category = "📊 Supporting Role"
                color = "#f87171"
                bg_color = "rgba(248, 113, 113, 0.15)"
            
            st.session_state['goals_result'] = {
                'input': inp,
                'goals': goals_pred,
                'category': category,
                'color': color,
                'bg_color': bg_color
            }
            
            show_football_transition()
            st.session_state['page'] = 'goals_result'
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state['page']='home'
            st.rerun()

# -------------------
# ASSISTS RESULT PAGE
# -------------------
elif st.session_state['page'] == 'assists_result':
    result = st.session_state.get('assists_result')
    if result is None:
        st.warning("No result found — please enter inputs and predict again.")
        if st.button("Go to Assists Prediction"):
            st.session_state['page'] = 'assists'
            st.rerun()
    else:
        st.markdown("<h2>🎯 Top Assists Prediction — Result</h2>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'>🎉 Here's the predicted season assists</div>", unsafe_allow_html=True)
        
        inp = result['input']
        st.markdown(f"""
        <div class='prediction-card' style='max-width:680px;'>
            <div style='font-weight:700; font-size:1.15rem; margin-bottom:0.5rem; color:#ffffff;'>Input Summary</div>
            <div style='color: #ffffff;'>
                Position: {inp['position']} &nbsp;|&nbsp; Minutes: {inp['minutes_played']} &nbsp;|&nbsp; Current Assists: {inp['assists']}<br>
                Goals (Prev Season): {inp['goals_prev_season']} &nbsp;|&nbsp; xA: {inp['xa']} &nbsp;|&nbsp; Key Passes: {inp['key_passes']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            res_placeholder = st.empty()
            animate_number(result['assists'], res_placeholder, fmt="{:.0f} assists", duration=1.2)
        
        with col2:
            st.markdown(f"""
            <div class='result-display' style='height: auto; display: flex; align-items: center; justify-content: center;'>
                <div class='sentiment-badge' style='background:{result['bg_color']};color:{result['color']};border:3px solid {result['color']};margin:0;'>
                    {result['category']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2, gap="large")
        with btn_col1:
            if st.button("🏠 Back to Home", key="assists_result_home", use_container_width=True):
                st.session_state['page'] = 'home'
                st.rerun()
        with btn_col2:
            if st.button("🔁 Re-run Prediction (Edit Inputs)", key="assists_result_rerun", use_container_width=True):
                st.session_state['page'] = 'assists'
                st.rerun()

# -------------------
# GOALS RESULT PAGE
# -------------------
elif st.session_state['page'] == 'goals_result':
    result = st.session_state.get('goals_result')
    if result is None:
        st.warning("No result found — please enter inputs and predict again.")
        if st.button("Go to Goals Prediction"):
            st.session_state['page'] = 'goals'
            st.rerun()
    else:
        st.markdown("<h2>⚽ Top Goals Prediction — Result</h2>", unsafe_allow_html=True)
        st.markdown("<div class='info-box'>🎉 Here's the predicted season goals</div>", unsafe_allow_html=True)
        
        inp = result['input']
        st.markdown(f"""
        <div class='prediction-card' style='max-width:680px;'>
            <div style='font-weight:700; font-size:1.15rem; margin-bottom:0.5rem; color:#ffffff;'>Input Summary</div>
            <div style='color: #ffffff;'>
                Position: {inp['position']} &nbsp;|&nbsp; Age: {inp['age']} &nbsp;|&nbsp; Appearances: {inp['appearances']}<br>
                Minutes: {inp['minutes_played']} &nbsp;|&nbsp; Goals (Prev): {inp['goals_prev_season']} &nbsp;|&nbsp; Assists: {inp['assists']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            res_placeholder = st.empty()
            animate_number(result['goals'], res_placeholder, fmt="{:.0f} goals", duration=1.2)
        
        with col2:
            st.markdown(f"""
            <div class='result-display' style='height: auto; display: flex; align-items: center; justify-content: center;'>
                <div class='sentiment-badge' style='background:{result['bg_color']};color:{result['color']};border:3px solid {result['color']};margin:0;'>
                    {result['category']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2, gap="large")
        with btn_col1:
            if st.button("🏠 Back to Home", key="goals_result_home", use_container_width=True):
                st.session_state['page'] = 'home'
                st.rerun()
        with btn_col2:
            if st.button("🔁 Re-run Prediction (Edit Inputs)", key="goals_result_rerun", use_container_width=True):
                st.session_state['page'] = 'goals'
                st.rerun()
