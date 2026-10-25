# Requirements traceability – provisional

**Authoritative documents:** `SRS_Project_ID_22.pdf` in `main`, plus the team's original Software Architecture Design (SAD) and Test Plan submissions. The latter two were not found in the repository root on 25 October 2026.

This matrix uses *feature names from the repository README*, not invented SRS requirement identifiers. Owners must match each row to the exact FR/NFR ID from the PDFs before declaring compliance.

| README feature / quality area | Prototype implementation | Evidence | Remaining |
|---|---|---|---|
| Registration/login | `app.py` register/login, hashed passwords, expiring tokens | `tests/test_app.py` | Password reset/email validation unspecified |
| Profile and interests | SQLite users table; profile API/UI | `tests/test_app.py` | Compare SRS fields |
| Career goal | Fixed career catalog and profile form | `tests/test_app.py` | Verify goal taxonomy against SRS |
| Skill management and gaps | Skill inventory + requirements difference | `tests/test_app.py` | Verify skill definitions |
| AI recommendations | TF-IDF-ranked curated content recommendations | `tests/test_sprint2.py` | Evaluate against real dataset if mandated |
| Learning materials | `recommendations.py`; provider links | `tests/test_sprint2.py` | Verify all course/project/certification coverage |
| Student dashboard | Responsive frontend | Manual demo checklist | Accessibility and UI validation |
| Progress tracking | Practice flag in SQLite | `tests/test_app.py` and Sprint 2 tests | Not a proficiency assessment |
| Notifications | Opt-in in-app practice milestones | `tests/test_sprint2.py` | No outbound delivery |
| Administrator | Role-protected read/add operations | `tests/test_sprint2.py` | Full role and resource governance |
| Security NFR | Password hashing, bearer tokens, role checks, basic validation | Integration tests | Threat modelling / security review |
| Performance NFR | No measured target yet | No evidence | Benchmark vs actual SRS acceptance criteria |
| Reliability NFR | SQLite persistence and unit tests | CI run | Load and restart/recovery testing |

## Approval checklist
- [ ] Read SRS PDF and enter exact requirement IDs/acceptance thresholds.
- [ ] Link SAD design elements and original Test Plan test-case IDs.
- [ ] Validate every row with a team member and reviewer.
- [ ] Attach manual demo and GitHub Actions evidence.
- [ ] List approved deviations with rationale and impact.

**Do not mark traceability complete before these checks.**
