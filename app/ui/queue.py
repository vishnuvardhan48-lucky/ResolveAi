import streamlit as st
from app.database import query_all, query_one
from app.services.rule_engine import RuleEngine
from app.services.confidence_engine import ConfidenceEngine
from app.services.safety_controller import SafetyController
from app.services.ai_engine import AIEngine
from app.services.resolution_service import ResolutionService
from app.models.transaction import Transaction
from app.ui.dashboard import update_metrics

def render_queue():
    st.subheader("📋 Exception Queue")
    rows = query_all("SELECT * FROM transactions WHERE status IN ('OPEN', 'UNDER_REVIEW', 'AUTO_RESOLVABLE', 'HUMAN_REVIEW_REQUIRED')")
    if not rows:
        st.info("No open exceptions.")
        return

    for row in rows:
        tx = Transaction(**row)
        rule_results = RuleEngine.evaluate(tx)
        confidence = ConfidenceEngine.calculate(tx, rule_results)
        status_icon = "🔴" if confidence < 60 else "🟡" if confidence < 85 else "🟢"
        with st.expander(f"{status_icon} {tx.transaction_id} - {tx.vendor} - ₹{tx.amount:,.2f} (Conf: {confidence:.0f}%)"):
            col1, col2 = st.columns([3,1])
            col1.write(f"**Type:** {tx.transaction_type} | **Category:** {tx.category}")
            col1.write(f"**Age:** {tx.age_days} days | **Previous Exceptions:** {tx.previous_exceptions}")
            triggered = [r for r in rule_results if r.triggered]
            if triggered:
                col1.write("**Triggered rules:** " + ", ".join([f"{r.name}" for r in triggered]))
            else:
                col1.write("**No rules triggered**")

            allowed, reason = SafetyController.is_auto_resolution_allowed(tx, rule_results, confidence)
            if allowed:
                col2.success("✅ Auto-resolve permitted")
            else:
                col2.error("❌ Auto-resolve blocked")
                col2.caption(reason)

            if st.button(f"View Details", key=f"view_{tx.id}"):
                st.session_state.selected_transaction_id = tx.id
                st.rerun()  # <-- FIXED

            if allowed and st.button(f"Auto-Resolve Now", key=f"auto_{tx.id}"):
                reason_text = AIEngine.get_resolution_suggestion(tx, rule_results, confidence)[0]
                ResolutionService.auto_resolve(tx.id, reason_text, confidence, rule_results)
                st.success(f"Transaction {tx.transaction_id} auto-resolved.")
                st.session_state.dashboard_metrics = update_metrics()
                st.rerun()  # <-- FIXED