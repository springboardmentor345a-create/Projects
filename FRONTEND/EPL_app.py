import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os 
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier    

teams = [
    "Arsenal", "Aston Villa","Bournemouth","Brentford", "Brighton", "Burnley","Chelsea","Crystal Palace","Everton","Fulham","Leeds","Liverpool","Luton", "Man City", "Man United","Newcastle","Nott'm For","Sunderland","Tottenham","West Ham","Wolves"
]

goal_model = joblib.load("Top_Goal_Scorer/linear_regression_model.pkl")
league_model = joblib.load("League Winner/league_model.pkl")
st.title("Infosys Springboard Internship Project")

col1, col2 = st.columns(2)

with col1:
    if st.button("⚽ Top Goal Scorer", use_container_width=True):
        st.session_state['option'] = "Top Goal Scorer"
with col2:
    if st.button("🥇 League Winner", use_container_width=True):
        st.session_state['option'] = "League Winner"

if 'option' not in st.session_state:
    st.session_state['option'] = "Top Goal Scorer" 

st.markdown("---") 

if st.session_state.get('option') == "Top Goal Scorer":
    st.header("Top Goal Scorer Prediction")
    st.markdown("Enter player statistics to predict the total goals scored in the season.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        Age = st.number_input("Age", min_value=16, max_value=45, value=25)
        Appearances = st.number_input("Appearances", min_value=0, max_value=38, value=20)
        Goals_prev_season = st.number_input("Goals in Previous Season", min_value=0, value=5)
    with col_b:
        Goals_per_90 = st.number_input("Goals per 90 mins", min_value=0.0, format="%.2f", value=0.45)
        Big_6_Club_Feature = st.number_input("Big 6 Club Feature (0=No, 1=Yes)", min_value=0, max_value=1, value=0)
        League_Goals_per_Match = st.number_input("League Goals per Match", min_value=0.0, format="%.2f", value=2.80)

    positions = ["Attacking Midfielder", "Forward", "Midfielder", "Winger"]
    position_selected = st.selectbox("Select Position", positions)
    position_encoded = [0, 0, 0, 0]
    if position_selected == "Attacking Midfielder":
        position_encoded[0] = 1
    elif position_selected == "Forward":
        position_encoded[1] = 1
    elif position_selected == "Midfielder":
        position_encoded[2] = 1
    elif position_selected == "Winger":
        position_encoded[3] = 1

    st.markdown("---")
    
    if st.button("Predict Goals", type="primary", use_container_width=True):
        input_data = np.array([[Age, Appearances, Goals_prev_season,Goals_per_90,
                                Big_6_Club_Feature, League_Goals_per_Match,
                                *position_encoded]])
        prediction = goal_model.predict(input_data)
        
        st.markdown(
            f"""
            <div style="background-color:#007bff; padding:10px; border-radius:5px; text-align:center; margin-top:15px;">
                <h3 style="color:white; margin:0;">Predicted Goals: <span style="font-size:1.5em; font-weight:bold;">{int(round(prediction[0]))}</span></h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
    sample_data = {
        "Age": [23, 22, 23, 24],
        "Appearances": [31, 33, 35, 37],
        "Goals_per_90": [0.85, 0.61, 0.54, 0.41],
        "Goals_prev_season": [36, 3, 11, 7],
        "Big_6_Club_Feature": [1, 1, 1, 1],
        "League_Goals_per_Match": [2.83, 2.83, 2.83, 2.85],
        "Position": ["Forward", "Attacking Midfielder", "Winger", "Midfielder"],
    }
    sample_df = pd.DataFrame(sample_data, index=["1", "2", "3", "4"])
    st.dataframe(sample_df)
else: 
    st.header("League Winner Prediction")
    st.markdown("Enter season-end team statistics to predict the probability of winning the league.")

    col_stats_1, col_stats_2 = st.columns(2)

    with col_stats_1:
        Matches_played = st.number_input("Matches Played", min_value=0, value=40)
        won = st.number_input("Wins", min_value=0, value=27)
        drawn = st.number_input("Draws", min_value=0, value=8)
        lost = st.number_input("Losses", min_value=0, value=5)

    with col_stats_2:
        gf = st.number_input("Goals For (GF)", min_value=0, value=80)
        ga = st.number_input("Goals Against (GA)", min_value=0, value=30)
        gd = st.number_input("Goal Difference (GD)", value=50)
        points = st.number_input("Points", min_value=0, value=89)

    st.markdown("---")

    if st.button("Calculate League Probability", type="primary", use_container_width=True):
        new_data = pd.DataFrame([{
            "played": Matches_played, 
            "won": won, 
            "drawn": drawn, 
            "lost": lost,
            "gf": gf, 
            "ga": ga, 
            "gd": gd, 
            "points": points
        }])

        expected_features = league_model.feature_names_in_
        new_data = new_data.reindex(columns=expected_features, fill_value=0)

        prob = league_model.predict_proba(new_data)[0][1]
        
        if prob * 100 > 50:
            result_color = "#28a745" 
        else:
            result_color = "#dc3545"
        st.markdown(
            f"""
            <div style="background-color:{result_color}; padding:15px; border-radius:8px; text-align:center; margin-top:20px;">
                <h3 style="color:white; margin:0;">
                    Probability of Winning the League: <span style="font-size:1.5em; font-weight:bold;">{prob*100:.2f}%</span>
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.subheader("Sample League Table for Context")
    
    sample_data = {
        "played": [42, 42, 42],
        "won": [24, 21, 21],
        "drawn": [12, 11, 9],
        "lost": [6, 10, 12],
        "gf": [67, 57, 61],
        "ga": [31, 40, 65],
        "gd": [36, 17, -4],
        "points": [84, 74, 72]
    }
    sample_df = pd.DataFrame(sample_data, index=["1","2","3"])
    st.dataframe(sample_df)