import pytest
import sqlite3
from nav_calculator import calculate_nav

def setup_test_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE funds (fund_id INTEGER, cash REAL, liabilities REAL, shares_outstanding REAL)")
    conn.execute("CREATE TABLE holdings (fund_id INTEGER, quantity REAL, price REAL)")
    conn.execute("INSERT INTO funds VALUES (1, 1000, 200, 100)")
    conn.execute("INSERT INTO holdings VALUES (1, 10, 50)")
    conn.commit()
    return conn

def test_calculate_nav():
    conn = setup_test_db()
    nav = calculate_nav(1, conn)
    assert nav == 13.0

def test_zero_shares_raises():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE funds (fund_id INTEGER, cash REAL, liabilities REAL, shares_outstanding REAL)")
    conn.execute("CREATE TABLE holdings (fund_id INTEGER, quantity REAL, price REAL)")
    conn.execute("INSERT INTO funds VALUES (1, 1000, 200, 0)")
    conn.commit()
    with pytest.raises(ValueError):
        calculate_nav(1, conn)
