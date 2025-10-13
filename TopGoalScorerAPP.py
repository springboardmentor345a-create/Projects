import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load your model (make sure the path is correct)
goal_model = joblib.load("Random_forest_model.pkl")

st.title("EPL PREDICTOR🥎")
st.title("Top Goal Scorer Prediction🏆")

st.markdown("Enter season-end team statistics to predict the probability of winning the league.")

st.title("Infosys Springboard Internship Project")

# Header and description for Top Goal Scorer only
st.markdown("Enter player statistics to predict the total goals scored in the season.")

# Input columns
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
    input_data = np.array([[Age, Appearances, Goals_prev_season, Goals_per_90,
                            Big_6_Club_Feature, League_Goals_per_Match,
                            *position_encoded]], dtype=float)

    # Debug prints to check input data and prediction
    st.write("Input data:", input_data)

    prediction = goal_model.predict(input_data)

    st.write("Raw prediction:", prediction)

    st.markdown(
        f"""
        <div style="background-color:#007bff; padding:10px; border-radius:5px; text-align:center; margin-top:15px;">
            <h3 style="color:white; margin:0;">Predicted Goals: <span style="font-size:1.5em; font-weight:bold;">{int(round(prediction[0]))}</span></h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# Sample data table for context
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
