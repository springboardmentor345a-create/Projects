import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def main():
    # 1. Load dataset
    file_path = "newupdatedgoals.csv"
    df = pd.read_csv(file_path)

    print("Raw shape:", df.shape)

    # 2. Remove duplicates
    df = df.drop_duplicates()
    print("After drop_duplicates:", df.shape)

    # 3. Drop unwanted columns (ignore if not present)
    drop_cols = ["Season", "Rank", "Player", "Club", "Penalty_Goals", "Non-Penalty_Goals"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")
    print("After dropping unwanted columns:", df.shape)

    # 4. Drop rows where target is null
    if "Goals" not in df.columns:
        raise ValueError("No 'Goals' column in dataset.")
    df = df.dropna(subset=["Goals"])
    print("After dropping null Goals:", df.shape)

    # 5. Remove rows that are completely empty (if any)
    df = df.dropna(how="all")

    # 6. Encode categorical features (Position) with LabelEncoder if exists
    le = None
    if "Position" in df.columns:
        le = LabelEncoder()
        # Fill Position NA temporarily with string 'Unknown' before encoding
        df["Position"] = df["Position"].fillna("Unknown")
        df["Position"] = le.fit_transform(df["Position"])
        print("Encoded 'Position' with LabelEncoder. Classes:", le.classes_)
    else:
        print("No 'Position' column. Skipping LabelEncoder.")

    # 7. Prepare features and target
    X = df.drop(columns=["Goals"])
    y = df["Goals"]

    # 8. Impute missing values in features using median
    imputer = SimpleImputer(strategy="median")
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)
    print("After imputation. Any nulls left:", X_imputed.isnull().sum().sum())

    # 9. Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)
    print("Train shape:", X_train.shape, "Test shape:", X_test.shape)

    # 10. Train model (Gradient Boosting)
    model = GradientBoostingRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # 11. Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = (mean_squared_error(y_test, y_pred))**0.5
    r2 = r2_score(y_test, y_pred)

    print("\\nModel performance:")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2: {r2:.4f}")

    # 12. Save artifacts
    joblib.dump(model, "model.pkl")
    joblib.dump(imputer, "imputer.pkl")
    if le is not None:
        joblib.dump(le, "label_encoder.pkl")

    print("Saved model.pkl, imputer.pkl, and label_encoder.pkl (if created).")

if __name__ == '__main__':
    main()
