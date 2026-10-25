# JobMatch — Job Recommendation System

## Overview

JobMatch is a content-based job recommendation system that ranks job opportunities according to a user's skills and the relevance of job titles, categories, and descriptions.

The project combines TF-IDF text similarity, skill matching, and title relevance to generate personalized job recommendations.

## Features

- Skill-based job recommendations
- TF-IDF text vectorization with unigrams and bigrams
- Hybrid recommendation scoring
- Matched-skill display and recommendation scores
- FastAPI REST API
- Streamlit web interface
- Automated tests for the recommendation engine and API
- Manual relevance evaluation using Precision@5

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- FastAPI and Uvicorn
- Streamlit
- Pytest

## Recommendation Method

The recommender uses a weighted combination of:

- Text similarity: 35%
- Skill coverage: 45%
- Job-title relevance: 20%

**Final score = 0.35 × text similarity + 0.45 × skill coverage + 0.20 × title relevance**

These weights are the current implementation's chosen settings, not values proven to be optimal.

## Dataset

The project uses the `batuhanmtl/job-skill-set` dataset from Hugging Face.

The data includes job titles, categories, descriptions, and skill sets. Refer to the original dataset's license and terms before redistributing it.

## Project Structure

```text
api/          FastAPI application
app/          Streamlit frontend
data/         Raw and processed datasets
evaluation/   Evaluation scripts and results
models/       Saved TF-IDF artifacts
notebooks/   Data exploration and model development
src/          Recommendation engine
tests/        Automated tests
```

## Run Locally

### 1. Create and activate a virtual environment

Windows CMD:

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 2. Install dependencies

```cmd
python -m pip install -r requirements.txt
```

### 3. Start the API

```cmd
python -m uvicorn api.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 4. Start the frontend

Open a second CMD window, activate the same virtual environment, navigate to the project folder, and run:

```cmd
python -m streamlit run app/streamlit_app.py
```

Open the local URL shown in the terminal, normally http://localhost:8501.

### 5. Run automated tests

```cmd
python -m pytest tests -v
```

## Evaluation

The current manual evaluation uses five test queries and human-assigned relevance labels. The observed macro-average Precision@5 was 0.96 on that small evaluation set.

This result is preliminary and does not represent 96% accuracy or guarantee performance on unseen users and queries. A larger, more representative evaluation is needed.

## Limitations

- Recommendations depend on the dataset's available jobs and skills.
- Skill matching uses normalized skill names and configured aliases.
- Job-title relevance is based on heuristics rather than a trained classifier.
- Evaluation labels are manually assigned, and the current sample is small.

## Future Improvements

- Add job-category filters and richer search controls.
- Expand the evaluation dataset and test more user profiles.
- Add filters for experience level, location, and job type when reliable data is available.
- Deploy the application so users can access it online.

## Dataset and License

This project uses the [LinkedIn Job Postings dataset](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings), created by Arsh Koneru.

**Dataset license:** [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

The dataset was cleaned and processed for use in this Job Recommendation System. Changes include data cleaning and preprocessing for the recommendation pipeline.

The original dataset is attributed to its creator. The processed dataset, to the extent it constitutes adapted material covered by the original license, is distributed under CC BY-SA 4.0.

This project is an independent portfolio project and is not affiliated with or endorsed by the dataset creator or LinkedIn.

## Author

Hemant Singh Ghosi

- LinkedIn: https://www.linkedin.com/in/hemant-singh-394095386/
- GitHub: https://github.com/hemantsinghg6268
