# train_league.py
"""
Train a classifier to predict whether a team row is the champion (position == 1).
Uses ONLY numeric features: played, won, drawn, lost, gf, ga, gd, points
Saves: models/league_model.pkl, models/league_scaler.pkl, models/league_meta.json
"""

import os, joblib, json, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from sklearn.calibration import CalibratedClassifierCV

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'datasets', 'league_data.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_OUT = os.path.join(MODELS_DIR, 'league_model.pkl')
SCALER_OUT = os.path.join(MODELS_DIR, 'league_scaler.pkl')
META_OUT = os.path.join(MODELS_DIR, 'league_meta.json')

RANDOM_STATE = 42

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Expected dataset at '{DATA_PATH}'.")

print("Loading dataset:", DATA_PATH)
data = pd.read_csv(DATA_PATH)

# required columns (no team/season required for features)
expected_cols = {'position','played','won','drawn','lost','gf','ga','gd','points'}
missing = expected_cols - set(data.columns)
if missing:
    raise ValueError("Missing columns: " + ", ".join(missing))

# target
data['is_champion'] = (pd.to_numeric(data['position'], errors='coerce') == 1).astype(int)

# Numeric features (8)
numeric_cols = ['played','won','drawn','lost','gf','ga','gd','points']
for c in numeric_cols:
    data[c] = pd.to_numeric(data[c], errors='coerce')

before = len(data)
data = data.dropna(subset=numeric_cols)
after = len(data)
print(f"Dropped {before-after} rows with missing numeric values.")

# Build numeric matrix
X_numeric = data[numeric_cols].copy()
y = data['is_champion'].copy()

# Scale numeric only
scaler = StandardScaler()
X_num_scaled = scaler.fit_transform(X_numeric)  # shape (n_samples, 8)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_num_scaled, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
)

# Train classifier + calibrate probabilities
base_clf = RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1, class_weight='balanced')
calib = CalibratedClassifierCV(estimator=base_clf, method='sigmoid', cv=5)
print("Training calibrated RandomForest...")
calib.fit(X_train, y_train)

# Evaluate
y_pred = calib.predict(X_test)
y_proba = calib.predict_proba(X_test)[:, 1]
print("Test accuracy:", accuracy_score(y_test, y_pred))
try:
    print("ROC AUC:", roc_auc_score(y_test, y_proba))
except Exception:
    pass
print("Classification report:")
print(classification_report(y_test, y_pred, digits=4))

# Save artifacts
joblib.dump(calib, MODEL_OUT)
joblib.dump(scaler, SCALER_OUT)

meta = {
    "numeric_cols": numeric_cols,
    "use_team_encoded": False,
    "feature_order": numeric_cols  # final order expected by scaler/model
}
with open(META_OUT, "w") as f:
    json.dump(meta, f)

print("Saved calibrated model, scaler and metadata to models/")
