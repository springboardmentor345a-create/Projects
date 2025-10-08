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
        filter: drop-shadow(0 5px 20px rgba(102,126,234,0.6));
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
    
    /* Enhanced Creator Badge - DOUBLED SIZE */
    .creator-badge {
        text-align: center;
        color: rgba(255,255,255,0.7);
        font-size: 2rem;
        margin-bottom: 3rem;
        padding: 1.5rem;
        animation: fadeInUp 1s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .creator-badge .creator-name {
        background: linear-gradient(120deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.4rem;
        display: inline-block;
        letter-spacing: 1px;
        animation: glow 2.5s ease-in-out infinite, textShine 3s linear infinite;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
        position: relative;
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        cursor: pointer;
    }
    
    .creator-badge:hover .creator-name {
        transform: translateY(-8px) scale(1.05);
        filter: drop-shadow(0 15px 40px rgba(102,126,234,0.8));
    }
    
    .creator-badge .creator-name::before {
        content: '✨';
        position: absolute;
        left: -40px;
        animation: sparkle 2s ease-in-out infinite;
    }
    
    .creator-badge .creator-name::after {
        content: '✨';
        position: absolute;
        right: -40px;
        animation: sparkle 2s ease-in-out infinite 1s;
    }
    
    @keyframes sparkle {
        0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
        50% { opacity: 0.5; transform: scale(1.3) rotate(180deg); }
    }
    
    @keyframes glow {
        0%, 100% { filter: brightness(1) drop-shadow(0 0 10px rgba(102, 126, 234, 0.5)); }
        50% { filter: brightness(1.4) drop-shadow(0 0 25px rgba(118, 75, 162, 0.8)); }
    }
    
    @keyframes textShine {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
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
            box-shadow: 0 0 30px rgba(102,126,234,.4), 0 0 60px rgba(118,75,162,0.2); 
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
        filter: drop-shadow(0 5px 20px rgba(102,126,234,0.5));
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
    
    /* Celebration particles */
    .celebration-particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
    
    .particle {
        position: absolute;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        animation: particleFall 3s ease-out forwards;
    }
    
    @keyframes particleFall {
        0% {
            opacity: 1;
            transform: translateY(0) rotate(0deg);
        }
        100% {
            opacity: 0;
            transform: translateY(100vh) rotate(720deg);
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
# LOAD MODELS (.pkl only)
# ------------------------------------------------------
@st.cache_resource
def load_models():
    models_dir = Path("models")
    winner_model = None
    points_model = None
    scaler = None

    def load_pkl(path):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading {path.name}: {e}")
            return None

    if models_dir.exists():
        winner_path = models_dir / "League_winner_model.pkl"
        points_path = models_dir / "Points_model.pkl"
        scaler_path = models_dir / "scaler.pkl"

        if winner_path.exists():
            winner_model = load_pkl(winner_path)
        if points_path.exists():
            points_model = load_pkl(points_path)
        if scaler_path.exists():
            scaler = load_pkl(scaler_path)

    return winner_model, points_model, scaler


winner_model, points_model, scaler = load_models()

# ------------------------------------------------------
# HELPERS
# ------------------------------------------------------
EPL_TEAMS = [
    'Arsenal','Aston Villa','Bournemouth','Brentford','Brighton',
    'Chelsea','Crystal Palace','Everton','Fulham','Leicester City',
    'Liverpool','Manchester City','Manchester United','Newcastle United',
    'Nottingham Forest','Southampton','Tottenham Hotspur','West Ham United',
    'Wolverhampton Wanderers','Leeds United'
]

def prep_features(inp):
    df = pd.DataFrame([{
        'team': inp['team'],
        'played': inp['played'],
        'wins': inp['wins'],
        'draws': inp['draws'],
        'losses': inp['losses'],
        'points': inp['wins']*3 + inp['draws'],
        'win_rate': inp['wins']/max(1,inp['played']),
        'draw_rate': inp['draws']/max(1,inp['played']),
        'loss_rate': inp['losses']/max(1,inp['played']),
        'team_encoded': EPL_TEAMS.index(inp['team']) if inp['team'] in EPL_TEAMS else 0
    }])
    X = df[['played','wins','draws','losses','points','win_rate','draw_rate','loss_rate','team_encoded']]
    if scaler is not None:
        try:
            X = scaler.transform(X)
        except Exception:
            pass
    return X

def animate_number(target, placeholder, fmt="{:.1f}", duration=1.0):
    steps = 40
    for i in range(steps + 1):
        val = target * (i / steps)
        with placeholder.container():
            st.markdown(f"<div class='result-display'><div class='result-number'>{fmt.format(val)}</div></div>", unsafe_allow_html=True)
        time.sleep(duration / steps)

def inputs_block(prefix=''):
    col1, col2 = st.columns(2)
    with col1:
        team = st.selectbox("🏆 Team Name", EPL_TEAMS, key=f'{prefix}_team')
        played = st.number_input("📊 Matches Played", 1, 38, 10, key=f'{prefix}_played')
    with col2:
        wins = st.number_input("✅ Wins", 0, 38, 5, key=f'{prefix}_wins')
        draws = st.number_input("🤝 Draws", 0, 38, 2, key=f'{prefix}_draws')
    losses = played - (wins + draws)
    if wins + draws > played:
        st.error("⚠️ Check your inputs — total matches exceeded!")
        losses = 0
    else:
        st.markdown(f"<p class='loss-display'>❌ <strong>Losses (auto-calculated):</strong> {losses}</p>", unsafe_allow_html=True)
    return {'team':team,'played':played,'wins':wins,'draws':draws,'losses':losses}

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
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Header with football icon
st.markdown("""
<div class='header-container'>
    <div class='football-icon'>⚽</div>
    <h1 style='margin: 0;'>EPL ScoreSight</h1>
</div>
""", unsafe_allow_html=True)

if st.session_state['page'] == 'home':
    st.markdown("<p class='subtitle'>AI-Powered Premier League Predictions</p>", unsafe_allow_html=True)
    
    # Enhanced Creator Badge
    st.markdown("""
    <div class='creator-badge'>
        <span class='creator-name'>SAI KARTHIK GARDAS</span> 
        <br>
        <span style='font-size: 1.4rem; color: rgba(255,255,255,0.7); margin-top: 0.5rem; display: inline-block;'>
            presents these prediction models
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Prediction cards and buttons in proper layout
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class='prediction-card'>
            <div class='card-icon'>🏆</div>
            <div class='card-title'>League Winner Prediction</div>
            <div class='card-description'>Calculate probability of winning the EPL title</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Button container for proper centering
        btn_col1, btn_col2, btn_col3 = st.columns([0.5, 2, 0.5])
        with btn_col2:
            if st.button("🚀 Open Winner Prediction", key="winner", use_container_width=True): 
                show_football_transition()
                st.session_state['page']='winner'
                st.rerun()
    
    with col2:
        st.markdown("""
        <div class='prediction-card'>
            <div class='card-icon'>📈</div>
            <div class='card-title'>Points Prediction</div>
            <div class='card-description'>Estimate total season points for any team</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Button container for proper centering
        btn_col1, btn_col2, btn_col3 = st.columns([0.5, 2, 0.5])
        with btn_col2:
            if st.button("🚀 Open Points Prediction", key="points", use_container_width=True): 
                show_football_transition()
                st.session_state['page']='points'
                st.rerun()

elif st.session_state['page'] == 'winner':
    st.markdown("<h2>🏆 League Winner Prediction</h2>", unsafe_allow_html=True)
    st.markdown('<div class="info-box">📋 Enter team statistics to predict their championship probability</div>', unsafe_allow_html=True)
    inp = inputs_block('winner')
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Predict League Win Probability", use_container_width=True):
            placeholder = st.empty()
            X = prep_features(inp)
            prob = None
            if winner_model is not None:
                try:
                    prob = float(winner_model.predict_proba(X)[0][1]) * 100
                except Exception:
                    prob = None
            if prob is None:
                prob = (inp['wins']/max(1,inp['played']))*50 + 5
            res_box = st.empty()
            animate_number(prob, res_box, fmt="{:.1f}%", duration=1.2)
            
            if prob>50: 
                sentiment="🟩 High Championship Contender"
                color="#4ade80"
                bg_color="rgba(74, 222, 128, 0.15)"
            elif prob>=20: 
                sentiment="🟨 Top-6 Possibility"
                color="#facc15"
                bg_color="rgba(250, 204, 21, 0.15)"
            else: 
                sentiment="🟥 Unlikely to Win"
                color="#f87171"
                bg_color="rgba(248, 113, 113, 0.15)"
            
            st.markdown(f"""
            <div class='sentiment-badge' style='background:{bg_color};color:{color};border:3px solid {color};'>
                {sentiment}
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state['page']='home'
            st.rerun()

elif st.session_state['page'] == 'points':
    st.markdown("<h2>📈 Points Prediction</h2>", unsafe_allow_html=True)
    st.markdown('<div class="info-box">📋 Calculate expected total points for the season</div>', unsafe_allow_html=True)
    inp = inputs_block('points')
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Predict Total Points", use_container_width=True):
            placeholder = st.empty()
            X = prep_features(inp)
            pts = None
            if points_model is not None:
                try:
                    pts = float(points_model.predict(X)[0])
                except Exception:
                    pts = None
            if pts is None:
                pts = (inp['wins']*3 + inp['draws'])/max(1,inp['played'])*38
            res_box = st.empty()
            animate_number(pts, res_box, fmt="{:.0f} pts", duration=1.0)
            st.progress(min(100,int(pts)))
            
            if pts>=70: 
                zone="⚡ Champions League Zone"
                c="#4ade80"
                bg="rgba(74, 222, 128, 0.15)"
            elif pts>=40: 
                zone="⚖️ Mid-table Finish"
                c="#facc15"
                bg="rgba(250, 204, 21, 0.15)"
            else: 
                zone="⚠️ Relegation Risk"
                c="#f87171"
                bg="rgba(248, 113, 113, 0.15)"
            
            st.markdown(f"""
            <div class='sentiment-badge' style='background:{bg};color:{c};border:3px solid {c};'>
                {zone}
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state['page']='home'
            st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='caption'>EPL ScoreSight v2.0 | Place your .pkl models and scaler in /models</div>", unsafe_allow_html=True)