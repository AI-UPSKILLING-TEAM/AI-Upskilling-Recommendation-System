# Verification Evidence
Application baseline tested on 25 October; release gates and final Sprint 2 recording verified on 26 October 2026. These are actual observed results, with raw artifacts in evidence/. GitHub CI status must be checked for the published commit; a local pass does not assert remote CI success.

| Check | Observed result | Artifact |
|---|---|---|
| Python API/security/regression | 28 tests passed | python-tests.txt |
| JavaScript | Syntax check and DOM contract tests passed | CI / Python frontend contract |
| Real-browser student/admin workflows | Passed; no uncaught JS exceptions | browser-results.json |
| Mobile | 390x844; no horizontal overflow | mobile-dashboard.png |
| Automated accessibility | 0 WCAG 2.1 A/AA violations; 21 passing rules; 0 checks require review | accessibility.json |
| Recommendations | Synthetic 12-case MRR 1.0000, fixed-order 0.5097, hit@3 1.0000 | recommender-evaluation.json |
| Serial dashboard timing | Median 5.0ms; p95 20.96ms; max 26.91ms | performance.json |
| Five-worker timing | Median 49.86ms; p95 160.17ms; max 282.34ms | performance.json |
| Outbound links | All 19 returned HTTP 200 during audit | link-audit.json |
| Backup/recovery | SQLite integrity ok; all table contents compared equal | backup-verification.json |
| Recordings | 60.00s and 120.00s; full decode checks passed | videos/recording-metadata.json |

The benchmark uses a small local catalog and disposable account; it is not production capacity certification. The synthetic ranking set is non-independent and does not measure real-student learning effectiveness. axe-core leaves human usability/screen-reader review outstanding. The current candidate is ready for independent review, not a fabricated team approval.

## Release preparation verification (26 October)
Seven offline release-gate simulations pass (evidence/release-gate-tests.json). These are simulations, not an actual release. The new final Sprint 2 recording is 120.00 seconds and passes full decode verification; its actual capture timestamp is in videos/Sprint_2_Demo.metadata.json. Application code is unchanged from the previously passing baseline.

## Fresh verification - 15 November 2026

A clean clone of candidate `1064d8a161367ec3ebb3835e52e8c5cdd20c0aa7` passed all 28 Python tests, JavaScript syntax, real Chrome student/admin workflows, 390px mobile overflow check and automated accessibility (zero violations). SQLite backup integrity and all 13 table contents matched. All 48 SRS requirement identifiers are mapped in the RTM. Local request maxima were 28.79ms serial and 168.69ms with five workers. Seven offline release-gate cases passed. The 12 synthetic ranking cases reproduced the earlier metrics and retain their non-independent-data limitation.

Raw results and screenshots: `evidence/final-verification-2026-11-15/`. Fresh automated outbound audit reached 17/19 links; Khan Academy timed out and Cloudflare returned 403. Separate web fetch retrieved Cloudflare content; Khan Academy returned no readable content. These outcomes do not establish dead links. Human usability, teammate acceptance and college receipt verification remain separate. See VERIFICATION_AND_HANDOVER.md for the submission statement, review status and limits.
