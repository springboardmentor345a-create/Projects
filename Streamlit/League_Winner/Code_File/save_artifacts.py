import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# --- Configuration (Based on your input) ---
TARGET_COL = 'Winner'
FEATURE_COLS = ['played', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd', 'points']
BEST_LR_PARAMS = {'C': 1, 'penalty': 'l2', 'solver': 'liblinear'}
MODEL_NAME = 'logreg_league_winner'

# --- Setup ---
BASE_DIR = Path(__file__).resolve().parent

print("1. Loading Data...")
try:
    # Assuming pl-tables.csv is the file provided for this project
    df = pd.read_csv(BASE_DIR / 'pl-tables.csv')
except FileNotFoundError:
    print("FATAL ERROR: 'pl-tables.csv' not found. Please ensure it is in the project folder.")
    exit()

# --- 2. Feature Engineering & Cleaning ---
print("2. Engineering Features & Cleaning...")

# Target Definition: Winner is position 1
df[TARGET_COL] = (df['position'] == 1).astype(int)

# Drop columns specified in your notebook (plus the original position column)
drop_cols = ['season_end_year', 'team', 'notes', 'position']
df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors='ignore')

# Prepare X and y
X = df[FEATURE_COLS]
y = df[TARGET_COL]

# --- 3. Encoding and Scaling ---
print("3. Encoding and Scaling...")

# No categorical features are selected for X, but we save the LabelEncoder for the target.
le = LabelEncoder()
y_enc = le.fit_transform(y)

# Scaling features (Standard Practice for Logistic Regression)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=FEATURE_COLS)

# --- 4. Training the best model: Logistic Regression ---
print(f"4. Training the best model: Logistic Regression...")

# Use the scaled data for LogReg
X_train, X_test, y_train, y_test = train_test_split(X_scaled_df, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

# Instantiate and fit the final model using the best known parameters
final_model = LogisticRegression(
    **BEST_LR_PARAMS, 
    max_iter=1000, 
    random_state=42
)
final_model.fit(X_train, y_train)

# Calculate final accuracy for the user
y_pred = final_model.predict(X_test)
final_accuracy = accuracy_score(y_test, y_pred)

# --- 5. Saving Artifacts ---
joblib.dump(final_model, BASE_DIR / f'{MODEL_NAME}_model.pkl')
joblib.dump(scaler, BASE_DIR / f'{MODEL_NAME}_scaler.pkl')
joblib.dump(le, BASE_DIR / f'{MODEL_NAME}_le.pkl')
joblib.dump(X.columns.tolist(), BASE_DIR / f'{MODEL_NAME}_feature_cols.pkl')
joblib.dump(final_accuracy, BASE_DIR / f'{MODEL_NAME}_accuracy.pkl')

# --- Success Message ---
print("\n--- SUCCESS ---")
print(f"Final Model Trained (Accuracy on Test Set): {final_accuracy:.4f}")
print("Artifacts saved. You are now ready for local testing/deployment.")
