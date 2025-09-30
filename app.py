import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load trained models
goal_model = joblib.load("Top_Goal_Scorer/linear_regression_model.pkl")
match_model = joblib.load("Match_Winner/decision_tree_model.pkl")

# Team list
teams = [
    "Arsenal", "Aston Villa","Bournemouth","Brentford", "Brighton", "Burnley","Chelsea","Crystal Palace","Everton","Fulham","Leeds","Liverpool","Luton", "Man City", "Man United","Newcastle","Nott'm For","Sunderland","Tottenham","West Ham","Wolves"
]

# Streamlit UI
st.title("Infosys Springboard Internship Project")

st.sidebar.header("Navigation")
option = st.sidebar.radio("Choose Model",["Top Goal Scorer", "Match Winner"])

# Top Goal Scorer Predictor
if option == "Top Goal Scorer":
    st.header("Top Goal Scorer Prediction")

    Age = st.number_input("Age", value=0)
    Appearances = st.number_input("Appearances", value=0)
    Goals_prev_season = st.number_input("Goals in Previous Season", value=0)
    Penalty_Goals = st.number_input("Penalty Goals", value=0)
    Non_Penalty_Goals = st.number_input("Non-Penalty Goals", value=0)
    Goals_per_90 = st.number_input("Goals per 90 mins", value=0.0, format="%.2f")
    Big_6_Club_Feature = st.number_input("Big 6 Club Feature (0/1)", value=0)
    League_Goals_per_Match = st.number_input("League Goals per Match", value=0.0, format="%.2f")

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

    if st.button("Predict Goals"):
        input_data = np.array([[Age, Appearances, Goals_prev_season,
                                Penalty_Goals, Non_Penalty_Goals, Goals_per_90,
                                Big_6_Club_Feature, League_Goals_per_Match,
                                *position_encoded]])
        prediction = goal_model.predict(input_data)
        st.success(f"Predicted Goals: {int(round(prediction[0]))}")

# Match Winner Predictor
else:
    st.header("Match Winner Prediction")

    col_home, col_away = st.columns(2)

    with col_home:
        st.subheader("Home Team Stats")
        home_team = st.selectbox("Select Home Team", teams)
        HomeShots = st.number_input("Home Shots", value=0)
        HomeShotsOnTarget = st.number_input("Home Shots on Target", value=0)
        HomeCorners = st.number_input("Home Corners", value=0)
        HomeFouls = st.number_input("Home Fouls", value=0)
        HomeYellowCards = st.number_input("Home Yellow Cards", value=0)
        HomeRedCards = st.number_input("Home Red Cards", value=0)

    with col_away:
        st.subheader("Away Team Stats")
        away_team = st.selectbox("Select Away Team", teams)
        AwayShots = st.number_input("Away Shots", value=0)
        AwayShotsOnTarget = st.number_input("Away Shots on Target", value=0)
        AwayCorners = st.number_input("Away Corners", value=0)
        AwayFouls = st.number_input("Away Fouls", value=0)
        AwayYellowCards = st.number_input("Away Yellow Cards", value=0)
        AwayRedCards = st.number_input("Away Red Cards", value=0)

    if st.button("Predict Match Result"):
        feature_dict = {f"Home_{team}": 0 for team in teams}
        feature_dict.update({f"Away_{team}": 0 for team in teams})

        feature_dict[f"Home_{home_team}"] = 1
        feature_dict[f"Away_{away_team}"] = 1

        feature_dict.update({
            "HomeShots": HomeShots,
            "AwayShots": AwayShots,
            "HomeShotsOnTarget": HomeShotsOnTarget,
            "AwayShotsOnTarget": AwayShotsOnTarget,
            "HomeCorners": HomeCorners,
            "AwayCorners": AwayCorners,
            "HomeFouls": HomeFouls,
            "AwayFouls": AwayFouls,
            "HomeYellowCards": HomeYellowCards,
            "AwayYellowCards": AwayYellowCards,
            "HomeRedCards": HomeRedCards,
            "AwayRedCards": AwayRedCards
        })

        input_df = pd.DataFrame([feature_dict])

        input_df = input_df.reindex(columns=match_model.feature_names_in_, fill_value=0)

        prediction = match_model.predict(input_df)[0]

        if prediction == "H":
            st.success("Predicted Result: Home Win")
        elif prediction == "A":
            st.success("Predicted Result: Away Win")
        else:
            st.success("Predicted Result: Draw")
