# EPL Prediction App

## STREAMLIT APP DEPLOYED LINK
```bash
https://eplapp-hsz6wty4ealwyajj5awpfq.streamlit.app/
```

This Streamlit app allows you to predict:  

1. **Top Goal Scorer** – Predicts the number of goals a player is likely to score.  
2. **Match Winner** – Predicts the outcome of a match between two teams (Home Win, Away Win, or Draw).  

---

## Features

- Select prediction type from the **sidebar**.  
- **Top Goal Scorer**: Enter player stats and position to predict expected goals.  
- **Match Winner**: Enter home and away team stats side by side and predict match result.  
- Uses **one-hot encoding** for teams to match model training features.  
- **Dark mode** theme with blue highlights.  

---

## Requirements / Libraries

Make sure you have **Python 3.10+** installed. Install required libraries using `pip`:

```bash
pip install streamlit pandas numpy scikit-learn joblib
```
- **streamlit** – For creating the interactive web application interface  
- **pandas** – For data manipulation and analysis  
- **numpy** – For numerical computations  
- **scikit-learn** – For loading and using trained machine learning models  
- **joblib** – For loading serialized model files efficiently

## File Structure
```bash
Project/
│
├─ app.py                   # Main Streamlit app
├─ Top_Goal_Scorer/
│   └─ linear_regression_model.pkl
│   └─ Top_Goal_Scorer.ipynb
│   └─ Top Goals.csv
├─ Match_Winner/
│   └─ decision_tree_model.pkl
│   └─ Match_Winner.ipynb
│   └─ Match_winner.csv
└─ .streamlit/
    └─ config.toml          # Streamlit theme configuration
```
## How to Run the App
Navigate to the project folder in your terminal:
```bash
cd path/to/your_project
```
## Run the Streamlit app:
```bash
streamlit run app.py
```