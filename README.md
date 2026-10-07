# fund-nav-platform

A small Python tool that calculates a fund's **NAV per share** (Net Asset Value per share) from a SQLite database and writes the result to a JSON report. It is wrapped in the engineering habits real teams use: unit tests, a static security scan, a Docker image, and a GitHub Actions pipeline.

## What is NAV?

A fund is a shared pot of money. Investors own *shares* of it. NAV per share answers: if the fund sold everything and paid every debt, what would one share be worth?

```
NAV per share = (value of holdings + cash - liabilities) / shares outstanding
```

Worked example from the sample data (fund 1):

| Step | Calculation | Result |
|------|-------------|--------|
| Holdings value | 5000 x 190.50 + 3000 x 420.10 + 2000 x 175.30 | 2,563,400 |
| Total assets | 2,563,400 + 500,000 cash | 3,063,400 |
| Net assets | 3,063,400 - 120,000 liabilities | 2,943,400 |
| NAV per share | 2,943,400 / 1,000,000 shares | **2.9434** |

## Tech stack

| Area | Technology | Purpose |
|------|------------|---------|
| Language | Python 3.11 | Application logic |
| Database | SQLite (`sqlite3` module) | Stores funds and holdings in a single file |
| Testing | pytest | Unit tests on an in-memory database |
| Security scan | Bandit | Static analysis (SAST) of the application code |
| Containers | Docker (python:3.11-slim) | Reproducible packaging |
| CI | GitHub Actions | Runs tests, scan and image build on every push to `main` |
| Infrastructure as code | Terraform (`random`, `local` providers) | Learning scaffold, see Limitations |
| Configuration management | Ansible | Learning scaffold, see Limitations |

## How it works

```
data/setup_db.sql --> data/fund.db (SQLite)
                          |
                          v
        app/nav_calculator.py
          get_connection()  -> opens the database
          calculate_nav()   -> queries holdings, cash, liabilities, shares; computes NAV
          generate_report() -> writes data/nav_report.json
```

- `get_connection(db_path)` takes the path as a parameter, so tests can pass an in-memory database.
- `calculate_nav(fund_id, conn)` uses parameterised SQL (`?` placeholders), so values are never concatenated into queries. It raises `ValueError` if shares outstanding is zero.
- `generate_report(fund_id, conn, output_path)` calls `calculate_nav` and writes `{fund_id, date, nav_per_share}` as JSON.

## Data model

| Table | One row is | Columns |
|-------|------------|---------|
| `funds` | one fund | `fund_id`, `name`, `cash`, `liabilities`, `shares_outstanding` |
| `holdings` | one stock held by a fund | `id`, `fund_id`, `ticker`, `quantity`, `price` |

`holdings.fund_id` is a foreign key to `funds.fund_id`.

## Project structure

```
app/
  nav_calculator.py        Core logic
  test_nav_calculator.py   Unit tests
  requirements.txt         Python dependencies
  Dockerfile               Container image
data/
  setup_db.sql             Schema and sample data
terraform/                 Terraform scaffold
ansible/                   Ansible playbook scaffold
.github/workflows/         CI pipeline
```

## Prerequisites

- Python 3.11 or newer
- The `sqlite3` command line tool (preinstalled on macOS and most Linux systems)
- Docker (optional, only for the container steps)

## Quick start

Run everything from the **repository root**.

```bash
git clone https://github.com/parth01032000/fund-nav-platform.git
cd fund-nav-platform
python3 -m venv venv
source venv/bin/activate
pip install pytest bandit
sqlite3 data/fund.db < data/setup_db.sql
python3 app/nav_calculator.py
```

Expected output:

```
NAV report generated: {'fund_id': 1, 'date': '<today>', 'nav_per_share': 2.9434}
```

The report is saved to `data/nav_report.json`.

To start again with fresh data:

```bash
rm -f data/fund.db && sqlite3 data/fund.db < data/setup_db.sql
```

## Inspect the data

```bash
sqlite3 data/fund.db ".tables"
sqlite3 data/fund.db "SELECT * FROM funds;"
sqlite3 data/fund.db "SELECT ticker, quantity, price FROM holdings;"
```

## Run the tests

```bash
cd app
python -m pytest -v
```

Two tests run against an in-memory SQLite database:

- `test_calculate_nav` checks a hand-calculated result: (10 x 50 + 1000 - 200) / 100 = 13.0
- `test_zero_shares_raises` checks that zero shares outstanding raises `ValueError`

## Security scan

```bash
bandit -r app -x app/test_nav_calculator.py
```

Test files are excluded because pytest uses `assert` on purpose, which Bandit flags (B101).

## Run in Docker

```bash
docker build -t fund-nav ./app
docker run --rm -v "$(pwd)/data:/app/data" fund-nav
```

The image contains only the script and its dependencies. The database is mounted as a volume, so data stays separate from code. Create `data/fund.db` first (see Quick start).

## CI pipeline

`.github/workflows/ci-cd.yml` runs on every push to `main`:

1. Set up Python 3.11 and install pytest and Bandit
2. Run the tests
3. Run the Bandit security scan (tests excluded)
4. Build the Docker image, tagged with the commit SHA

## Design decisions

- **Dependency injection for the connection:** makes the code testable without touching real data.
- **Parameterised queries:** protects against SQL injection.
- **Explicit zero-shares guard:** a clear error instead of a crash or a silently wrong number.
- **Calculation and reporting are separate functions:** each can be tested independently.
- **Tests on an in-memory database:** fast, isolated and repeatable.

## Limitations

Stated plainly, so nothing is overclaimed:

- Terraform uses only the `random` and `local` providers. It writes a note about a *planned* ECR repository and **does not create any AWS resources**.
- The Ansible playbook is written but has **not been run** against a real host.
- ECR image scanning and Trivy are planned, not implemented.
- Money is stored as floating point. Production should use `Decimal` or integer cents.
- Requesting a fund that does not exist currently raises a `TypeError` instead of a clear message.
- `fund_id` is fixed to 1 in the command-line entry point.
- No logging, no coverage threshold, no deployment stage in CI.

## Roadmap: running this on AWS

| Today | Target on AWS |
|-------|---------------|
| SQLite file | RDS Postgres in private subnets, credentials in Secrets Manager |
| Docker image on a laptop | Image in ECR with scan on push |
| Manual run | ECS Fargate scheduled task triggered by EventBridge |
| JSON report on disk | Report written to S3 |
| Local logs | CloudWatch logs and alarms |
| `local` and `random` Terraform providers | Terraform `aws` provider |
| CI only | GitHub Actions assuming an IAM role via OIDC to push images (no stored AWS keys) |
