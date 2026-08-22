import streamlit as st
from app.database import query_all, query_one, execute

def get_settings():
    """Fetch current settings from DB, with defaults if missing."""
    threshold_row = query_one("SELECT value FROM settings WHERE key='confidence_threshold'")
    limit_row = query_one("SELECT value FROM settings WHERE key='auto_resolve_limit'")
    
    threshold = float(threshold_row["value"]) if threshold_row else 85.0
    limit = float(limit_row["value"]) if limit_row else 50000.0
    
    return threshold, limit

def render_rules():
    st.subheader("⚙️ Business Rules Configuration")
    
    # --- Rule configs (no form needed, each has its own button) ---
    rows = query_all("SELECT * FROM rules ORDER BY rule_id")
    for row in rows:
        with st.expander(f"{row['rule_id']} - {row['name']}"):
            enabled = st.checkbox("Enabled", value=bool(row['enabled']), key=f"en_{row['id']}")
            severity = st.selectbox("Severity", ["LOW", "MEDIUM", "HIGH"], 
                                    index=["LOW","MEDIUM","HIGH"].index(row['severity']), 
                                    key=f"sev_{row['id']}")
            threshold_val = st.number_input("Threshold value", 
                                            value=float(row['threshold_value']), 
                                            key=f"thr_{row['id']}")
            if st.button(f"Update Rule {row['rule_id']}", key=f"upd_{row['id']}"):
                try:
                    execute(
                        "UPDATE rules SET enabled=?, severity=?, threshold_value=? WHERE id=?",
                        (1 if enabled else 0, severity, threshold_val, row['id'])
                    )
                    st.success(f"Rule {row['rule_id']} updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("⚡ Auto-Resolution Settings")
    
    # --- Fetch current settings ---
    current_threshold, current_limit = get_settings()
    
    # Use a form to submit both updates together (optional, but cleaner)
    with st.form(key="settings_form"):
        new_threshold = st.number_input(
            "Confidence Threshold (%)", 
            value=current_threshold, 
            step=1.0,
            min_value=0.0,
            max_value=100.0,
            key="threshold_input"
        )
        new_limit = st.number_input(
            "Auto-Resolution Amount Limit (₹)", 
            value=current_limit, 
            step=1000.0,
            min_value=0.0,
            key="limit_input"
        )
        
        # Two separate submit buttons inside the same form
        col1, col2 = st.columns(2)
        with col1:
            submitted_threshold = st.form_submit_button("Update Threshold")
        with col2:
            submitted_limit = st.form_submit_button("Update Limit")
    
    # Process submissions
    if submitted_threshold:
        try:
            execute("UPDATE settings SET value=? WHERE key='confidence_threshold'", (new_threshold,))
            st.success(f"✅ Threshold updated to {new_threshold}%")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating threshold: {e}")
    
    if submitted_limit:
        try:
            execute("UPDATE settings SET value=? WHERE key='auto_resolve_limit'", (new_limit,))
            st.success(f"✅ Limit updated to ₹{new_limit:,.2f}")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating limit: {e}")
    
    # Show current values for clarity
    st.caption(f"Current threshold: **{current_threshold}%** | Current limit: **₹{current_limit:,.2f}**")