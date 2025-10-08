import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load the trained Random Forest model
model = joblib.load("model_latest.joblib")  # Ensure it's in the same folder

st.title("🏆 Predict League Winner")
st.markdown("Enter team statistics to predict the league winner.")

# --- USER INPUTS ---
numeric_features = {
    'won': (0, 50, 10),
    'drawn': (0, 50, 10),
    'lost': (0, 50, 10),
    'gf': (0, 150, 50),   # goals for
    'ga': (0, 150, 50),   # goals against
    'gd': (-100, 100, 0)  # goal difference
}

user_input = {}
for feature, (min_val, max_val, default) in numeric_features.items():
    user_input[feature] = st.number_input(
        feature, 
        min_value=min_val, 
        max_value=max_val, 
        value=default, 
        step=1
    )

# --- PREDICTION BUTTON ---
if st.button("Predict"):
    # Convert inputs to array
    X_input = np.array(list(user_input.values())).reshape(1, -1)

    # Predict and get probability
    pred = model.predict(X_input)[0]
    prob = model.predict_proba(X_input)[0][1]  # probability of being champion

    # Display result with style
    st.subheader("Predicted League Outcome")

    if pred == 1:
        st.success(f"🏆 Champion! (Probability: {prob*100:.2f}%)")
        st.balloons()  # confetti animation
    else:
        st.error(f"❌ Not Champion (Probability: {prob*100:.2f}%)")




