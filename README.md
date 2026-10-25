# Job Recommendation System

An end-to-end machine learning project that recommends relevant job opportunities based on a user's skills.

## Live Demo

- **Streamlit App:** https://job-recommendation-system-hwbdik4kt3wezsnqhu8dpg.streamlit.app/
- **FastAPI Backend:** https://job-recommendation-api-w6oe.onrender.com
- **API Documentation:** https://job-recommendation-api-w6oe.onrender.com/docs

## Overview

The Job Recommendation System helps users discover relevant job opportunities by entering their skills. It processes the input and ranks jobs based on skill relevance using a TF-IDF-based recommendation approach.

## Features

- Skill-based job recommendations
- Ranked job results
- Recommendation scores
- Skill coverage and matched-skill information
- Job descriptions displayed with recommendations
- FastAPI backend for serving recommendations
- Streamlit interface for user interaction

## Tech Stack

- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn, TF-IDF
- **Backend:** FastAPI, Uvicorn
- **Frontend:** Streamlit
- **Testing:** Pytest
- **Version Control:** Git and GitHub

## Machine Learning Approach

1. Load and preprocess job data.
2. Convert job-related text into numerical representations using TF-IDF.
3. Compare user-provided skills with job information.
4. Rank job opportunities by relevance.
5. Return recommendations through the FastAPI backend.
6. Display the results in the Streamlit frontend.

## Project Structure

```text
job-recommendation-system/
├── api/
│   └── main.py
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   └── processed/
├── evaluation/
├── models/
├── notebooks/
├── src/
│   └── recommender.py
├── tests/
├── requirements.txt
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/hemantsinghg6268/job-recommendation-system.git
cd job-recommendation-system
```

### 2. Create and activate a virtual environment

**Windows CMD:**

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

Open one terminal and run:

```cmd
uvicorn api.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 5. Start the Streamlit frontend

Open another terminal in the project directory and run:

```cmd
python -m streamlit run app\streamlit_app.py
```

If you use a custom API URL, configure the `API_URL` environment variable or your Streamlit Cloud secrets as appropriate.

## API Endpoint

**POST** `/recommend`

Accepts user skills and a requested number of recommendations. See the interactive API documentation at `/docs` for the request schema and response format.

## Testing

Run the test suite:

```cmd
python -m pytest tests -v
```

## Dataset and Attribution

The project uses job-skill data derived from the `batuhanmtl/job-skill-set` dataset on Hugging Face. The original dataset source is the [LinkedIn Job Postings dataset on Kaggle](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings) by Arsh Koneru.

Refer to the repository's dataset attribution and licensing information for the applicable terms.

## Future Improvements

- Evaluate recommendation quality with suitable ranking metrics.
- Improve matching for related skills and synonyms.
- Add filters for job title, location, and experience level.
- Expand the dataset and improve data quality.

## Author

**Hemant Singh Ghosi**

- LinkedIn: https://www.linkedin.com/in/hemant-singh-394095386/
- GitHub: [@hemantsinghg6268](https://github.com/hemantsinghg6268)
