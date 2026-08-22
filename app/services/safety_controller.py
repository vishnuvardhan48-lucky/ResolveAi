from app.services.confidence_engine import ConfidenceEngine
from app.database.db import query_one, execute

class SafetyController:

    @staticmethod
    def get_threshold():
        row = query_one("SELECT value FROM settings WHERE key = 'confidence_threshold'")
        if row:
            return float(row["value"])
        return 85.0  # default

    @staticmethod
    def get_auto_resolve_limit():
        row = query_one("SELECT value FROM settings WHERE key = 'auto_resolve_limit'")
        if row:
            return float(row["value"])
        return 50000.0

    @staticmethod
    def is_auto_resolution_allowed(transaction, rule_results, confidence):
        threshold = SafetyController.get_threshold()
        limit = SafetyController.get_auto_resolve_limit()

        # Conditions
        if confidence < threshold:
            return False, f"Confidence {confidence:.0f}% < required {threshold:.0f}%"

        # Check for HIGH severity triggered
        high_triggered = any(r.triggered and r.severity == "HIGH" for r in rule_results)
        if high_triggered:
            return False, "HIGH severity rule triggered"

        # Check conflicting evidence – we'll set a flag if both amount and quantity mismatches exist
        # We'll simulate by checking if variance > 0 and quantity mismatch
        if (abs(transaction.amount - transaction.expected_amount) > 0 and 
            transaction.quantity != transaction.expected_quantity):
            return False, "Conflicting evidence (amount and quantity mismatch)"

        # Check amount limit
        if transaction.amount > limit:
            return False, f"Amount ₹{transaction.amount:,.2f} exceeds autonomous limit ₹{limit:,.2f}"

        # Check status
        if transaction.status not in ["OPEN", "UNDER_REVIEW"]:
            return False, f"Transaction status '{transaction.status}' not eligible"

        return True, "All safety checks passed"