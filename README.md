# fund-nav-platform

Small Python project that calculates a fund's NAV (net asset value) from a SQLite database, with tests and CI.

## Run (from repo root)

    python3 -m venv venv && source venv/bin/activate
    pip install pytest bandit
    sqlite3 data/fund.db < data/setup_db.sql
    python3 app/nav_calculator.py

Output: NAV printed to terminal, report written to data/nav_report.json.

## Test

    cd app && pytest -q

## Security scan

    bandit -r app -x app/test_nav_calculator.py

## CI

GitHub Actions (.github/workflows/ci-cd.yml): pytest, Bandit SAST, Docker build.

## Status / honesty notes

- terraform/ uses only the random and local providers (learning exercise). It does NOT create AWS resources.
- ansible/deploy.yml is written but has not been run against a real host.
- AWS ECR push and Trivy scanning are planned, not implemented.
