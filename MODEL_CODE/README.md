# Football Goals Predictor

This Flask app predicts number of goals based on player features.

## Contents

- `train_model.py` - full data cleaning + training script. Produces `model.pkl`, `imputer.pkl`, and `label_encoder.pkl`.
- `app.py` - Flask web app that loads artifacts and provides a UI to enter features for prediction.
- `templates/index.html` - HTML for the UI.
- `static/style.css` - simple CSS.
- `requirements.txt` - Python dependencies for deployment.
- `features.txt` - feature names used by the app (generated after training).

## How to train locally (optional)
1. Put `newupdatedgoals.csv` in the project root.
2. Run `python3 train_model.py`
3. This creates `model.pkl`, `imputer.pkl`, `label_encoder.pkl` (if Position present), and `features.txt`.

## Deploy on Render
1. Push this repository to GitHub.
2. Create a Web Service on Render and connect the repo.
3. Use the default build; Start Command: `gunicorn app:app`
4. Ensure `newupdatedgoals.csv` is NOT needed on the server (we used artifacts).

