import streamlit as st

# Set page config
st.set_page_config(page_title="Scoresight", page_icon="⚽", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main background and fonts */
    .stApp {
        background: linear-gradient(120deg, #0a0e17, #1a1f2e);
    }
    
    /* Welcome section styling - Full screen hero */
    .welcome-section {
        position: relative;
        text-align: center;
        min-height: 100vh;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 0;
        margin: 0;
        overflow: hidden;
    }
    
    .hero-content {
        position: absolute;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 10;
        width: 90%;
        max-width: 1200px;
        padding: 40px 20px;
        background: linear-gradient(to bottom, rgba(10, 14, 23, 0.4), rgba(10, 14, 23, 0.7));
        backdrop-filter: blur(5px);
        border-radius: 20px;
    }
    
    .main-title {
        font-size: clamp(2em, 5vw, 4.5em);
        font-weight: 800;
        color: #ffffff;
        text-shadow: 4px 4px 15px rgba(0,0,0,0.8);
        margin-bottom: 20px;
        letter-spacing: 3px;
        animation: fadeInDown 1s ease-out;
    }
    
    .subtitle {
        font-size: clamp(1em, 2.5vw, 1.8em);
        color: #ffffff;
        margin-bottom: 0;
        font-weight: 400;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.7);
        animation: fadeInUp 1s ease-out 0.3s backwards;
    }
    
    .welcome-image-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 1;
    }
    
    .welcome-image-container img {
        width: 100%;
        height: 100%;
        min-height: 100vh;
        object-fit: cover;
        object-position: center;
        display: block;
    }
    
    /* Responsive adjustments for mobile */
    @media (max-width: 768px) {
        .hero-content {
            width: 95%;
            padding: 30px 15px;
            top: 35%;
        }
        
        .main-title {
            letter-spacing: 1px;
        }
        
        .scroll-indicator {
            bottom: 20px;
        }
    }
    
    @media (max-width: 480px) {
        .hero-content {
            padding: 20px 10px;
        }
    }
    
    /* Ensure full height on different devices */
    @media (min-height: 900px) {
        .welcome-section {
            min-height: 100vh;
        }
    }
    
    .scroll-indicator {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
        animation: bounce 2s infinite;
        cursor: pointer;
    }
    
    .scroll-indicator span {
        font-size: 2.5em;
        color: rgba(255, 255, 255, 0.8);
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateX(-50%) translateY(0);
        }
        40% {
            transform: translateX(-50%) translateY(-10px);
        }
        60% {
            transform: translateX(-50%) translateY(-5px);
        }
    }
    
    /* Section divider */
    .section-divider {
        text-align: center;
        margin: 80px 0 40px 0;
        padding: 40px 20px;
        background: linear-gradient(180deg, rgba(10, 14, 23, 0), rgba(26, 31, 46, 0.5));
    }
    
    .section-title {
        font-size: 2.2em;
        color: #ffffff;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .section-subtitle {
        font-size: 1.1em;
        color: #8b96a8;
        margin-bottom: 40px;
    }
    
    /* Card styling with equal heights - targeting containers */
    [data-testid="column"] > div > div[data-testid="stVerticalBlock"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 35px 25px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        min-height: 400px;
    }
    
    [data-testid="column"] > div > div[data-testid="stVerticalBlock"]:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border-color: rgba(102, 126, 234, 0.5);
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="column"] h3 {
        font-size: 1.8em;
        color: #ffffff;
        margin-bottom: 20px;
        font-weight: 600;
    }
    
    [data-testid="column"] p {
        font-size: 1.05em;
        color: #b8c5d6;
        line-height: 1.6;
        margin-bottom: auto;
        padding-bottom: 25px;
    }
    
    /* Button styling - aligned at bottom */
    [data-testid="column"] div.stButton {
        margin-top: auto;
        padding-top: 10px;
    }
    
    div.stButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 12px 35px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 1.05em;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    div.stButton > button:hover {
        background: linear-gradient(90deg, #7b8fff, #8b5dc4);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        transform: translateY(-2px);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        margin-top: 80px;
        padding: 30px;
        color: #6b7688;
        font-size: 0.95em;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Make columns equal height */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
    }
    
    [data-testid="column"] > div {
        height: 100%;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    </style>
""", unsafe_allow_html=True)

# Welcome Section - Full screen hero
import base64
import os

# Function to convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Could not load image: {e}")
        return None

# Try to load the image
image_path = "prem image.png"
if os.path.exists(image_path):
    img_base64 = get_base64_image(image_path)
    if img_base64:
        st.markdown(f"""
            <div class='welcome-section'>
                <div class='welcome-image-container'>
                    <img src='data:image/png;base64,{img_base64}' alt='Premier League'>
                </div>
                <div class='hero-content'>
                    <h1 class='main-title'>⚽ Welcome to Scoresight</h1>
                    <p class='subtitle'>AI-Powered Football Analytics & Predictions</p>
                </div>
                <div class='scroll-indicator' onclick='window.scrollTo({{top: window.innerHeight, behavior: "smooth"}})'>
                    <span>⬇</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Failed to encode image")
else:
    st.error(f"Image file '{image_path}' not found in directory: {os.getcwd()}")
    st.info(f"Files in current directory: {os.listdir('.')}")

# Section Divider
st.markdown("<div class='section-divider'>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>Choose Your Prediction</h2>", unsafe_allow_html=True)
st.markdown("<p class='section-subtitle'>Select a prediction model to explore AI-driven football insights</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Two main feature cards with equal heights
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("### 🏆 Predict League Winner")
        st.write("Use AI models trained on past seasons to predict which team has the highest chance to win the league.")
        if st.button("Go to League Winner Predictor", key="league_btn"):
            st.session_state.page = "league"
            st.switch_page("pages/league_winner.py")

with col2:
    with st.container():
        st.markdown("### 🎯 Predict Top Assists")
        st.write("Estimate the top assist provider for the season using player stats and performance data.")
        if st.button("Go to Top Assist Predictor", key="assists_btn"):
            st.session_state.page = "assists"
            st.switch_page("pages/top_assists.py")

# Footer
st.markdown("<div class='footer'>© 2025 Scoresight | Built with Streamlit ⚡</div>", unsafe_allow_html=True)