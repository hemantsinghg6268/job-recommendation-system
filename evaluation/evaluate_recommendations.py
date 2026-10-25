
from pathlib import Path
import sys

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from src.recommender import recommend_jobs


PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_DIR / "evaluation" / "recommendation_candidates.csv"

# Test different skill profiles, not just one query.
TEST_QUERIES = [
    "Python, SQL, pandas, machine learning",
    "Python, scikit-learn, data science, statistics",
    "SQL, Power BI, Excel, data analysis",
    "Python, ETL, SQL, data engineering",
    "Python, machine learning, NLP, natural language processing",
]

all_results = []

for query in TEST_QUERIES:
    results = recommend_jobs(query, top_n=5)

    for rank, (_, job) in enumerate(results.iterrows(), start=1):
        matched = job.get("matched_skills", [])

        all_results.append({
            "query": query,
            "rank": rank,
            "job_id": job.get("job_id", ""),
            "job_title": job.get("job_title", ""),
            "matched_skills": ", ".join(map(str, matched)),
            "final_score": job.get("final_score", 0),
            "relevant": "",
        })

evaluation_df = pd.DataFrame(all_results)
evaluation_df.to_csv(OUTPUT_PATH, index=False)

print(f"Saved {len(evaluation_df)} recommendations to:")
print(OUTPUT_PATH)
print("\nReview these candidates and fill in the 'relevant' column.")
print("Use 1 for relevant and 0 for not relevant.\n")

if not evaluation_df.empty:
    print(
        evaluation_df[
            ["query", "rank", "job_title", "matched_skills"]
        ].to_string(index=False)
    )
else:
    print("No recommendations were returned for the test queries.")
