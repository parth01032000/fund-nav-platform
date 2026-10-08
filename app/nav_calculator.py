import sqlite3
import json
from datetime import date

def get_connection(db_path="data/fund.db"):
    return sqlite3.connect(db_path)

def calculate_nav(fund_id, conn):
    cur = conn.cursor()

    cur.execute(
        "SELECT cash, liabilities, shares_outstanding FROM funds WHERE fund_id = ?",
        (fund_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"Fund {fund_id} not found")
    cash, liabilities, shares = (value or 0 for value in row)

    if shares == 0:
        raise ValueError("Shares outstanding cannot be zero")

    cur.execute("SELECT SUM(quantity * price) FROM holdings WHERE fund_id = ?", (fund_id,))
    holdings_value = cur.fetchone()[0] or 0

    net_assets = holdings_value + cash - liabilities
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
