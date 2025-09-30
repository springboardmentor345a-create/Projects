# EPL Prediction Hub

## Overview
AI-powered Premier League prediction application with machine learning models for goal scoring and match outcome predictions.

## Project Structure

### Core Application
- **Flask Web App** running on port 5000
- **Two ML Models**:
  1. Goal Scorer Prediction (Gradient Boosting Regressor)
  2. Match Winner Prediction (Random Forest Classifier)

### Key Features
1. **Landing Page**: Modern UI with two prediction options
2. **Goal Scorer Prediction**: Predicts season goals based on player stats
3. **Match Winner Prediction**: Predicts match outcomes (Home/Away/Draw)

## Technical Stack
- Python 3.11
- Flask 2.2.5
- scikit-learn 1.2.2
- pandas 2.2.2
- numpy 1.25.2
- gunicorn 20.1.0 (production server)

## Model Files
- `model.pkl` - Goal scorer prediction model
- `imputer.pkl` - Data imputer for missing values
- `label_encoder.pkl` - Encodes player positions
- `match_winner_model.pkl` - Match outcome prediction model
- `match_label_encoders.pkl` - Encodes team names and categorical data
- `features.txt` - Goal scorer feature list
- `match_features.txt` - Match prediction feature list
- `teams.json` - EPL teams database

## Deployment

### Development (Replit)
- Workflow configured to run Flask app on port 5000
- Access via Replit webview

### Production (Render)
- Complete deployment package in `render_deployment/` folder
- Includes comprehensive deployment guide
- Uses gunicorn as production WSGI server
- See `render_deployment/DEPLOYMENT_GUIDE.md` for detailed instructions

## Training Models
- `train_model.py` - Trains goal scorer model
- `train_match_winner.py` - Trains match winner model
- `every_match.csv` - Historical match data (9,380 matches)
- `newupdatedgoals.csv` - Player statistics data

## Recent Changes
- 2025-09-30: Major redesign with dual prediction features
- Added match winner prediction capability
- Implemented modern gradient UI with purple theme
- Created comprehensive Render deployment package
- Separated predictions into dedicated pages with navigation

## Architecture
```
/
├── app.py                    # Main Flask application
├── templates/                # HTML templates
│   ├── home.html            # Landing page
│   ├── goal_scorer.html     # Goal prediction form
│   └── match_winner.html    # Match prediction form
├── static/
│   └── style.css            # Modern CSS with gradients
├── [model files]            # ML models and encoders
└── render_deployment/       # Production deployment package
```

## User Preferences
- Modern, gradient-based UI design
- Responsive layout for mobile and desktop
- Clean, professional aesthetic
- Clear call-to-action buttons
