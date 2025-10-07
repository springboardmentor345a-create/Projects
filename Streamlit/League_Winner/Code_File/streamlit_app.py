import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.exceptions import NotFittedError
import time 

# --- Setup ---
MODEL_NAME = 'logreg_league_winner'
BASE_DIR = Path(__file__).resolve().parent

# --- Global CSS Styling ---
st.markdown("""
    <style>
    /* 1. Page Configuration & Background */
    .stApp {
        background-color: #121212; /* Very dark gray/Black background */
        color: #ffffff; /* Default text color to white for contrast */
    }
    /* Ensure main header text is visible (Streamlit handles h1, h2 well, but this is a fallback) */
    h1, h2, h3, h4, .stMarkdown {
        color: #ffffff;
    }

    /* 2. Floating Particles */
    .particle-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -100;
    }
    .particle {
        position: absolute;
        background: rgba(255, 215, 0, 0.6); /* Gold color for visibility on dark background */
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.8); /* Gold shadow */
        border-radius: 50%;
        animation: float 20s infinite ease-in-out;
    }
    .particle:nth-child(1) { width: 5px; height: 5px; top: 10%; left: 5%; animation-duration: 15s; }
    .particle:nth-child(2) { width: 8px; height: 8px; top: 80%; left: 15%; animation-duration: 25s; }
    .particle:nth-child(3) { width: 4px; height: 4px; top: 30%; left: 25%; animation-duration: 10s; }
    .particle:nth-child(4) { width: 6px; height: 6px; top: 60%; left: 40%; animation-duration: 30s; }
    .particle:nth-child(5) { width: 7px; height: 7px; top: 20%; left: 70%; animation-duration: 18s; }
    .particle:nth-child(6) { width: 5px; height: 5px; top: 90%; left: 85%; animation-duration: 22s; }
    .particle:nth-child(7) { width: 9px; height: 9px; top: 50%; left: 95%; animation-duration: 12s; }
    .particle:nth-child(8) { width: 4px; height: 4px; top: 40%; left: 55%; animation-duration: 28s; }
    .particle:nth-child(9) { width: 6px; height: 6px; top: 75%; left: 30%; animation-duration: 17s; }
    .particle:nth-child(10) { width: 8px; height: 8px; top: 25%; left: 85%; animation-duration: 26s; }

    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-30px) rotate(180deg); opacity: 0.3; }
        100% { transform: translateY(0px) rotate(360deg); }
    }
    
    /* 3. Card Styling for Metrics - Adjusted for dark background */
    div[data-testid="stMetric"] {
        background-color: #1e1e1e; /* Slightly lighter dark gray for metric cards */
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); /* Stronger shadow on dark background */
        border: 1px solid #333333;
        transition: transform 0.3s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }
    
    /* 4. Custom Submit Button Style */
    button[kind="primary"] {
        background-color: #FFD700; /* Gold button for premium look */
        color: #000000;
        border: none;
        transition: background-color 0.3s ease;
    }
    button[kind="primary"]:hover {
        background-color: #CCAA00;
    }
    /* Adjust input backgrounds for visibility */
    .stSelectbox, .stNumberInput, .stForm {
        color: #ffffff;
        background-color: #252525;
    }

    </style>
    <!-- HTML to generate particles -->
    <div class="particle-container">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    """, unsafe_allow_html=True)


# --- Artifact Loading Function (Initial Load Animation) ---
@st.cache_resource
def load_artifacts():
    """Loads all necessary model and preprocessing artifacts."""
    
    # 1. Simulate RGB Loading Effect (Fast)
    load_placeholder = st.empty()
    colors = ["#FF0000", "#FFA500", "#FFFF00", "#00FF00", "#00BFFF", "#0000FF", "#8A2BE2"] # Rainbow colors
    
    with load_placeholder.container():
        # Display the thinking state with the ❓ emoji and colored text
        st.markdown("### ❓ Initializing Prediction Engine... ❓")
        progress_bar = st.progress(0)
        
        # Fast simulation of RGB progress
        for i in range(1, 101, 10):
            color_index = int(i / 10) % len(colors)
            progress_bar.progress(i / 100)
            # Use HTML to apply RGB fading effect to text
            progress_bar.markdown(f"### <span style='color: {colors[color_index]};'>Loading Artifacts... {i}%</span>", unsafe_allow_html=True)
            time.sleep(0.01) # Very fast simulation
            
        # Final success visual
        progress_bar.empty()
        load_placeholder.empty()
        
    # 2. Perform actual loading
    try:
        model = joblib.load(BASE_DIR / f'{MODEL_NAME}_model.pkl')
        scaler = joblib.load(BASE_DIR / f'{MODEL_NAME}_scaler.pkl')
        le = joblib.load(BASE_DIR / f'{MODEL_NAME}_le.pkl')
        feature_cols = joblib.load(BASE_DIR / f'{MODEL_NAME}_feature_cols.pkl')
        final_accuracy = joblib.load(BASE_DIR / f'{MODEL_NAME}_accuracy.pkl')
        
        # Load data to get unique teams for dropdowns
        try:
            df_teams = pd.read_csv(BASE_DIR / 'pl-tables.csv', usecols=['team'])
            unique_teams = sorted(df_teams['team'].unique())
        except FileNotFoundError:
            unique_teams = ["Manchester City", "Arsenal", "Liverpool", "Chelsea", "Tottenham"] # Fallback

        
        return model, scaler, le, feature_cols, final_accuracy, unique_teams
    except Exception as e:
        st.error(f"Error loading model artifacts. Please ensure you have successfully run 'python save_artifacts.py' first.")
        st.code(f"Details: {e}")
        return None, None, None, None, None, None

model, scaler, le, feature_cols, final_accuracy, unique_teams = load_artifacts()

if model is None:
    st.stop()

# --- Prediction Function (Unchanged) ---
def make_prediction(input_data):
    """Processes input data and returns the probability of winning."""
    
    # 1. Convert input dictionary to DataFrame and select only the 8 features
    input_df = pd.DataFrame([input_data])
    input_df = input_df[feature_cols]

    # 2. Align Columns (Ensure order matches training)
    final_input = input_df[feature_cols]

    # 3. Scale Numerical Features
    try:
        final_input_scaled = scaler.transform(final_input)
    except NotFittedError:
        raise Exception("Scaler is not fitted. Artifacts may be corrupted.")

    # 4. Predict probability (Logistic Regression predicts P(class 1) which is Winner)
    proba = model.predict_proba(final_input_scaled)[0]
    
    # The 'Winner' class (1) index is 1 in the LabelEncoder classes [0, 1]
    # Check if '1' (Winner) is in the classes. If not, default to 0.
    if 1 in le.classes_:
        winner_proba = proba[le.classes_ == 1][0]
    else:
        # Should not happen if training was correct, but handles edge case
        winner_proba = 0.0 
    
    return winner_proba

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="ScoreSight: League Winner Predictor", layout="wide")
st.title("🏆 ScoreSight: EPL League Winner Prediction")
st.subheader("Predicting League Winner Status based on Final Season Statistics")
st.markdown("---")

# --- MAIN PAGE: Input Form ---
st.markdown("### 📊 Team Performance Input")
st.markdown("*(Enter the team's final seasonal metrics to predict its likelihood of finishing 1st.)*")

with st.container():
    # Team Selection for context
    team_context = st.selectbox("Select Team (For Context)", unique_teams, index=0)

with st.form("league_prediction_form"):
    
    # --- Input Grid for the 8 Features ---
    st.subheader("Match Statistics")
    
    # Grid 1: Played, Won, Drawn, Lost
    col_p, col_w, col_d, col_l = st.columns(4)
    with col_p:
        played = st.number_input("Matches Played", min_value=1, max_value=38, value=38, step=1)
    with col_w:
        won = st.number_input("Matches Won", min_value=0, max_value=38, value=28, step=1)
    with col_d:
        drawn = st.number_input("Matches Drawn", min_value=0, max_value=38, value=5, step=1)
    with col_l:
        lost = st.number_input("Matches Lost", min_value=0, max_value=38, value=5, step=1)

    # Grid 2: GF, GA, GD, Points
    col_gf, col_ga, col_gd, col_points = st.columns(4)
    with col_gf:
        gf = st.number_input("Goals For (GF)", min_value=0, value=91, step=5)
    with col_ga:
        ga = st.number_input("Goals Against (GA)", min_value=0, value=29, step=5)
    with col_gd:
        # Note: GD is auto-calculated but user input is required for model consistency
        gd_val = gf - ga
        gd = st.number_input("Goal Difference (GD)", value=gd_val, help=f"Expected: {gd_val}") 
    with col_points:
        calculated_points = (won * 3) + drawn
        points = st.number_input(f"Points (Won*3 + Drawn)", min_value=0, value=calculated_points, step=1, help=f"Expected Points: {calculated_points}")

    st.markdown("---")
    submitted = st.form_submit_button(f"🚀 Predict {team_context}'s Winner Chance", type="primary")

# --- Results Display ---
if submitted:
    # --- Input Validation ---
    if played != won + drawn + lost:
        st.error("🛑 Input Error: Matches Played must equal the sum of Won, Drawn, and Lost matches.")
    elif points != (won * 3) + drawn:
        st.error("🛑 Input Error: Points must be equal to (Won * 3) + Drawn.")
    else:
        input_data = {
            'played': played, 'won': won, 'drawn': drawn, 'lost': lost,
            'gf': gf, 'ga': ga, 'gd': gd, 'points': points
        }
        
        with st.spinner(f'Calculating prediction for {team_context}...'):
            try:
                winner_proba = make_prediction(input_data)
                proba_pct = winner_proba * 100
                
                st.markdown("## Prediction Outcome")
                
                # --- Result Card ---
                if proba_pct > 90:
                    st.success(f"### {team_context} is predicted to be the League Winner! 🏆")
                elif proba_pct > 50:
                    st.info(f"### {team_context} has a **{proba_pct:.0f}%** chance of winning the league.")
                else:
                    st.warning(f"### {team_context} is unlikely to win the league.")

                # --- Visual Metrics ---
                col_met1, col_met2 = st.columns([1, 2])
                with col_met1:
                    st.metric(label=f"Probability of Finishing 1st", 
                              value=f"{proba_pct:.2f}%",
                              delta="High Confidence" if proba_pct > 80 else None)
                with col_met2:
                    st.progress(winner_proba, text="Prediction Confidence")
                
                st.caption(f"Model Accuracy (from notebook): {final_accuracy*100:.2f}%. This high score is consistent with using final-season metrics.")
                
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
                st.write("Please check the input values and ensure all model artifacts are correctly loaded.")
