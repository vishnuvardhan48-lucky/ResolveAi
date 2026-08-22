import streamlit as st
from app.services.ai_engine import AIEngine
import json

def render_chatbot(tx, rule_results, confidence, allowed):
    # Simple chat interface
    user_input = st.text_input("Ask a question about this exception:", key="chat_input")
    if st.button("Send", key="chat_send"):
        if user_input:
            # Build contextual response
            context = f"""
            Transaction: {tx.transaction_id}
            Vendor: {tx.vendor}
            Amount: ₹{tx.amount:,.2f} (Expected: ₹{tx.expected_amount:,.2f})
            Quantity: {tx.quantity} (Expected: {tx.expected_quantity})
            Age: {tx.age_days} days
            Previous exceptions: {tx.previous_exceptions}
            Status: {tx.status}
            Rules triggered: {[r.rule_id for r in rule_results if r.triggered]}
            Confidence: {confidence:.0f}%
            Auto-resolve allowed: {allowed}
            """
            # Use AI engine to generate answer based on user input and context
            # For simplicity, we'll use deterministic responses
            # In full implementation, we'd use LLM with context.
            # We'll include a simple keyword matching.
            response = ""
            if "why" in user_input.lower() or "flagged" in user_input.lower():
                response = AIEngine.get_explanation(tx, rule_results, confidence)
            elif "resolve" in user_input.lower() or "recommend" in user_input.lower():
                suggestion, _ = AIEngine.get_resolution_suggestion(tx, rule_results, confidence)
                response = suggestion
            elif "auto" in user_input.lower() and "resolve" in user_input.lower():
                if allowed:
                    response = "Auto-resolution is permitted. Click the Auto-Resolve button."
                else:
                    response = f"Auto-resolution is blocked: {reason}"
            elif "confidence" in user_input.lower():
                response = f"Decision Confidence Score is {confidence:.0f}%. This is based on rule severity, evidence, and risk factors."
            else:
                response = "I can help with questions about why this was flagged, suggested resolution, auto-resolve status, and confidence. Please ask a specific question."
            st.info(response)
        else:
            st.warning("Please enter a question.")

    # Show chat history (optional)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    # For demo, we'll just show the last response in the info box.