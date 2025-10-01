import streamlit as st
import joblib
import numpy as np
import pandas as pd

try:
    goal_model = joblib.load(r"Top_Goal_Scorer/linear_regression_model.pkl")
    match_model = joblib.load(r"Match_Winner\logistic_regression_model.pkl")
except FileNotFoundError as e:
    class DummyModel:
        def predict(self, data):
            if data.shape[1] == 12:
                return [20] 
            else: # Match Winner features
                if "HTHG" in data.columns and "HTAG" in data.columns:
                    if data["HTHG"].iloc[0] > data["HTAG"].iloc[0]:
                        return ["H"]
                    elif data["HTAG"].iloc[0] > data["HTHG"].iloc[0]:
                        return ["A"]
                return ["D"] # Default to Draw if no clear half-time lead
        
        @property
        def feature_names_in_(self):
            return [
                "HTHG", "HTAG", # New features at the start
                "HomeShots", "AwayShots", "HomeShotsOnTarget", "AwayShotsOnTarget",
                "HomeCorners", "AwayCorners", "HomeFouls", "AwayFouls",
                "HomeYellowCards", "AwayYellowCards", "HomeRedCards", "AwayRedCards"
            ] + [f"Home_{t}" for t in teams] + [f"Away_{t}" for t in teams]
            
    goal_model = DummyModel()
    match_model = DummyModel()

# Team list
teams = [
    "Arsenal", "Aston Villa","Bournemouth","Brentford", "Brighton", "Burnley","Chelsea","Crystal Palace","Everton","Fulham","Leeds","Liverpool","Luton", "Man City", "Man United","Newcastle","Nott'm For","Sunderland","Tottenham","West Ham","Wolves"
]

team_logos = {
    "Arsenal": r"Logos\Arsenal.png",
    "Aston Villa": r"Logos\Aston Villa.png",
    "Bournemouth": r"Logos\Bournemouth.png",
    "Brentford": r"Logos\Brentford.png",
    "Brighton": r"Logos\Brentford.png",
    "Burnley": r"Logos\Burnley.png",
    "Chelsea": r"Logos\Chelsea.png",
    "Crystal Palace": r"Logos\Crystal Palace.png",
    "Everton": r"Logos\Everton.png",
    "Fulham": r"Logos\Fulham.png",
    "Leeds": r"Logos\Leeds.png",
    "Liverpool": r"Logos\Liverpool.png",
    "Luton": r"Logos\Luton.png",
    "Man City": r"Logos\Man City.png",
    "Man United": r"Logos\Man United.png",
    "Newcastle": r"Logos\Newcastle.png",
    "Nott'm For": r"Logos\Nottingham Forest.png",
    "Sunderland":r"Logos\Sunderland.png",
    "Tottenham": r"Logos\Tottenham.png",
    "West Ham": r"Logos\West Ham.png",
    "Wolves": r"Logos\Wolves.png"
}

st.title("Infosys Springboard Internship Project")

col1, col2 = st.columns(2)

with col1:
    if st.button("Top Goal Scorer Prediction", use_container_width=True):
        st.session_state['option'] = "Top Goal Scorer"
with col2:
    if st.button("Match Winner Prediction", use_container_width=True):
        st.session_state['option'] = "Match Winner"

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
        Penalty_Goals = st.number_input("Penalty Goals", min_value=0, value=1)
        
    with col_b:
        Non_Penalty_Goals = st.number_input("Non-Penalty Goals", min_value=0, value=4)
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
        input_data = np.array([[Age, Appearances, Goals_prev_season,
                                Penalty_Goals, Non_Penalty_Goals, Goals_per_90,
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

else:
    st.header("Match Winner Prediction")
    st.markdown("Enter match statistics to predict the final result (Home Win, Away Win, or Draw).")

    col_home_select, col_away_select = st.columns(2)
    with col_home_select:
        home_team = st.selectbox("Select Home Team", teams, key="home_team_select")
    with col_away_select:
        away_team = st.selectbox("Select Away Team", teams, key="away_team_select", index=1)

    col_img_home, col_vs, col_img_away = st.columns([1, 0.5, 1])

    with col_img_home:
        st.subheader(home_team)
        if home_team in team_logos:
            st.image(team_logos[home_team], width=100) 
        else:
            st.markdown(f"[]")

    with col_vs:
        st.markdown("<h2 style='text-align: center; margin-top: 50px;'>VS</h2>", unsafe_allow_html=True)
        
    with col_img_away:
        st.subheader(away_team)
        if away_team in team_logos:
            st.image(team_logos[away_team], width=100)
        else:
            st.markdown(f"[]") 

    st.markdown("---")

    col_home, col_away = st.columns(2)

    with col_home:
        st.subheader(f"{home_team} Stats (Home)")
        HomeHalfTimeGoals = st.number_input("Half Time Goals (HTHG)", key="HomeHTGoals", min_value=0, value=1)
        HomeShots = st.number_input("Total Shots", key="HomeShots", min_value=0, value=15)
        HomeShotsOnTarget = st.number_input("Shots on Target", key="HomeShotsOnTarget", min_value=0, value=5)
        HomeCorners = st.number_input("Corners", key="HomeCorners", min_value=0, value=7)
        HomeFouls = st.number_input("Fouls", key="HomeFouls", min_value=0, value=10)
        HomeYellowCards = st.number_input("Yellow Cards", key="HomeYellowCards", min_value=0, value=1)
        HomeRedCards = st.number_input("Red Cards", key="HomeRedCards", min_value=0, value=0)

    with col_away:
        st.subheader(f"{away_team} Stats (Away)")
        AwayHalfTimeGoals = st.number_input("Half Time Goals (HTAG)", key="AwayHTGoals", min_value=0, value=0)
        AwayShots = st.number_input("Total Shots", key="AwayShots", min_value=0, value=10)
        AwayShotsOnTarget = st.number_input("Shots on Target", key="AwayShotsOnTarget", min_value=0, value=3)
        AwayCorners = st.number_input("Corners", key="AwayCorners", min_value=0, value=4)
        AwayFouls = st.number_input("Fouls", key="AwayFouls", min_value=0, value=12)
        AwayYellowCards = st.number_input("Yellow Cards", key="AwayYellowCards", min_value=0, value=2)
        AwayRedCards = st.number_input("Red Cards", key="AwayRedCards", min_value=0, value=0)

    st.markdown("---")

    if st.button("Predict Match Result", type="primary", use_container_width=True):
        if home_team == away_team:
            st.error("Home Team and Away Team cannot be the same. Please select different teams.")
        else:
            feature_dict = {
                "HTHG": HomeHalfTimeGoals,
                "HTAG": AwayHalfTimeGoals
            }
            
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

            team_ohe = {f"Home_{team}": 0 for team in teams}
            team_ohe.update({f"Away_{team}": 0 for team in teams})
            team_ohe[f"Home_{home_team}"] = 1
            team_ohe[f"Away_{away_team}"] = 1
            feature_dict.update(team_ohe)

            input_df = pd.DataFrame([feature_dict])
            try:
                expected_features = match_model.feature_names_in_ 
            except AttributeError:
                expected_features = [
                    "HTHG", "HTAG",
                    "HomeShots", "AwayShots", "HomeShotsOnTarget", "AwayShotsOnTarget",
                    "HomeCorners", "AwayCorners", "HomeFouls", "AwayFouls",
                    "HomeYellowCards", "AwayYellowCards", "HomeRedCards", "AwayRedCards"
                ] + [f"Home_{t}" for t in teams] + [f"Away_{t}" for t in teams]

            input_df = input_df.reindex(columns=expected_features, fill_value=0)

            prediction = match_model.predict(input_df)[0]

            winner_team_logo = None
            if prediction == "H":
                result_text = f"**{home_team}** Win (Home Win)"
                bg_color = "#28a745" 
                winner_team_logo = team_logos.get(home_team)
            elif prediction == "A":
                result_text = f"**{away_team}** Win (Away Win)"
                bg_color = "#ffc107" 
                winner_team_logo = team_logos.get(away_team)
            else:
                result_text = "Draw"
                bg_color = "#17a2b8" 
                draw_col1, draw_col2 = st.columns(2)
                with draw_col1:
                    if home_team in team_logos:
                        st.image(team_logos[home_team], width=70)
                with draw_col2:
                    if away_team in team_logos:
                        st.image(team_logos[away_team], width=70)

            st.markdown(
                f"""
                <div style="background-color:{bg_color}; padding:15px; border-radius:8px; text-align:center; margin-top:20px;">
                    <h3 style="color:white; margin:0;">{result_text}</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if winner_team_logo:
                st.markdown(f"<div style='text-align:center; margin-top:10px;'>", unsafe_allow_html=True)
                st.image(winner_team_logo, width=150, caption=f"{home_team if prediction == 'H' else away_team} - Predicted Winner")
                st.markdown(f"</div>", unsafe_allow_html=True)