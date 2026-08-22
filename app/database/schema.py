import sqlite3

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT UNIQUE,
    vendor TEXT,
    transaction_type TEXT,
    amount REAL,
    expected_amount REAL,
    quantity INTEGER,
    expected_quantity INTEGER,
    transaction_date TEXT,
    age_days INTEGER,
    category TEXT,
    payment_method TEXT,
    customer_vendor_tier TEXT,
    previous_exceptions INTEGER,
    status TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id TEXT UNIQUE,
    name TEXT,
    description TEXT,
    enabled INTEGER DEFAULT 1,
    threshold_value REAL,
    severity TEXT,
    weight INTEGER
);

CREATE TABLE IF NOT EXISTS rule_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER,
    rule_id TEXT,
    triggered INTEGER,
    severity TEXT,
    evidence TEXT,
    weight INTEGER,
    evaluated_at TEXT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

CREATE TABLE IF NOT EXISTS resolutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER,
    action TEXT,
    resolution_details TEXT,
    resolved_at TEXT,
    reviewer TEXT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    actor TEXT,
    transaction_id INTEGER,
    action TEXT,
    reason TEXT,
    confidence REAL,
    rule_results TEXT,
    outcome TEXT
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""

def init_db():
    conn = sqlite3.connect("resolveai.db")
    conn.executescript(CREATE_TABLES)
    conn.commit()
    conn.close()