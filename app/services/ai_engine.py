import os
import openai
from app.models.transaction import Transaction
from app.services.rule_engine import RuleEngine
from app.services.confidence_engine import ConfidenceEngine
from app.services.safety_controller import SafetyController
import json

class AIEngine:

    @staticmethod
    def get_explanation(transaction: Transaction, rule_results, confidence):
        # Build deterministic explanation first
        triggered = [r for r in rule_results if r.triggered]
        if not triggered:
            base = f"Transaction {transaction.transaction_id} has no triggered rules and appears clean."
        else:
            reasons = "; ".join([f"{r.name} ({r.evidence})" for r in triggered])
            base = f"Transaction {transaction.transaction_id} was flagged because: {reasons}."
            base += f" Decision Confidence is {confidence:.0f}%."

        # Try LLM if key exists
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai.api_key = api_key
            try:
                prompt = f"""
                Provide a clear, concise explanation for this transaction exception.
                Data:
                {json.dumps(transaction.__dict__, default=str, indent=2)}
                Rule results: {[r.__dict__ for r in rule_results]}
                Confidence: {confidence:.0f}%
                """
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a financial exception assistant. Explain why this transaction was flagged based on the data provided. Do not make up facts."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=150
                )
                llm_text = response.choices[0].message.content
                return f"{llm_text}\n\n(Confidence: {confidence:.0f}%)"
            except Exception as e:
                return base + f" (AI language service unavailable: {str(e)})"
        else:
            return base

    @staticmethod
    def get_resolution_suggestion(transaction: Transaction, rule_results, confidence):
        # deterministic
        triggered = [r for r in rule_results if r.triggered]
        if not triggered:
            return "No action needed; transaction appears normal.", confidence
        # suggest based on triggered rules
        suggestions = []
        for r in triggered:
            if r.rule_id == "R001":
                suggestions.append("Request corrected invoice or adjust expected amount based on purchase order.")
            elif r.rule_id == "R002":
                suggestions.append("Verify quantity discrepancy with supplier.")
            elif r.rule_id == "R003":
                suggestions.append("Review vendor history and consider escalations.")
            elif r.rule_id == "R004":
                suggestions.append("Follow up with vendor for overdue transaction.")
            elif r.rule_id == "R005":
                suggestions.append("Requires senior approval due to high value.")
        suggestion = " ".join(suggestions)
        # check if auto-allowed
        allowed, reason = SafetyController.is_auto_resolution_allowed(transaction, rule_results, confidence)
        if allowed:
            suggestion += " This transaction is eligible for auto-resolution."
        else:
            suggestion += f" Auto-resolution is blocked: {reason}."
        return suggestion, confidence