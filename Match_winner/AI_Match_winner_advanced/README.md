Live Premier League Match Predictor

🏆 Project Overview
This is an advanced AI-powered web application built to predict the outcomes of English Premier League football matches developed by Arvind K N as a part of the infosys internship. It moves beyond simple historical analysis by integrating a live data pipeline, fetching the current league table in real-time to provide the most accurate, context-aware predictions possible.

This project was developed as a demonstration of a complete, end-to-end MLOps (Machine Learning Operations) workflow, from data engineering and model training to deployment and front-end design.

✨ Key Features
Live Data Integration: The application automatically scrapes the official Premier League table, ensuring predictions are based on the most up-to-date team standings.

Sophisticated Feature Engineering: It employs a hybrid feature strategy, combining:

Live League Rank: The most powerful signal of a team's current standing.

True Team Form: Calculated from a team's most recent matches.

Historical Context: Averaged Head-to-Head (H2H) stats and betting odds provide a stable baseline.

Dual-Model Architecture: A specialized two-model system (a "Draw-Finder" and a "Winner-Picker") works in tandem to produce nuanced, three-way predictions (Home Win, Away Win, Draw).

Professional UI/UX: A clean, intuitive, and visually engaging user interface built with Streamlit, providing a delightful user experience.

🛠️ Technology Stack
Backend & Modeling: Python, Pandas, Scikit-learn, XGBoost

Frontend: Streamlit

Data Pipeline: Requests, BeautifulSoup4

🚀 How to Run Locally
Clone the repository:

git clone <your-repo-link>
cd <your-repo-name>

Create and activate a Conda environment:

conda create --name predictor_env python=3.11
conda activate predictor_env

Install the required libraries:

pip install -r requirements.txt

Run the application:

streamlit run app.py
or run the appliocation via this link: https://akn-football-predictor.streamlit.app/
