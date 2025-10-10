"""
Train a regressor to predict season assists for players using Backend/datasets/assists_data.csv
Saves pipeline + metadata to Backend/models/.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'datasets', 'assists_data.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

PIPELINE_OUT = os.path.join(MODELS_DIR, 'assists_pipeline.pkl')
METADATA_OUT = os.path.join(MODELS_DIR, 'assists_metadata.pkl')

RANDOM_STATE = 42

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Expected dataset at '{DATA_PATH}'. Put your file there or update the path.")

print(f"Loading assists dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

if 'Assists' not in df.columns:
    raise ValueError("Dataset must contain an 'Assists' column.")

# Standardize missing markers
df = df.replace({'N/A': np.nan, 'NA': np.nan, 'n/a': np.nan, '': np.nan})

# Candidate numeric and categorical features (only keep those in CSV)
numeric_features = [
    'Age','Minutes_Played','Assists_prev_season','Goals_prev_season',
    'Key_Passes','Expected_Assists_(xA)','Crosses_Completed',
    'Dribbles_Completed','Shots_Assisted','Club_Total_Goals',
    'Club_League_Rank','Club_Attack_Share','Club_xG',
    'Assists_per_90','xA_per_90','Key_Passes_per_90'
]
categorical_features = ['Position','Set_Piece_Involvement','Big6_Club_Feature']

numeric_features = [c for c in numeric_features if c in df.columns]
categorical_features = [c for c in categorical_features if c in df.columns]

features = numeric_features + categorical_features
if len(features) == 0:
    raise ValueError("No recognized features found in CSV.")

# Coerce numeric columns and drop rows with missing target
for c in numeric_features:
    df[c] = pd.to_numeric(df[c], errors='coerce')

before = len(df)
df = df.dropna(subset=['Assists'])
after = len(df)
print(f"Dropped {before-after} rows missing target 'Assists'.")

if len(df) == 0:
    raise ValueError("No data left after dropping missing targets.")

# Impute numerics with median (and store values)
impute_values = {}
for c in numeric_features:
    median = float(df[c].median(skipna=True)) if df[c].dropna().shape[0] > 0 else 0.0
    impute_values[c] = median
    df[c] = df[c].fillna(median)

# Encode categoricals with LabelEncoder and save encoders
label_encoders = {}
for c in categorical_features:
    le = LabelEncoder()
    df[c] = df[c].fillna('UNKNOWN').astype(str)
    le.fit(df[c])
    df[c + '_enc'] = le.transform(df[c])
    label_encoders[c] = le

# Final ordered columns used for training
X_cols = numeric_features + [c + '_enc' for c in categorical_features]
X = df[X_cols].copy()
y = pd.to_numeric(df['Assists'], errors='coerce').fillna(0.0)

# Build pipeline: scaler + regressor
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('rf', RandomForestRegressor(n_estimators=200, random_state=RANDOM_STATE, n_jobs=-1))
])

# Fit
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
print("Training pipeline (StandardScaler + RandomForestRegressor)...")
pipeline.fit(X_train, y_train)

# Cross-val (RMSE)
try:
    from sklearn.model_selection import cross_val_score
    neg_mse = cross_val_score(pipeline, X, y, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
    rmse = np.sqrt(-neg_mse)
    print(f"5-fold CV RMSEs: {rmse}")
    print(f"Mean CV RMSE: {rmse.mean():.4f}")
except Exception as e:
    print("Cross-val failed (non-fatal):", e)

# Test eval
y_pred = pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = (mean_squared_error(y_test, y_pred))**0.5
r2 = r2_score(y_test, y_pred)
print("\nTest eval:")
print(f"MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")

# Save pipeline + metadata (X_cols, impute values, encoders)
joblib.dump(pipeline, PIPELINE_OUT)
metadata = {
    'feature_names': X_cols,
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
    'impute_values': impute_values,
    'label_encoders_keys': list(label_encoders.keys())
}
joblib.dump(metadata, METADATA_OUT)
# Save encoders separately so backend can use them for unseen labels handling
joblib.dump(label_encoders, os.path.join(MODELS_DIR, 'assists_labelencoders.pkl'))

print(f"\nSaved pipeline to {PIPELINE_OUT}")
print(f"Saved metadata to {METADATA_OUT}")
print(f"Saved label encoders to {os.path.join(MODELS_DIR, 'assists_labelencoders.pkl')}")
