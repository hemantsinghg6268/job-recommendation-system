
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_DIR / "evaluation" / "recommendation_candidates.csv"

df = pd.read_csv(CSV_PATH)

if "relevant" not in df.columns:
    raise ValueError("The CSV must contain a 'relevant' column.")

# Blank judgments are not treated as irrelevant.
judgments = df["relevant"].replace(r"^\s*$", pd.NA, regex=True)
df["relevant"] = pd.to_numeric(judgments, errors="coerce")

if df["relevant"].isna().any():
    raise ValueError(
        "Some jobs have not been judged yet. Fill every 'relevant' cell "
        "with 1 (relevant) or 0 (not relevant), then save the CSV."
    )

if not df["relevant"].isin([0, 1]).all():
    raise ValueError("Judgments must be 1 (relevant) or 0 (not relevant).")

if df.empty:
    raise ValueError("The evaluation CSV contains no recommendations.")

# Precision@5 for each query: relevant jobs among its first five results / 5.
# If fewer than five results exist, divide by the number actually returned.
per_query = []

for query, group in df.groupby("query"):
    group = group.sort_values("rank").head(5)
    if group.empty:
        continue

    precision = group["relevant"].sum() / len(group)

    per_query.append({
        "query": query,
        "results_evaluated": len(group),
        "relevant_results": int(group["relevant"].sum()),
        "precision_at_5": precision,
    })

metrics = pd.DataFrame(per_query)

print("\nPrecision@5 by query:")
print(metrics.to_string(index=False))

if not metrics.empty:
    mean_precision = metrics["precision_at_5"].mean()
    print(f"\nMacro-average Precision@5: {mean_precision:.3f}")
    print(f"Percentage: {mean_precision * 100:.1f}%")

    output = PROJECT_DIR / "evaluation" / "evaluation_results.csv"
    metrics.to_csv(output, index=False)
    print(f"Saved query-level results to: {output}")
