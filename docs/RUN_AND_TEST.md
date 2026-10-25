# Project 22: Run and Test Guide

## Requirements
- Python 3.10 or newer.
- No external Python packages required.

## Run
1. From the repository root, run `python app.py`.
2. Open http://127.0.0.1:8000 in a browser.
3. Register with a disposable password of at least 8 characters, sign in, choose a career goal, select skills and save.
4. Review the missing skills, recommended topics and learning progress checklist.
5. Stop the server with Ctrl+C.

The server binds to 127.0.0.1 by default for local demonstration; it is not configured for production deployment. SQLite creates a local upskill.db file automatically. The .gitignore excludes database files.

## Tests
Run `python -m unittest discover -s tests -v`.
A GitHub Actions workflow runs the same test command on pull requests to main.

## Application scope
Implemented: account creation, authentication, profile, skill selection, career goal, deterministic skill-gap analysis, suggestions, progress flags and dashboard.

Not yet implemented: actual machine-learning recommendations, curated external course links, notifications, administrator management, cloud deployment and multi-user load testing.

## Safety and limitations
This is an educational prototype, not a production service. Do not enter real student personal data. Tokens are stored in browser sessionStorage; no third-party tracking is used. Use HTTPS, stronger session/CSRF controls, user-data retention design, account recovery, and further security review before any real deployment.
