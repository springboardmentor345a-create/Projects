# EPL Prediction Hub

AI-powered Premier League prediction application with machine learning models.

## Features

- **Goal Scorer Prediction**: Predict how many goals a player will score based on their statistics
- **Match Winner Prediction**: Predict match outcomes (Home Win/Away Win/Draw) based on team statistics

## Tech Stack

- Python 3.11
- Flask 2.2.5
- scikit-learn 1.2.2
- pandas, numpy
- gunicorn (production server)

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
python app.py
```

3. Open http://localhost:5000

## Deploy on Render

1. Push this repository to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Render will automatically detect the configuration from:
   - `requirements.txt` - Python dependencies
   - `Procfile` - Start command
   - `runtime.txt` - Python version

5. Click "Deploy"

Your app will be live at `https://your-app-name.onrender.com`

## Project Structure

```
/
├── app.py                    # Flask application
├── templates/                # HTML templates
│   ├── home.html            # Landing page
│   ├── goal_scorer.html     # Goal prediction
│   └── match_winner.html    # Match prediction
├── static/
│   └── style.css            # Styles
├── model.pkl                # Goal scorer ML model
├── match_winner_model.pkl   # Match winner ML model
├── requirements.txt         # Dependencies
└── Procfile                 # Render start command
```
