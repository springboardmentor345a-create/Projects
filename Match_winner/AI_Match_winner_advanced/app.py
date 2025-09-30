import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import numpy as np
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Live Football Match Predictor",
    page_icon="⚽",
    layout="wide",
)

# --- MASTER TEAM LIST (USER DEFINED) ---
# This list now controls which teams appear in the app
ALLOWED_TEAMS = [
    "Arsenal", "Aston Villa", "Birmingham", "Blackburn", "Blackpool", "Bolton", "Bournemouth",
    "Bradford", "Brentford", "Brighton", "Burnley", "Cardiff", "Charlton", "Chelsea", "Coventry",
    "Crystal Palace", "Derby", "Everton", "Fulham", "Huddersfield", "Hull", "Ipswich", "Leeds",
    "Leicester", "Liverpool", "Luton", "Man City", "Man United", "Middlesbrough", "Newcastle",
    "Norwich", "Nott'm Forest", "Portsmouth", "QPR", "Reading", "Sheffield United", "Southampton",
    "Stoke", "Sunderland", "Swansea", "Tottenham", "Watford", "West Brom", "West Ham", "Wigan", "Wolves"
]

# --- TEAM LOGOS (COMPREHENSIVE & UPGRADED) ---
# This dictionary will be filtered based on the ALLOWED_TEAMS list
ALL_TEAM_LOGOS = {
    # Existing Teams with Aliases
    "Arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "Aston Villa": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282023%29.svg",
    "Bournemouth": "https://upload.wikimedia.org/wikipedia/en/e/e5/AFC_Bournemouth_%282013%29.svg",
    "Brentford": "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg",
    "Brighton": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
    "Brighton and Hove Albion": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
    "Chelsea": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    "Crystal Palace": "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg",
    "Everton": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
    "Fulham": "https://upload.wikimedia.org/wikipedia/en/e/eb/F.C._Fulham_crest.svg",
    "Liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
    "Man City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "Manchester City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "Man United": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
    "Manchester United": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
    "Newcastle": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    "Newcastle United": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    "Nott'm Forest": "https://upload.wikimedia.org/wikipedia/en/d/d2/Nottingham_Forest_F.C._logo.svg",
    "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/en/d/d2/Nottingham_Forest_F.C._logo.svg",
    "Tottenham": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
    "Tottenham Hotspur": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
    "West Ham": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    "West Ham United": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    "Wolves": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
    "Wolverhampton Wanderers": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
    "Burnley": "https://upload.wikimedia.org/wikipedia/en/6/62/Burnley_F.C._logo.svg",
    "Luton": "https://upload.wikimedia.org/wikipedia/en/8/8b/Luton_Town_FC_logo.svg",
    "Luton Town": "https://upload.wikimedia.org/wikipedia/en/8/8b/Luton_Town_FC_logo.svg",
    "Sheffield United": "https://upload.wikimedia.org/wikipedia/en/9/9c/Sheffield_United_FC_logo.svg",
    "Sheffield Utd": "https://upload.wikimedia.org/wikipedia/en/9/9c/Sheffield_United_FC_logo.svg",
    "Ipswich Town": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town.svg",
    "Ipswich": "https://upload.wikimedia.org/wikipedia/en/4/43/Ipswich_Town.svg",
    "Leicester City": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
    "Leicester": "https://upload.wikimedia.org/wikipedia/en/2/2d/Leicester_City_crest.svg",
    "Southampton": "https://upload.wikimedia.org/wikipedia/en/c/c9/Southampton_FC.svg",
    "Leeds United": "https://upload.wikimedia.org/wikipedia/en/5/54/Leeds_United_F.C._logo.svg",
    "Leeds": "https://upload.wikimedia.org/wikipedia/en/5/54/Leeds_United_F.C._logo.svg",
    "Norwich City": "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City.svg",
    "Norwich": "https://upload.wikimedia.org/wikipedia/en/8/8c/Norwich_City.svg",
    "Watford": "https://upload.wikimedia.org/wikipedia/en/e/e2/Watford.svg",
    "West Bromwich Albion": "https://upload.wikimedia.org/wikipedia/en/8/8b/West_Bromwich_Albion.svg",
    "West Brom": "https://upload.wikimedia.org/wikipedia/en/8/8b/West_Bromwich_Albion.svg",
    "Birmingham": "https://upload.wikimedia.org/wikipedia/en/6/68/Birmingham_City_FC_logo.svg",
    "Blackburn": "https://upload.wikimedia.org/wikipedia/en/0/0f/Blackburn_Rovers.svg",
    "Blackpool": "https://upload.wikimedia.org/wikipedia/en/d/df/Blackpool_FC_logo.svg",
    "Bolton": "https://upload.wikimedia.org/wikipedia/en/8/82/Bolton_Wanderers_FC_logo.svg",
    "Bradford": "https://upload.wikimedia.org/wikipedia/en/8/85/Bradford_City_AFC_logo.svg",
    "Cardiff": "https://upload.wikimedia.org/wikipedia/en/3/3c/Cardiff_City_crest.svg",
    "Charlton": "https://upload.wikimedia.org/wikipedia/en/5/5b/Charlton_Athletic.svg",
    "Coventry": "https://upload.wikimedia.org/wikipedia/en/9/94/Coventry_City_FC_logo.svg",
    "Derby": "https://upload.wikimedia.org/wikipedia/en/4/4a/Derby_County_crest.svg",
    "Huddersfield": "https://upload.wikimedia.org/wikipedia/en/5/5a/Huddersfield_Town_A.F.C._logo.svg",
    "Hull": "https://upload.wikimedia.org/wikipedia/en/4/4f/Hull_City_A.F.C._logo.svg",
    "Middlesbrough": "https://upload.wikimedia.org/wikipedia/en/2/2c/Middlesbrough_FC_crest.svg",
    "Portsmouth": "https://upload.wikimedia.org/wikipedia/en/3/3c/Portsmouth_FC_crest.svg",
    "QPR": "https://upload.wikimedia.org/wikipedia/en/3/31/Queens_Park_Rangers_crest.svg",
    "Reading": "https://upload.wikimedia.org/wikipedia/en/1/11/Reading_FC.svg",
    "Stoke": "https://upload.wikimedia.org/wikipedia/en/2/29/Stoke_City_FC.svg",
    "Sunderland": "https://upload.wikimedia.org/wikipedia/en/7/77/Sunderland_AFC_logo.svg",
    "Swansea": "https://upload.wikimedia.org/wikipedia/en/1/16/Swansea_City_AFC_logo.svg",
    "Wigan": "https://upload.wikimedia.org/wikipedia/en/4/43/Wigan_Athletic.svg",
}

# --- Filter the logos based on the allowed teams list ---
TEAM_LOGOS = {key: value for key, value in ALL_TEAM_LOGOS.items() if any(allowed in key for allowed in ALLOWED_TEAMS)}


# --- ASSET LOADING ---
@st.cache_resource
def load_assets():
    """Load all models, encoders, and the main dataset from disk."""
    try:
        script_dir = os.path.dirname(__file__)

        # Construct the full, absolute path to each asset file
        win_lose_model_path = os.path.join(script_dir, 'win_lose_model.pkl')
        draw_model_path = os.path.join(script_dir, 'draw_model.pkl')
        win_loss_encoders_path = os.path.join(script_dir, 'win_loss_encoders.pkl')
        draw_encoders_path = os.path.join(script_dir, 'draw_encoders.pkl')
        dataset_path = os.path.join(script_dir, 'full_feature_dataset_expanded.csv')

        # --- THE DEFINITIVE FIX: Use the full path variables ---
        with open(win_lose_model_path, 'rb') as file:
            win_lose_model = pickle.load(file)
        with open(draw_model_path, 'rb') as file:
            draw_model = pickle.load(file)
        with open(win_loss_encoders_path, 'rb') as file:
            win_loss_encoders = pickle.load(file)
        with open(draw_encoders_path, 'rb') as file:
            draw_encoders = pickle.load(file)
        
        df = pd.read_csv(dataset_path)
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        # Sort dataframe by date to easily find the latest matches
        df = df.sort_values('Date', ascending=False).reset_index(drop=True)
        return win_lose_model, draw_model, win_loss_encoders, draw_encoders, df
    except FileNotFoundError as e:
        st.error(f"Error loading asset file: {e}. Please make sure all .pkl and the .csv dataset are in the same folder.")
        return None, None, None, None, None

# --- LIVE DATA ENGINE ---
@st.cache_data(ttl=3600) # Cache the table for 1 hour
def fetch_live_epl_table():
    """Scrapes the live EPL table from a trusted source."""
    try:
        url = "https://www.bbc.com/sport/football/premier-league/table"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        tables = pd.read_html(response.content)
        df_table = tables[0]

        df_table['Team'] = df_table['Team'].str.replace(r'^\d+', '', regex=True).str.strip()
        rank_map = {row['Team']: row.name + 1 for _, row in df_table.iterrows()}
        
        name_corrections = {
            "Manchester United": "Man United", "Manchester City": "Man City", "Tottenham Hotspur": "Tottenham",
            "Wolverhampton Wanderers": "Wolves", "Nottingham Forest": "Nott'm Forest",
            "West Ham United": "West Ham", "Newcastle United": "Newcastle", "Brighton and Hove Albion": "Brighton"
        }
        corrected_rank_map = {name_corrections.get(team, team): rank for team, rank in rank_map.items()}
        return corrected_rank_map
    except Exception as e:
        st.error(f"Failed to fetch live league table. Using historical simulation. Error: {e}")
        return None

# --- NEW: Fallback Prediction Logic ---
def predict_with_ranks_only(live_rank_map, home_team, away_team):
    """A simple prediction logic for when no H2H data is available."""
    st.warning("⚠️ No historical H2H data found. A simplified prediction will be made based on current league rank.")
    
    if not live_rank_map:
        st.error("Could not fetch live league table, and no historical data exists. Cannot make a prediction.")
        return

    home_rank = live_rank_map.get(home_team, 21) # Default to a low rank
    away_rank = live_rank_map.get(away_team, 21)
    
    rank_difference = abs(home_rank - away_rank)
    
    # Define a threshold for what constitutes a "close" match
    DRAW_THRESHOLD = 5 
    
    with st.container(border=True):
        st.subheader('Final Verdict (Rank-Based)', anchor=False)
        
        # Remember: lower rank number is better
        if rank_difference > DRAW_THRESHOLD:
            if home_rank < away_rank:
                # Home team is significantly better
                logo_url = TEAM_LOGOS.get(home_team)
                _, center_col, _ = st.columns([1, 1, 1])
                if logo_url:
                    center_col.image(logo_url, width=150)
                center_col.success(f"🥇 Based on rank, a **{home_team}** win is likely.", icon="📈")
                st.balloons()
            else:
                # Away team is significantly better
                logo_url = TEAM_LOGOS.get(away_team)
                _, center_col, _ = st.columns([1, 1, 1])
                if logo_url:
                    center_col.image(logo_url, width=150)
                center_col.success(f"🥇 Based on rank, an **{away_team}** win is likely.", icon="📈")
                st.balloons()
        else:
            # Teams are closely ranked
            _, center_col, _ = st.columns([1, 1, 1])
            center_col.markdown("<h1 style='text-align: center;'>🤝</h1>", unsafe_allow_html=True)
            center_col.info(f"🤝 Teams are closely ranked. A **DRAW** is a likely outcome.", icon="⚖️")


with st.spinner('Loading advanced models and historical match data...'):
    assets = load_assets()

# --- HEADER ---
st.image("https://images.unsplash.com/photo-1579952363873-27f3bade9f55?q=80&w=2970", use_container_width=True)
st.title('Live Football Match Predictor')
st.markdown("### Harnessing AI to Forecast Premier League Outcomes")
st.markdown("---")

if all(a is not None for a in assets):
    win_lose_model, draw_model, win_loss_encoders, draw_encoders, df_final = assets
    
    live_ranks = fetch_live_epl_table()
    
    # --- DYNAMIC FEATURE ENGINEERING ENGINE ---
    def get_advanced_features(df, home_team, away_team, live_rank_map, num_matches_for_avg=5):
        relevant_matches = df[((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team))]
        if relevant_matches.empty:
            return None # CRUCIAL: This triggers the fallback logic

        recent_encounters = relevant_matches.head(num_matches_for_avg)
        h2h_feature_names = [col for col in df.columns if 'H2H' in col]
        odds_feature_names = [col for col in df.columns if 'Avg_Odds' in col]
        features_to_average = h2h_feature_names + odds_feature_names
        averaged_features = recent_encounters[features_to_average].mean().to_dict()

        latest_h2h_match = relevant_matches.iloc[0]
        form_diff_names = [col for col in df.columns if 'form' in col and 'diff' in col]
        form_diff_features = latest_h2h_match[form_diff_names].to_dict()

        if live_rank_map:
            home_rank = live_rank_map.get(home_team, 20)
            away_rank = live_rank_map.get(away_team, 20)
        else:
            st.warning("Using historical rank as a fallback.")
            temp_ranks = {team: i+1 for i, team in enumerate(df['HomeTeam'].unique())}
            home_rank = temp_ranks.get(home_team, 20)
            away_rank = temp_ranks.get(away_team, 20)

        home_team_matches = df[(df['HomeTeam'] == home_team) | (df['AwayTeam'] == home_team)]
        home_form_features = {}
        if not home_team_matches.empty:
            latest_match = home_team_matches.iloc[0]
            old_prefix = 'H_form_' if latest_match['HomeTeam'] == home_team else 'A_form_'
            new_prefix = 'H_form_'
            form_cols = [c for c in df.columns if c.startswith(old_prefix)]
            for col in form_cols:
                new_col_name = new_prefix + col[len(old_prefix):]
                home_form_features[new_col_name] = latest_match[col]

        away_team_matches = df[(df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team)]
        away_form_features = {}
        if not away_team_matches.empty:
            latest_match = away_team_matches.iloc[0]
            old_prefix = 'H_form_' if latest_match['HomeTeam'] == away_team else 'A_form_'
            new_prefix = 'A_form_'
            form_cols = [c for c in df.columns if c.startswith(old_prefix)]
            for col in form_cols:
                new_col_name = new_prefix + col[len(old_prefix):]
                away_form_features[new_col_name] = latest_match[col]

        final_features = {
            **home_form_features, **away_form_features, **form_diff_features,
            **averaged_features, 'HomeTeam_League_Rank': home_rank,
            'AwayTeam_League_Rank': away_rank, 'HomeTeam': home_team, 'AwayTeam': away_team
        }
        return pd.DataFrame([final_features])

    # --- UI & INPUTS ---
    with st.container(border=True):
        st.subheader("Select a Matchup", anchor=False)
        all_teams_from_df = sorted(list(set(df_final['HomeTeam'].unique()) | set(df_final['AwayTeam'].unique())))
        all_teams = [team for team in all_teams_from_df if team in ALLOWED_TEAMS]

        col1, col2 = st.columns(2)
        with col1:
            home_team = st.selectbox('Home Team', options=all_teams, index=all_teams.index("Man United") if "Man United" in all_teams else 0)
        with col2:
            away_team = st.selectbox('Away Team', options=all_teams, index=all_teams.index("Liverpool") if "Liverpool" in all_teams else 1)

    # --- PREDICTION LOGIC ---
    if st.button('🔮 Predict Outcome', type="primary", use_container_width=True):
        if home_team == away_team:
            st.warning("Please select two different teams.")
        else:
            with st.spinner(f"Calculating features for {home_team} vs {away_team}..."):
                input_df = get_advanced_features(df_final, home_team, away_team, live_ranks)

            # --- NEW: INTEGRATED FALLBACK LOGIC ---
            if input_df is None:
                # Trigger the simple prediction if no H2H data is found
                predict_with_ranks_only(live_ranks, home_team, away_team)
            else:
                # Proceed with the full AI prediction
                st.success("Generated advanced features! Making a prediction...")
                input_df_draw = input_df.copy()
                input_df_win_loss = input_df.copy()
                
                try:
                    draw_model_features = draw_model.get_booster().feature_names
                    input_df_draw['HomeTeam'] = draw_encoders['home_team'].transform(input_df_draw['HomeTeam'])
                    input_df_draw['AwayTeam'] = draw_encoders['away_team'].transform(input_df_draw['AwayTeam'])
                    input_df_draw = input_df_draw[draw_model_features]
                    
                    win_loss_model_features = win_lose_model.get_booster().feature_names
                    input_df_win_loss['HomeTeam'] = win_loss_encoders['home_team'].transform(input_df_win_loss['HomeTeam'])
                    input_df_win_loss['AwayTeam'] = win_loss_encoders['away_team'].transform(input_df_win_loss['AwayTeam'])
                    input_df_win_loss = input_df_win_loss[win_loss_model_features]
                except Exception as e:
                    st.error(f"An error occurred during data preparation: {e}")
                    st.stop()

                draw_proba = draw_model.predict_proba(input_df_draw)[0][1]
                win_loss_probs = win_lose_model.predict_proba(input_df_win_loss)[0]
                
                away_class_index = np.where(win_loss_encoders['y_encoder_wl'].classes_ == 'A')[0][0]
                home_class_index = np.where(win_loss_encoders['y_encoder_wl'].classes_ == 'H')[0][0]
                
                away_win_prob_conditional = win_loss_probs[away_class_index]
                home_win_prob_conditional = win_loss_probs[home_class_index]

                away_win_proba = away_win_prob_conditional * (1 - draw_proba)
                home_win_proba = home_win_prob_conditional * (1 - draw_proba)
                
                total_proba = home_win_proba + away_win_proba + draw_proba
                if total_proba == 0: total_proba = 1
                home_win_proba /= total_proba
                away_win_proba /= total_proba
                draw_proba /= total_proba
                
                with st.container(border=True):
                    st.subheader('🏆 Prediction Probabilities', anchor=False)
                    outcomes = {'Home Win': home_win_proba, 'Draw': draw_proba, 'Away Win': away_win_proba}
                    final_call = max(outcomes, key=outcomes.get)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label=f"P({home_team} Win)", value=f"{home_win_proba:.2%}")
                    with col2:
                        st.metric(label="P(Draw)", value=f"{draw_proba:.2%}")
                    with col3:
                        st.metric(label=f"P({away_team} Win)", value=f"{away_win_proba:.2%}")
                    
                    st.divider()
                    st.subheader('Final Verdict', anchor=False)
                    
                    if final_call == 'Home Win':
                        logo_url = TEAM_LOGOS.get(home_team)
                        _, center_col, _ = st.columns([1, 1, 1])
                        if logo_url:
                            center_col.image(logo_url, width=150)
                        center_col.success(f"🥇 The system predicts a **{home_team}** win!", icon="🎉")
                        st.balloons()
                    elif final_call == 'Away Win':
                        logo_url = TEAM_LOGOS.get(away_team)
                        _, center_col, _ = st.columns([1, 1, 1])
                        if logo_url:
                            center_col.image(logo_url, width=150)
                        center_col.success(f"🥇 The system predicts an **{away_team}** win!", icon="🎉")
                        st.balloons()
                    else: # Draw
                        _, center_col, _ = st.columns([1, 1, 1])
                        center_col.markdown("<h1 style='text-align: center;'>🤝</h1>", unsafe_allow_html=True)
                        center_col.info(f"🤝 The system predicts a **DRAW**.", icon="⚖️")
else:
    st.info('Select two teams and click "Predict Outcome" to see the AI in action.')

# --- NEW: Explanation Section ---
with st.expander("🔬 How does this work?"):
    st.markdown("""
    This prediction engine is more than just a model; it's a complete analytical pipeline that combines historical data with live, real-world information.
    
    **1. Live League Table:** The app scrapes the current, official Premier League table from the web. This gives the model the most accurate possible signal of a team's current standing.
    
    **2. True Team Form:** It calculates each team's recent form by analyzing their performance in their last few matches against *any* opponent, providing a sharp signal of current momentum.
    
    **3. Historical Context:** It looks at the history between the two selected teams, averaging their past Head-to-Head (H2H) stats and betting odds to establish a stable, long-term baseline.
    
    **4. AI Prediction:** These three distinct types of features are combined and fed into two specialized XGBoost models that work together to forecast the final outcome.
    
    **5. Graceful Fallback:** In cases where no direct historical data exists between two teams, the system automatically switches to a simplified prediction model based purely on their current league ranking.
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown("Developed with ❤️ by AKN. This is a portfolio project demonstrating advanced AI engineering concepts for Infosys Inernship.")

