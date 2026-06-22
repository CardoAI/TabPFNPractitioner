# TabPFNPractitioner: editorial brief

Teaching notebooks on working with TabPFN, for practitioners who built their instincts on gradient
boosting. This file is the brief: who the notebooks are for, and how to write them.

## Who it is for

Data scientists fluent in gradient boosting (XGBoost, LightGBM, CatBoost) and the usual pre-modeling
reflexes: scaling, imputation, encoding, feature work. Comfortable with pandas, numpy and sklearn.
They lose focus on dense code and distrust hand-wavy claims.

## The shape of each notebook

The value is organization, not novelty. Mirror what the reader already knows, then show the TabPFN
shift. Each topic follows four beats:

1. The familiar checklist: the classical practice for this data type.
2. What TabPFN does: the same checklist re-answered (what is redundant, what changed).
3. One measured result, from a runnable cell.
4. The deep dive: the nuances, thresholds, and corner cases.

Ground first to earn trust, then go deep. The depth is the differentiator and is never cut, only
sequenced last.

## How to write the code

- Lean and legible over clever: explicit loops, named variables, one statement per line, docstrings
  on helpers. Readers lose focus on big harnesses and dense one-liners.
- Self-contained synthetic constructions are fine, and usually clearer than a real dataset, as long
  as the model behaviour we observe is real. Constructing a corner case to make a point is fine.
- Verify before claiming: run the cell, never assert a result from intuition, no fabricated numbers.
- Do not draw strong conclusions from a single dataset. Prefer results that are structural (true by
  construction) or shown across several settings, and caveat what is dataset-dependent.
- Each notebook should run top to bottom and be easy to excerpt for a post.

## How we work

- Be skeptical, including of the author's own claims. Do not indulge a result you cannot reproduce, and flag thin evidence rather than dressing it up.
- Work in small steps and check as you go. One change or one question at a time beats a long batch that is hard to verify.
- Keep answers short and concrete. Say what you did and what it showed, then stop. Skip the preamble and the recap.

## Style

- No em-dashes or double hyphens. Use commas, colons, parentheses, or split the sentence.
- Plain, direct prose. State the takeaway; do not hedge a verified result.
