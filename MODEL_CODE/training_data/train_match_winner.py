import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Loading match data...")
df = pd.read_csv("every_match.csv")

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

y = df["FullTimeResult"]

leakage_cols = [
    "FullTimeHomeGoals", "FullTimeAwayGoals",
    "HalfTimeHomeGoals", "HalfTimeAwayGoals", "HalfTimeResult"
]
X = df.drop(columns=["Season", "MatchDate", "FullTimeResult"] + leakage_cols)

label_encoders = {}
for col in X.columns:
    if X[col].dtype == "object":
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

print(f"Features used: {X.columns.tolist()}")

with open("match_features.txt", "w") as f:
    for col in X.columns:
        f.write(col + "\n")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining Random Forest Classifier...")
clf = RandomForestClassifier(random_state=42, n_estimators=100)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nSaving model artifacts...")
joblib.dump(clf, "match_winner_model.pkl")
joblib.dump(label_encoders, "match_label_encoders.pkl")

print("\nModel training complete!")
print(f"Saved: match_winner_model.pkl")
print(f"Saved: match_label_encoders.pkl")
print(f"Saved: match_features.txt")
