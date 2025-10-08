import streamlit as st
import numpy as np
import joblib

# Load the trained model and scaler
model = joblib.load('linear_regression_model.pkl')
scaler = joblib.load('scaler.pkl')

st.title("🎯 Predict Top Assists")
st.markdown("Enter player stats to predict the number of assists in the upcoming season.")

# --- USER INPUTS ---
numeric_features = {
    'Age': (16, 45, 25),
    'Minutes_Played': (0, 4000, 2000),
    'Assists_prev_season': (0, 20, 5),
    'Shots_Assisted': (0, 200, 50),
    'Club_Attack_Share': (0.0, 1.0, 0.5),
    'Assists_per_90': (0.0, 2.0, 0.5),
    'xA_per_90': (0.0, 2.0, 0.5)
}

user_input = {}
for feature, (min_val, max_val, default) in numeric_features.items():
    step = 0.01 if isinstance(default, float) else 1
    user_input[feature] = st.number_input(feature, min_value=min_val, max_value=max_val, value=default, step=step)

# Position selection
positions = ['Forward', 'Fullback', 'Midfielder', 'Winger']
position_selected = st.selectbox("Position", positions)

# --- PREDICTION BUTTON ---
if st.button("Predict"):
    # One-hot encode position
    position_features = ['Position_Forward', 'Position_Fullback', 'Position_Midfielder', 'Position_Winger']
    position_input = [1 if position_selected.lower() in p.lower() else 0 for p in position_features]

    # Combine numeric and position inputs
    X_input = np.array(list(user_input.values()) + position_input).reshape(1, -1)

    # Scale only numeric features
    X_input[:, :7] = scaler.transform(X_input[:, :7])

    # Predict and round to int
    pred = int(round(model.predict(X_input)[0]))

    # Ensure prediction is >= 0
    pred = max(pred, 0)

    # Display result
    st.subheader("Predicted Assists This Season")
    st.success(f"{pred} assists")
