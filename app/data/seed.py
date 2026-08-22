from app.database.db import execute
from app.database.schema import init_db
import random
from datetime import datetime, timedelta

def seed_database():
    init_db()
    # Clear existing data (optional)
    execute("DELETE FROM transactions")
    execute("DELETE FROM rules")
    execute("DELETE FROM settings")
    execute("DELETE FROM audit_events")
    execute("DELETE FROM resolutions")
    execute("DELETE FROM rule_results")

    # Insert default rules
    rules = [
        ("R001", "Amount Variance", "Triggers when actual amount differs from expected by threshold percent", 1, 5.0, "HIGH", 30),
        ("R002", "Quantity Variance", "Triggers when actual quantity differs from expected", 1, 0.0, "MEDIUM", 20),
        ("R003", "Repeated Exception", "Triggers when previous exceptions exceed threshold", 1, 2, "MEDIUM", 20),
        ("R004", "Ageing Transaction", "Triggers when age in days exceeds threshold", 1, 14, "MEDIUM", 15),
        ("R005", "High-Value Transaction", "Triggers when amount exceeds threshold", 1, 50000, "HIGH", 25),
    ]
    for r in rules:
        execute("INSERT INTO rules (rule_id, name, description, enabled, threshold_value, severity, weight) VALUES (?,?,?,?,?,?,?)", r)

    # Insert settings
    execute("INSERT INTO settings (key, value) VALUES ('confidence_threshold', '85')")
    execute("INSERT INTO settings (key, value) VALUES ('auto_resolve_limit', '50000')")

    # Generate 12 synthetic transactions
    now = datetime.now()
    statuses = ["OPEN", "UNDER_REVIEW", "AUTO_RESOLVABLE", "HUMAN_REVIEW_REQUIRED", "RESOLVED"]
    transactions = [
        # 1. Simple amount mismatch
        ("EX-1001", "ABC Supplies", "Invoice", 54500, 50000, 10, 10, (now - timedelta(days=2)).isoformat(), 2, "Office Supplies", "Credit", "Tier 2", 1, "OPEN"),
        # 2. Quantity mismatch
        ("EX-1002", "Nova Logistics", "Invoice", 28000, 28000, 12, 10, (now - timedelta(days=5)).isoformat(), 5, "Logistics", "Credit", "Tier 1", 0, "OPEN"),
        # 3. High-value
        ("EX-1003", "XYZ Corp", "Invoice", 125000, 120000, 5, 5, (now - timedelta(days=1)).isoformat(), 1, "Services", "Wire", "Tier 3", 2, "OPEN"),
        # 4. Low-confidence
        ("EX-1004", "Delta Inc", "Invoice", 52000, 50000, 8, 10, (now - timedelta(days=3)).isoformat(), 3, "IT Equipment", "Credit", "Tier 1", 1, "OPEN"),
        # 5. Repeated exception
        ("EX-1005", "EcoEnergy", "Invoice", 34000, 34000, 10, 10, (now - timedelta(days=10)).isoformat(), 10, "Utilities", "Debit", "Tier 2", 3, "OPEN"),
        # 6. Ageing
        ("EX-1006", "GlobalTrade", "Invoice", 45000, 45000, 15, 15, (now - timedelta(days=20)).isoformat(), 20, "Consulting", "Wire", "Tier 1", 0, "OPEN"),
        # 7. Safe auto-resolvable
        ("EX-1007", "LocalMart", "Invoice", 30000, 30000, 20, 20, (now - timedelta(days=1)).isoformat(), 1, "Retail", "Credit", "Tier 2", 0, "OPEN"),
        # 8. Conflicting evidence
        ("EX-1008", "Omega LLC", "Invoice", 54000, 50000, 12, 10, (now - timedelta(days=4)).isoformat(), 4, "Equipment", "Credit", "Tier 1", 0, "OPEN"),
        # 9. Multiple rules
        ("EX-1009", "Prime Corp", "Invoice", 62000, 55000, 5, 5, (now - timedelta(days=8)).isoformat(), 8, "Marketing", "Wire", "Tier 3", 2, "OPEN"),
        # 10. Borderline confidence
        ("EX-1010", "BlueWave", "Invoice", 48000, 45000, 10, 10, (now - timedelta(days=2)).isoformat(), 2, "Software", "Credit", "Tier 2", 1, "OPEN"),
        # 11. Clean low-risk
        ("EX-1011", "GreenEnergy", "Invoice", 22000, 22000, 5, 5, (now - timedelta(days=0)).isoformat(), 0, "Utilities", "Debit", "Tier 1", 0, "OPEN"),
        # 12. High-risk financial
        ("EX-1012", "FinanceOne", "Invoice", 98000, 95000, 3, 3, (now - timedelta(days=15)).isoformat(), 15, "Financial", "Wire", "Tier 3", 4, "OPEN"),
    ]

    for t in transactions:
        execute("""INSERT INTO transactions 
            (transaction_id, vendor, transaction_type, amount, expected_amount, quantity, expected_quantity, 
             transaction_date, age_days, category, payment_method, customer_vendor_tier, previous_exceptions, status)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", t)

    # Create some resolved items for testing
    # We'll resolve EX-1007 later by UI, but we can also seed one already resolved:
    # Actually we keep all open for demo.