# Project 22 — SRS requirements traceability (audit draft)

**SRS source:** `SRS_Project_ID_22.pdf` in repository `main`, extracted by the `SRS requirement outline` GitHub Actions job on 25 October 2026. **No SRS contents or FR/NFR IDs are fabricated.**

The actual SRS contains FR-01–FR-38 and NFR-01–NFR-10. Text from PDF page 11 (covering portions of FR-18–FR-31) was not extractable as plain text by pypdf; requirement section ranges are confirmed by the SRS summary on page 14. Before final acceptance, inspect page 11 visually and verify each exact requirement.

| SRS requirements | Feature | Code / evidence | Assessment |
|---|---|---|---|
| FR-01–FR-04 (p. 9) | Register, validate input, login and invalid-login errors | `app.py`, `tests/test_app.py` | Implemented prototype |
| FR-05–FR-07 (p. 10) | Create/edit profile and academic/career data | Profile, interests, goal in `app.py`; portfolio records | Partial: detailed academic info to verify |
| FR-08–FR-10 (p. 10) | Add, edit/remove and persist student skills | `/api/skills`, SQLite, automated tests | Implemented prototype |
| FR-11–FR-13 (p. 10) | List, choose and persist career goal | Catalog and profile endpoint | Implemented prototype |
| FR-14–FR-17 (p. 10) | Skill inventory, career requirements, missing/weak skills, gap display | `gap_report()`, dashboard | Partial: missing skills, not graded weakness |
| FR-18–FR-22 (p. 11, SRS summary p. 14) | AI recommendation system | `recommendations.py` content-based TF-IDF ranking | Partial: not a trained ML model; exact FR wording needs visual review |
| FR-23–FR-25 (p. 11, summary p. 14) | Learning resources | Curated reference links, admin resource additions, course/project/certification portfolio | Partial: exact matching and provider verification incomplete |
| FR-26–FR-29 (p. 11, summary p. 14) | Progress tracking | SQLite practice tracking, persistence/opt-in milestones | Partial: progress tracked per skill, not per learning-resource ID |
| FR-30–FR-33 (pp. 11–12, summary p. 14) | Dashboard | Profile, gaps, resource links, progress | Implemented prototype; manual usability check pending |
| FR-34–FR-38 (p. 12) | Manage students, skills, roles, courses/resources and role requirements | Admin list, resource additions, role/requirement editor, audit log | Partial: admin student editing and catalog skill management limited |
| NFR-01–NFR-02 (p. 12) | Response time / recommendation latency | Lightweight stdlib server and local algorithm | Needs measured acceptance evidence (SRS says "reasonable time") |
| NFR-03 (p. 12) | Secure password storage | PBKDF2-HMAC-SHA256 salted hashes | Implemented locally; independent security review pending |
| NFR-04–NFR-05 (p. 12) | Only authenticated user data access; admin-only operations | Bearer sessions, per-user SQL queries, admin role checks | Automated regression tests; further threat testing pending |
| NFR-06–NFR-07 (p. 12) | Usability, navigation | Responsive frontend | Human accessibility/usability evidence pending |
| NFR-08–NFR-09 (p. 12) | Recommendations based on available data; progress persistence | SQLite + unit/integration tests | Implemented prototype |
| NFR-10 (p. 13) | Modularity | Separate `app.py`, `recommendations.py`, frontend and tests | Implemented prototype |

## Missing course project management evidence
SRS pages 3 and 7 explicitly mention student **courses, projects and certifications**. The prototype now allows students to add and remove all three types in their private portfolio, and these titles can affect the recommendation context. It does not infer skill mastery from the portfolio automatically.

## Needed for acceptance
- [ ] Visually confirm scanned/nonextractable page 11 and exact FR-18–FR-31 wording.
- [ ] Obtain the previously submitted SAD and Test Plan; map design sections/test IDs to each SRS row.
- [ ] Test on desktop and mobile browsers using real manual evidence.
- [ ] Have the assigned reviewer check and approve the traceability and deviations.
- [ ] Provide actual one-minute and two-minute demo videos.
- [ ] Link GitHub Projects backlog board and confirm team assignments.

**Status:** Audit draft. Do not claim full SRS/SAD/Test Plan conformity before these steps.
