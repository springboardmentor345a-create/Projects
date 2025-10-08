import streamlit as st
import pandas as pd
import joblib

# --------------------------
# Custom CSS Styling
# --------------------------
st.markdown("""
<style>
    /* (Removed selectbox width override) */
/* Hide Streamlit's custom number input steppers */
div[data-baseweb="input"] button {
    display: none !important;
}
/* Hide native browser steppers */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none !important;
    margin: 0 !important;
    display: none !important;
}
input[type=number] {
    -moz-appearance: textfield !important;
}
<style>
    /* Main background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Sidebar - Hide it */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1F2F33 !important;
        font-weight: 700 !important;
    }
    
    /* Input labels */
    label {
        color: #1F2F33 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* CRITICAL: Hide +/- buttons on number inputs */
    input[type=number]::-webkit-inner-spin-button,
    input[type=number]::-webkit-outer-spin-button {
        -webkit-appearance: none !important;
        margin: 0 !important;
        display: none !important;
    }
    
    input[type=number] {
        -moz-appearance: textfield !important;
    }
    
    /* Remove the step buttons container */
    div[data-baseweb="input"] button {
        display: none !important;
    }
    
    /* Input fields styling: thin colored border, higher box-shadow */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background-color: white;
        border: 1.2px solid #4A90E2 !important;
        color: #1F2F33;
        border-radius: 8px;
        padding: 10px 12px;
        box-shadow: 0 4px 18px rgba(31,47,51,0.18);
        transition: box-shadow 0.2s;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1F2F33;
        color: #F8FAFC;
        border: none;
        border-radius: 10px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #2d4449;
        box-shadow: 0 6px 20px rgba(31, 47, 51, 0.3);
        transform: translateY(-3px);
    }
    
    /* Top bar for heading */
    .top-bar {
        width: 100vw;
        position: fixed;
        left: 0;
        top: 0;
            margin-top: 40px;
        z-index: 1000;
        background: linear-gradient(90deg, #1F2F33 0%, #2d4449 100%);
        color: #F8FAFC;
        padding: 24px 0 24px 0;
        marginTop: -24px;
        text-align: center;
        box-shadow: 0 2px 16px rgba(31, 47, 51, 0.12);
    }
    /* Remove Streamlit's default padding at the top */
    .main .block-container {
           padding-top: 130px !important;
    }
    .top-bar-title {
        color: #F8FAFC !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        letter-spacing: 1px;
        display: inline-block;
        vertical-align: middle;
    }
    .top-bar-icon {
        font-size: 2.5rem;
        margin-right: 16px;
        vertical-align: middle;
    }
    
    /* Feature cards jointed style */
    .feature-card {
        background-color: white;
        padding: 30px 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(31, 47, 51, 0.1);
        margin: 20px 0;
        border: 3px solid transparent;
        transition: all 0.4s ease;
        height: 100%;
    }
    .feature-card:hover {
        border-color: #1F2F33;
        box-shadow: 0 8px 30px rgba(31, 47, 51, 0.2);
        transform: translateY(-8px);
    }
    
    .feature-icon {
        font-size: 48px;
        margin-bottom: 15px;
    }
    
    .feature-title {
        color: #1F2F33;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    
    .feature-description {
        color: #1F2F33;
        font-size: 15px;
        line-height: 1.6;
        opacity: 0.8;
    }
    
    /* Input sections */
    .input-section {
        background-color: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(31, 47, 51, 0.08);
        margin: 25px 0;
    }
    
    .section-title {
        color: #1F2F33;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #F8FAFC;
    }
    
    /* Back button */
    .back-button {
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Page configuration
# --------------------------
st.set_page_config(page_title="EPL Predictor Hub", layout="centered", page_icon="⚽")

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# --------------------------
# Load models
# --------------------------
def load_models():
    if 'models_loaded' not in st.session_state:
        st.session_state.assists_pipeline = joblib.load("EPL Frontend/topassists_pipeline.pkl")
        st.session_state.league_model = joblib.load("EPL Frontend/league_winner_model.pkl")
        st.session_state.models_loaded = True

# --------------------------
# LANDING PAGE
# --------------------------
if st.session_state.page == 'landing':
    
    # Top Bar Heading
    st.markdown("""
    <div class='top-bar'>
        <span class='top-bar-icon'>⚽</span><span class='top-bar-title'>EPL PREDICTOR HUB</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("<h2 style='text-align: center; margin: 50px 0 35px 0; font-size: 36px;'>Choose Your Prediction Model</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container():
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>🏆</div>
                <div class='feature-title'>League Winner Predictor</div>
                <div class='feature-description'>
                    Analyze team performance metrics including wins, goals, and points to predict 
                    championship probability. Our model evaluates season-long statistics to determine 
                    which teams have what it takes to lift the trophy.
                </div>
            """, unsafe_allow_html=True)
            # Button inside the card visually
            btn1 = st.button("🚀 Launch League Winner Predictor", key="league_btn")
            st.markdown("</div>", unsafe_allow_html=True)
            if btn1:
                st.session_state.page = 'league_winner'
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>🎯</div>
                <div class='feature-title'>Player Assists Predictor</div>
                <div class='feature-description'>
                    Forecast individual player assist totals based on comprehensive statistics including 
                    key passes, expected assists (xA), and team dynamics. Perfect for fantasy football 
                    managers and performance analysts.
                </div>
            """, unsafe_allow_html=True)
            # Button inside the card visually
            btn2 = st.button("🚀 Launch Assists Predictor", key="assists_btn")
            st.markdown("</div>", unsafe_allow_html=True)
            if btn2:
                st.session_state.page = 'top_assists'
                st.rerun()
    
    # Why Choose Us Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin: 40px 0 30px 0;'>Why Use Our Platform?</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 40px; margin-bottom: 10px;'>📊</div>
            <div style='font-weight: 600; color: #1F2F33; margin-bottom: 8px;'>Data-Driven</div>
            <div style='color: #1F2F33; opacity: 0.8; font-size: 14px;'>Powered by advanced ML algorithms</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 40px; margin-bottom: 10px;'>⚡</div>
            <div style='font-weight: 600; color: #1F2F33; margin-bottom: 8px;'>Instant Results</div>
            <div style='color: #1F2F33; opacity: 0.8; font-size: 14px;'>Get predictions in seconds</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 40px; margin-bottom: 10px;'>🎯</div>
            <div style='font-weight: 600; color: #1F2F33; margin-bottom: 8px;'>Accurate</div>
            <div style='color: #1F2F33; opacity: 0.8; font-size: 14px;'>Trained on historical EPL data</div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------
# LEAGUE WINNER PAGE
# --------------------------
elif st.session_state.page == 'league_winner':
    load_models()
    
    # Back to Home button (left, no background, triggers Python)
    # Back to Home button at the absolute leftmost corner
    st.markdown("""
    <div style='width:100%;display:flex;justify-content:flex-start;margin-bottom:0;'>
    <div style='margin:0;padding:0;'>
    """, unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_league", help="Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    st.markdown("""
    </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; margin: 0 0 10px 0;'>🏆 League Winner Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1F2F33; font-size: 17px; margin-bottom: 18px;'>Enter team statistics to predict championship probability</p>", unsafe_allow_html=True)

    # Inputs in a single div, plain text inputs with validation
    st.markdown("""
    <div style='background:#fff;padding:30px 30px 10px 30px;border-radius:12px;box-shadow:0 2px 10px rgba(31,47,51,0.08);margin-bottom:20px;'>
        <div style='font-size:18px;font-weight:600;margin-bottom:18px;color:#1F2F33;'>Team Performance Metrics</div>
    """, unsafe_allow_html=True)
    input_cols = st.columns(4)
    with input_cols[0]:
        played = st.text_input("Matches Played", "38")
    with input_cols[1]:
        won = st.text_input("Wins", "25")
    with input_cols[2]:
        drawn = st.text_input("Draws", "8")
    with input_cols[3]:
        lost = st.text_input("Losses", "5")
    input_cols2 = st.columns(4)
    with input_cols2[0]:
        gf = st.text_input("Goals For", "80")
    with input_cols2[1]:
        ga = st.text_input("Goals Against", "30")
    with input_cols2[2]:
        gd = st.text_input("Goal Difference", "50")
    with input_cols2[3]:
        points = st.text_input("Points", "90")
    st.markdown("</div>", unsafe_allow_html=True)

    # Predict button with validation
    if st.button("🔮 Predict Championship Probability", key="predict_league"):
        # Validate all inputs are integers
        try:
            played_i = int(played)
            won_i = int(won)
            drawn_i = int(drawn)
            lost_i = int(lost)
            gf_i = int(gf)
            ga_i = int(ga)
            gd_i = int(gd)
            points_i = int(points)
        except ValueError:
            st.error("Please enter valid numbers for all fields.")
            st.stop()
        input_data = pd.DataFrame({
            "played": [played_i],
            "won": [won_i],
            "drawn": [drawn_i],
            "lost": [lost_i],
            "gf": [gf_i],
            "ga": [ga_i],
            "gd": [gd_i],
            "points": [points_i]
        })
        prediction = st.session_state.league_model.predict(input_data)[0]
        proba = st.session_state.league_model.predict_proba(input_data)[0][1] * 100

        # Output box with light background and improved message
        if prediction == 1:
            msg = f"<b>This team has strong chances to win the league!</b><br>Probability: <span style='font-size:2rem;color:#1F2F33;font-weight:700'>{proba:.1f}%</span>"
            bg = "#e6f7ec"
            icon = "🏆"
        elif proba > 30:
            msg = f"<b>This team has some chances of winning the league.</b><br>Probability: <span style='font-size:2rem;color:#1F2F33;font-weight:700'>{proba:.1f}%</span>"
            bg = "#fffbe6"
            icon = "⚽"
        else:
            msg = f"<b>This team has no realistic chance of winning the league.</b><br>Probability: <span style='font-size:2rem;color:#1F2F33;font-weight:700'>{proba:.1f}%</span>"
            bg = "#ffeaea"
            icon = "❌"
        st.markdown(f"""
        <div style='background:{bg};padding:32px 24px 24px 24px;border-radius:14px;margin-top:28px;text-align:center;box-shadow:0 2px 10px rgba(31,47,51,0.08);'>
            <div style='font-size:54px;margin-bottom:10px;'>{icon}</div>
            <div style='font-size:20px;color:#1F2F33;margin-bottom:8px;'>{msg}</div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------
# TOP ASSISTS PAGE
# --------------------------
elif st.session_state.page == 'top_assists':
    load_models()
    
    # Back to Home button at the absolute leftmost corner (fixed position)
    st.markdown("""
    <div style='position:fixed;left:0;top:0;z-index:2000;margin:0;padding:0;width:100vw;'>
        <div style='display:flex;justify-content:flex-start;'>
            <div style='margin-left:-18px;'>
    """, unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_assists", help="Back to Home"):
        st.session_state.page = 'landing'
        st.rerun()
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; margin: 10px 0 10px 0;'>🎯 Player Assists Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1F2F33; font-size: 17px; margin-bottom: 18px;'>Enter player statistics to forecast season assists</p>", unsafe_allow_html=True)

    positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
    set_piece_options = ["Yes", "No"]
    big6_options = ["Yes", "No"]

    # Player Information and Stats in a single styled div
    st.markdown("""
    <div style='background:#fff;padding:18px 24px 6px 24px;border-radius:12px;box-shadow:0 2px 10px rgba(31,47,51,0.08);margin-bottom:16px;min-height:40px;'>
        <div style='font-size:17px;font-weight:600;margin-bottom:10px;color:#1F2F33;'>Player & Team Information</div>
    """, unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        Age = st.text_input("Age", "25")
        Position = st.selectbox("Position", positions)
        Minutes_Played = st.text_input("Minutes Played", "2000")
    with col2:
        
        Set_Piece_Involvement = st.selectbox("Set Piece Taker?", set_piece_options)
        Assists_prev_season = st.text_input("Previous Season Assists", "5")
        Goals_prev_season = st.text_input("Previous Season Goals", "3")
    with col3:
        Key_Passes = st.text_input("Key Passes", "50")
        Expected_Assists_xA = st.text_input("Expected Assists (xA)", "5.0")
        Dribbles_Completed = st.text_input("Dribbles Completed", "40")
        
    with col4:
        Shots_Assisted = st.text_input("Shots Assisted", "20")
        Big6_Club_Feature = st.selectbox("Big 6 Club?", big6_options)
        Club_Attack_Share = st.text_input("Player's Attack Share", "0.5")
        Club_xG = st.text_input("Club Expected Goals (xG)", "50.0")
    st.markdown("</div>", unsafe_allow_html=True)

    # Predict button with validation
    st.markdown("<div style='margin-top:-18px'></div>", unsafe_allow_html=True)
    if st.button("🔮 Predict Season Assists", key="predict_assists"):
        # Validate all numeric inputs
        try:
            Age_i = int(Age)
            Minutes_Played_i = int(Minutes_Played)
            Assists_prev_season_i = int(Assists_prev_season)
            Goals_prev_season_i = int(Goals_prev_season)
            Key_Passes_i = int(Key_Passes)
            Expected_Assists_xA_f = float(Expected_Assists_xA)
            Dribbles_Completed_i = int(Dribbles_Completed)
            Shots_Assisted_i = int(Shots_Assisted)
            Club_Attack_Share_f = float(Club_Attack_Share)
            Club_xG_f = float(Club_xG)
        except ValueError:
            st.error("Please enter valid numbers for all fields.")
            st.stop()
        input_df = pd.DataFrame({
            "Age": [Age_i],
            "Position": [Position],
            "Minutes_Played": [Minutes_Played_i],
            "Assists_prev_season": [Assists_prev_season_i],
            "Goals_prev_season": [Goals_prev_season_i],
            "Key_Passes": [Key_Passes_i],
            "Expected_Assists_(xA)": [Expected_Assists_xA_f],
            "Dribbles_Completed": [Dribbles_Completed_i],
            "Shots_Assisted": [Shots_Assisted_i],
            "Set_Piece_Involvement": [Set_Piece_Involvement],
            "Big6_Club_Feature": [Big6_Club_Feature],
            "Club_Attack_Share": [Club_Attack_Share_f],
            "Club_xG": [Club_xG_f]
        })

        for col in [ "Position", "Set_Piece_Involvement", "Big6_Club_Feature"]:
            input_df[col] = input_df[col].astype(str)

        input_df["Goals_per_90"] = input_df["Goals_prev_season"] / (input_df["Minutes_Played"]/90)
        input_df["Dribbles_per_90"] = input_df["Dribbles_Completed"] / (input_df["Minutes_Played"]/90)
        input_df["Shots_Assisted_per_90"] = input_df["Shots_Assisted"] / (input_df["Minutes_Played"]/90)
        input_df["Assists_prev_per_90"] = input_df["Assists_prev_season"] / (input_df["Minutes_Played"]/90)
        input_df["Key_Passes_per_90"] = input_df["Key_Passes"] / (input_df["Minutes_Played"]/90)
        input_df["Goals_prev_per_90"] = input_df["Goals_prev_season"] / (input_df["Minutes_Played"]/90)
        input_df["Minutes_Attack"] = input_df["Minutes_Played"] * input_df["Club_Attack_Share"]

        prediction = st.session_state.assists_pipeline.predict(input_df)[0]
        prediction_int = round(prediction)

        # Output box with light background and improved message
        if prediction_int >= 15:
            msg = f"<b>This player is highly likely to be a top assist provider!</b><br>Predicted Assists: <span style='font-size:2rem;color:#1F2F33;font-weight:700'>{prediction_int}</span>"
            bg = "#e6f7ec"
            icon = "🎯"
        elif prediction_int >= 7:
            msg = f"<b>This player has a fair chance of being among the top assist providers.</b><br>Predicted Assists: <span style='font-size:2rem;color:#1F2F33;font-weight:700'>{prediction_int}</span>"
            bg = "#fffbe6"
            icon = "⚽"
        else:
            msg = f"<b>This player is unlikely to be a top assist provider.</b><br>Predicted Assists: <span style='font-size:2rem;color:#1F2F33;font-weight:700'>{prediction_int}</span>"
            bg = "#ffeaea"
            icon = "❌"
        st.markdown(f"""
        <div style='background:{bg};padding:32px 24px 24px 24px;border-radius:14px;margin-top:28px;text-align:center;box-shadow:0 2px 10px rgba(31,47,51,0.08);'>
            <div style='font-size:54px;margin-bottom:10px;'>{icon}</div>
            <div style='font-size:20px;color:#1F2F33;margin-bottom:8px;'>{msg}</div>
        </div>
        """, unsafe_allow_html=True)