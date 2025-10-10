from flask import Flask, request, jsonify, render_template, send_from_directory
import os, joblib, traceback, numpy as np

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'Frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

app = Flask(__name__, template_folder=FRONTEND_DIR, static_folder=STATIC_DIR)

# --- Feature definitions ---
LEAGUE_NUMERIC_COLS = ['played','won','drawn','lost','gf','ga','gd','points']

ASSISTS_NUMERIC_COLS = [
    'Age','Minutes_Played','Assists_prev_season','Goals_prev_season',
    'Key_Passes','Expected_Assists_(xA)','Crosses_Completed',
    'Dribbles_Completed','Shots_Assisted','Club_Total_Goals',
    'Club_League_Rank','Club_Attack_Share','Club_xG',
    'Assists_per_90','xA_per_90','Key_Passes_per_90'
]
ASSISTS_CATEGORICAL_COLS = ['Position','Set_Piece_Involvement','Big6_Club_Feature']

# --- Load models safely ---
def load_if_exists(path):
    try:
        return joblib.load(path) if os.path.exists(path) else None
    except Exception as e:
        print(f"Failed loading {path}: {e}")
        return None

league_model = load_if_exists(os.path.join(MODELS_DIR, 'league_model.pkl'))
league_scaler = load_if_exists(os.path.join(MODELS_DIR, 'league_scaler.pkl'))

assists_model = load_if_exists(os.path.join(MODELS_DIR, 'assists_model.pkl'))
assists_scaler = load_if_exists(os.path.join(MODELS_DIR, 'assists_scaler.pkl'))
assists_labelencoders = load_if_exists(os.path.join(MODELS_DIR, 'assists_labelencoders.pkl'))

# --- Helper to serve frontend ---
def serve_frontend_file(filename):
    try:
        return render_template(filename)
    except Exception as e:
        return f"Template rendering failed: {str(e)}", 500

# --- Routes ---
@app.route('/')
def home(): return serve_frontend_file('index.html')

@app.route('/league_winner')
@app.route('/league_winner.html')
def league_page(): return serve_frontend_file('league_winner.html')

@app.route('/top_assists')
@app.route('/top_assists.html')
def assists_page(): return serve_frontend_file('top_assists.html')

@app.route('/static/<path:p>')
def static_files(p): return send_from_directory(STATIC_DIR, p)

# --- League prediction ---
@app.route('/predict_league', methods=['POST'])
def predict_league():
    if league_model is None: return jsonify({"error":"League model missing"}), 500
    data = request.get_json(force=True, silent=True)
    if not data: return jsonify({"error":"No JSON payload"}), 400
    try:
        row = [float(data.get(c, 0)) for c in LEAGUE_NUMERIC_COLS]
        X = np.array(row).reshape(1, -1)
        if league_scaler is not None and hasattr(league_scaler, 'mean_'):
            if X.shape[1] != league_scaler.mean_.shape[0]:
                return jsonify({"error":"League input features mismatch"}), 400
            X = league_scaler.transform(X)
        prob = float(league_model.predict_proba(X)[0,1]) if hasattr(league_model, 'predict_proba') else float(league_model.predict(X)[0])
        return jsonify({"probability": prob})
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({"error": str(e), "trace": tb}), 500

# --- Assists prediction ---
@app.route('/predict_assists', methods=['POST'])
def predict_assists():
    if assists_model is None or assists_scaler is None or assists_labelencoders is None:
        return jsonify({"error":"Assists pipeline missing"}), 500

    data = request.get_json(force=True, silent=True)
    if not data: return jsonify({"error":"No JSON payload"}), 400

    try:
        # --- 1. Numeric features ---
        row = []
        for c in ASSISTS_NUMERIC_COLS:
            val = data.get(c, None)
            if val is None:
                val = 0.0
            row.append(float(val))

        # --- 2. Categorical features (encoded with label encoders) ---
        for c in ASSISTS_CATEGORICAL_COLS:
            le = assists_labelencoders.get(c)
            val = str(data.get(c, 'UNKNOWN'))
            if le is not None:
                # If value not seen before, assign most frequent class
                if val in le.classes_:
                    enc = int(le.transform([val])[0])
                else:
                    enc = int(np.bincount(le.transform(le.classes_)).argmax())
            else:
                enc = 0
            row.append(enc)

        # --- 3. Convert to numpy array and reshape ---
        X = np.array(row).reshape(1, -1)

        # --- 4. Scale using training scaler ---
        if assists_scaler is not None and hasattr(assists_scaler, 'mean_'):
            if X.shape[1] != assists_scaler.mean_.shape[0]:
                return jsonify({"error":"Assists input features mismatch"}), 400
            X = assists_scaler.transform(X)

        # --- 5. Predict ---
        pred = float(assists_model.predict(X)[0])

        # --- 6. Compute per90 ---
        minutes = float(data.get('Minutes_Played', 0))
        per90 = (pred / (minutes / 90)) if minutes > 0 else None

        return jsonify({"assists": round(pred, 2), "assists_per_90": round(per90, 2) if per90 else None})

    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        return jsonify({"error": str(e), "trace": tb}), 500

if __name__ == '__main__':
    print("Starting Flask app; templates from:", FRONTEND_DIR)
    app.run(host='127.0.0.1', port=5000, debug=True)
