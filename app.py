import streamlit as st
import joblib
import pandas as pd
import sys
import sklearn

league_model = joblib.load("league_model.pkl")

st.title("EPL PREDICTOR🥎")
st.title("League Winner Prediction🏆")

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
sample_df = pd.DataFrame(sample_data, index=["1", "2", "3"])
st.dataframe(sample_df)




