from app.database.db import execute, query_all
from datetime import datetime
import json

class AuditService:

    @staticmethod
    def log_event(transaction_id, actor, action, reason, confidence=None, rule_results=None, outcome=None):
        rule_results_json = json.dumps([r.__dict__ for r in rule_results]) if rule_results else None
        execute(
            """INSERT INTO audit_events 
               (timestamp, actor, transaction_id, action, reason, confidence, rule_results, outcome)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(), actor, transaction_id, action, reason, confidence, rule_results_json, outcome)
        )

    @staticmethod
    def get_events(transaction_id=None):
        if transaction_id:
            return query_all("SELECT * FROM audit_events WHERE transaction_id = ? ORDER BY timestamp DESC", (transaction_id,))
        else:
            return query_all("SELECT * FROM audit_events ORDER BY timestamp DESC")