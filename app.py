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
match_model = joblib.load("Match_Winner/logistic_regression_model.pkl")
league_model = joblib.load("League Winner/league_model.pkl")

LOGO_DIR = "Logos"
team_logos = {team: os.path.join(LOGO_DIR, f"{team}.png") for team in teams}
team_logos["Nott'm For"] = os.path.join(LOGO_DIR, "Nottingham Forest.png")

st.title("Infosys Springboard Internship Project")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚽ Top Goal Scorer", use_container_width=True):
        st.session_state['option'] = "Top Goal Scorer"
with col2:
    if st.button("🏆 Match Winner", use_container_width=True):
        st.session_state['option'] = "Match Winner"
with col3:
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


elif st.session_state.get('option') == "Match Winner":
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
        st.image(team_logos[home_team], width=100, caption="Home Team Logo") 

    with col_vs:
        st.markdown("<h2 style='text-align: center; margin-top: 50px;'>VS</h2>", unsafe_allow_html=True)
        
    with col_img_away:
        st.subheader(away_team)
        st.image(team_logos[away_team], width=100, caption="Away Team Logo") 

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
            feature_dict = { "HTHG": HomeHalfTimeGoals, "HTAG": AwayHalfTimeGoals }
            
            feature_dict.update({
                "HomeShots": HomeShots, "AwayShots": AwayShots, "HomeShotsOnTarget": HomeShotsOnTarget, 
                "AwayShotsOnTarget": AwayShotsOnTarget, "HomeCorners": HomeCorners, "AwayCorners": AwayCorners, 
                "HomeFouls": HomeFouls, "AwayFouls": AwayFouls, "HomeYellowCards": HomeYellowCards, 
                "AwayYellowCards": AwayYellowCards, "HomeRedCards": HomeRedCards, "AwayRedCards": AwayRedCards
            })

            team_ohe = {f"Home_{team}": 0 for team in teams}
            team_ohe.update({f"Away_{team}": 0 for team in teams})
            team_ohe[f"Home_{home_team}"] = 1
            team_ohe[f"Away_{away_team}"] = 1
            feature_dict.update(team_ohe)

            input_df = pd.DataFrame([feature_dict])
            
            expected_features = match_model.feature_names_in_ 
            input_df = input_df.reindex(columns=expected_features, fill_value=0)

            prediction = match_model.predict(input_df)[0]
            
            if prediction == "H":
                result_text = f"Predicted Result: **{home_team}** Win (Home Win)"
                bg_color = "#28a745"
            elif prediction == "A":
                result_text = f"Predicted Result: **{away_team}** Win (Away Win)"
                bg_color = "#ffc107"
            else:
                result_text = "Predicted Result: Draw"
                bg_color = "#17a2b8"
                
            st.markdown(
                f"""
                <div style="background-color:{bg_color}; padding:15px; border-radius:8px; text-align:center; margin-top:20px;">
                    <h3 style="color:white; margin:0;">{result_text}</h3>
                </div>
                """, 
                unsafe_allow_html=True
            )
            st.markdown("---")
    sample_datah = {
        "HalfTimeHomeGoals": [2, 1, 0],
        "HomeShots": [17, 6, 5],
        "HomeShotsOnTarget": [14, 4, 4],
        "HomeCorners": [6, 5, 5],
        "HomeFouls": [13, 11, 12],
        "HomeYellowCards": [1, 1, 2],
        "HomeRedCards": [0, 0, 0]
    }

    sample_dataa = {
        "HalfTimeAwayGoals": [0, 2, 0],
        "AwayShots": [8, 13, 5],
        "AwayShotsOnTarget": [4, 6, 3],
        "AwayCorners": [6, 8, 4],
        "AwayFouls": [12, 13, 12],
        "AwayYellowCards": [2, 1, 3],
        "AwayRedCards": [0, 0, 0]
    }

    home_df = pd.DataFrame(sample_datah, index=["Match 1", "Match 2", "Match 3"])
    away_df = pd.DataFrame(sample_dataa, index=["Match 1", "Match 2", "Match 3"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Home Stats")
        st.dataframe(home_df)

    with col2:
        st.subheader("Away Stats")
        st.dataframe(away_df)
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