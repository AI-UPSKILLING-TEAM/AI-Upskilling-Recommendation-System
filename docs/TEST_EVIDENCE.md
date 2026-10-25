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
