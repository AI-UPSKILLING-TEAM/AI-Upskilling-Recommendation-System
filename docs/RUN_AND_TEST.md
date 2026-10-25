# Project 22 – Running and Testing the Prototype

## Prerequisites
- Python 3.10 or newer.
- No external Python packages are needed for the application.
- GitHub's separate SRS-outline workflow installs `pypdf` solely to read requirements.

## Start locally
1. In the repository directory, run `python app.py`.
2. Open **http://127.0.0.1:8000** on the same machine.
3. Register using a demo-only email and **unique, disposable** password.
4. Sign in. Set a career goal and your interests; select existing skills.
5. Add demo courses, projects or certifications to your portfolio.
6. Examine role readiness, missing skills and ranked external learning links.
7. Tick a practice activity; check the *Practice progress* percentage.
8. Opt into practice notifications and try marking a notification as read.
9. Sign out and verify protected dashboard access is denied.

## Optional admin demonstration
To promote an **already registered** local demo user from the command line, stop the server and run:

```bash
python app.py promote-admin demo@example.com
python app.py
```

After signing in, the role-protected admin panel supports adding resources and updating required skills for career roles. Only perform this on your own local test database; do not promote a real user or store genuine student data.

## Automated verification
```bash
python -m compileall -q app.py recommendations.py scripts
python -m unittest discover -s tests -v
node --check app.js
```

The JS check requires Node.js; Python tests use the standard library. GitHub Actions performs all checks on PRs into main.

## Known boundaries
- Recommendations rank course/resource descriptions with TF-IDF cosine similarity; there is **no trained predictive AI model**.
- Learning links are educational references, not guaranteed to be current or universally appropriate.
- Notifications are local in-app events, not messages sent by email, SMS or push.
- Not all FR-01–FR-38 and NFR-01–NFR-10 acceptance criteria are met; see `REQUIREMENTS_TRACEABILITY_DRAFT.md`.
- This is a local demonstration server bound to 127.0.0.1 by default. Do **not** expose it publicly without HTTPS, stronger account and session controls, testing and privacy protections.
