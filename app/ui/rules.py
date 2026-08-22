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
            if st.button(f"Update Rule {row['rule_id']}", key=f"upd_{row['id']}"):
                try:
                    execute(
                        "UPDATE rules SET enabled=?, severity=?, threshold_value=? WHERE id=?",
                        (1 if enabled else 0, severity, threshold, row['id'])
                    )
                    st.success(f"Rule {row['rule_id']} updated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating rule: {e}")

    st.subheader("Auto-Resolution Settings")
    
    # Confidence Threshold
    current_threshold_row = query_one("SELECT value FROM settings WHERE key='confidence_threshold'")
    if current_threshold_row:
        current_threshold = float(current_threshold_row["value"])
    else:
        current_threshold = 85.0
        execute("INSERT INTO settings (key, value) VALUES ('confidence_threshold', '85')")
    
    new_threshold = st.number_input("Confidence Threshold (%)", value=current_threshold, step=1.0, key="threshold_input")
    if st.button("Update Threshold", key="update_threshold"):
        try:
            execute("UPDATE settings SET value=? WHERE key='confidence_threshold'", (new_threshold,))
            st.success(f"Threshold updated to {new_threshold}%")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating threshold: {e}")

    # Auto-Resolution Limit
    current_limit_row = query_one("SELECT value FROM settings WHERE key='auto_resolve_limit'")
    if current_limit_row:
        current_limit = float(current_limit_row["value"])
    else:
        current_limit = 50000.0
        execute("INSERT INTO settings (key, value) VALUES ('auto_resolve_limit', '50000')")
    
    new_limit = st.number_input("Auto-Resolution Amount Limit (₹)", value=current_limit, step=1000.0, key="limit_input")
    if st.button("Update Limit", key="update_limit"):
        try:
            execute("UPDATE settings SET value=? WHERE key='auto_resolve_limit'", (new_limit,))
            st.success(f"Limit updated to ₹{new_limit:,.2f}")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating limit: {e}")