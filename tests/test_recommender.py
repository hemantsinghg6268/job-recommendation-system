
# from src.recommender import recommend_jobs


# results = recommend_jobs(
#     "Python machine learning pandas scikit-learn SQL",
#     top_n=5
# )

# print(results[["job_title", "category", "similarity_score"]])




import pytest

from src.recommender import recommend_jobs


def test_valid_skills_return_recommendations():
    results = recommend_jobs(
        "Python, SQL, machine learning, pandas",
        top_n=5,
    )

    assert results is not None
    assert len(results) <= 5
    assert "job_title" in results.columns
    assert "matched_skills" in results.columns
    assert "skill_coverage" in results.columns
    assert "final_score" in results.columns


def test_skill_coverage_is_between_zero_and_one():
    results = recommend_jobs(
        "Python, SQL, pandas",
        top_n=5,
    )

    if not results.empty:
        assert results["skill_coverage"].between(0, 1).all()


def test_empty_skills_raise_error():
    with pytest.raises(ValueError):
        recommend_jobs("", top_n=5)


def test_whitespace_skills_raise_error():
    with pytest.raises(ValueError):
        recommend_jobs("   ", top_n=5)


def test_zero_top_n_raises_error():
    with pytest.raises(ValueError):
        recommend_jobs("Python, SQL", top_n=0)


def test_negative_top_n_raises_error():
    with pytest.raises(ValueError):
        recommend_jobs("Python, SQL", top_n=-1)


def test_too_many_recommendations_are_limited():
    results = recommend_jobs(
        "Python, SQL, machine learning",
        top_n=3,
    )

    assert len(results) <= 3
