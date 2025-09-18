import streamlit as st
from birdeye_page import show_birdeye
from moralis_page import show_moralis

# ----- PAGE CONFIG -----
st.set_page_config(
    page_title="MemesWatch Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----- CUSTOM CSS -----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .stRadio > div {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
        gap: 15px;
    }
    
    .stRadio > div > label {
        font-size: 16px;
        font-weight: 600;
        color: #FFFFFF;
        background: linear-gradient(135deg, #8A4AF3 0%, #9945FF 100%);
        padding: 12px 24px;
        border-radius: 25px;
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(138, 74, 243, 0.3);
    }
    
    .stRadio > div > label:hover {
        background: linear-gradient(135deg, #00FFF0 0%, #8A4AF3 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 255, 240, 0.4);
        border-color: #00FFF0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(138, 74, 243, 0.3);
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #00FFF0;
        box-shadow: 0 12px 40px rgba(0, 255, 240, 0.2);
        transform: translateY(-2px);
    }
    
    .health-score-excellent {
        color: #00FF88;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .health-score-good {
        color: #4ECDC4;
        font-weight: 700;
    }
    
    .health-score-warning {
        color: #FFB347;
        font-weight: 700;
    }
    
    .health-score-critical {
        color: #FF6B6B;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
    }
    
    .insight-box {
        background: linear-gradient(135deg, rgba(138, 74, 243, 0.1) 0%, rgba(0, 255, 240, 0.1) 100%);
        border-left: 4px solid #00FFF0;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        font-style: italic;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(255, 181, 71, 0.1) 0%, rgba(255, 107, 107, 0.1) 100%);
        border-left: 4px solid #FFB347;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stDataFrame > div {
        border-radius: 10px;
        overflow: hidden;
    }

    .hero {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #8A4AF3, #00FFF0);
        border-radius: 15px;
        margin-bottom: 30px;
        color: white;
        box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    }
    
    .hero h1 {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .hero p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# ----- SIDEBAR -----
st.sidebar.markdown("""
    <div class="sidebar-card">
        <h2>📊 MemesWatch</h2>
        <p>Real-time Meme Token Tracking</p>
    </div>
    <p><b>Track:</b></p>
    - 🚀 New Listings <br>
    - 🐳 Whale Holders <br>
    - 📉 Market Insights
""", unsafe_allow_html=True)

# ----- HERO BANNER -----
st.markdown("""
    <div class="hero">
        <h1>🚀 MemesWatch Dashboard</h1>
        <p>Live Meme Token Analytics • Whale Tracking • Market Insights</p>
    </div>
""", unsafe_allow_html=True)

# ----- NAVIGATION -----
st.markdown(
    """
    <style>
    .center-radio {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 30px;
    }
    div[data-baseweb="radio"] {
        gap: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="center-radio">', unsafe_allow_html=True)
page = st.radio(
    "Navigation",
    ["🐦 New Listings", "🐳 Token Top Holders"],
    horizontal=True,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ----- PAGES -----
if page == "🐦 New Listings":
    show_birdeye()
elif page == "🐳 Token Top Holders":
    show_moralis()
