# Maintenance Plan

Project 22 - AI Upskilling Recommendation System. Version 1.0, prepared 15 November 2026. Proposed operational responsibilities require team acceptance; this document does not record sign-off.

## Scope and ownership

Maintain the local Python/SQLite coursework application, student/admin browser client, curated recommendation catalog, documentation and verification tools. The repository maintainer coordinates releases; a different authorized teammate reviews each change. The person operating the local server safeguards its database and backups. Assign named owners at final acceptance.

## Routine maintenance

Before each demonstration, start the application on loopback, verify `/health`, sign in with disposable data, inspect the dashboard and confirm admin access controls. Before each proposed release, run the Python suite, JavaScript syntax check, Chromium acceptance/accessibility scan, recommender evaluation, performance check and release-gate simulations using README commands. Recheck learning links monthly while the project is used and before submission. Record date, commit, environment, command, outcome and evidence path. A provider blocking automated requests must be checked in a browser before treating its link as broken.

Review development dependency updates monthly while maintained. Keep package-lock.json, use `npm ci`, and rerun browser verification after updates. Runtime uses Python's standard library; keep the supported Python version patched. Update the SRS/RTM, SAD, tests and user manual whenever behavior or storage changes.

## Backup and verified recovery

Use an absolute path outside the repository and a new filename: `python scripts/backup_db.py <backup-path> --source <live-db-path>`. The script uses SQLite online backup and integrity checking. Back up before schema changes, before demonstrations that modify important data, and daily during active use. Proposed retention is seven daily backups and four weekly backups; the operator must confirm storage and retention at acceptance. Restrict access to the operator and authorized maintainer. Exclude all database copies and credentials from Git and submission archives.

For recovery, stop the app. Preserve the failed database separately. Restore a backup into a new path, run `PRAGMA integrity_check`, set UPSKILL_DB to that restored file, and restart on loopback. Verify login, profile, skills, portfolio and progress before resuming use. Compare expected record counts and known demonstration data. Never overwrite the sole original or sole backup. Perform a restore drill before release and after migration changes. Proposed recovery targets are one working day to restore and at most one active day's changes lost; these are team proposals, not measured service guarantees.

## Defects and incidents

Record defects in GitHub with reproducible steps, expected/actual behavior, affected revision, severity and sanitized evidence. Do not include passwords, tokens or student data. Data exposure/corruption and broken authorization block release; stop sharing the affected server, preserve evidence privately, revoke affected sessions, restore safely if needed, and verify the fix. Registration/login failure or incorrect saved progress is high priority. Cosmetic defects can be scheduled with explicit team agreement. Record the owner and resolution; close only after reproduction fails on the fixed revision and relevant regressions pass.

## Changes and rollback

Use a dedicated branch and PR with tests and updated documents. Require an independent authorized review and passing required checks. Database changes must be additive where possible, with a pre-change backup and a tested rollback/recovery path. To roll back an application change, run the prior accepted release with a compatible database; if schema compatibility is uncertain, use the corresponding verified backup. Do not move an existing release tag. Later fixes require a new reviewed version and release notes identifying impact and recovery steps.

## Freeze and handover

Freeze only after the final revision is independently approved, merged, and verified on main. Record accepted commit, reviewer, main CI run, release/tag, asset hashes, demo acceptance and academic submission receipts. Existing release automation checks PR #17 approval and main CI, but does not prove college submission or team attendance. Keep those acceptance records separately. Preserve source, SRS, SAD, Test Plan, RTM, Test Evidence, this plan, report and demo captions/videos in the handover package. Public hosting requires a separate deployment design and security review.
