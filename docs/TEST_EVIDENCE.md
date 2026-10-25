# Test evidence – Project 22

Automated tests run via GitHub Actions on the open pull request:

https://github.com/AI-UPSKILLING-TEAM/AI-Upskilling-Recommendation-System/pull/17

The project includes:
- `tests/test_app.py`: registration, login, profile, goal, skill-gap, practice persistence and rejection of invalid input.
- `tests/test_sprint2.py`: learning resources, TF-IDF ranking, notification isolation/opt-in, admin permissions and portfolio operations.
- `tests/test_frontend_contract.py`: referenced DOM ids, duplicate HTML ids, linked browser script, external link rel safeguards.
- GitHub Actions: Python compile/tests plus `node --check app.js`; separate SRS outline job.

**Important:** GitHub Action success is evidence for the automated tests it ran, not proof of all SRS functionality. No browser accessibility audit, independent penetration test, real-user study, request-latency benchmark, or complete manual acceptance demonstration is claimed. See GitHub Actions for per-commit run and timestamps.

Previous regression: a skill-requirement ordering change caused an earlier test failure; the role-skill query now preserves stable insertion order, and subsequent CI runs passed. Retain transparent test history instead of pretending a failure never occurred.
