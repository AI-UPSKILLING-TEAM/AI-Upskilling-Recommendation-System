# SkillPath - AI-Powered Upskilling Recommendation System
Software Engineering Mini-Project | Project ID 22 | PES University

A runnable student career-planning application with academic profiles, self-assessed skill levels, missing/weak gap analysis, personalized learning paths, original project suggestions, optional official credential references, private portfolios, persistent practice progress, notifications and protected administrator management.

## Run
Requires Python 3.10 or newer. No third-party Python package is needed to run the product.

```sh
python app.py
```

Open http://127.0.0.1:8000 . Windows users can also run START_WINDOWS.cmd. Register a demonstration account and sign in. Data persists in upskill.db (excluded from Git). Set UPSKILL_DB, HOST or PORT to change configuration; keep loopback binding for local use.

To enable a legitimate administrator, register that account and run locally:

```sh
python app.py promote-admin your-account@example.com
```

Refresh or sign in again. There is no default admin password or remote promotion endpoint. See [User manual](docs/USER_MANUAL.md).

## Verify
```sh
python -m unittest discover -s tests -v
node --check app.js
npm ci
npx playwright install chromium
npm run test:browser
python scripts/evaluate_recommender.py
python scripts/benchmark.py
python scripts/audit_links.py
```

Normal use needs only Python. Node/Playwright/axe-core are development tools. Optional PDF generation uses requirements-docs.txt. CI tests Linux/Windows, Python 3.11/3.12 and Chromium. Raw local results and screenshots are in evidence/.

## Documents and demonstration
- [Architecture and design](docs/SAD.md)
- [Test plan](docs/TEST_PLAN.md) and [actual results](docs/TEST_EVIDENCE.md)
- [All 38 FR and 10 NFR mapped](docs/REQUIREMENTS_TRACEABILITY.md)
- [Sprint plan](docs/SPRINT_PLAN.md) and [GitHub Project](https://github.com/orgs/AI-UPSKILLING-TEAM/projects/1)
- [Recommender method and limits](docs/RECOMMENDER_METHOD_AND_LIMITS.md)
- [Design decisions / process status](docs/DEVIATIONS_AND_PENDING.md)
- [Demo guide](docs/DEMO_RECORDING_GUIDE.md) and [release/freeze checklist](docs/RELEASE_AND_FREEZE_CHECKLIST.md)
- [One-minute Sprint 1 recovery demo](evidence/videos/Sprint_1_Demo.mp4)
- [Two-minute Sprint 2 working-product demo](evidence/videos/Sprint_2_Demo.mp4)
- Original source: [SRS](SRS_Project_ID_22.pdf)

The new SAD/Test Plan were created because the originals were unavailable. Sprint 1 recovery evidence is dated 25 October. The final Sprint 2 demo is dated 26 October, within its scheduled 26-30 October week. PR #17 remains subject to genuine independent review, owner merge and formal sprint acceptance/freeze. This branch and the submission package contain the candidate; main changes only after review/merge.

## Recommendation method
TF-IDF cosine similarity ranks curated reference resources for missing/weak skills using goal, interests and portfolio context. The SRS allows reference data. This is content-based ranking, not a trained predictor of student outcomes. Practice completion does not prove proficiency. The synthetic evaluation and its limitations are documented.

## Team

| Name | SRN | GitHub |
|---|---|---|
| Poojitha V | PES2UG24AM113 | poojithav77 |
| Manasa C | PES2UG25AM803 | manasachandru12345 |
| Shanmuga | PES2UG24AM083 | shanmugavel30072006-blip |
| Manish S | PES2UG24AM085 | ManishS943 |

## Backup and operational scope
Use `python scripts/backup_db.py backup.db` for a verified online backup. Keep backups outside source publication. This is a local coursework server; internet deployment requires production hosting, HTTPS and a separate security/operations review.

## Accepted release and freeze
PR #17 is queued for native auto-merge behind a genuine teammate approval and required CI. After the reviewed merge and successful main verification, .github/workflows/release.yml checks the actual final-revision approval, creates the frozen v1.0.0 release with verified report/videos and closes accepted backlog items. See docs/RELEASE_AND_FREEZE_CHECKLIST.md. The automation cannot create a teammate approval.
