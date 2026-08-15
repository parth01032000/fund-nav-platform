CREATE TABLE IF NOT EXISTS funds (
    fund_id INTEGER PRIMARY KEY,
    name TEXT,
    cash REAL,
    liabilities REAL,
    shares_outstanding REAL
);

CREATE TABLE IF NOT EXISTS holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    ticker TEXT,
    quantity REAL,
    price REAL,
    FOREIGN KEY (fund_id) REFERENCES funds(fund_id)
);

INSERT INTO funds (fund_id, name, cash, liabilities, shares_outstanding)
VALUES (1, 'Sample Growth Fund', 500000, 120000, 1000000);

INSERT INTO holdings (fund_id, ticker, quantity, price) VALUES
(1, 'AAPL', 5000, 190.50),
(1, 'MSFT', 3000, 420.10),
(1, 'GOOGL', 2000, 175.30);
