from app.models.transaction import Transaction
from app.services.rule_engine import RuleEngine

class ConfidenceEngine:

    @staticmethod
    def calculate(transaction: Transaction, rule_results):
        # Start with base 100
        score = 100.0

        # Deduct for triggered rules
        for result in rule_results:
            if result.triggered:
                if result.severity == "HIGH":
                    score -= 20
                elif result.severity == "MEDIUM":
                    score -= 10
                elif result.severity == "LOW":
                    score -= 5

        # Deduct for conflicting evidence (simulate)
        # We'll treat conflicting evidence if there is a variance > 0 and also a quantity mismatch? 
        # For demo, we'll flag if both amount and quantity mismatches occur -> conflict
        if (abs(transaction.amount - transaction.expected_amount) > 0 and 
            transaction.quantity != transaction.expected_quantity):
            score -= 30
            # also set a flag for conflicting evidence

        # Deduct for high value (risk)
        if transaction.amount > 50000:
            score -= 10

        # Deduct for repeated exceptions
        if transaction.previous_exceptions >= 2:
            score -= 10

        # Deduct for ageing
        if transaction.age_days > 14:
            score -= 5

        # Ensure within 0-100
        score = max(0, min(100, score))
        return score