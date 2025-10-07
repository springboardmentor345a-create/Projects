import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from io import BytesIO

# --- Configuration and Caching ---
st.set_page_config(
    page_title="ScoreSight EPL Goal Predictor", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Hardcoded Model Performance (from your notebook results)
MAE_SCORE = 0.6020
R2_SCORE = 0.9530

# Use st.cache_data to cache the data loading, processing, and model training
@st.cache_data(show_spinner="Training Model and Preparing Data...")
def load_and_prepare_data(csv_file="topgoals.csv"):
    """Loads, cleans, preprocesses data, and trains the GBR model."""
    try:
        # NOTE: In a real deployment, you would ensure topgoals.csv is available
        df = pd.read_csv(csv_file)
    except Exception:
        # Fallback in case the file is not found (important for cloud deployment testing)
        st.error("Could not find 'topgoals.csv'. Please ensure it's in the root directory.")
        return None, None, None, None, None

    # --- Data Cleaning and Feature Engineering (Matching Notebook) ---
    TARGET = 'Goals'
    # Drop columns identified as leakage or irrelevant in the notebook
    DROP_COLS = [
        'Rank', 'Player', 'Club', 'Season', 'Non-Penalty_Goals',
        'Club_League_Rank', 'Club_Total_Goals', 'League_Goals_per_Match'
    ]
    
    df_cleaned = df.drop(columns=[col for col in DROP_COLS if col in df.columns])

    # Impute Missing Values
    numeric_cols = df_cleaned.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df_cleaned.select_dtypes(include='object').columns.tolist()

    imputer_numeric = SimpleImputer(missing_values=np.nan, strategy='median')
    df_cleaned[numeric_cols] = imputer_numeric.fit_transform(df_cleaned[numeric_cols])

    for col in categorical_cols:
        imputer_cat = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
        df_cleaned[col] = imputer_cat.fit_transform(df_cleaned[[col]])[:, 0]

    # One-Hot Encoding for 'Position'
    df_encoded = pd.get_dummies(df_cleaned, columns=categorical_cols, drop_first=True)

    # Define X and y
    X = df_encoded.drop(columns=[TARGET])
    y = df_encoded[TARGET]
    
    # Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Scaling (GBR often doesn't require scaling, but we scale for input consistency)
    scaler = StandardScaler()
    numeric_features_to_scale = X_train.select_dtypes(include=np.number).columns.tolist()
    X_train[numeric_features_to_scale] = scaler.fit_transform(X_train[numeric_features_to_scale])
    
    # --- Train the Gradient Boosting Regressor ---
    gbr = GradientBoostingRegressor(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        random_state=42
    )
    gbr.fit(X_train, y_train)
    
    # Store average values for comparison charts
    average_stats = df_cleaned[numeric_cols].mean().to_dict()

    return gbr, scaler, numeric_features_to_scale, X.columns.tolist(), average_stats

# --- Load cached data ---
model, scaler, numeric_features, feature_names, average_stats = load_and_prepare_data()

if model is None:
    st.stop()


# --- Streamlit UI: Enhanced Layout and Visuals ---

st.title("🎯 ScoreSight: EPL Top Scorer Predictor")
st.markdown("An ML application built during my Infosys Internship to predict a player's seasonal goal tally using a **Gradient Boosting Regressor**.")
st.markdown("---")

# Mentor Feedback: UI Layout - Use Sidebar for Inputs, Main Area for Results
st.sidebar.header("Player Profile & Season Expectations")
st.sidebar.markdown("Adjust the input features below to predict a player's goal total.")


# --- Sidebar Inputs ---

position = st.sidebar.selectbox(
    "Player Position",
    ['Forward', 'Midfielder', 'Attacking Midfielder', 'Winger'],
    index=0
)
big_6_feature = st.sidebar.selectbox(
    "Plays for a 'Big 6' Club?",
    options=['Yes', 'No'],
    index=0
)
is_big_6 = 1 if big_6_feature == 'Yes' else 0

st.sidebar.subheader("Performance Inputs")

col_a, col_b = st.sidebar.columns(2)

with col_a:
    age = st.number_input("Age", 18, 40, 25)
    goals_prev_season = st.number_input("Goals (Prev. Season)", 0, 40, 15)
    goals_per_90 = st.number_input("Goals per 90", 0.0, 1.5, 0.5, step=0.01)

with col_b:
    appearances = st.number_input("Appearances (Expected)", 1, 38, 30)
    minutes = st.number_input("Minutes Played", 100, 3420, 2500)
    assists = st.number_input("Assists (Expected)", 0, 25, 5)

st.sidebar.subheader("Contextual Inputs")
col_c, col_d = st.sidebar.columns(2)

with col_c:
    penalty_goals = st.number_input("Expected Penalty Goals", 0, 15, 1)

with col_d:
    goals_last_3_avg = st.number_input("Goals (Last 3 Avg)", 0.0, 35.0, 12.0, step=0.1)
    
# Games_in_Season is fixed based on EPL format but included for feature consistency
games_in_season = 38.0 


# --- Prediction Button and Logic ---
if st.sidebar.button("RUN PREDICTION", type="primary"):
    
    # 1. Prepare Input Data
    input_data = {
        'Age': age,
        'Appearances': appearances,
        'Minutes_Played': minutes,
        'Goals_prev_season': goals_prev_season,
        'Assists': assists,
        'Penalty_Goals': penalty_goals,
        'Goals_per_90': goals_per_90,
        'Big_6_Club_Feature': is_big_6,
        'Games_in_Season': games_in_season,
        'Goals_last_3_seasons_avg': goals_last_3_avg
    }
    input_df = pd.DataFrame([input_data])

    # 2. Handle OHE for Position
    position_cols = [col for col in feature_names if col.startswith('Position_')]
    for col in position_cols:
        input_df[col] = 0
    pos_col_name = f'Position_{position}'
    if pos_col_name in feature_names:
        input_df[pos_col_name] = 1
    
    # 3. Ensure all features are present and in the correct order
    for col in feature_names:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_names]

    # 4. Scale Data
    input_df_scaled = input_df.copy()
    input_df_scaled[numeric_features] = scaler.transform(input_df[numeric_features])
    
    # 5. Predict
    prediction = model.predict(input_df_scaled)[0]
    predicted_goals = max(0, round(prediction))
    
    st.subheader("Results and Analysis")
    st.markdown("---")

    # Mentor Feedback: Visual Element (Metric Card and Model Performance)
    col_met1, col_met2, col_met3 = st.columns(3)
    
    with col_met1:
        st.metric(
            label="Predicted Goals Tally ⚽", 
            value=f"{predicted_goals}", 
            delta=f"Raw Model Output: {prediction:.2f}"
        )

    with col_met2:
        st.metric(label="Model R² Score (Test Set)", value=f"{R2_SCORE:.4f}", help="Indicates the model explains 95.30% of the variance.")
        
    with col_met3:
        st.metric(label="Model MAE (Test Set)", value=f"{MAE_SCORE:.4f}", help="Mean Absolute Error: On average, the prediction is off by only 0.6 goals.")

    # Status/Tier based on prediction
    if predicted_goals >= 25:
        st.success("👑 Golden Boot Contender! This player has the stats for an elite season.")
    elif predicted_goals >= 15:
        st.info("⭐ Top Scorer Candidate! Expect a strong contribution.")
    elif predicted_goals >= 8:
        st.warning("🤝 Key Contributor! Solid, but not expected to lead the charts.")
    else:
        st.error("📉 Low Goal Expectation based on inputs.")

    st.markdown("---")

    # Mentor Feedback: Feature Display / Visual Element (Comparison Chart)
    st.subheader("Player Stats vs. EPL Historical Average")
    st.markdown("Visualizing key input features against the average of all top scorers in the dataset.")
    
    # Create comparison data for the chart
    input_stats = {k: v for k, v in input_data.items() if k in average_stats}
    
    # Prepare data for plotting
    comp_df = pd.DataFrame({
        'Metric': list(input_stats.keys()),
        'Player Value': list(input_stats.values()),
        'EPL Average': [average_stats[k] for k in input_stats.keys()]
    })
    
    # Melt the data for Streamlit's built-in charting (altair/matplotlib compatibility)
    comp_df_melted = comp_df.melt('Metric', var_name='Type', value_name='Value')

    # Matplotlib chart for better control and aesthetics
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='Metric', 
        y='Value', 
        hue='Type', 
        data=comp_df_melted, 
        palette={'Player Value': '#0070c0', 'EPL Average': '#FF5733'},
        ax=ax
    )
    ax.set_title('Key Performance Indicators Comparison', fontsize=16)
    ax.set_xlabel('')
    ax.set_ylabel('Value', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Value Type')
    plt.tight_layout()
    st.pyplot(fig)
