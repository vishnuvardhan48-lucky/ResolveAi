import streamlit as st
from app.database import query_all
from app.models.transaction import Transaction
from app.services.rule_engine import RuleEngine
from app.services.confidence_engine import ConfidenceEngine
from app.services.safety_controller import SafetyController

def compute_metrics():
    all_rows = query_all("SELECT * FROM transactions")
    open_rows = [r for r in all_rows if r["status"] in ("OPEN", "UNDER_REVIEW", "AUTO_RESOLVABLE", "HUMAN_REVIEW_REQUIRED")]
    resolved = len([r for r in all_rows if r["status"] == "RESOLVED"])
    total = len(all_rows)

    auto_resolvable = 0
    human_review = 0
    high_risk = 0

    for row in open_rows:
        tx = Transaction(**row)
        rule_results = RuleEngine.evaluate(tx)
        confidence = ConfidenceEngine.calculate(tx, rule_results)
        allowed, _ = SafetyController.is_auto_resolution_allowed(tx, rule_results, confidence)
        if allowed:
            auto_resolvable += 1
        else:
            human_review += 1
        if row["amount"] > 50000:
            high_risk += 1

    return {
        "OPEN": len(open_rows),
        "HIGH_RISK": high_risk,
        "AUTO_RESOLVABLE": auto_resolvable,
        "HUMAN_REVIEW": human_review,
        "RESOLVED": resolved,
        "TOTAL": total
    }

def render_dashboard():
    st.subheader("📊 Dashboard")
    metrics = compute_metrics()

    col1, col2, col3 = st.columns(3)
    col1.metric("🟡 Open Exceptions", metrics["OPEN"])
    col2.metric("🔴 High Risk", metrics["HIGH_RISK"])
    col3.metric("✅ Auto-Resolvable", metrics["AUTO_RESOLVABLE"])

    col4, col5, col6 = st.columns(3)
    col4.metric("👤 Human Review", metrics["HUMAN_REVIEW"])
    col5.metric("✔ Resolved", metrics["RESOLVED"])
    col6.metric("📦 Total", metrics["TOTAL"])

    if st.button("Refresh Metrics"):
        st.rerun()  # ✅ Fixed: replaces experimental_rerun

# Helper function for other modules that call update_metrics()
def update_metrics():
    return compute_metrics()