# Software Architecture and Design (SAD)
Project 22 | Version 1.0 | Created 25 October 2026

## Document status
This SAD was newly created with user authorization because the original submitted SAD was unavailable. It documents the implemented system and does not claim to reproduce an earlier submission. Sources are the 15-page repository SRS, its use-case and ER diagrams, and the Part-2 deliverables brief.

## Problem, users and scope
Students maintain their academic profile, skills, qualifications and career goal. The product compares self-assessed skills with role targets, identifies missing and weak skills, generates a personal learning path and stores practice progress. Administrators manage student metadata, skills, career requirements and courses/resources. Opt-in milestone notifications are stored in the application.

## Architecture
The same-origin HTML/CSS/JavaScript client calls a Python JSON API. SQLite persists application state. Recommendation computation runs on the server without an external AI service. Only explicitly allowed static assets are served.

| Component | Responsibility | Main interface |
|---|---|---|
| index.html, style.css | Semantic forms, dashboard, responsive layout | Browser UI |
| app.js | Requests, safe text rendering and workflow state | Same-origin JSON |
| app.py | Routing, authentication, profiles, progress, transactions | API / make_server |
| administration.py | Validate and apply protected management operations | execute / ValidationError |
| recommendations.py | Curated data, TF-IDF ranking, projects, certificates | rank_learning |
| SQLite | Accounts, catalogs, sessions, progress and audit events | connect_db |
| tests, scripts | Regression, browser, accessibility and measured evidence | CLI commands |

## Deployment
One Python process listens on 127.0.0.1:8000; a browser connects over local HTTP. Python 3.10+ is sufficient for normal operation, with no mandatory third-party runtime dependency. HOST, PORT and UPSKILL_DB configure binding and storage. This is a local coursework demonstration server. Public hosting needs HTTPS, a production server/reverse proxy, abuse controls, monitoring and an independent deployment security review.

## Database design
| Table | Identity / principal information | Integrity |
|---|---|---|
| users | id; name; unique email; salt; password_hash; interests; goal; role; department; academic_year; phone | student role by default |
| skills | user_id + skill; proficiency level | student ownership; cascade deletion |
| skill_catalog | unique name | master skill list |
| career_roles | unique name | role identity |
| career_role_skills | role + skill; required_level | role cascade |
| portfolio | id; user_id; kind; title; skill | course/project/certification discriminator |
| learning_resources | id; skill; title; url; description; kind | admin-managed course/resource |
| recommendation_snapshots | user_id; JSON analysis; updated_at | latest persisted recommendation |
| progress | user_id + skill; completed_at | practice activity completion |
| sessions | token_hash; user_id; expires_at | raw token never stored |
| notification_preferences | user_id; enabled | disabled by default |
| notifications | id; user_id; title; created_at; read_at | private to student |
| audit_log | id; actor_id; action; target; created_at | admin mutation evidence |

Foreign keys are enabled per connection. Writes are transactional and database handles close deterministically. Additive migrations preserve existing accounts and progress. In-use skills and selected career roles are protected from deletion. Student deletion cascades to their owned data and sessions.

## Mapping to the SRS ER diagram
Student and Administrator share users with a role discriminator. Course, Project and Certification share portfolio with a kind discriminator. Unique skill/role names stand in for conceptual IDs. Proficiency_Level and Required_Level map to skills.level and career_role_skills.required_level. Recommendation uses a latest snapshot rather than an unbounded history. Progress represents one binary practice activity per skill; the dashboard computes its percentage for the chosen goal. The conceptual diagram includes optional provider, difficulty, issue-date and project-link metadata that is not separately modeled in this implementation. These decisions are documented deviations for the final demo.

## Authentication and security
Passwords use random per-user salts and PBKDF2-HMAC-SHA256 with 300,000 iterations. Login compares derived digests in constant time and returns a random 256-bit bearer token for eight hours. Only SHA-256 token hashes are persisted. The browser keeps its token in sessionStorage; logout revokes it. Personalized queries always constrain user_id. Every admin mutation checks the database role before applying changes. Promotion is a local maintenance command, never a public endpoint.

JSON request bodies are limited to 16 KB. Values use parameterized SQL. Frontend user content uses textContent. Resource URLs require public HTTPS references and reject credentials, local/private numeric addresses and malformed ports; the server does not fetch submitted URLs. API replies use no-store and nosniff. Static replies use a Content Security Policy. These are tested controls, not a penetration-test certification. Password recovery, email verification, rate-limit infrastructure and public-deployment availability are outside this local baseline.

## Gap and recommendation algorithm
Required skills are taken from the selected role. Missing means absent from the student's inventory; weak means present but below the role's required level. Candidate topics are the union of missing and weak skills. Readiness = 100 * requirements met / required skills. Practice progress = 100 * practiced required topics / required topics. No goal gives zero readiness and no career-specific path. Practice never automatically changes proficiency.

Each candidate document contains its skill and curated resource description. The query combines career goal, interests and portfolio titles. Tokenization uses lower-case alphanumeric terms. TF = 1 + ln(count); IDF = 1 + ln((1+n)/(1+document_frequency)). Cosine similarity ranks the vectors, with deterministic source order for ties. The latest custom resource for a skill overrides its default. A custom skill without a course receives an explicitly local practice project. Completed practice topics sort after unpracticed ones. Optional certifications are shown only for supported applicable roles with gaps, without asserting eligibility.

The method is content-based ranking using reference data, which the SRS permits. It is not a learned predictor of student outcomes. Twelve synthetic relevance cases compare ranking with fixed catalog order; the dataset, per-case results and limitations are preserved.

## Main sequences
Student: register -> login -> save academic profile and goal -> save skills/levels -> inspect gaps/path -> add portfolio item -> log practice -> refresh/reprioritize. Administrator: local authorized promotion -> login -> change shared catalogs or student metadata -> inspect audit log. Confirmations precede destructive UI actions. All state is saved by the server before a success message.

## API and error contract
| Route group | Access | Purpose |
|---|---|---|
| GET /health, /api/catalog, /api/resources | Public | Liveness and shared reference data |
| POST /api/register, /api/login | Public | Create account / obtain session |
| GET /api/dashboard, /api/portfolio | Signed in | Own profile, analysis and qualifications |
| POST /api/profile, /api/skills | Signed in | Save own profile / skill inventory and levels |
| POST /api/portfolio/add, /api/portfolio/delete | Signed in | Manage own typed portfolio |
| POST /api/progress, /api/logout | Signed in | Practice state / session revocation |
| GET /api/notifications | Signed in | Preference and private events |
| POST /api/notifications/preferences, /api/notifications/read | Signed in | Opt-in and read own event |
| GET /api/admin/users, /api/admin/audit | Administrator | Student records and audit history |
| POST /api/admin/users, /api/admin/users-delete | Administrator | Edit metadata / delete student |
| POST /api/admin/skills, /api/admin/skills-delete | Administrator | Add / remove unused skill |
| POST /api/admin/roles, /api/admin/roles-delete | Administrator | Save target requirements / delete unused role |
| POST /api/admin/resources, /api/admin/resources-delete | Administrator | Add/edit/delete course or resource |

Expected errors are JSON: 400 invalid data, 401 missing/expired credentials, 403 forbidden administration, 404 unknown route, 409 duplicate email. The UI displays errors in a live status region. Invalid input must not terminate the server.

## Quality, operations and change control
A proposed local acceptance ceiling is two seconds for dashboard/recommendations; this makes the SRS's 'reasonable time' measurable without inventing an original SLA. The benchmark covers 30 serial requests and 30 with five workers. Responsive behavior is checked at 390px and desktop widths. axe-core checks detectable WCAG A/AA issues; human usability acceptance is separate.

Stop the server before copying the database or use scripts/backup_db.py for an online SQLite backup. Verify backup integrity, restore to a separate file and point UPSKILL_DB to it. Never publish databases, passwords or session tokens. CI runs Python regressions on Linux/Windows and a Chromium workflow. Independent teammate review and current checks are required before owner merge and formal release freeze.
