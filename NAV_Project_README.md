# Fund NAV Calculation Platform

A simplified Net Asset Value (NAV) calculation service for a mutual fund, built to demonstrate a full DevOps toolchain — Python, SQL, Docker, Terraform, GitHub Actions CI/CD, and security scanning — applied to a domain-relevant financial workflow.

## What this project does

Every asset manager calculates a fund's Net Asset Value daily: the per-share price of the fund, based on its total holdings, cash, and liabilities. This project implements a simplified version of that calculation, reading fund data from a SQL database and generating a daily NAV report.

**NAV formula:**
```
NAV per share = (Total Assets − Total Liabilities) ÷ Shares Outstanding
Total Assets = (holdings value: quantity × price, summed) + cash
```

## Why this project exists

Built specifically to demonstrate hands-on experience with a real-world DevOps and cloud stack — Python, SQL, Docker, Terraform, CI/CD, and security scanning — applied to a domain-relevant problem rather than a generic demo. This isn't based on real financial data or prior industry experience; it's a self-directed project built to understand both the technology and the business context together.

## Architecture

```
fund-nav-platform/
├── app/
│   ├── nav_calculator.py       → core NAV calculation logic
│   ├── test_nav_calculator.py  → unit tests (pytest)
│   ├── requirements.txt
│   └── Dockerfile
├── data/
│   └── setup_db.sql            → sample fund and holdings schema + seed data
├── terraform/
│   └── main.tf                 → provisions an AWS ECR repository (with vulnerability scanning)
├── .github/workflows/
│   └── ci-cd.yml                → tests, SAST scan (Bandit), Docker build
└── README.md
```

## Pipeline flow

```
Push to main
   │
   ▼
Run pytest (unit tests)
   │
   ▼
Run Bandit SAST scan (application code only, tests excluded)
   │
   ▼
Build Docker image
```

## Running it locally

Requires: Python 3.11+, SQLite3 (pre-installed on macOS), Docker.

```bash
# 1. Clone and set up environment
git clone https://github.com/parth01032000/fund-nav-platform.git
cd fund-nav-platform
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt

# 2. Set up the sample database
sqlite3 data/fund.db < data/setup_db.sql

# 3. Run the NAV calculation
cd app
python3 nav_calculator.py
cd ..
cat data/nav_report.json

# 4. Run tests
cd app
pytest -v
cd ..

# 5. Run the SAST security scan
bandit -r app/ -f screen --exclude ./app/test_nav_calculator.py
```

## Running it in Docker

```bash
docker build -t fund-nav-platform:latest ./app
docker run --rm -v $(pwd)/data:/app/data fund-nav-platform:latest
```
Note: the local `data/` folder is mounted into the container (`-v $(pwd)/data:/app/data`) since the container image itself doesn't include the SQLite database — this keeps the database separate from the application code, closer to how a real deployment would connect to an external database rather than bundling data into the image.

## Infrastructure (Terraform)

```bash
cd terraform
terraform init
terraform plan
terraform apply   # optional — creates a real AWS ECR repository with scan-on-push enabled
```

## What I'd add for a production version

- Real cloud deployment with the ECR repository actually provisioned and wired into the CI pipeline
- A managed database (RDS Postgres) instead of local SQLite
- DAST scanning (e.g. OWASP ZAP) against a running instance
- Ansible playbook for automated deployment to a target host
- Approval gates before promoting any change to a production environment

## Tech stack

Python · SQL (SQLite) · Docker · Terraform · GitHub Actions · Bandit (SAST) · Trivy (SCA, via ECR scan-on-push)
