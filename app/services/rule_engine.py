from app.models.transaction import Transaction
from app.models.rule import Rule, RuleResult
from app.database.db import query_all, get_db
import datetime

class RuleEngine:

    @staticmethod
    def get_enabled_rules():
        rows = query_all("SELECT * FROM rules WHERE enabled = 1")
        rules = []
        for r in rows:
            rules.append(Rule(
                rule_id=r["rule_id"],
                name=r["name"],
                description=r["description"],
                enabled=bool(r["enabled"]),
                threshold_value=r["threshold_value"] or 0.0,
                severity=r["severity"],
                weight=r["weight"]
            ))
        return rules

    @staticmethod
    def evaluate(transaction: Transaction):
        rules = RuleEngine.get_enabled_rules()
        results = []
        for rule in rules:
            triggered = False
            evidence = ""
            if rule.rule_id == "R001":  # Amount Variance
                threshold = rule.threshold_value  # in percent
                if transaction.expected_amount > 0:
                    var = abs(transaction.amount - transaction.expected_amount) / transaction.expected_amount * 100
                    if var > threshold:
                        triggered = True
                        evidence = f"Actual ₹{transaction.amount:,.2f} vs Expected ₹{transaction.expected_amount:,.2f} (variance {var:.1f}%)"
            elif rule.rule_id == "R002":  # Quantity Variance
                if transaction.quantity != transaction.expected_quantity:
                    triggered = True
                    evidence = f"Actual {transaction.quantity} vs Expected {transaction.expected_quantity}"
            elif rule.rule_id == "R003":  # Repeated Exception
                if transaction.previous_exceptions >= int(rule.threshold_value):
                    triggered = True
                    evidence = f"{transaction.previous_exceptions} previous exceptions (threshold {int(rule.threshold_value)})"
            elif rule.rule_id == "R004":  # Ageing
                if transaction.age_days > rule.threshold_value:
                    triggered = True
                    evidence = f"Age {transaction.age_days} days (threshold {rule.threshold_value} days)"
            elif rule.rule_id == "R005":  # High Value
                if transaction.amount > rule.threshold_value:
                    triggered = True
                    evidence = f"Amount ₹{transaction.amount:,.2f} exceeds threshold ₹{rule.threshold_value:,.2f}"
            # Add more rules as needed

            results.append(RuleResult(
                rule_id=rule.rule_id,
                name=rule.name,
                triggered=triggered,
                severity=rule.severity,
                evidence=evidence,
                weight=rule.weight
            ))
        return results