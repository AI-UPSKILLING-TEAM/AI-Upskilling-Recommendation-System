# Prototype Test Plan

## Objective
Verify the core student workflow in the submitted Project 22 prototype. The already-submitted course Test Plan should remain authoritative once shared/linked.

## Automated acceptance checks
1. Health endpoint and career catalog respond successfully.
2. Dashboard cannot be accessed anonymously.
3. Registration and login succeed with valid input.
4. Duplicate registration and wrong passwords are rejected.
5. Profile, career goal and skill selection persist to SQLite.
6. Skill-gap analysis lists missing required skills and computes readiness correctly.
7. Practiced-topic progress persists and logout revokes the session.
8. Invalid goal, unknown skill and malformed progress values are rejected.

## Run
`python -m unittest discover -s tests -v`

## Manual verification before demo
- Open the app from a fresh browser session.
- Register an account, log in and save a career goal.
- Select two known skills and confirm the displayed missing skills.
- Mark a learning item as practiced, refresh and verify it stays checked.
- Sign out; verify the dashboard is inaccessible without signing in.
- Resize to a mobile width and verify forms remain usable.

## Not yet validated
Accessibility audit, high-volume concurrent load, security penetration testing, AI model evaluation, notification delivery and admin authorization. Do not report these tests as passed.
