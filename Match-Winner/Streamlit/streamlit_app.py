import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# Set base directory for artifact loading
BASE_DIR = Path(__file__).resolve().parent

# --- Artifact Loading Function ---
@st.cache_resource
def load_artifacts():
    """Loads all necessary model and preprocessing artifacts."""
    try:
        model = joblib.load(BASE_DIR / 'logreg_tuned_model.pkl')
        scaler = joblib.load(BASE_DIR / 'scaler.pkl')
        le = joblib.load(BASE_DIR / 'label_encoder.pkl')
        feature_cols = joblib.load(BASE_DIR / 'feature_columns.pkl')
        num_cols = joblib.load(BASE_DIR / 'numeric_columns.pkl')
        
        # Load data to get unique teams for dropdowns
        df_teams = pd.read_csv(BASE_DIR / 'Match Winner.csv', usecols=['HomeTeam', 'AwayTeam'])
        unique_teams = sorted(pd.concat([df_teams['HomeTeam'], df_teams['AwayTeam']]).unique())
        
        return model, scaler, le, feature_cols, num_cols, unique_teams
    except Exception as e:
        st.error(f"Error loading model artifacts. Please ensure you have successfully run 'python save_artifacts.py' first.")
        st.code(f"Details: {e}")
        return None, None, None, None, None, None

model, scaler, le, feature_cols, num_cols, unique_teams = load_artifacts()

if model is None:
    st.stop()

# --- Prediction Function ---
def make_prediction(input_data):
    """Processes input data and returns the prediction and probabilities."""
    # 1. Convert input dictionary to DataFrame
    input_df = pd.DataFrame([input_data])

    # 2. Re-create engineered features (Matching notebook logic)
    input_df['HalfTimeGoalDiff'] = input_df['HalfTimeHomeGoals'] - input_df['HalfTimeAwayGoals']
    
    # Determine HalfTimeState (Matching notebook logic)
    if input_df['HalfTimeHomeGoals'].iloc[0] > input_df['HalfTimeAwayGoals'].iloc[0]:
        ht_state = 'HomeLead'
    elif input_df['HalfTimeHomeGoals'].iloc[0] < input_df['HalfTimeAwayGoals'].iloc[0]:
        ht_state = 'AwayLead'
    else:
        ht_state = 'Level'
    input_df['HalfTimeState'] = ht_state

    # 3. One-Hot Encode Categorical Features
    cat_cols_ohe = ['HomeTeam', 'AwayTeam', 'HalfTimeResult', 'HalfTimeState']
    input_df_encoded = pd.get_dummies(input_df, columns=cat_cols_ohe, drop_first=True)
    
    # 4. Align and Validate Columns (CRITICAL STEP for OHE consistency)
    final_input = pd.DataFrame(0, index=[0], columns=feature_cols)
    
    # Fill in the values from the current input
    for col in input_df_encoded.columns:
        if col in final_input.columns:
            final_input[col] = input_df_encoded[col].iloc[0]

    # 5. Scale Numerical Features
    final_input[num_cols] = scaler.transform(final_input[num_cols])

    # 6. Predict
    prediction_encoded = model.predict(final_input)
    prediction_proba = model.predict_proba(final_input)[0]
    
    # 7. Decode result
    predicted_class = le.inverse_transform(prediction_encoded)[0]
    
    # Map probabilities to classes
    proba_df = pd.DataFrame({
        'Result': le.classes_, 
        'Probability': prediction_proba
    }).sort_values('Probability', ascending=False).reset_index(drop=True)
    
    return predicted_class, proba_df

# --- Streamlit UI ---
st.set_page_config(page_title="ScoreSight: Match Winner Predictor", layout="wide")
st.title("⚽ ScoreSight: EPL Match Winner Predictor")
st.markdown(f"***Model Used: LogReg (Tuned)*** | *Accuracy: ~0.6359*")
st.markdown("---")

# --- User Input Form ---
with st.form("match_prediction_form"):
    st.header("Match Details")
    
    col1, col2 = st.columns(2)
    with col1:
        home_team = st.selectbox("🏡 Home Team", unique_teams, index=unique_teams.index('Arsenal') if 'Arsenal' in unique_teams else 0)
    with col2:
        away_team = st.selectbox("✈️ Away Team", unique_teams, index=unique_teams.index('Man City') if 'Man City' in unique_teams else 0)

    st.subheader("Half-Time Goals")
    
    col3, col4, col5 = st.columns(3)
    with col3:
        ht_h_goals = st.number_input("Home Goals (HT)", min_value=0, max_value=5, value=1, step=1)
    with col4:
        ht_a_goals = st.number_input("Away Goals (HT)", min_value=0, max_value=5, value=0, step=1)
    
    # Calculate HT Result automatically for display and use
    ht_result_val = 'H' if ht_h_goals > ht_a_goals else ('A' if ht_h_goals < ht_a_goals else 'D')
    with col5:
        st.info(f"**HT Result:** {ht_result_val}")

    st.header("Full-Match Statistics (Current)")
    st.markdown("*(Enter match stats up to the time you want the prediction)*")
    
    # --- Performance Metrics ---
    st.subheader("Shots & Corners")
    col_s_1, col_s_2, col_s_3, col_s_4 = st.columns(4)
    with col_s_1:
        h_shots = st.number_input("Home Shots", min_value=0, value=15, step=1)
    with col_s_2:
        a_shots = st.number_input("Away Shots", min_value=0, value=10, step=1)
    with col_s_3:
        h_sot = st.number_input("Home Shots On Target", min_value=0, value=7, step=1)
    with col_s_4:
        a_sot = st.number_input("Away Shots On Target", min_value=0, value=4, step=1)
        
    col_c_1, col_c_2 = st.columns(2)
    with col_c_1:
        h_corners = st.number_input("Home Corners", min_value=0, value=6, step=1)
    with col_c_2:
        a_corners = st.number_input("Away Corners", min_value=0, value=5, step=1)


    st.subheader("Discipline")
    col_d_1, col_d_2, col_d_3, col_d_4 = st.columns(4)
    with col_d_1:
        h_fouls = st.number_input("Home Fouls", min_value=0, value=10, step=1)
    with col_d_2:
        a_fouls = st.number_input("Away Fouls", min_value=0, value=12, step=1)
    with col_d_3:
        h_y_cards = st.number_input("Home Yellow Cards", min_value=0, max_value=6, value=1, step=1)
    with col_d_4:
        a_y_cards = st.number_input("Away Yellow Cards", min_value=0, max_value=6, value=2, step=1)

    col_r_1, col_r_2 = st.columns(2)
    with col_r_1:
        h_r_cards = st.number_input("Home Red Cards", min_value=0, max_value=3, value=0, step=1)
    with col_r_2:
        a_r_cards = st.number_input("Away Red Cards", min_value=0, max_value=3, value=0, step=1)

    # Prediction button
    submitted = st.form_submit_button("Predict Full-Time Winner", type="primary")

# --- Results Display ---
if submitted:
    if home_team == away_team:
        st.error("The Home Team and Away Team cannot be the same. Please adjust your selections.")
    else:
        input_data = {
            'HomeTeam': home_team, 
            'AwayTeam': away_team,
            'HalfTimeHomeGoals': ht_h_goals,
            'HalfTimeAwayGoals': ht_a_goals,
            'HalfTimeResult': ht_result_val, 
            'HomeShots': h_shots,
            'AwayShots': a_shots,
            'HomeShotsOnTarget': h_sot,
            'AwayShotsOnTarget': a_sot,
            'HomeCorners': h_corners,
            'AwayCorners': a_corners,
            'HomeFouls': h_fouls,
            'AwayFouls': a_fouls,
            'HomeYellowCards': h_y_cards,
            'AwayYellowCards': a_y_cards,
            'HomeRedCards': h_r_cards,
            'AwayRedCards': a_r_cards
        }
        
        with st.spinner('Calculating prediction using LogReg (Tuned)...'):
            try:
                predicted_class, proba_df = make_prediction(input_data)
                
                # Custom result mapping for display
                result_map = {
                    'H': "Home Win 🏡",
                    'D': "Draw 🤝",
                    'A': "Away Win ✈️"
                }

                # Display Main Result
                st.subheader("Prediction Result")
                st.balloons()
                st.success(f"The most likely full-time result is: **{result_map.get(predicted_class, predicted_class)}**")
                
                # Display Probabilities
                st.markdown("---")
                st.subheader("Confidence Breakdown (Probabilities)")
                
                prob_cols = st.columns(3)
                for i, row in proba_df.iterrows():
                    result_name = result_map.get(row['Result'])
                    probability = row['Probability'] * 100
                    
                    with prob_cols[i]:
                        st.metric(label=result_name, value=f"{probability:.2f}%")
                        
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
                st.write("Please check the input values and ensuring all artifacts are correctly loaded.")
