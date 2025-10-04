# import streamlit as st
# import pandas as pd
# import joblib
# from tensorflow.keras.models import load_model
# import plotly.graph_objects as go
# import plotly.express as px

# # -----------------------------
# # Page Configuration
# # -----------------------------
# st.set_page_config(
#     page_title="Premier League Predictor",
#     page_icon="⚽",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # -----------------------------
# # Custom CSS for Better Styling
# # -----------------------------
# st.markdown("""
#     <style>
#     /* Animated Football Background */
#     .stApp {
#         background-image: url('https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1920');
#         background-size: cover;
#         background-position: center;
#         background-attachment: fixed;
#         background-repeat: no-repeat;
#     }
    
#     .stApp::before {
#         content: '';
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background: rgba(255, 255, 255, 0.50);  /* Adjust opacity: 0.92 = 92% white, lower = more visible background */
#         backdrop-filter: blur(2px);  /* BLUR STRENGTH: Increase number for more blur (try 12px, 15px) */
#         z-index: 0;
#         pointer-events: none;
#     }
    
#     .main {
#         padding: 0rem 1rem;
#         position: relative;
#         z-index: 1;
#     }
    
#     /* Celebration Animation */
#     @keyframes confetti-fall {
#         0% {
#             transform: translateY(100vh) rotate(0deg);
#             opacity: 1;
#         }
#         100% {
#             transform: translateY(-10vh) rotate(720deg);
#             opacity: 0;
#         }
#     }
    
#     @keyframes trophy-bounce {
#         0%, 100% { transform: translateY(0) scale(1); }
#         50% { transform: translateY(-20px) scale(1.1); }
#     }
    
#     .celebration-container {
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         pointer-events: none;
#         z-index: 9999;
#         overflow: hidden;
#     }
    
#     .confetti {
#         position: absolute;
#         width: 15px;
#         height: 15px;
#         animation: confetti-fall 4s linear infinite;
#     }
    
#     .trophy-float {
#         animation: trophy-bounce 2s ease-in-out infinite;
#         display: inline-block;
#     }
    
#     .stButton>button {
#         width: 100%;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         font-weight: bold;
#         border-radius: 10px;
#         padding: 0.75rem;
#         font-size: 1.1rem;
#         border: none;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         transition: all 0.3s ease;
#     }
#     .stButton>button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
#     }
#     .prediction-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 2rem;
#         border-radius: 15px;
#         color: white;
#         text-align: center;
#         box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
#         margin: 1rem 0;
#     }
#     .metric-card {
#         background: rgba(255, 255, 255, 0.95);
#         padding: 1.5rem;
#         border-radius: 10px;
#         box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
#         border-left: 4px solid #667eea;
#         backdrop-filter: blur(10px);
#     }
#     .info-box {
#         background: rgba(240, 242, 246, 0.95);
#         padding: 1rem;
#         border-radius: 8px;
#         border-left: 4px solid #38003c;
#         margin: 1rem 0;
#         color: #38003c;
#         font-weight: 500;
#         backdrop-filter: blur(10px);
#     }
#     h1 {
#         color: #38003c;
#         font-weight: 700;
#     }
#     .stTabs [data-baseweb="tab-list"] {
#         gap: 2rem;
#         background: rgba(255, 255, 255, 0.8);
#         backdrop-filter: blur(10px);
#         border-radius: 10px;
#         padding: 0.5rem;
#     }
#     .stTabs [data-baseweb="tab"] {
#         padding: 1rem 2rem;
#         font-size: 1.1rem;
#         font-weight: 600;
#         background: transparent;
#     }
    
#     /* Sidebar styling */
#     [data-testid="stSidebar"] {
#         background: rgba(255, 255, 255, 0.95);
#         backdrop-filter: blur(10px);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # Load models and scaler
# # -----------------------------
# @st.cache_resource
# def load_models():
#     try:
#         nn_model = load_model("nn_smote_model.keras")
#         scaler = joblib.load("scaler.pkl")
#         top_assists_model = joblib.load("top_assists.pkl")
#         return nn_model, scaler, top_assists_model
#     except Exception as e:
#         st.error(f"Error loading models: {e}")
#         return None, None, None

# nn_model, scaler, top_assists_model = load_models()

# # -----------------------------
# # Header
# # -----------------------------
# st.markdown("<h1 style='text-align: center; color: #white;'>⚽ Premier League AI Predictor</h1>", unsafe_allow_html=True)
# st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Predict league winners and top assist makers using advanced ML models</p>", unsafe_allow_html=True)
# st.markdown("---")

# # -----------------------------
# # Sidebar Information
# # -----------------------------
# with st.sidebar:
#     st.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/1200px-Premier_League_Logo.svg.png", width=200)
#     st.markdown("### 📊 About the Models")
#     st.info("""
#     **League Winner Model:**
#     - Neural Network (Deep Learning)
#     - Trained on historical PL data
#     - 95%+ accuracy
    
#     **Top Assists Model:**
#     - Advanced regression model
#     - Considers 20+ features
#     - Player performance prediction
#     """)
    
#     st.markdown("### 📖 Quick Guide")
#     st.markdown("""
#     1. Select prediction type
#     2. Enter team/player stats
#     3. Click predict button
#     4. View results & insights
#     """)

# # -----------------------------
# # Main Content - Tabs
# # -----------------------------
# tab1, tab2 = st.tabs(["🏆 League Winner", "🅰️ Top Assists"])

# # -----------------------------
# # TAB 1: League Winner Prediction
# # -----------------------------
# with tab1:
#     st.markdown("### Predict League Champion")
#     st.markdown("<div class='info-box'>Enter the team's season statistics to predict championship probability</div>", unsafe_allow_html=True)
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.markdown("#### 📋 Match Statistics")
        
#         # Row 1: Basic Stats
#         c1, c2, c3, c4 = st.columns(4)
#         with c1:
#             played = st.number_input("🎮 Matches Played", 0, 42, 38, help="Total matches played in the season")
#         with c2:
#             won = st.number_input("✅ Wins", 0, 42, 28, help="Number of matches won")
#         with c3:
#             drawn = st.number_input("🤝 Draws", 0, 42, 6, help="Number of matches drawn")
#         with c4:
#             lost = st.number_input("❌ Losses", 0, 42, 4, help="Number of matches lost")
        
#         st.markdown("#### ⚽ Goal Statistics")
        
#         # Row 2: Goal Stats
#         g1, g2, g3 = st.columns(3)
#         with g1:
#             gf = st.number_input("🎯 Goals For", 0, 200, 89, help="Total goals scored")
#         with g2:
#             ga = st.number_input("🛡️ Goals Against", 0, 200, 33, help="Total goals conceded")
#         with g3:
#             gd = st.number_input("📊 Goal Difference", -100, 200, 56, help="GF - GA")
        
#         # Calculate Points
#         points = (won * 3) + drawn
        
#         st.markdown("---")
#         st.markdown(f"**📈 Calculated Points:** `{points}`")
        
#         predict_btn = st.button("🔮 Predict Championship Probability", use_container_width=True)
    
#     with col2:
#         st.markdown("#### 📊 Quick Stats")
#         st.metric("Win Rate", f"{(won/played*100):.1f}%")
#         st.metric("Total Points", points)
#         st.metric("Goals/Match", f"{(gf/played):.2f}")
#         st.metric("Clean Sheets", f"~{int((played-ga/1.5))}")
    
#     # Prediction Results
#     if predict_btn:
#         if nn_model and scaler:
#             with st.spinner("🔄 Analyzing team performance..."):
#                 input_data = pd.DataFrame(
#                     [[played, won, drawn, lost, gf, ga, gd]],
#                     columns=['played', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd']
#                 )
#                 input_scaled = scaler.transform(input_data)
                
#                 nn_prob = float(nn_model.predict(input_scaled, verbose=0)[0][0])
                
#                 st.markdown("---")
#                 st.markdown("### 🎯 Prediction Results")
                
#                 # Result Card
#                 result_emoji = "🏆" if nn_prob >= 0.5 else "❌"
#                 result_text = "CHAMPION" if nn_prob >= 0.5 else "NOT CHAMPION"
#                 result_color = "#28a745" if nn_prob >= 0.5 else "#dc3545"
                
#                 # Add celebration animation if champion
#                 if nn_prob >= 0.5:
#                     st.markdown("""
#                         <div class="celebration-container" id="celebration">
#                             <script>
#                                 function createConfetti() {
#                                     const colors = ['#FFD700', '#FFA500', '#FF6347', '#4169E1', '#32CD32', '#FF1493'];
#                                     const shapes = ['⚽', '🏆', '⭐', '🎉', '🎊', '✨'];
#                                     const container = document.getElementById('celebration');
                                    
#                                     for (let i = 0; i < 50; i++) {
#                                         setTimeout(() => {
#                                             const confetti = document.createElement('div');
#                                             confetti.className = 'confetti';
#                                             confetti.innerHTML = shapes[Math.floor(Math.random() * shapes.length)];
#                                             confetti.style.left = Math.random() * 100 + '%';
#                                             confetti.style.fontSize = (Math.random() * 20 + 20) + 'px';
#                                             confetti.style.animationDelay = (Math.random() * 2) + 's';
#                                             confetti.style.animationDuration = (Math.random() * 2 + 3) + 's';
#                                             container.appendChild(confetti);
                                            
#                                             setTimeout(() => confetti.remove(), 6000);
#                                         }, i * 100);
#                                     }
#                                 }
#                                 createConfetti();
#                             </script>
#                         </div>
#                     """, unsafe_allow_html=True)
                
#                 st.markdown(f"""
#                     <div style='background: {result_color}; padding: 2rem; border-radius: 15px; text-align: center; color: white; position: relative; z-index: 10;'>
#                         <h1 style='color: white; margin: 0;'><span class='{"trophy-float" if nn_prob >= 0.5 else ""}'>{result_emoji}</span> {result_text}</h1>
#                         <h2 style='color: white; margin-top: 1rem;'>{nn_prob*100:.1f}% Probability</h2>
#                     </div>
#                 """, unsafe_allow_html=True)
                
#                 st.markdown("")
                
#                 # Model Display
#                 col_a, col_b = st.columns(2)
#                 with col_a:
#                     st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                     st.metric("Neural Network Prediction", f"{nn_prob*100:.1f}%")
#                     st.markdown("</div>", unsafe_allow_html=True)
#                 with col_b:
#                     st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                     confidence = "High" if abs(nn_prob - 0.5) > 0.3 else "Medium" if abs(nn_prob - 0.5) > 0.15 else "Low"
#                     st.metric("Confidence Level", confidence)
#                     st.markdown("</div>", unsafe_allow_html=True)
                
#                 # Visualization
#                 fig = go.Figure()
                
#                 fig.add_trace(go.Bar(
#                     name='Championship',
#                     x=['Prediction'],
#                     y=[nn_prob*100],
#                     marker_color='#38003c',
#                     text=[f'{nn_prob*100:.1f}%'],
#                     textposition='auto',
#                     width=0.4
#                 ))
                
#                 fig.add_trace(go.Bar(
#                     name='Not Champion',
#                     x=['Prediction'],
#                     y=[(1-nn_prob)*100],
#                     marker_color='#e90052',
#                     text=[f'{(1-nn_prob)*100:.1f}%'],
#                     textposition='auto',
#                     width=0.4
#                 ))
                
#                 fig.update_layout(
#                     title="Championship Probability",
#                     yaxis_title="Probability (%)",
#                     barmode='group',
#                     height=400,
#                     plot_bgcolor='rgba(0,0,0,0)',
#                     paper_bgcolor='rgba(0,0,0,0)',
#                 )
                
#                 st.plotly_chart(fig, use_container_width=True)
                
#                 # Insights
#                 st.markdown("#### 💡 Key Insights")
#                 insights = []
#                 if points >= 90:
#                     insights.append("✅ Excellent point total for a champion")
#                 elif points >= 80:
#                     insights.append("⚠️ Good points, but may need more for the title")
#                 else:
#                     insights.append("❌ Points total typically below championship level")
                
#                 if gd >= 50:
#                     insights.append("✅ Outstanding goal difference")
#                 elif gd >= 30:
#                     insights.append("⚠️ Decent goal difference")
#                 else:
#                     insights.append("❌ Goal difference needs improvement")
                
#                 if won/played >= 0.7:
#                     insights.append("✅ Dominant win rate")
#                 else:
#                     insights.append("⚠️ Win rate could be higher")
                
#                 for insight in insights:
#                     st.markdown(f"- {insight}")

# # -----------------------------
# # TAB 2: Top Assists Prediction
# # -----------------------------
# with tab2:
#     st.markdown("### Predict Player Assists for Next Season")
#     st.markdown("<div class='info-box'>Enter comprehensive player statistics to predict expected assists next season</div>", unsafe_allow_html=True)
    
#     # Organize inputs into logical sections
#     with st.form("top_assists_form"):
#         st.markdown("#### 👤 Player Information")
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             age = st.number_input("Age", 16, 40, 25, help="Player's age")
#         with col2:
#             position = st.selectbox("Position", ["Forward", "Midfielder", "Defender", "Goalkeeper"], help="Playing position")
#             position_num = {"Forward": 1, "Midfielder": 2, "Defender": 3, "Goalkeeper": 4}[position]
#         with col3:
#             minutes_played = st.number_input("Minutes Played", 0, 3800, 2800, help="Total minutes played")
        
#         st.markdown("#### 📊 Previous Season Stats")
#         col4, col5, col6 = st.columns(3)
        
#         with col4:
#             assists_prev = st.number_input("Previous Assists", 0, 30, 8, help="Assists last season")
#         with col5:
#             goals_prev = st.number_input("Previous Goals", 0, 50, 5, help="Goals last season")
#         with col6:
#             key_passes = st.number_input("Key Passes", 0, 200, 60, help="Total key passes")
        
#         st.markdown("#### 🎯 Advanced Metrics")
#         col7, col8, col9 = st.columns(3)
        
#         with col7:
#             expected_assists = st.number_input("Expected Assists (xA)", 0.0, 30.0, 7.5, 0.1, help="xA metric")
#         with col8:
#             dribbles_completed = st.number_input("Dribbles Completed", 0, 300, 80, help="Successful dribbles")
#         with col9:
#             shots_assisted = st.number_input("Shots Assisted", 0, 200, 70, help="Shots created")
        
#         st.markdown("#### 🏟️ Team Context")
#         col10, col11, col12, col13 = st.columns(4)
        
#         with col10:
#             set_piece_involvement = st.number_input("Set Piece Inv.", 0, 100, 25, help="Set piece contributions")
#         with col11:
#             club_total_goals = st.number_input("Club Total Goals", 0, 150, 75, help="Team's total goals")
#         with col12:
#             club_league_rank = st.number_input("Club Rank", 1, 20, 4, help="Team's league position")
#         with col13:
#             big6_club = st.selectbox("Big 6 Club?", ["Yes", "No"], help="Playing for top 6 club")
#             big6_num = 1 if big6_club == "Yes" else 0
        
#         st.markdown("#### 📈 Per 90 & Ratio Stats")
#         col14, col15, col16 = st.columns(3)
        
#         with col14:
#             club_attack_share = st.slider("Club Attack Share (%)", 0.0, 100.0, 15.0, 0.5, help="% of team's attacks")
#         with col15:
#             club_xg = st.number_input("Club xG", 0.0, 100.0, 65.0, 0.5, help="Team's expected goals")
#         with col16:
#             assists_per_90 = st.number_input("Assists per 90", 0.0, 2.0, 0.25, 0.01, help="Assists per 90 mins")
        
#         col17, col18, col19, col20 = st.columns(4)
        
#         with col17:
#             goals_per_90 = st.number_input("Goals per 90", 0.0, 2.0, 0.15, 0.01)
#         with col18:
#             contribution_ratio = st.number_input("Contribution Ratio", 0.0, 5.0, 0.35, 0.01, help="Goal involvement ratio")
#         with col19:
#             dribbles_per_90 = st.number_input("Dribbles per 90", 0.0, 10.0, 2.5, 0.1)
#         with col20:
#             shots_assisted_per_90 = st.number_input("Shots Assisted per 90", 0.0, 10.0, 2.2, 0.1)
        
#         st.markdown("---")
#         submitted = st.form_submit_button("🔮 Predict Next Season Assists", use_container_width=True)
        
#         if submitted:
#             if top_assists_model:
#                 with st.spinner("🔄 Analyzing player data..."):
#                     input_values = [
#                         age, position_num, minutes_played, assists_prev, goals_prev,
#                         key_passes, expected_assists, dribbles_completed, shots_assisted,
#                         set_piece_involvement, club_total_goals, club_league_rank, big6_num,
#                         club_attack_share, club_xg, assists_per_90, goals_per_90,
#                         contribution_ratio, dribbles_per_90, shots_assisted_per_90
#                     ]
                    
#                     top_assists_cols = [
#                         'Age', 'Position', 'Minutes_Played', 'Assists_prev_season',
#                         'Goals_prev_season', 'Key_Passes', 'Expected_Assists_(xA)',
#                         'Dribbles_Completed', 'Shots_Assisted', 'Set_Piece_Involvement',
#                         'Club_Total_Goals', 'Club_League_Rank', 'Big6_Club_Feature',
#                         'Club_Attack_Share', 'Club_xG', 'Assists_per_90', 'Goals_per_90',
#                         'Contribution_Ratio', 'Dribbles_per_90', 'Shots_Assisted_per_90'
#                     ]
                    
#                     input_df = pd.DataFrame([input_values], columns=top_assists_cols)
#                     prediction = float(top_assists_model.predict(input_df)[0])
                    
#                     st.markdown("---")
#                     st.markdown("### 🎯 Prediction Results")
                    
#                     # Result visualization
#                     st.markdown(f"""
#                         <div style='background: linear-gradient(135deg, #38003c 0%, #e90052 100%); 
#                                     padding: 2rem; border-radius: 15px; text-align: center; color: white;'>
#                             <h1 style='color: white; margin: 0;'>🅰️ Predicted Assists</h1>
#                             <h2 style='color: white; margin-top: 1rem; font-size: 3rem;'>{prediction:.1f}</h2>
#                             <p style='color: white; opacity: 0.9;'>Expected assists for next season</p>
#                         </div>
#                     """, unsafe_allow_html=True)
                    
#                     st.markdown("")
                    
#                     # Performance categories
#                     col_p1, col_p2, col_p3 = st.columns(3)
#                     with col_p1:
#                         st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                         st.metric("Performance Level", 
#                                  "Elite" if prediction >= 12 else "Good" if prediction >= 8 else "Average")
#                         st.markdown("</div>", unsafe_allow_html=True)
                    
#                     with col_p2:
#                         st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                         st.metric("Rank Potential", 
#                                  "Top 5" if prediction >= 12 else "Top 10" if prediction >= 8 else "Top 20")
#                         st.markdown("</div>", unsafe_allow_html=True)
                    
#                     with col_p3:
#                         st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
#                         confidence = "High" if assists_prev >= 5 else "Medium"
#                         st.metric("Prediction Confidence", confidence)
#                         st.markdown("</div>", unsafe_allow_html=True)
                    
#                     # Comparison chart
#                     comparison_data = {
#                         'Category': ['Last Season', 'Predicted', 'League Avg'],
#                         'Assists': [assists_prev, prediction, 6.5]
#                     }
                    
#                     fig = px.bar(comparison_data, x='Category', y='Assists',
#                                 title="Assists Comparison",
#                                 color='Assists',
#                                 color_continuous_scale=['#e90052', '#38003c'])
                    
#                     fig.update_layout(
#                         height=400,
#                         showlegend=False,
#                         plot_bgcolor='rgba(0,0,0,0)',
#                         paper_bgcolor='rgba(0,0,0,0)',
#                     )
                    
#                     st.plotly_chart(fig, use_container_width=True)
                    
#                     # Player insights
#                     st.markdown("#### 💡 Player Analysis")
                    
#                     if prediction > assists_prev * 1.2:
#                         st.success("📈 Significant improvement expected!")
#                     elif prediction > assists_prev:
#                         st.info("📊 Moderate improvement projected")
#                     else:
#                         st.warning("⚠️ Performance may decline or remain stable")
                    
#                     if big6_num == 1:
#                         st.markdown("- ⭐ Playing for top club provides better opportunities")
                    
#                     if minutes_played >= 2500:
#                         st.markdown("- ✅ High playing time ensures consistent contribution")
                    
#                     if expected_assists > assists_prev:
#                         st.markdown("- 🎯 Underperformed xA last season - regression to mean expected")

# # -----------------------------
# # Footer
# # -----------------------------
# st.markdown("---")
# st.markdown("""
#     <div style='text-align: center; color: #666; padding: 2rem;'>
#         <p>⚽ Powered by Advanced Machine Learning Models</p>
#     </div>
# """, unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import joblib
from tensorflow.keras.models import load_model
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Premier League Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS for Better Styling
# -----------------------------
st.markdown("""
    <style>
    /* Animated Football Background */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=1920');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.50);  /* Adjust opacity: 0.92 = 92% white, lower = more visible background */
        backdrop-filter: blur(2px);  /* BLUR STRENGTH: Increase number for more blur (try 12px, 15px) */
        z-index: 0;
        pointer-events: none;
    }
    
    .main {
        padding: 0rem 1rem;
        position: relative;
        z-index: 1;
    }
    
    /* Celebration Animation */
    @keyframes confetti-fall {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-10vh) rotate(720deg);
            opacity: 0;
        }
    }
    
    @keyframes trophy-bounce {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-20px) scale(1.1); }
    }
    
    @keyframes firework-burst {
        0% {
            transform: translate(0, 0) scale(0);
            opacity: 1;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translate(var(--tx), var(--ty)) scale(1);
            opacity: 0;
        }
    }
    
    .celebration-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        overflow: hidden;
    }
    
    .confetti {
        position: absolute;
        width: 15px;
        height: 15px;
        animation: confetti-fall 4s linear infinite;
    }
    
    .firework {
        position: absolute;
        width: 5px;
        height: 5px;
        border-radius: 50%;
        animation: firework-burst 1.5s ease-out forwards;
    }
    
    .trophy-float {
        animation: trophy-bounce 2s ease-in-out infinite;
        display: inline-block;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1.1rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        backdrop-filter: blur(10px);
    }
    .info-box {
        background: rgba(240, 242, 246, 0.95);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #38003c;
        margin: 1rem 0;
        color: #38003c;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    h1 {
        color: #38003c;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        background: transparent;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Load models and scaler
# -----------------------------
@st.cache_resource
def load_models():
    try:
        nn_model = load_model("nn_smote_model.keras")
        scaler = joblib.load("scaler.pkl")
        top_assists_model = joblib.load("top_assists.pkl")
        return nn_model, scaler, top_assists_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

nn_model, scaler, top_assists_model = load_models()

# -----------------------------
# Header
# -----------------------------
st.markdown("<h1 style='text-align: center; color: #white;'>⚽ Premier League AI Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666;'>Predict league winners and top assist makers using advanced ML models</p>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# Sidebar Information
# -----------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/f2/Premier_League_Logo.svg/1200px-Premier_League_Logo.svg.png", width=200)
    st.markdown("### 📊 About the Models")
    st.info("""
    **League Winner Model:**
    - Neural Network (Deep Learning)
    - Trained on historical PL data
    - 95%+ accuracy
    
    **Top Assists Model:**
    - Advanced regression model
    - Considers 20+ features
    - Player performance prediction
    """)
    
    st.markdown("### 📖 Quick Guide")
    st.markdown("""
    1. Select prediction type
    2. Enter team/player stats
    3. Click predict button
    4. View results & insights
    """)

# -----------------------------
# Main Content - Tabs
# -----------------------------
tab1, tab2 = st.tabs(["🏆 League Winner", "🅰️ Top Assists"])

# -----------------------------
# TAB 1: League Winner Prediction
# -----------------------------
with tab1:
    st.markdown("### Predict League Champion")
    st.markdown("<div class='info-box'>Enter the team's season statistics to predict championship probability</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📋 Match Statistics")
        
        # Row 1: Basic Stats
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            played = st.number_input("🎮 Matches Played", 0, 42, 38, help="Total matches played in the season")
        with c2:
            won = st.number_input("✅ Wins", 0, 42, 28, help="Number of matches won")
        with c3:
            drawn = st.number_input("🤝 Draws", 0, 42, 6, help="Number of matches drawn")
        with c4:
            lost = st.number_input("❌ Losses", 0, 42, 4, help="Number of matches lost")
        
        st.markdown("#### ⚽ Goal Statistics")
        
        # Row 2: Goal Stats
        g1, g2, g3 = st.columns(3)
        with g1:
            gf = st.number_input("🎯 Goals For", 0, 200, 89, help="Total goals scored")
        with g2:
            ga = st.number_input("🛡️ Goals Against", 0, 200, 33, help="Total goals conceded")
        with g3:
            gd = st.number_input("📊 Goal Difference", -100, 200, 56, help="GF - GA")
        
        # Calculate Points
        points = (won * 3) + drawn
        
        st.markdown("---")
        st.markdown(f"**📈 Calculated Points:** `{points}`")
        
        predict_btn = st.button("🔮 Predict Championship Probability", use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Quick Stats")
        st.metric("Win Rate", f"{(won/played*100):.1f}%")
        st.metric("Total Points", points)
        st.metric("Goals/Match", f"{(gf/played):.2f}")
        st.metric("Clean Sheets", f"~{int((played-ga/1.5))}")
    
    # Prediction Results
    if predict_btn:
        if nn_model and scaler:
            with st.spinner("🔄 Analyzing team performance..."):
                input_data = pd.DataFrame(
                    [[played, won, drawn, lost, gf, ga, gd]],
                    columns=['played', 'won', 'drawn', 'lost', 'gf', 'ga', 'gd']
                )
                input_scaled = scaler.transform(input_data)
                
                nn_prob = float(nn_model.predict(input_scaled, verbose=0)[0][0])
                
                st.markdown("---")
                st.markdown("### 🎯 Prediction Results")
                
                # Result Card
                result_emoji = "🏆" if nn_prob >= 0.5 else "❌"
                result_text = "CHAMPION" if nn_prob >= 0.5 else "NOT CHAMPION"
                result_color = "#28a745" if nn_prob >= 0.5 else "#dc3545"
                
                # Add celebration animation if champion
                if nn_prob >= 0.5:
                    st.markdown("""
                        <div class="celebration-container" id="celebration">
                            <script>
                                // Confetti Animation
                                function createConfetti() {
                                    const colors = ['#FFD700', '#FFA500', '#FF6347', '#4169E1', '#32CD32', '#FF1493'];
                                    const shapes = ['⚽', '🏆', '⭐', '🎉', '🎊', '✨'];
                                    const container = document.getElementById('celebration');
                                    
                                    for (let i = 0; i < 50; i++) {
                                        setTimeout(() => {
                                            const confetti = document.createElement('div');
                                            confetti.className = 'confetti';
                                            confetti.innerHTML = shapes[Math.floor(Math.random() * shapes.length)];
                                            confetti.style.left = Math.random() * 100 + '%';
                                            confetti.style.fontSize = (Math.random() * 20 + 20) + 'px';
                                            confetti.style.animationDelay = (Math.random() * 2) + 's';
                                            confetti.style.animationDuration = (Math.random() * 2 + 3) + 's';
                                            container.appendChild(confetti);
                                            
                                            setTimeout(() => confetti.remove(), 100000);
                                        }, i * 100);
                                    }
                                }
                                
                                // Fireworks Animation
                                function createFirework(x, y) {
                                    const container = document.getElementById('celebration');
                                    const colors = ['#FFD700', '#FF6347', '#4169E1', '#32CD32', '#FF1493', '#FFA500', '#00CED1', '#FF69B4'];
                                    const particleCount = 30;
                                    
                                    for (let i = 0; i < particleCount; i++) {
                                        const particle = document.createElement('div');
                                        particle.className = 'firework';
                                        
                                        const angle = (Math.PI * 2 * i) / particleCount;
                                        const velocity = 50 + Math.random() * 100;
                                        const tx = Math.cos(angle) * velocity;
                                        const ty = Math.sin(angle) * velocity;
                                        
                                        particle.style.left = x + '%';
                                        particle.style.top = y + '%';
                                        particle.style.setProperty('--tx', tx + 'px');
                                        particle.style.setProperty('--ty', ty + 'px');
                                        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                                        particle.style.boxShadow = `0 0 ${Math.random() * 10 + 5}px ${colors[Math.floor(Math.random() * colors.length)]}`;
                                        
                                        container.appendChild(particle);
                                        
                                        setTimeout(() => particle.remove(), 15000);
                                    }
                                }
                                
                                // Launch multiple fireworks
                                function launchFireworks() {
                                    const positions = [
                                        {x: 20, y: 30}, {x: 50, y: 20}, {x: 80, y: 30},
                                        {x: 30, y: 50}, {x: 70, y: 50}, {x: 40, y: 25},
                                        {x: 60, y: 35}
                                    ];
                                    
                                    positions.forEach((pos, index) => {
                                        setTimeout(() => {
                                            createFirework(pos.x, pos.y);
                                        }, index * 400);
                                    });
                                    
                                    // Repeat fireworks
                                    setTimeout(launchFireworks, 3000);
                                }
                                
                                // Start celebrations
                                createConfetti();
                                launchFireworks();
                            </script>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style='background: {result_color}; padding: 2rem; border-radius: 15px; text-align: center; color: white; position: relative; z-index: 10;'>
                        <h1 style='color: white; margin: 0;'><span class='{"trophy-float" if nn_prob >= 0.5 else ""}'>{result_emoji}</span> {result_text}</h1>
                        <h2 style='color: white; margin-top: 1rem;'>{nn_prob*100:.1f}% Probability</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("")
                
                # Model Display
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.metric("Neural Network Prediction", f"{nn_prob*100:.1f}%")
                    st.markdown("</div>", unsafe_allow_html=True)
                with col_b:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    confidence = "High" if abs(nn_prob - 0.5) > 0.3 else "Medium" if abs(nn_prob - 0.5) > 0.15 else "Low"
                    st.metric("Confidence Level", confidence)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Visualization
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='Championship',
                    x=['Prediction'],
                    y=[nn_prob*100],
                    marker_color='#38003c',
                    text=[f'{nn_prob*100:.1f}%'],
                    textposition='auto',
                    width=0.4
                ))
                
                fig.add_trace(go.Bar(
                    name='Not Champion',
                    x=['Prediction'],
                    y=[(1-nn_prob)*100],
                    marker_color='#e90052',
                    text=[f'{(1-nn_prob)*100:.1f}%'],
                    textposition='auto',
                    width=0.4
                ))
                
                fig.update_layout(
                    title="Championship Probability",
                    yaxis_title="Probability (%)",
                    barmode='group',
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Insights
                st.markdown("#### 💡 Key Insights")
                insights = []
                if points >= 90:
                    insights.append("✅ Excellent point total for a champion")
                elif points >= 80:
                    insights.append("⚠️ Good points, but may need more for the title")
                else:
                    insights.append("❌ Points total typically below championship level")
                
                if gd >= 50:
                    insights.append("✅ Outstanding goal difference")
                elif gd >= 30:
                    insights.append("⚠️ Decent goal difference")
                else:
                    insights.append("❌ Goal difference needs improvement")
                
                if won/played >= 0.7:
                    insights.append("✅ Dominant win rate")
                else:
                    insights.append("⚠️ Win rate could be higher")
                
                for insight in insights:
                    st.markdown(f"- {insight}")

# -----------------------------
# TAB 2: Top Assists Prediction
# -----------------------------
with tab2:
    st.markdown("### Predict Player Assists for Next Season")
    st.markdown("<div class='info-box'>Enter comprehensive player statistics to predict expected assists next season</div>", unsafe_allow_html=True)
    
    # Organize inputs into logical sections
    with st.form("top_assists_form"):
        st.markdown("#### 👤 Player Information")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", 16, 40, 25, help="Player's age")
        with col2:
            position = st.selectbox("Position", ["Forward", "Midfielder", "Defender", "Goalkeeper"], help="Playing position")
            position_num = {"Forward": 1, "Midfielder": 2, "Defender": 3, "Goalkeeper": 4}[position]
        with col3:
            minutes_played = st.number_input("Minutes Played", 0, 3800, 2800, help="Total minutes played")
        
        st.markdown("#### 📊 Previous Season Stats")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            assists_prev = st.number_input("Previous Assists", 0, 30, 8, help="Assists last season")
        with col5:
            goals_prev = st.number_input("Previous Goals", 0, 50, 5, help="Goals last season")
        with col6:
            key_passes = st.number_input("Key Passes", 0, 200, 60, help="Total key passes")
        
        st.markdown("#### 🎯 Advanced Metrics")
        col7, col8, col9 = st.columns(3)
        
        with col7:
            expected_assists = st.number_input("Expected Assists (xA)", 0.0, 30.0, 7.5, 0.1, help="xA metric")
        with col8:
            dribbles_completed = st.number_input("Dribbles Completed", 0, 300, 80, help="Successful dribbles")
        with col9:
            shots_assisted = st.number_input("Shots Assisted", 0, 200, 70, help="Shots created")
        
        st.markdown("#### 🏟️ Team Context")
        col10, col11, col12, col13 = st.columns(4)
        
        with col10:
            set_piece_involvement = st.number_input("Set Piece Inv.", 0, 100, 25, help="Set piece contributions")
        with col11:
            club_total_goals = st.number_input("Club Total Goals", 0, 150, 75, help="Team's total goals")
        with col12:
            club_league_rank = st.number_input("Club Rank", 1, 20, 4, help="Team's league position")
        with col13:
            big6_club = st.selectbox("Big 6 Club?", ["Yes", "No"], help="Playing for top 6 club")
            big6_num = 1 if big6_club == "Yes" else 0
        
        st.markdown("#### 📈 Per 90 & Ratio Stats")
        col14, col15, col16 = st.columns(3)
        
        with col14:
            club_attack_share = st.slider("Club Attack Share (%)", 0.0, 100.0, 15.0, 0.5, help="% of team's attacks")
        with col15:
            club_xg = st.number_input("Club xG", 0.0, 100.0, 65.0, 0.5, help="Team's expected goals")
        with col16:
            assists_per_90 = st.number_input("Assists per 90", 0.0, 2.0, 0.25, 0.01, help="Assists per 90 mins")
        
        col17, col18, col19, col20 = st.columns(4)
        
        with col17:
            goals_per_90 = st.number_input("Goals per 90", 0.0, 2.0, 0.15, 0.01)
        with col18:
            contribution_ratio = st.number_input("Contribution Ratio", 0.0, 5.0, 0.35, 0.01, help="Goal involvement ratio")
        with col19:
            dribbles_per_90 = st.number_input("Dribbles per 90", 0.0, 10.0, 2.5, 0.1)
        with col20:
            shots_assisted_per_90 = st.number_input("Shots Assisted per 90", 0.0, 10.0, 2.2, 0.1)
        
        st.markdown("---")
        submitted = st.form_submit_button("🔮 Predict Next Season Assists", use_container_width=True)
        
        if submitted:
            if top_assists_model:
                with st.spinner("🔄 Analyzing player data..."):
                    input_values = [
                        age, position_num, minutes_played, assists_prev, goals_prev,
                        key_passes, expected_assists, dribbles_completed, shots_assisted,
                        set_piece_involvement, club_total_goals, club_league_rank, big6_num,
                        club_attack_share, club_xg, assists_per_90, goals_per_90,
                        contribution_ratio, dribbles_per_90, shots_assisted_per_90
                    ]
                    
                    top_assists_cols = [
                        'Age', 'Position', 'Minutes_Played', 'Assists_prev_season',
                        'Goals_prev_season', 'Key_Passes', 'Expected_Assists_(xA)',
                        'Dribbles_Completed', 'Shots_Assisted', 'Set_Piece_Involvement',
                        'Club_Total_Goals', 'Club_League_Rank', 'Big6_Club_Feature',
                        'Club_Attack_Share', 'Club_xG', 'Assists_per_90', 'Goals_per_90',
                        'Contribution_Ratio', 'Dribbles_per_90', 'Shots_Assisted_per_90'
                    ]
                    
                    input_df = pd.DataFrame([input_values], columns=top_assists_cols)
                    prediction = float(top_assists_model.predict(input_df)[0])
                    
                    st.markdown("---")
                    st.markdown("### 🎯 Prediction Results")
                    
                    # Result visualization
                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #38003c 0%, #e90052 100%); 
                                    padding: 2rem; border-radius: 15px; text-align: center; color: white;'>
                            <h1 style='color: white; margin: 0;'>🅰️ Predicted Assists</h1>
                            <h2 style='color: white; margin-top: 1rem; font-size: 3rem;'>{prediction:.1f}</h2>
                            <p style='color: white; opacity: 0.9;'>Expected assists for next season</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("")
                    
                    # Performance categories
                    col_p1, col_p2, col_p3 = st.columns(3)
                    with col_p1:
                        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                        st.metric("Performance Level", 
                                 "Elite" if prediction >= 12 else "Good" if prediction >= 8 else "Average")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col_p2:
                        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                        st.metric("Rank Potential", 
                                 "Top 5" if prediction >= 12 else "Top 10" if prediction >= 8 else "Top 20")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col_p3:
                        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                        confidence = "High" if assists_prev >= 5 else "Medium"
                        st.metric("Prediction Confidence", confidence)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Comparison chart
                    comparison_data = {
                        'Category': ['Last Season', 'Predicted', 'League Avg'],
                        'Assists': [assists_prev, prediction, 6.5]
                    }
                    
                    fig = px.bar(comparison_data, x='Category', y='Assists',
                                title="Assists Comparison",
                                color='Assists',
                                color_continuous_scale=['#e90052', '#38003c'])
                    
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Player insights
                    st.markdown("#### 💡 Player Analysis")
                    
                    if prediction > assists_prev * 1.2:
                        st.success("📈 Significant improvement expected!")
                    elif prediction > assists_prev:
                        st.info("📊 Moderate improvement projected")
                    else:
                        st.warning("⚠️ Performance may decline or remain stable")
                    
                    if big6_num == 1:
                        st.markdown("- ⭐ Playing for top club provides better opportunities")
                    
                    if minutes_played >= 2500:
                        st.markdown("- ✅ High playing time ensures consistent contribution")
                    
                    if expected_assists > assists_prev:
                        st.markdown("- 🎯 Underperformed xA last season - regression to mean expected")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>⚽ Powered by Advanced Machine Learning Models</p>
    </div>
""", unsafe_allow_html=True)
