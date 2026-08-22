import streamlit as st
from app.database import query_all, query_one, execute

def render_rules():
    st.subheader("⚙️ Business Rules Configuration")
    rows = query_all("SELECT * FROM rules ORDER BY rule_id")
    for row in rows:
        with st.expander(f"{row['rule_id']} - {row['name']}"):
            enabled = st.checkbox("Enabled", value=bool(row['enabled']), key=f"en_{row['id']}")
            severity = st.selectbox("Severity", ["LOW", "MEDIUM", "HIGH"], index=["LOW","MEDIUM","HIGH"].index(row['severity']), key=f"sev_{row['id']}")
            threshold = st.number_input("Threshold value", value=float(row['threshold_value']), key=f"thr_{row['id']}")
            if st.button("Update", key=f"upd_{row['id']}"):
                execute("UPDATE rules SET enabled=?, severity=?, threshold_value=? WHERE id=?", (1 if enabled else 0, severity, threshold, row['id']))
                st.success("Rule updated.")
                st.rerun()  # <-- FIXED

    st.subheader("Auto-Resolution Settings")
    current_threshold = query_one("SELECT value FROM settings WHERE key='confidence_threshold'")['value']
    new_threshold = st.number_input("Confidence Threshold (%)", value=float(current_threshold), step=1.0)
    if st.button("Update Threshold"):
        execute("UPDATE settings SET value=? WHERE key='confidence_threshold'", (new_threshold,))
        st.success(f"Threshold updated to {new_threshold}%")
        st.rerun()  # <-- FIXED

    current_limit = query_one("SELECT value FROM settings WHERE key='auto_resolve_limit'")['value']
    new_limit = st.number_input("Auto-Resolution Amount Limit (₹)", value=float(current_limit), step=1000.0)
    if st.button("Update Limit"):
        execute("UPDATE settings SET value=? WHERE key='auto_resolve_limit'", (new_limit,))
        st.success(f"Limit updated to ₹{new_limit:,.2f}")
        st.rerun()  # <-- FIXED