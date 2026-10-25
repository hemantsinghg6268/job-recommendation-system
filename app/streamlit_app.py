
# import requests
# import streamlit as st

# # Address of our running FastAPI backend
# API_URL = "http://127.0.0.1:8000/recommend"

# # Configure the page
# st.set_page_config(
#     page_title="AI Job Finder",
#     page_icon="💼",
#     layout="wide"
# )

# st.title("💼 AI Job Finder")
# st.write("Discover jobs that match your skills and interests.")

# # Collect user input
# skills = st.text_area(
#     "Enter your skills",
#     placeholder="Example: Python, SQL, Machine Learning, Pandas"
# )

# top_n = st.slider(
#     "Number of recommendations",
#     min_value=1,
#     max_value=20,
#     value=5
# )

# # Send the request to our API
# if st.button("Recommend Jobs", type="primary"):
#     if not skills.strip():
#         st.warning("Please enter your skills first.")
#     else:
#         try:
#             with st.spinner("Finding matching jobs..."):
#                 response = requests.post(
#                     API_URL,
#                     json={
#                         "skills": skills,
#                         "top_n": top_n
#                     },
#                     timeout=30
#                 )

#             if response.status_code == 200:
#                 data = response.json()
#                 jobs = data["recommendations"]

#                 st.subheader(
#                     f"Recommended Jobs ({len(jobs)})"
#                 )

#                 if not jobs:
#                     st.info(
#                         "No matching jobs found. Try different skills."
#                     )

#                 for index, job in enumerate(jobs, start=1):
#                     with st.container(border=True):
#                         st.subheader(
#                             f"{index}. {job.get('job_title', 'Untitled job')}"
#                         )

#                         st.write(
#                             "**Category:**",
#                             job.get("category", "Not specified")
#                         )

#                         score = job.get("similarity_score")
#                         if score is not None:
#                             st.write(
#                                 f"**Text similarity:** {score:.1%}"
#                             )

#                         description = job.get("job_description")
#                         if description:
#                             with st.expander("View job description"):
#                                 st.write(description)

#                         job_skills = job.get("job_skill_set")
#                         if job_skills:
#                             st.write("**Job skills:**", job_skills)

#             else:
#                 st.error(
#                     f"API error {response.status_code}: "
#                     f"{response.text}"
#                 )

#         except requests.exceptions.ConnectionError:
#             st.error(
#                 "Cannot connect to the API. "
#                 "Please start FastAPI in another terminal."
#             )

#         except requests.exceptions.RequestException as error:
#             st.error(f"Request failed: {error}")



# import requests
# import streamlit as st
# import pandas as pd

# API_URL = "http://127.0.0.1:8000/recommend"

# st.set_page_config(
#     page_title="Job Recommendation System",
#     page_icon="💼",
#     layout="wide",
# )

# st.title("💼 Job Recommendation System")
# st.write(
#     "Enter your skills to discover jobs that match your profile."
# )

# with st.form("recommendation_form"):
#     skills = st.text_input(
#         "Your skills",
#         placeholder="Python, SQL, machine learning, pandas",
#     )

#     top_n = st.slider(
#         "Number of recommendations",
#         min_value=1,
#         max_value=10,
#         value=5,
#     )

#     submitted = st.form_submit_button("Find matching jobs")

# if submitted:
#     if not skills.strip():
#         st.warning("Please enter at least one skill.")
#     else:
#         try:
#             with st.spinner("Finding matching jobs..."):
#                 response = requests.post(
#                     API_URL,
#                     json={
#                         "skills": skills,
#                         "top_n": top_n,
#                     },
#                     timeout=60,
#                 )

#             if response.ok:
#                 data = response.json()
#                 jobs = data.get("recommendations", [])

#                 st.subheader("Your job recommendations")
#                 st.write(
#                     f"Found {len(jobs)} matching jobs."
#                 )

#                 if not jobs:
#                     st.info(
#                         "No matching jobs found. Try adding "
#                         "more skills or using alternative terms."
#                     )

#                 for index, job in enumerate(jobs, start=1):
#                     title = job.get("job_title", "Untitled job")
#                     category = job.get("category", "Uncategorized")

#                     with st.container(border=True):
#                         st.markdown(f"### {index}. {title}")
#                         st.caption(f"Category: {category}")

#                         matched = job.get("matched_skills", [])
#                         st.write("**Matched skills:**")
#                         st.write(
#                             ", ".join(matched)
#                             if matched
#                             else "No exact skill matches"
#                         )

#                         score = job.get("final_score")
#                         if score is not None:
#                             st.metric(
#                                 "Recommendation score",
#                                 f"{float(score):.3f}",
#                             )

#                         description = job.get("job_description")
#                         if description:
#                             with st.expander("View job description"):
#                                 st.write(description)

#             else:
#                 st.error(
#                     f"API error ({response.status_code}): "
#                     f"{response.text[:1000]}"
#                 )

#         except requests.RequestException as exc:
#             st.error(
#                 "Could not connect to the API. "
#                 "Make sure the FastAPI server is running. "
#                 f"Details: {exc}"
#             )





import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(
    page_title="JobMatch | Job Recommendation System",
    page_icon="💼",
    layout="wide",
)

st.title("💼 JobMatch")
st.subheader("Find jobs that match your skills")
st.write(
    "Enter your skills to discover relevant job opportunities "
    "ranked by skill coverage and text similarity."
)

with st.form("recommendation_form"):
    skills = st.text_input(
        "Your skills",
        placeholder="Python, SQL, pandas, machine learning",
    )

    top_n = st.slider(
        "Number of recommendations",
        min_value=1,
        max_value=10,
        value=5,
    )

    submitted = st.form_submit_button(
        "Find matching jobs",
        use_container_width=True,
    )

if submitted:
    if not skills.strip():
        st.warning("Please enter at least one skill.")
    else:
        try:
            with st.spinner("Finding jobs that match your skills..."):
                response = requests.post(
                    API_URL,
                    json={"skills": skills, "top_n": top_n},
                    timeout=60,
                )

            if response.ok:
                data = response.json()
                jobs = data.get("recommendations", [])

                st.divider()
                st.subheader("Your recommendations")

                col1, col2 = st.columns(2)
                col1.metric("Jobs found", len(jobs))
                col2.metric(
                    "Skills entered",
                    len([s for s in skills.split(",") if s.strip()]),
                )

                if not jobs:
                    st.info(
                        "No matching jobs found. Try adding more skills "
                        "or using alternative terms."
                    )

                for index, job in enumerate(jobs, start=1):
                    title = job.get("job_title", "Untitled job")
                    category = job.get("category", "Uncategorized")
                    matched = job.get("matched_skills", [])
                    score = job.get("final_score")
                    coverage = job.get("skill_coverage")

                    with st.container(border=True):
                        st.markdown(f"### {index}. {title}")
                        st.caption(f"Category: {category}")

                        metric1, metric2 = st.columns(2)

                        if score is not None:
                            metric1.metric(
                                "Recommendation score",
                                f"{float(score):.3f}",
                            )

                        if coverage is not None:
                            metric2.metric(
                                "Skill coverage",
                                f"{float(coverage) * 100:.1f}%",
                            )

                        st.write("**Matched skills**")
                        st.write(
                            ", ".join(matched)
                            if matched
                            else "No exact skill matches detected."
                        )

                        description = job.get("job_description")
                        if description:
                            with st.expander("View job description"):
                                st.write(description)

            else:
                st.error(
                    f"API error ({response.status_code}): "
                    f"{response.text[:500]}"
                )

        except requests.RequestException as exc:
            st.error(
                "Could not connect to the API. Make sure the FastAPI "
                f"server is running. Details: {exc}"
            )
