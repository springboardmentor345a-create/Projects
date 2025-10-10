import streamlit as st
import time

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="AI ScoreSight Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------------------------
# CUSTOM CSS - MATCHES YOUR DESIGN
# ------------------------------------------------------
def inject_custom_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg,#0f0c29 0%,#302b63 50%,#24243e 100%);
        font-family:'Inter',sans-serif;
    }
    
    #MainMenu, footer, header {visibility:hidden;}
    
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
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(-5deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
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
    
    .prediction-card{
        background:rgba(255,255,255,0.06);
        border:2px solid rgba(255,255,255,0.15);
        border-radius:25px;
        padding:3rem 2rem;
        backdrop-filter:blur(15px);
        transition:all .5s cubic-bezier(.4,0,.2,1);
        cursor:pointer;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: cardFadeIn 0.8s ease-out;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
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
        animation: iconFloat 3s ease-in-out infinite;
        filter: drop-shadow(0 5px 15px rgba(102,126,234,0.5));
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0px) rotate(-5deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
    }
    
    .card-title {
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    .card-description {
        color: rgba(255,255,255,0.75);
        font-size: 1.05rem;
        margin-bottom: 0;
        line-height: 1.6;
    }
    
    .stButton {
        display: flex;
        justify-content: center;
        margin: 2rem auto 0;
        width: 100%;
    }
    
    .stButton>button{
        background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
        color:#fff;
        border:none;
        border-radius:35px;
        padding:1.2rem 3rem;
        font-weight:700;
        font-size: 1.15rem;
        letter-spacing: 0.5px;
        box-shadow:0 8px 25px rgba(102,126,234,.4);
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        position: relative;
        overflow: hidden;
        width: 100%;
    }
    
    .stButton>button:hover{
        transform:translateY(-5px) scale(1.05);
        box-shadow:0 15px 40px rgba(102,126,234,.6), 0 0 30px rgba(118,75,162,0.4);
        background:linear-gradient(135deg,#764ba2 0%,#667eea 100%);
    }

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

    hr{
        border:none;
        height:2px;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,.3),transparent);
        margin:4rem 0;
    }

    </style>""", unsafe_allow_html=True)

inject_custom_css()

# ------------------------------------------------------
# TRANSITION ANIMATION
# ------------------------------------------------------
def show_football_transition():
    transition_placeholder = st.empty()
    transition_placeholder.markdown("""
    <div class='football-transition'>
        <div class='football-flying'>⚽</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1.0)
    transition_placeholder.empty()

# ------------------------------------------------------
# MAIN PAGE
# ------------------------------------------------------

st.markdown("""
<div class='header-container'>
    <div class='football-icon'>⚽</div>
    <h1 style='margin: 0;'>AI ScoreSight</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='subtitle'>Explore All AI-Powered Football Prediction Apps</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

# Card 1: League Winner & Points
with col1:
    st.markdown("""
    <div class='prediction-card'>
        <div>
            <div class='card-icon'>🏆</div>
            <div class='card-title'>League Winner & Overall Points</div>
            <div class='card-description'>Calculate probability of winning the EPL title and estimate total season points for any team</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Open League Winner & Points", key="app1", use_container_width=True):
        show_football_transition()
        st.markdown('<meta http-equiv="refresh" content="0;url=https://sai-karthik-gardas-epl.streamlit.app">', unsafe_allow_html=True)

# Card 2: Top Goals & Top Assists
with col2:
    st.markdown("""
    <div class='prediction-card'>
        <div>
            <div class='card-icon'>⚽</div>
            <div class='card-title'>Top Goals & Top Assists</div>
            <div class='card-description'>Predict top goal scorers and assist leaders throughout the season based on player performance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Open Top Goals & Assists", key="app2", use_container_width=True):
        show_football_transition()
        st.markdown('<meta http-equiv="refresh" content="0;url=https://epl-project-top-assist-and-goals.streamlit.app">', unsafe_allow_html=True)

# Card 3: Match Winner (placeholder)
with col3:
    st.markdown("""
    <div class='prediction-card'>
        <div>
            <div class='card-icon'>🎯</div>
            <div class='card-title'>Match Winner</div>
            <div class='card-description'>Predict which team is likely to win based on head-to-head stats and current form analysis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Open Match Winner", key="app3", use_container_width=True):
        show_football_transition()
        st.markdown('<meta http-equiv="refresh" content="0;url=https://placeholder-link.com">', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p class='caption' style='text-align:center;color:rgba(255,255,255,.6);font-size:.95rem;margin-top:2rem;'>🏆 Powered by Machine Learning & Advanced Analytics</p>", unsafe_allow_html=True)
