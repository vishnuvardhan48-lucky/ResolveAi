import sqlite3
import json
from datetime import datetime

DB_PATH = "resolveai.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def query_one(sql, params=()):
    conn = get_db()
    conn.row_factory = dict_factory
    cur = conn.execute(sql, params)
    row = cur.fetchone()
    conn.close()
    return row

def query_all(sql, params=()):
    conn = get_db()
    conn.row_factory = dict_factory
    cur = conn.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def execute(sql, params=()):
    conn = get_db()
    cur = conn.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id