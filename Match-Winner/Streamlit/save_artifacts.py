import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
# Imports below are needed to match the full notebook import list, ensuring compatibility
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import joblib
import scipy.stats as stats
from imblearn.over_sampling import SMOTE
from sklearn.utils.class_weight import compute_class_weight

# --- 1. Load Data (Replicating Notebook Section 2) ---
print("1. Loading Data...")
try:
    df = pd.read_csv("Match Winner.csv")
except FileNotFoundError:
    print("Error: 'Match Winner.csv' not found. Please ensure the file is in the same directory.")
    exit()

# --- 2. Data Cleaning and Feature Selection (Replicating Notebook Sections 4 & 5) ---
target_col = 'FullTimeResult'
# DROPPED COLUMNS: 'Season','MatchDate','FullTimeHomeGoals','FullTimeAwayGoals' (as confirmed in notebook cell 6)
drop_cols = ['Season', 'MatchDate', 'FullTimeHomeGoals', 'FullTimeAwayGoals']
cols_to_drop = [c for c in drop_cols if c in df.columns]
df.drop(columns=cols_to_drop, inplace=True)

# Drop rows missing the target or half-time columns (as per notebook logic in cell 9)
df.dropna(subset=[target_col, 'HalfTimeHomeGoals', 'HalfTimeAwayGoals', 'HalfTimeResult'], inplace=True)

# Impute remaining NaNs with median/Missing (as per notebook logic, though few exist)
if df.isnull().sum().sum() > 0:
    num_cols_all = df.select_dtypes(include=np.number).columns.tolist()
    for c in num_cols_all:
        df[c].fillna(df[c].median(), inplace=True)
    cat_cols_all = df.select_dtypes(include='object').columns.tolist()
    for c in cat_cols_all:
        df[c].fillna('Missing', inplace=True)

# --- 3. Feature Engineering (Replicating Notebook Section 9) ---
print("2. Engineering Features...")
def ht_state(row):
    """Categorizes the Half Time score difference."""
    if row['HalfTimeHomeGoals'] > row['HalfTimeAwayGoals']:
        return 'HomeLead'
    elif row['HalfTimeHomeGoals'] < row['HalfTimeAwayGoals']:
        return 'AwayLead'
    else:
        return 'Level'

df['HalfTimeGoalDiff'] = df['HalfTimeHomeGoals'] - df['HalfTimeAwayGoals']
df['HalfTimeState'] = df.apply(ht_state, axis=1)

# --- 4. Prepare X, y (Replicating Notebook Section 10) ---
X = df.drop(columns=[target_col])
y = df[target_col].copy()

# --- 5. Encoding and Scaling Setup (Replicating Notebook Sections 11, 12, 13) ---
print("3. Encoding and Scaling Data...")
le = LabelEncoder()
y_enc = le.fit_transform(y)
joblib.dump(le, 'label_encoder.pkl')

cat_cols = X.select_dtypes(include='object').columns.tolist()
X_encoded = pd.get_dummies(X, columns=cat_cols, drop_first=True)

# --- CRITICAL: Save the column names for input validation ---
feature_cols = X_encoded.columns.tolist()
joblib.dump(feature_cols, 'feature_columns.pkl')

# Train-Test Split (needed to fit the scaler, consistent with notebook cell 19)
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

scaler = StandardScaler()
num_cols = X_train.select_dtypes(include=np.number).columns.tolist()

# Fit scaler only on training data (consistent with notebook cell 20)
X_train_scaled = X_train.copy()
X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])

# Save the fitted scaler and numeric column list
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(num_cols, 'numeric_columns.pkl')

# --- 6. Train the BEST Model: Logistic Regression (Tuned) (Replicating Notebook Section 17) ---
print("4. Training the best model: Logistic Regression (Tuned)...")

# Exact parameter distribution used for LR tuning in the notebook
param_dist_lr = [{'penalty':['l2'],'C': [0.01,0.1,1,10],'solver':['liblinear']},
                 {'penalty':['l1'],'C':[0.01,0.1,1,10],'solver':['saga']}]

# Use RandomizedSearchCV (RS) to find the best estimator parameters
rs_lr = RandomizedSearchCV(LogisticRegression(max_iter=2000, random_state=42), 
                           param_distributions=param_dist_lr, 
                           n_iter=6, # Matching notebook's n_iter=6
                           cv=3, 
                           scoring='accuracy', 
                           n_jobs=-1, 
                           random_state=42)

# Scale the FULL X_encoded data before final training
X_full_scaled = X_encoded.copy()
X_full_scaled[num_cols] = scaler.transform(X_full_scaled[num_cols])

# Fit RS on the full dataset (scaled) to find the absolute best parameters
rs_lr.fit(X_full_scaled, y_enc)
best_lr = rs_lr.best_estimator_

# Save the trained model
joblib.dump(best_lr, 'logreg_tuned_model.pkl')

print(f"\n--- SUCCESS ---")
print(f"Best LR Parameters Found: {rs_lr.best_params_}")
print(f"Final Model Accuracy (Approximation from RS): {rs_lr.best_score_:.4f}")
print("Artifacts saved. You are now ready for local testing/deployment.")
