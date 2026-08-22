import sys
import os

# Add parent directory to Python path so 'app' package is found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from app.database import init_db
from app.data.seed import seed_database

# ---------- CUSTOM CSS for Enterprise Look ----------
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main background and font */
    .main {
        background-color: #f8f9fc;
    }
    .stApp {
        background-color: #f8f9fc;
    }
    
    /* Sidebar styling */
    .css-1d391kg { /* sidebar background */
        background-color: #0a1e3c;
    }
    .css-1d391kg .stRadio > label {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 1.1rem;
    }
    .css-1d391kg .stRadio > div {
        background: transparent;
    }
    .css-1d391kg .stRadio [data-baseweb="radio"] {
        background: #ffffff10;
    }
    .css-1d391kg .stRadio [data-baseweb="radio"]:hover {
        background: #ffffff20;
    }
    .css-1d391kg .stRadio [data-baseweb="radio"] .st-bv {
        color: #ffd700;
    }
    
    /* Metrics cards */
    [data-testid="metric-container"] {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        padding: 16px 12px;
        border-left: 4px solid #1a3a6b;
        transition: transform 0.15s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }
    [data-testid="metric-container"] .stMetricDelta {
        color: #1a3a6b;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0a1e3c !important;
        font-weight: 600 !important;
    }
    .stSubheader {
        color: #1a3a6b !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0a1e3c;
        color: white;
        border-radius: 8px;
        font-weight: 500;
        border: none;
        padding: 0.5rem 1.2rem;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background-color: #1a3a6b;
        color: #ffd700;
    }
    .stButton > button:disabled {
        background-color: #b0b8c4;
        color: #ffffff80;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #e9edf4;
        font-weight: 500;
        color: #0a1e3c;
        transition: border 0.2s;
    }
    .streamlit-expanderHeader:hover {
        border-color: #0a1e3c;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #0a1e3c;
    }
    
    /* Rule cards */
    .stExpander {
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Initialize database and seed if empty
init_db()
from app.database import query_one
if not query_one("SELECT 1 FROM transactions LIMIT 1"):
    seed_database()

# Streamlit page config
st.set_page_config(page_title="ResolveAI", layout="wide", page_icon="🧠")

# Main UI – Brand header
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 0px; padding-bottom: 0px;">
    <h1 style="margin: 0; color: #0a1e3c; font-size: 2.4rem; font-weight: 700;">🧠 ResolveAI</h1>
    <span style="margin-left: 16px; color: #1a3a6b; font-size: 1rem; font-weight: 300;">Real-Time Human-in-the-Loop Exception Resolution</span>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; margin-top: 10px; margin-bottom: 20px;">
        <div style="font-size: 3rem; line-height: 1;">🧠</div>
        <div style="color: #ffd700; font-weight: 700; font-size: 1.2rem; letter-spacing: 2px;">RESOLVE AI</div>
        <div style="color: #ffffff80; font-size: 0.7rem;">v1.0 · Enterprise</div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio("Navigation", ["Dashboard", "Exception Queue", "Rules", "Audit Trail"],
                    index=0,
                    format_func=lambda x: f"📌 {x}")

# Import UI modules
from app.ui.dashboard import render_dashboard
from app.ui.queue import render_queue
from app.ui.exception_detail import render_exception_detail
from app.ui.rules import render_rules
from app.ui.audit import render_audit

# Page routing
if page == "Dashboard":
    render_dashboard()
elif page == "Exception Queue":
    render_queue()
    render_exception_detail()
elif page == "Rules":
    render_rules()
elif page == "Audit Trail":
    render_audit()