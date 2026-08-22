import streamlit as st
from app.database import query_one, execute
from app.services.rule_engine import RuleEngine
from app.services.confidence_engine import ConfidenceEngine
from app.services.safety_controller import SafetyController
from app.services.ai_engine import AIEngine
from app.services.resolution_service import ResolutionService
from app.models.transaction import Transaction
from app.ui.chatbot import render_chatbot
from app.ui.dashboard import update_metrics

def render_exception_detail():
    if "selected_transaction_id" not in st.session_state:
        st.info("Select a transaction from the queue to view details.")
        return

    tx_id = st.session_state.selected_transaction_id
    row = query_one("SELECT * FROM transactions WHERE id = ?", (tx_id,))
    if not row:
        st.error("Transaction not found.")
        return

    tx = Transaction(**row)
    rule_results = RuleEngine.evaluate(tx)
    confidence = ConfidenceEngine.calculate(tx, rule_results)
    allowed, reason = SafetyController.is_auto_resolution_allowed(tx, rule_results, confidence)

    st.subheader(f"📄 Transaction {tx.transaction_id}")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("**Details**")
        st.write(f"Vendor: {tx.vendor}")
        st.write(f"Type: {tx.transaction_type}")
        st.write(f"Amount: ₹{tx.amount:,.2f} (Expected: ₹{tx.expected_amount:,.2f})")
        st.write(f"Quantity: {tx.quantity} (Expected: {tx.expected_quantity})")
        st.write(f"Date: {tx.transaction_date}")
        st.write(f"Age: {tx.age_days} days")
        st.write(f"Category: {tx.category}")
        st.write(f"Payment: {tx.payment_method}")
        st.write(f"Tier: {tx.customer_vendor_tier}")
        st.write(f"Previous Exceptions: {tx.previous_exceptions}")
        st.write(f"Status: {tx.status}")

        st.markdown("**Rule Evaluation**")
        for r in rule_results:
            icon = "✅" if r.triggered else "❌"
            st.write(f"{icon} {r.rule_id} - {r.name} {'(Triggered)' if r.triggered else '(Passed)'} : {r.evidence} (Severity: {r.severity})")

    with col2:
        st.markdown("**Safety Decision Card**")
        st.metric("Decision Confidence", f"{confidence:.0f}%")
        st.metric("Required Threshold", f"{SafetyController.get_threshold():.0f}%")
        st.metric("Auto-Resolve", "✅ YES" if allowed else "❌ NO")
        if not allowed:
            st.error(f"Blocked: {reason}")
        else:
            st.success("All safety checks passed")

        if st.button("💬 Explain"):
            explanation = AIEngine.get_explanation(tx, rule_results, confidence)
            st.session_state.explanation = explanation
        if "explanation" in st.session_state:
            st.info(st.session_state.explanation)

        if st.button("💡 Suggest Resolution"):
            suggestion, _ = AIEngine.get_resolution_suggestion(tx, rule_results, confidence)
            st.session_state.suggestion = suggestion
        if "suggestion" in st.session_state:
            st.info(st.session_state.suggestion)

        if allowed:
            if st.button("⚡ Auto-Resolve", key="auto_detail"):
                suggestion, _ = AIEngine.get_resolution_suggestion(tx, rule_results, confidence)
                ResolutionService.auto_resolve(tx.id, suggestion, confidence, rule_results)
                st.success("Auto-resolved!")
                st.session_state.selected_transaction_id = None
                st.session_state.dashboard_metrics = update_metrics()
                st.rerun()  # <-- FIXED
        else:
            st.button("⚡ Auto-Resolve", disabled=True, help=f"Disabled: {reason}")

        col_h1, col_h2, col_h3 = st.columns(3)
        if col_h1.button("✅ Approve", key="approve"):
            ResolutionService.human_resolve(tx.id, "APPROVED", "Human approved", reviewer="user")
            st.success("Approved")
            st.rerun()  # <-- FIXED
        if col_h2.button("❌ Reject", key="reject"):
            ResolutionService.human_resolve(tx.id, "REJECTED", "Human rejected", reviewer="user")
            st.success("Rejected")
            st.rerun()  # <-- FIXED
        if col_h3.button("⬆ Escalate", key="escalate"):
            ResolutionService.human_resolve(tx.id, "ESCALATED", "Escalated to manager", reviewer="user")
            st.success("Escalated")
            st.rerun()  # <-- FIXED

    st.markdown("---")
    st.subheader("🤖 AI Assistant (Contextual)")
    render_chatbot(tx, rule_results, confidence, allowed)