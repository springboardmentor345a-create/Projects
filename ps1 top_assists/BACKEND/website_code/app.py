from flask import Flask, render_template, request, send_from_directory
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

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

ASSIST_MODEL_PATH = "assist_model.pkl"
ASSIST_LE_PATH = "assist_label_encoder.pkl"
ASSIST_FEATURES_META = "assist_features.txt"

assist_model = joblib.load(ASSIST_MODEL_PATH)
assist_label_encoder = joblib.load(ASSIST_LE_PATH)

if os.path.exists(ASSIST_FEATURES_META):
    with open(ASSIST_FEATURES_META, "r") as f:
        ASSIST_FEATURE_NAMES = [line.strip() for line in f if line.strip()]
else:
    ASSIST_FEATURE_NAMES = []

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
            prediction = int(round(pred))
        except Exception as e:
            error = f"Prediction error: {e}"

    return render_template("goal_scorer.html", 
                         feature_names=GOAL_FEATURE_NAMES, 
                         prediction=prediction,
                         error=error)

@app.route("/top-assist", methods=["GET", "POST"])
def top_assist():
    prediction = None
    error = None
    form_data = {}
    
    if not ASSIST_FEATURE_NAMES:
        error = "Feature metadata missing for top assist prediction."
    
    if request.method == "POST" and not error:
        try:
            data = {}
            for feat in ASSIST_FEATURE_NAMES:
                raw = request.form.get(feat)
                form_data[feat] = raw
                
                if feat == "Position":
                    if raw and raw in assist_label_encoder.classes_:
                        data[feat] = assist_label_encoder.transform([raw])[0]
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

            df = pd.DataFrame([data], columns=ASSIST_FEATURE_NAMES)
            pred = assist_model.predict(df)[0]
            prediction = int(round(pred))
            
        except Exception as e:
            error = f"Prediction error: {e}"

    positions = list(assist_label_encoder.classes_)
    
    return render_template("top_assist.html", 
                         feature_names=ASSIST_FEATURE_NAMES,
                         positions=positions,
                         prediction=prediction, 
                         error=error,
                         form_data=form_data)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
