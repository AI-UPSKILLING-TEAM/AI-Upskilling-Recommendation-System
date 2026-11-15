# Test Plan and Acceptance Criteria
New document created 25 October 2026 for the actual implementation. The earlier submitted test plan was unavailable; this plan does not claim to reproduce it.

## Scope and environment
Verify FR-01 through FR-38 and NFR-01 through NFR-10. Use Python unittest for calculation/HTTP integration, Playwright for real browser workflows, axe-core for machine-detectable WCAG A/AA checks, and separate evaluation, benchmark and link-audit scripts. Local testing uses Windows, Python 3.12 and Chromium. CI covers Python 3.11/3.12 on Linux and Windows. Disposable example.com accounts and isolated SQLite databases keep test data separate from any real student information.

## Entry and exit criteria
Entry: SRS available, application starts, schema initialized, expected requirement behavior identified. Exit: all automated regressions and browser acceptance pass; no known functional defect remains; documents and demo recordings match the tested product; independent teammate review and owner merge are recorded before final acceptance/freeze. A passing local suite is not a signed acceptance record.

## Functional test cases
| Case | Requirements | Action and expected result | Evidence |
|---|---|---|---|
| T01 | FR-01,02 | Valid registration succeeds; invalid name/email/password rejected; duplicate returns 409 | test_app auth/validation; test_nfr |
| T02 | FR-03,04 | Login succeeds; wrong password denied; expired/revoked token denied | test_app auth/logout; test_nfr expiry |
| T03 | FR-05,06,07 | Save/edit academic profile, goal and contact information; reload retains it | test_completion academic profile; browser |
| T04 | FR-08,09,10 | Add/update/remove skills and levels; invalid levels rejected | test_completion weak skill; test_app |
| T05 | FR-11,12,13 | List roles; save valid goal; reject unknown role | catalog/profile tests; browser |
| T06 | FR-14,15 | Identify existing skills and role targets | gap_report; role lifecycle tests |
| T07 | FR-16,17 | Distinguish missing and below-target skill; correct readiness | test_completion academic_profile_and_weak_skill_gap |
| T08 | FR-18,19 | Rank gap topics deterministically using goal/context | test_sprint2 ranking; recommender evaluation |
| T09 | FR-20 | Course/resource metadata matches a missing/weak skill | metadata tests; link audit |
| T10 | FR-21 | Practical project prompt for every candidate, including custom skill | project tests; catalog lifecycle |
| T11 | FR-22 | Applicable certificate reference; omit unsupported path | test_sprint2 project_and_optional_certification |
| T12 | FR-23,24,25 | Resources categorized by skill and viewable via safe links | browser; frontend contract; link audit |
| T13 | FR-26,27,28 | Mark/unmark practice, compute percent and retain saved state | progress/persistence tests; browser |
| T14 | FR-29 | Practiced topics sort below unpracticed topics | test_app skills_goal_recommendations_and_progress |
| T15 | FR-30,31,32,33 | Goal, gaps, recommendations and progress visible | browser-results.json; screenshots |
| T16 | FR-34 | Admin edits student data; deleting student invalidates related data/sessions | test_completion admin_student_edit_and_cascading_account_delete |
| T17 | FR-35 | Admin adds/deletes unused skill; used skill protected | test_completion catalog_resource_and_role_lifecycle |
| T18 | FR-36,38 | Create/update role skills and target levels; protect selected role | completion lifecycle; test_sprint2 role edit |
| T19 | FR-37 | Add/edit/delete custom course/resource; analysis uses update | completion lifecycle; browser admin flow |
| T20 | SRS diagrams | Portfolio private; opt-in milestone once; own read status | test_sprint2 portfolio/notifications |

## Non-functional criteria
| ID | Proposed acceptance / method | Limits |
|---|---|---|
| NFR-01 | All measured local dashboard requests under 2000ms; 30 serial, 30 with five workers | Project proposal, not an original numeric SRS SLA |
| NFR-02 | Recommendation calculation included in dashboard timing | Small catalog/local hardware |
| NFR-03 | Salted password hash and no stored raw session token | Control verification, not certification |
| NFR-04 | Missing/expired credentials denied; data constrained to owner | API isolation cases |
| NFR-05 | All eight admin mutation routes reject students/anonymous users | Explicit enumeration in test_completion |
| NFR-06 | Zero axe-core WCAG 2.1 A/AA violations on tested student dashboard | Does not replace human usability review |
| NFR-07 | Consistent anchors/forms; no horizontal overflow at 390px | Tested browser/viewport only |
| NFR-08 | Deterministic available-data path; no-goal empty; custom-skill fallback | Curated reference approach |
| NFR-09 | Saved data survives initialization and reload; backup integrity verified | Normal operation and local recovery smoke test |
| NFR-10 | Separate modules; compile/API/browser regression repeatable | CI and documented design |

## Negative/security cases
Reject non-object JSON, invalid skill lists, boolean/out-of-range proficiency and oversized/invalid input. Deny missing/invalid/expired/revoked sessions and every student attempt at admin mutation. Verify another account cannot view/delete portfolio or read notifications. Reject javascript URLs, private numeric addresses, embedded URL credentials and malformed ports. Serve only allowlisted assets. Render user content as text.

## Execution and evidence
The baseline Python suite contains 28 tests. Browser acceptance separately covers registration, login, academics, weak skills, portfolio, practice/reload, mobile overflow, admin skill/role/course changes and uncaught exceptions. JSON evidence records accessibility, recommendation reference cases, response times and outbound link status. Keep full Python output in evidence/python-tests.txt. Tests must run against the actual API and frontend, not mocks.

Run `python -m unittest discover -s tests -v`, `node --check app.js`, `npm ci`, `npx playwright install chromium`, and `npm run test:browser`. Run the three scripts evaluate_recommender.py, benchmark.py and audit_links.py to regenerate measured evidence. See USER_MANUAL.md for startup and admin setup.

## Human acceptance and limitations
A real teammate must independently review the PR and verify the live demo. Human keyboard/screen-reader usability, real-student usefulness, cross-browser certification, penetration testing and public-deployment capacity are not claimed by automated checks. The synthetic relevance cases use catalog-like vocabulary and cannot establish real-world prediction accuracy. Scheduled sprint participation and owner approval cannot be generated by tests.
