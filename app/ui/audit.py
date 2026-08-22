import streamlit as st
from app.database.db import query_all

def render_audit():
    st.subheader("📜 Audit Trail")
    events = query_all("SELECT * FROM audit_events ORDER BY timestamp DESC LIMIT 50")
    if not events:
        st.info("No audit events yet.")
        return
    for ev in events:
        st.write(f"**{ev['timestamp']}** | {ev['actor']} | {ev['action']} | TX: {ev['transaction_id']} | {ev['reason']}")
        if ev['confidence']:
            st.write(f"Confidence: {ev['confidence']:.0f}%")
        if ev['rule_results']:
            st.caption(f"Rules: {ev['rule_results']}")
        st.divider()