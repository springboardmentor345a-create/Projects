from flask import Flask, render_template, request, send_from_directory
import joblib
import pandas as pd
import numpy as np
import os
import json

app = Flask(__name__)

# Load goal scorer model artifacts
GOAL_MODEL_PATH = "model.pkl"
GOAL_IMPUTER_PATH = "imputer.pkl"
GOAL_LE_PATH = "label_encoder.pkl"
GOAL_FEATURES_META = "features.txt"

goal_model = joblib.load(GOAL_MODEL_PATH)
goal_imputer = joblib.load(GOAL_IMPUTER_PATH)
goal_label_encoder = None
if os.path.exists(GOAL_LE_PATH):
    goal_label_encoder = joblib.load(GOAL_LE_PATH)

if os.path.exists(GOAL_FEATURES_META):
    with open(GOAL_FEATURES_META, "r") as f:
        GOAL_FEATURE_NAMES = [line.strip() for line in f if line.strip()]
else:
    GOAL_FEATURE_NAMES = []

# Load match winner model artifacts
MATCH_MODEL_PATH = "match_winner_model.pkl"
MATCH_ENCODERS_PATH = "match_label_encoders.pkl"
MATCH_FEATURES_META = "match_features.txt"

match_model = joblib.load(MATCH_MODEL_PATH)
match_label_encoders = joblib.load(MATCH_ENCODERS_PATH)

if os.path.exists(MATCH_FEATURES_META):
    with open(MATCH_FEATURES_META, "r") as f:
        MATCH_FEATURE_NAMES = [line.strip() for line in f if line.strip()]
else:
    MATCH_FEATURE_NAMES = []

# Load teams list
with open("teams.json", "r") as f:
    TEAMS = json.load(f)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/goal-scorer", methods=["GET", "POST"])
def goal_scorer():
    prediction = None
    error = None
    
    if not GOAL_FEATURE_NAMES:
        error = "Feature metadata missing for goal scorer prediction."
    
    if request.method == "POST" and not error:
        try:
            data = {}
            for feat in GOAL_FEATURE_NAMES:
                raw = request.form.get(feat)
                if raw is None:
                    data[feat] = np.nan
                else:
                    try:
                        if raw == "":
                            data[feat] = np.nan
                        else:
                            data[feat] = float(raw)
                    except ValueError:
                        data[feat] = raw

            df = pd.DataFrame([data], columns=GOAL_FEATURE_NAMES)

            if "Position" in df.columns and goal_label_encoder is not None:
                position_value = df["Position"].astype(str).fillna("Unknown").iloc[0]
                position_lower = position_value.lower()
                
                classes_lower = [c.lower() for c in goal_label_encoder.classes_]
                if position_lower in classes_lower:
                    original_position = goal_label_encoder.classes_[classes_lower.index(position_lower)]
                    df["Position"] = goal_label_encoder.transform([original_position])
                else:
                    df["Position"] = 0

            df_imputed = pd.DataFrame(goal_imputer.transform(df), columns=GOAL_FEATURE_NAMES)
            pred = goal_model.predict(df_imputed)[0]
            prediction = float(pred)
        except Exception as e:
            error = f"Prediction error: {e}"

    return render_template("goal_scorer.html", 
                         feature_names=GOAL_FEATURE_NAMES, 
                         prediction=prediction,
                         error=error)

@app.route("/match-winner", methods=["GET", "POST"])
def match_winner():
    prediction = None
    error = None
    form_data = {}
    
    if not MATCH_FEATURE_NAMES:
        error = "Feature metadata missing for match winner prediction."
    
    if request.method == "POST" and not error:
        try:
            data = {}
            for feat in MATCH_FEATURE_NAMES:
                raw = request.form.get(feat)
                form_data[feat] = raw
                
                if feat in match_label_encoders:
                    if raw and raw in match_label_encoders[feat].classes_:
                        data[feat] = match_label_encoders[feat].transform([raw])[0]
                    else:
                        data[feat] = 0
                else:
                    try:
                        if raw == "" or raw is None:
                            data[feat] = 0
                        else:
                            data[feat] = float(raw)
                    except ValueError:
                        data[feat] = 0

            df = pd.DataFrame([data], columns=MATCH_FEATURE_NAMES)
            pred = match_model.predict(df)[0]
            
            home_team = form_data.get('HomeTeam', 'Home Team')
            away_team = form_data.get('AwayTeam', 'Away Team')
            
            result_map = {
                'H': f'{home_team} Wins',
                'A': f'{away_team} Wins',
                'D': 'Draw'
            }
            prediction = result_map.get(pred, pred)
            
        except Exception as e:
            error = f"Prediction error: {e}"

    return render_template("match_winner.html", 
                         teams=TEAMS,
                         feature_names=MATCH_FEATURE_NAMES,
                         prediction=prediction, 
                         error=error,
                         form_data=form_data)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
