from app.database.db import execute, query_one
from app.services.audit_service import AuditService
from datetime import datetime

class ResolutionService:

    @staticmethod
    def auto_resolve(transaction_id, reason, confidence, rule_results):
        # Update transaction status
        execute(
            "UPDATE transactions SET status = 'RESOLVED', updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), transaction_id)
        )
        # Insert into resolutions
        execute(
            "INSERT INTO resolutions (transaction_id, action, resolution_details, resolved_at, reviewer) VALUES (?, ?, ?, ?, ?)",
            (transaction_id, "AUTO_RESOLVED", reason, datetime.now().isoformat(), "system")
        )
        # Log audit
        AuditService.log_event(
            transaction_id=transaction_id,
            actor="system",
            action="AUTO_RESOLVED",
            reason=reason,
            confidence=confidence,
            rule_results=rule_results,
            outcome="success"
        )

    @staticmethod
    def human_resolve(transaction_id, action, reason, reviewer="human"):
        # action: 'APPROVED', 'REJECTED', 'ESCALATED'
        status_map = {
            "APPROVED": "RESOLVED",
            "REJECTED": "REJECTED",
            "ESCALATED": "ESCALATED"
        }
        new_status = status_map.get(action, "RESOLVED")
        execute(
            "UPDATE transactions SET status = ?, updated_at = ? WHERE id = ?",
            (new_status, datetime.now().isoformat(), transaction_id)
        )
        execute(
            "INSERT INTO resolutions (transaction_id, action, resolution_details, resolved_at, reviewer) VALUES (?, ?, ?, ?, ?)",
            (transaction_id, action, reason, datetime.now().isoformat(), reviewer)
        )
        AuditService.log_event(
            transaction_id=transaction_id,
            actor=reviewer,
            action=action,
            reason=reason,
            confidence=None,
            rule_results=None,
            outcome="success"
        )