
# from pathlib import Path
# import sys

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field

# # Add the project root to Python's import path
# PROJECT_ROOT = Path(__file__).resolve().parents[1]
# sys.path.insert(0, str(PROJECT_ROOT))

# from src.recommender import recommend_jobs


# # Create the API application
# app = FastAPI(
#     title="AI Job Recommendation API",
#     description="Recommend jobs based on skills and interests.",
#     version="1.0.0"
# )


# # Define the expected request format
# class RecommendationRequest(BaseModel):
#     skills: str = Field(
#         min_length=1,
#         description="Skills or interests, e.g. Python, SQL, machine learning"
#     )
#     top_n: int = Field(default=5, ge=1, le=20)


# # Basic health-check endpoint
# @app.get("/")
# def home():
#     return {"message": "AI Job Recommendation API is running!"}


# # Job recommendation endpoint
# @app.post("/recommend")
# def get_recommendations(request: RecommendationRequest):
#     try:
#         results = recommend_jobs(request.skills, request.top_n)

#         # Convert the DataFrame into JSON-compatible records
#         jobs = results.replace({float("nan"): None}).to_dict(
#             orient="records"
#         )

#         return {
#             "query": request.skills,
#             "total_recommendations": len(jobs),
#             "recommendations": jobs
#         }

#     except ValueError as error:
#         raise HTTPException(status_code=400, detail=str(error))



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.recommender import recommend_jobs

app = FastAPI(
    title="Job Recommendation API",
    description="Recommends jobs based on a user's skills.",
    version="1.0.0",
)


class RecommendationRequest(BaseModel):
    skills: str = Field(
        ...,
        min_length=1,
        description="Comma-separated skills, e.g. Python, SQL, machine learning",
    )
    top_n: int = Field(default=5, ge=1, le=20)


@app.get("/")
def home():
    return {"message": "Job Recommendation API is running"}


@app.post("/recommend")
def get_recommendations(request: RecommendationRequest):
    try:
        results = recommend_jobs(
            request.skills,
            top_n=request.top_n,
        )

        return {
            "query_skills": request.skills,
            "total_recommendations": len(results),
            "recommendations": results.to_dict(orient="records"),
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
