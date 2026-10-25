# Installation and User Manual
Project 22 | Python 3.10+ | Local browser application

## Start
From the project folder run `python app.py`, or double-click START_WINDOWS.cmd. Open http://127.0.0.1:8000. No pip installation is required for normal use. The first run creates upskill.db and seeds six career roles and sixteen skills. Press Ctrl+C to stop. HOST, PORT and UPSKILL_DB optionally change binding and database location.

## Student workflow
1. Register with a name, valid email and an 8-128 character password, then sign in. Duplicate emails and invalid credentials are rejected. Use demonstration data when sharing the screen.
2. Save your name, career goal, department/course, academic year, optional phone and interests. Select a role before expecting career-specific recommendations.
3. Check existing skills and choose Beginner (1), Intermediate (2) or Advanced (3), then save. Unchecking removes a skill. Checked skills can still be weak when below the role's target. Readiness measures self-reported requirements met, not employment eligibility.
4. Add completed courses, projects and certifications to the portfolio with title and related skill. Remove entries when needed. Portfolio titles inform recommendation context but do not automatically prove skill proficiency.
5. Inspect missing/weak gaps. Follow recommended course/resource links and practical project prompts. Optional certifications appear only where applicable; consult provider requirements directly.
6. Mark required topics Practiced as you complete them. Unchecking reverses completion. Progress is role-relative and survives refresh/restart. Switching goal changes the denominator while preserving stored topics. Practice completion does not change proficiency.
7. Enable in-app notifications to receive a new milestone event once per newly completed topic. Mark events read. No email/SMS service is used. Sign out to revoke the session.

## Administrator setup
Register the account normally, then run `python app.py promote-admin your-account@example.com` against the same database. Refresh or sign in again. Only a person with local server/database authority should run that command. No default admin password or remote promotion endpoint exists.

## Administrator workflow
Create skills in Skill catalog; in-use skills are protected from deletion. Create/update role requirements using comma-separated names with optional target levels, such as `Python:2, SQL:3`. Edit loads existing values; selected roles cannot be deleted. Create courses/resources using a catalog skill, title, public HTTPS URL and description. Edit loads the same id for updating. Delete removes the custom row; built-in reference data remains a fallback. Student forms support name, department and year edits; deleting an account removes its private data and sessions. Shared-data changes appear in the audit log.

## Troubleshooting and recovery
If the port is in use, select an available PORT and use that address. If a session expires, sign in again. Resolve user/role/resource/portfolio/progress references before removing a skill; reassign affected goals before removing a role. A new skill without a course has a practice project until an administrator adds a learning link. Refresh restores saved data, not unsaved edits. Back up with `python scripts/backup_db.py backup.db`; restore to a separate file and select it with UPSKILL_DB.

