
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Job Recommendation API is running"


def test_recommend_endpoint():
    response = client.post(
        "/recommend",
        json={
            "skills": "Python, SQL, pandas, machine learning",
            "top_n": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "recommendations" in data
    assert "total_recommendations" in data
    assert data["total_recommendations"] <= 5


def test_empty_skills_are_rejected():
    response = client.post(
        "/recommend",
        json={"skills": "", "top_n": 5},
    )

    assert response.status_code == 422


def test_invalid_top_n_is_rejected():
    response = client.post(
        "/recommend",
        json={"skills": "Python, SQL", "top_n": 0},
    )

    assert response.status_code == 422
