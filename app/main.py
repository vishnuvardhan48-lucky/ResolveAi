import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from app.database import init_db
from app.data.seed import seed_database

load_dotenv()
init_db()
from app.database import query_one
if not query_one("SELECT 1 FROM transactions LIMIT 1"):
    seed_database()

st.set_page_config(page_title="ResolveAI", layout="wide")
st.title("🧠 ResolveAI")
st.caption("Real-Time Human-in-the-Loop Exception Resolution Workbench")

with st.sidebar:
    # Replace with your own logo file or URL
    st.image("https://via.placeholder.com/150x50?text=ResolveAI", use_column_width=True)
    page = st.radio("Navigation", ["Dashboard", "Exception Queue", "Rules", "Audit Trail"])

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