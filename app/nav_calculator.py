import sqlite3
import json
from datetime import date

def get_connection(db_path="data/fund.db"):
    return sqlite3.connect(db_path)

def calculate_nav(fund_id, conn):
    cur = conn.cursor()

    cur.execute("SELECT SUM(quantity * price) FROM holdings WHERE fund_id = ?", (fund_id,))
    total_holdings_value = cur.fetchone()[0] or 0

    cur.execute("SELECT cash FROM funds WHERE fund_id = ?", (fund_id,))
    cash = cur.fetchone()[0] or 0

    cur.execute("SELECT liabilities FROM funds WHERE fund_id = ?", (fund_id,))
    liabilities = cur.fetchone()[0] or 0

    cur.execute("SELECT shares_outstanding FROM funds WHERE fund_id = ?", (fund_id,))
    shares = cur.fetchone()[0]

    total_assets = total_holdings_value + cash
    net_assets = total_assets - liabilities

    if shares == 0:
        raise ValueError("Shares outstanding cannot be zero")

    return round(net_assets / shares, 4)

def generate_report(fund_id, conn, output_path="data/nav_report.json"):
    nav = calculate_nav(fund_id, conn)
    report = {"fund_id": fund_id, "date": str(date.today()), "nav_per_share": nav}
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"NAV report generated: {report}")
    return report

if __name__ == "__main__":
    conn = get_connection()
    generate_report(fund_id=1, conn=conn)
