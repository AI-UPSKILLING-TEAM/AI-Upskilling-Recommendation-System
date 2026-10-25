# Project 22 – SRS requirements traceability (review draft)

**Source:** The 15-page repository `SRS_Project_ID_22.pdf`, requirement text extracted by the GitHub Actions SRS outline job on 25 October 2026. These requirement IDs are from that document, not invented IDs. The original SAD and submitted Test Plan were not available for comparison in the repository at review time.

**Evidence branch:** `feature/manish-part2-mvp` (PR #17). Feature is not accepted merely because code exists; team review and test evidence are required.

| Original SRS ID | Scope | Code/evidence | Status / limitation |
|---|---|---|---|
| FR-01–FR-04 | Student registration and login | `app.py`, `tests/test_app.py` | Implemented for local prototype. No email ownership verification/password recovery |
| FR-05–FR-07 | Student profile, academic/career data | Profile, interests, goals, portfolio | Partial: academic fields are not comprehensively modeled |
| FR-08–FR-10 | Student skill add/update/remove and persistence | Skills API, dashboard, tests | Implemented for fixed skill catalog |
| FR-11–FR-13 | Career role list/selection/storage | Career catalog, SQLite, profile | Implemented |
| FR-14–FR-17 | Existing/required/missing or weak skills and gap display | Gap report/dashboard | Partial: checks missing skill names; does not assess weak proficiency levels |
| FR-18–FR-20 | Analyze gaps, personalized recommendations and courses/resources | `recommendations.py`, curated links | Partial: TF-IDF content ranking, **not evaluated trained AI** |
| FR-21–FR-22 | Suitable project and certification recommendations | Concrete project prompts for each catalog skill and optional official certification options for Data Analyst, Cloud Engineer and Cybersecurity Analyst | Partial: limited catalog, not personalized certification eligibility |
| FR-23–FR-25 | Display/categorize/view learning resources | `/api/resources`, per-skill UI links | Implemented for a small educational catalog; no complete link audit |
| FR-26–FR-28 | Mark, calculate and display learning progress | Practice flags; progress percentage; UI/tests | Implemented for practice milestones, not skill mastery |
| FR-29 | Update recommendations after progress | Unpracticed resource cards appear first | Basic reprioritization; no personalized feedback-trained ranking |
| FR-30–FR-33 | Goal, gaps, resources, progress dashboard | `index.html`, `app.js`, tests | Implemented in local prototype; manual browser review pending |
| FR-34 | Administrator manages student data | Authorized user list | Partial: lacks student edit/suspension interface |
| FR-35 | Administrator manages skills | Admin edits career-role skill requirements | Partial: cannot create/delete master skill catalog |
| FR-36, FR-38 | Administrator manages career roles/required skills | `/api/admin/roles` | Basic update/create implemented |
| FR-37 | Administrator manages courses and learning resources | `/api/admin/resources` | Partial: add only, no edit/delete |
| NFR-01, NFR-02 | Response/recommendation time | Small local app, deterministic ranking | **Not benchmarked** against representative use |
| NFR-03 | Secure password storage | PBKDF2-HMAC-SHA256 salted hashes | Prototype control implemented; production audit needed |
| NFR-04 | Private data only for signed-in users | Bearer sessions, per-user queries, tests | Tested for core endpoints, additional security review needed |
| NFR-05 | Admin-only functions | Role checks/tests | Tested for exposed admin routes |
| NFR-06, NFR-07 | Usable interface and navigation | Responsive single-page dashboard, contract tests | Human usability/accessibility test pending |
| NFR-08, NFR-09 | Recommendations from available data; persistent progress | Catalog and SQLite/tests | Basic prototype support; recovery/load testing pending |
| NFR-10 | Maintainability/modular design | `app.py`, `recommendations.py`, automated tests | Basic modularization, design review pending |

## Source-specific observations
- SRS section 7 names Student, Skill, Career Role, Course, Project, Certification, Learning Resource, Recommendation, and Progress as entities. The current schema uses some simplified relations; it is **not** a one-to-one implementation of every SRS entity.
- The SRS requires course, project and applicable certification suggestions. This prototype now includes concrete per-skill projects and a limited official certification lookup. Broader project/certification coverage, prerequisites and relevance should be reviewed by the team.
- Weak-skill scoring requires actual proficiency measurements that the current demo has not collected.

## Before signing off
1. Review the submitted SAD, original Test Plan and any required acceptance thresholds against these exact IDs.
2. Run GitHub Actions, JS/HTML contract tests, and a human browser walkthrough; keep actual links/screenshots as evidence.
3. Review/merge PR with a **different teammate** after approval.
4. Upload genuine Sprint 1 (one-minute) and Sprint 2 (two-minute) demos when recorded.
5. Close corresponding issues only when accepted and document all deviations.
