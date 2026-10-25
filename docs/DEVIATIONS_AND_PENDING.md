# Design Decisions, Deviations and Process Status
Candidate prepared 25 October 2026. No work, commit, recording or approval is backdated.

## Implemented
Authentication, academic profile, skill/proficiency management, goal selection, missing/weak gap analysis, content-based learning recommendations, courses/resources, practical project prompts, optional certification references, private portfolio, persistent practice progress, dashboard, notifications and administrator management are implemented and tested. See TEST_EVIDENCE.md.

## Explicit decisions
1. TF-IDF uses curated reference data, as permitted by the SRS constraint. It is not a learned predictor.
2. Readiness compares self-reported skill levels with role targets. Progress is binary skill-based practice completion; neither proves mastery.
3. Course/project/certification records share a typed portfolio table. Student/admin accounts share role-based users. Recommendations retain a latest JSON snapshot.
4. Some optional metadata in the conceptual SRS ER diagram (provider, difficulty, issue date and project link) is not separately modeled. Normative FR behavior uses title, type, related skill and resource descriptions.
5. Admin-created courses/resources can be edited/deleted; version-controlled reference entries remain fallbacks. Latest custom resource per skill overrides its default.
6. Notifications are in-app. The SRS does not require email/SMS/push delivery.
7. SAD and Test Plan were newly created with user authorization because the earlier originals were unavailable. Equivalence to prior submissions cannot be verified.

## Genuine team/process actions
Sprint 1 was scheduled 19-23 October; current recovery work is dated 25 October. Sprint 2 is scheduled 26-30 October, so the two-minute recording prepared now is an implementation preview. Another authorized teammate must review the actual PR; an owner must merge after current checks pass. Teammates must raise their own contribution PRs for work they actually do. Current assignments allocate review/demo responsibility and do not manufacture contribution history. Formal freeze requires real acceptance and an owner-recorded final commit/date.

The application and review package are prepared; independent review, merge, in-period Sprint-2 acceptance and formal freeze remain visible process actions. See RELEASE_AND_FREEZE_CHECKLIST.md.
