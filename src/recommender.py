
# from pathlib import Path

# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity


# # Find the main project directory
# BASE_DIR = Path(__file__).resolve().parents[1]

# # Define paths to the dataset and saved model files
# DATA_PATH = BASE_DIR / "data" / "processed" / "jobs_cleaned.csv"
# VECTORIZER_PATH = BASE_DIR / "models" / "tfidf_vectorizer.pkl"
# MATRIX_PATH = BASE_DIR / "models" / "tfidf_matrix.pkl"


# # Load the dataset and saved TF-IDF components
# df = pd.read_csv(DATA_PATH)
# tfidf = joblib.load(VECTORIZER_PATH)
# tfidf_matrix = joblib.load(MATRIX_PATH)


# def recommend_jobs(user_skills: str, top_n: int = 5) -> pd.DataFrame:
#     """Recommend jobs based on the user's skills or interests."""

#     if not isinstance(user_skills, str) or not user_skills.strip():
#         raise ValueError("Please enter your skills or interests.")

#     if not isinstance(top_n, int) or top_n < 1:
#         raise ValueError("top_n must be a positive integer.")

#     # Convert the user's input into a TF-IDF vector
#     user_vector = tfidf.transform([user_skills])

#     # Calculate similarity against every job
#     scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

#     # Keep only jobs with a positive similarity score
#     matching_indices = np.where(scores > 0)[0]

#     if len(matching_indices) == 0:
#         return pd.DataFrame(
#             columns=["job_title", "category", "similarity_score"]
#         )

#     # Rank jobs from highest similarity to lowest
#     ranked_indices = matching_indices[
#         np.argsort(scores[matching_indices])[::-1]
#     ][:top_n]

#     # Select the available job details
#     columns = [
#         col for col in [
#             "job_id",
#             "job_title",
#             "category",
#             "job_description",
#             "job_skill_set"
#         ]
#         if col in df.columns
#     ]

#     results = df.iloc[ranked_indices][columns].copy()
#     results["similarity_score"] = scores[ranked_indices]

#     return results.reset_index(drop=True)




from pathlib import Path
import ast

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "processed" / "jobs_cleaned.csv"
MODEL_DIR = PROJECT_DIR / "models"

# Load the dataset and saved TF-IDF artifacts
df = pd.read_csv(DATA_PATH)

vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
tfidf_matrix = joblib.load(MODEL_DIR / "tfidf_matrix.pkl")

# Ensure the saved matrix corresponds to the current dataset
if len(df) != tfidf_matrix.shape[0]:
    raise ValueError(
        "Dataset and TF-IDF matrix have different row counts. "
        "Rerun the notebook's TF-IDF setup cell."
    )

ALIASES = {
    "sklearn": "scikit-learn",
    "ml": "machine learning",
    "structured query language": "sql",
}


def normalize_skill(skill):
    skill = str(skill).strip().lower()
    return ALIASES.get(skill, skill)


def parse_skills(value):
    if isinstance(value, list):
        return [normalize_skill(s) for s in value]

    if pd.isna(value):
        return []

    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return [normalize_skill(s) for s in parsed]
        except (ValueError, SyntaxError):
            pass

        return [
            normalize_skill(s)
            for s in value.split(",")
            if s.strip()
        ]

    return []


def skill_coverage(user_skills, job_skill_value):
    job_skills = set(parse_skills(job_skill_value))
    if not user_skills:
        return 0.0

    return len(set(user_skills) & job_skills) / len(set(user_skills))


def technical_role_relevance(title, description):
    title = str(title).lower().strip()
    description = str(description).lower()

    non_technical = [
        "business development representative",
        "sales representative",
        "account executive",
        "recruiter",
    ]

    if any(term in title for term in non_technical):
        return 0.0

    strong_titles = [
        "data scientist",
        "machine learning engineer",
        "ml engineer",
        "ai engineer",
        "data analyst",
        "data engineer",
        "software engineer",
        "software developer",
        "python developer",
        "backend developer",
        "full stack developer",
        "business intelligence analyst",
    ]

    if any(term in title for term in strong_titles):
        return 1.0

    moderate_titles = [
        "database administrator",
        "devops engineer",
        "cloud engineer",
        "information technology specialist",
        "it analyst",
        "systems analyst",
        "software architect",
    ]

    if any(term in title for term in moderate_titles):
        return 0.6

    technical_terms = [
        "software development",
        "data engineering",
        "machine learning",
        "programming",
        "data analytics",
    ]

    if any(term in description for term in technical_terms):
        return 0.3

    return 0.0


def recommend_jobs(user_skills, top_n=5):
    if not isinstance(user_skills, str) or not user_skills.strip():
        raise ValueError("Please enter your skills.")

    if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 1:
        raise ValueError("top_n must be a positive integer.")

    skills = {
        normalize_skill(skill)
        for skill in user_skills.split(",")
        if skill.strip()
    }

    if not skills:
        raise ValueError("Please enter at least one valid skill.")

    user_vector = vectorizer.transform([user_skills])
    text_scores = cosine_similarity(
        user_vector, tfidf_matrix
    ).flatten()

    skill_scores = np.array([
        skill_coverage(skills, value)
        for value in df["job_skill_set"]
    ])

    title_scores = np.array([
        technical_role_relevance(title, description)
        for title, description in zip(
            df["job_title"], df["job_description"]
        )
    ])

    final_scores = (
        0.35 * text_scores
        + 0.45 * skill_scores
        + 0.20 * title_scores
    )

    descriptions = (
        df["job_description"].fillna("").astype(str).str.lower()
    )

    pipeline_phrases = [
        "does not represent an actual job opening",
        "pipeline/repository",
        "talent pool",
        "future opportunities",
    ]

    invalid = descriptions.apply(
        lambda desc: any(p in desc for p in pipeline_phrases)
    ).to_numpy()

    eligible = (~invalid) & ((text_scores > 0) | (skill_scores > 0))
    candidates = np.where(eligible)[0]

    ranked = candidates[
        np.argsort(final_scores[candidates])[::-1]
    ][:top_n]

    results = df.iloc[ranked][
        [
            "job_id",
            "job_title",
            "category",
            "job_skill_set",
            "job_description",
        ]
    ].copy()

    results["matched_skills"] = [
        sorted(set(parse_skills(value)) & skills)
        for value in results["job_skill_set"]
    ]

    results["text_similarity"] = text_scores[ranked]
    results["skill_coverage"] = skill_scores[ranked]
    results["title_relevance"] = title_scores[ranked]
    results["final_score"] = final_scores[ranked]

    return results.reset_index(drop=True)
