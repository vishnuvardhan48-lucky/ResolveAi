import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from app.database import init_db
from app.data.seed import seed_database

# ---------- CUSTOM DARK CSS ----------
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {background: transparent !important;}
    
    /* Global background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .main {
        background-color: #0e1117;
    }
    
    /* Sidebar */
    .css-1d391kg, .stSidebar {
        background-color: #0a0e1a !important;
        border-right: 1px solid #2a2a3a;
    }
    .css-1d391kg .stRadio > label {
        color: #ffffff !important;
        font-weight: 500;
        font-size: 1.1rem;
    }
    .css-1d391kg .stRadio [data-baseweb="radio"] .st-bv {
        color: #ffd700;
    }
    
    /* Metrics cards */
    [data-testid="metric-container"] {
        background-color: #1a1d2b;
        border-radius: 12px;
        padding: 16px 12px;
        border: 1px solid #2a2d3e;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: transform 0.15s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    }
    [data-testid="metric-container"] .stMetricDelta {
        color: #ffd700;
    }
    [data-testid="metric-container"] label {
        color: #a0a0b0 !important;
    }
    
    /* Headers */
    h1, h2, h3, .stSubheader {
        color: #f0f0f0 !important;
        font-weight: 600 !important;
    }
    h1 {
        color: #ffd700 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #ffd700;
        color: #0a0e1a;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #ffed4a;
        color: #000;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }
    .stButton > button:disabled {
        background-color: #3a3a4a;
        color: #888;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #1a1d2b;
        border: 1px solid #2a2d3e;
        border-radius: 8px;
        color: #f0f0f0;
        font-weight: 500;
    }
    .streamlit-expanderHeader:hover {
        border-color: #ffd700;
    }
    .streamlit-expanderContent {
        background-color: #141724;
        border-radius: 0 0 8px 8px;
        border: 1px solid #2a2d3e;
        border-top: none;
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #1a1d2b !important;
        color: #f0f0f0 !important;
        border: 1px solid #2a2d3e !important;
        border-radius: 6px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2);
    }
    
    /* Checkbox */
    .stCheckbox label {
        color: #e0e0e0 !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        background-color: #1a1d2b;
        border-radius: 8px;
        border-left: 4px solid #ffd700;
        color: #f0f0f0;
    }
    .stAlert svg {
        fill: #ffd700;
    }
    .stSuccess {
        border-left-color: #00c853;
    }
    .stError {
        border-left-color: #ff1744;
    }
    
    /* Metric delta colors (positive/negative) */
    .stMetricDelta > div {
        color: #ffd700 !important;
    }
    
    /* Sidebar brand */
    .brand {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 10px 0 20px 0;
    }
    .brand-icon {
        font-size: 3rem;
        line-height: 1;
    }
    .brand-name {
        color: #ffd700;
        font-weight: 700;
        font-size: 1.2rem;
        letter-spacing: 2px;
    }
    .brand-version {
        color: #8888aa;
        font-size: 0.7rem;
    }
    
    /* Queue items */
    .stExpander {
        background: #141724;
        border: 1px solid #2a2d3e;
        border-radius: 10px;
        margin-bottom: 0.5rem;
    }
    
    /* Code blocks / pre (if any) */
    pre, code {
        background-color: #0e1117 !important;
        color: #ffd700 !important;
    }
</style>
""", unsafe_allow_html=True)

load_dotenv()

init_db()
from app.database import query_one
if not query_one("SELECT 1 FROM transactions LIMIT 1"):
    seed_database()

st.set_page_config(page_title="ResolveAI", layout="wide", page_icon="🧠")

# Brand header with dark theme
st.markdown("""
<div style="display: flex; align-items: center; margin-bottom: 0px; padding-bottom: 0px;">
    <h1 style="margin: 0; color: #ffd700; font-size: 2.4rem; font-weight: 700;">🧠 ResolveAI</h1>
    <span style="margin-left: 16px; color: #a0a0b0; font-size: 1rem; font-weight: 300;">Real-Time Human-in-the-Loop Exception Resolution</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🧠</div>
        <div class="brand-name">RESOLVE AI</div>
        <div class="brand-version">v1.0 · Enterprise</div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio("Navigation", ["Dashboard", "Exception Queue", "Rules", "Audit Trail"],
                    index=0,
                    format_func=lambda x: f"📌 {x}")

from app.ui.dashboard import render_dashboard
from app.ui.queue import render_queue
from app.ui.exception_detail import render_exception_detail
from app.ui.rules import render_rules
from app.ui.audit import render_audit

if page == "Dashboard":
    render_dashboard()
elif page == "Exception Queue":
    render_queue()
    render_exception_detail()
elif page == "Rules":
    render_rules()
elif page == "Audit Trail":
    render_audit()