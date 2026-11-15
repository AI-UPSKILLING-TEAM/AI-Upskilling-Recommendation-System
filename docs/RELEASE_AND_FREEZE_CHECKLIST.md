# Release Candidate and Development Freeze
Current preparation: 26 October 2026. The application, documents, 60-second Sprint 1 recovery video and new in-period 120-second Sprint 2 working-product demo are ready for actual review.

## Enforced acceptance gate
Main requires a pull request, one genuine independent approval, four Python matrix checks, browser-tests and outline. Stale approvals are dismissed; administrators cannot bypass this rule. The source author is ManishS943. Poojitha, Manasa and Shanmuga have review requests. Approval of PR #17 should cover code, the new SAD/Test Plan and the explicitly documented design decisions.

## Queued completion
GitHub auto-merge waits for a real approval and all required checks. After the merge, the Project verification workflow runs against main. Only a successful main push for PR #17's actual merge commit can trigger Accepted release and freeze. That workflow independently checks that the final PR revision has a non-author approval, creates an annotated v1.0.0 tag without moving an existing tag, uploads and SHA-256-verifies the report and both final demo videos, and publishes the release. Published release tags/assets are configured immutable. It then closes the 16 accepted backlog issues. The GitHub Project's closed-issue workflow updates their status.

## Final evidence location
The actual reviewer, accepted merge SHA, passing main run and release/freeze timestamp will be recorded at https://github.com/AI-UPSKILLING-TEAM/AI-Upskilling-Recommendation-System/releases/tag/v1.0.0 after the gate is satisfied. Until that release exists, independent approval, merge and final publication remain pending; this file does not invent them.

## Verification and limits
Seven offline release-gate simulations pass, covering missing, author-only and stale approval, foreign repository, unrelated merge, conflicting tag and the accepted publication order. These verify logic without contacting GitHub and do not claim that a real release was published. Future fixes require a separate reviewed version; the frozen tag is never moved.
