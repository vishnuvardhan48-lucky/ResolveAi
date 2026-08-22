import pytest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.transaction import Transaction
from app.services.rule_engine import RuleEngine
from app.services.confidence_engine import ConfidenceEngine
from app.services.safety_controller import SafetyController
from app.services.resolution_service import ResolutionService
from app.services.audit_service import AuditService
from app.database import init_db, execute, query_one, query_all      # <-- fixed import
from app.data.seed import seed_database

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    seed_database()
    yield

def test_amount_variance():
    tx = Transaction(amount=54500, expected_amount=50000)
    results = RuleEngine.evaluate(tx)
    r001 = next((r for r in results if r.rule_id == "R001"), None)
    assert r001 is not None
    assert r001.triggered is True
    assert "variance" in r001.evidence

def test_quantity_variance():
    tx = Transaction(quantity=12, expected_quantity=10)
    results = RuleEngine.evaluate(tx)
    r002 = next((r for r in results if r.rule_id == "R002"), None)
    assert r002 is not None
    assert r002.triggered is True

def test_repeated_exception():
    tx = Transaction(previous_exceptions=3)
    results = RuleEngine.evaluate(tx)
    r003 = next((r for r in results if r.rule_id == "R003"), None)
    assert r003 is not None
    assert r003.triggered is True

def test_ageing_rule():
    tx = Transaction(age_days=20)
    results = RuleEngine.evaluate(tx)
    r004 = next((r for r in results if r.rule_id == "R004"), None)
    assert r004 is not None
    assert r004.triggered is True

def test_high_value_rule():
    tx = Transaction(amount=125000)
    results = RuleEngine.evaluate(tx)
    r005 = next((r for r in results if r.rule_id == "R005"), None)
    assert r005 is not None
    assert r005.triggered is True

def test_confidence_calculation():
    tx = Transaction(amount=54500, expected_amount=50000, quantity=12, expected_quantity=10, previous_exceptions=2, age_days=20)
    results = RuleEngine.evaluate(tx)
    conf = ConfidenceEngine.calculate(tx, results)
    assert 0 <= conf <= 100
    assert conf < 80

def test_auto_resolution_allowed():
    tx = Transaction(amount=30000, expected_amount=30000, quantity=20, expected_quantity=20, previous_exceptions=0, age_days=1, status="OPEN")
    results = RuleEngine.evaluate(tx)
    conf = ConfidenceEngine.calculate(tx, results)
    allowed, reason = SafetyController.is_auto_resolution_allowed(tx, results, conf)
    assert allowed is True

def test_auto_resolution_blocked_high_risk():
    tx = Transaction(amount=125000, expected_amount=120000, previous_exceptions=3, age_days=20, status="OPEN")
    results = RuleEngine.evaluate(tx)
    conf = ConfidenceEngine.calculate(tx, results)
    allowed, reason = SafetyController.is_auto_resolution_allowed(tx, results, conf)
    assert allowed is False
    assert "HIGH severity" in reason or "limit" in reason

def test_low_confidence():
    tx = Transaction(amount=52000, expected_amount=50000, quantity=8, expected_quantity=10, previous_exceptions=1, age_days=3, status="OPEN")
    results = RuleEngine.evaluate(tx)
    conf = ConfidenceEngine.calculate(tx, results)
    assert conf < 85

def test_conflicting_evidence():
    tx = Transaction(amount=54000, expected_amount=50000, quantity=12, expected_quantity=10, status="OPEN")
    results = RuleEngine.evaluate(tx)
    conf = ConfidenceEngine.calculate(tx, results)
    allowed, reason = SafetyController.is_auto_resolution_allowed(tx, results, conf)
    assert allowed is False
    assert "conflicting" in reason.lower()

def test_threshold_change():
    tx = Transaction(amount=48000, expected_amount=45000, quantity=10, expected_quantity=10, previous_exceptions=1, age_days=2, status="OPEN")
    results = RuleEngine.evaluate(tx)
    conf = ConfidenceEngine.calculate(tx, results)
    execute("UPDATE settings SET value='80' WHERE key='confidence_threshold'")
    allowed1, _ = SafetyController.is_auto_resolution_allowed(tx, results, conf)
    execute("UPDATE settings SET value='90' WHERE key='confidence_threshold'")
    allowed2, _ = SafetyController.is_auto_resolution_allowed(tx, results, conf)
    if conf >= 80 and conf < 90:
        assert allowed1 is True and allowed2 is False
    execute("UPDATE settings SET value='85' WHERE key='confidence_threshold'")

def test_resolution():
    tx_id = 1
    results = RuleEngine.evaluate(Transaction(id=tx_id))
    conf = 90
    ResolutionService.auto_resolve(tx_id, "test reason", conf, results)
    row = query_one("SELECT status FROM transactions WHERE id=?", (tx_id,))
    assert row["status"] == "RESOLVED"
    audit = query_all("SELECT * FROM audit_events WHERE transaction_id=?", (tx_id,))
    assert len(audit) > 0

def test_queue_update():
    before = len(query_all("SELECT * FROM transactions WHERE status != 'RESOLVED'"))
    tx = query_one("SELECT id FROM transactions WHERE status='OPEN' LIMIT 1")
    if tx:
        ResolutionService.auto_resolve(tx["id"], "test", 90, [])
        after = len(query_all("SELECT * FROM transactions WHERE status != 'RESOLVED'"))
        assert after == before - 1

def test_audit_logging():
    AuditService.log_event(1, "system", "TEST_ACTION", "test reason", 95.0, [], "success")
    events = query_all("SELECT * FROM audit_events WHERE action='TEST_ACTION'")
    assert len(events) >= 1