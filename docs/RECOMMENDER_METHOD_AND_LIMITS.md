# Recommendation Method and Evaluation Limits
The SRS permits appropriate training or reference data. This system uses curated reference data and TF-IDF cosine similarity: a content-based recommendation method. No trained predictor, external LLM or student-outcome model is claimed.

Candidates are missing/weak skills for the chosen career goal. Documents combine skill and course descriptions; query context combines goal, interests and portfolio titles. Natural-log term frequency and smoothed IDF produce vectors; cosine similarity ranks them, with deterministic source-order ties. Practiced topics sort later without implying mastery. A custom skill without a course still receives an original practice-project prompt; an administrator can add a course URL.

The seeded catalog has 16 skills and six roles. Three supported role-specific credential references are optional; pricing and eligibility are not assessed. All 19 reference links are checked in evidence/link-audit.json. Project prompts are small original exercises, not accredited assignments.

Evaluation uses 12 author-defined synthetic cases, two per role, one relevant skill per case. The full reference set, expected topic and observed ranking are retained in evidence/recommender-evaluation.json. Mean reciprocal rank is the mean inverse rank of the first relevant result. Hit@3 is the share of cases with that result in the first three. Fixed catalog order is the baseline. Current MRR is 1.0000 versus 0.5097 for fixed order; hit@3 is 1.0000.

These small, non-independent, catalog-derived cases are a reproducibility check, not 100% real-world accuracy. Independent evaluation needs diverse student descriptions, teacher/student relevance judgments, a frozen held-out dataset and learning-outcome follow-up. Readiness is a self-reported checklist, not an academic or employment eligibility decision.
