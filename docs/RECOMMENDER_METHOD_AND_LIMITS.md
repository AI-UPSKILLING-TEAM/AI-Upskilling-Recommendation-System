# Recommendation design and evaluation limitations

The previous baseline recommended every missing skill in fixed role order. The current implementation performs **TF-IDF + cosine content-based ranking** over a small curated corpus of descriptions of learning resources.

## Inputs and output
Inputs: student-provided career goal, interests, completed skill inventory, and a fixed role-to-required-skill mapping. Missing skills are derived by set difference. Candidate learning materials are associated with those missing skills. The query string (career + interests) and resource text are tokenized, transformed into TF-IDF vectors, and ranked by cosine score with original skill order as a stable tie-breaker.

Outputs: readiness fraction; missing skills; ranked recommendations with skill, resource title, HTTPS URL, type, relevance score, and a short project activity.

## What is and is not AI
TF-IDF/cosine is a classical information retrieval and content-based recommendation approach. It does **not** learn from historical student engagement data, does not train neural networks, and does not establish prediction accuracy or educational effectiveness. Do not present it as a trained machine-learning model.

## Reproducible technical checks
- `python -m unittest discover -s tests -v`: checks deterministic ranking, supported HTTPS links, skill coverage, and authorization.
- Compare outputs with the original static-order rule as a baseline; this is a *technical*, not educational outcome, comparison.
- For a defensible recommender evaluation, obtain consented/anonymized relevance judgments and compute Precision@K, Recall@K, NDCG@K and coverage. No such dataset or metrics are claimed for this submission.

## Limitations
- Small hand-written corpus; vocabulary and role requirements may be incomplete.
- Content cosine relevance is not skill mastery or placement suitability.
- Course availability and certificate criteria may change.
- Admin-added resources override the displayed resource link for a skill, but are not used in the TF-IDF candidate corpus.
- Real ML training, fairness checks, online feedback and validation remain future work.
