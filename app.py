
import streamlit as st
import pickle
import pandas as pd

def recommend(role):
    role_index=jobs[jobs['Role']==role].index[0]
    dist=similarity[role_index]
    job_list=sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:11]
    recommended_jobs=[]
    seen = set()  # Track unique combinations of role, experience, location
    for i in job_list:
        job_role = jobs.iloc[i[0]].Role
        # Get additional info from CSV
        job_info = jobs_df[jobs_df['Role'] == job_role]
        if not job_info.empty:
            experience = job_info.iloc[0]['Job Experience Required']
            location = job_info.iloc[0]['Location']
            # Create unique key to check for duplicates
            unique_key = (job_role, experience, location)
            if unique_key not in seen:
                seen.add(unique_key)
                recommended_jobs.append({
                    'Role': job_role,
                    'Experience': experience,
                    'Location': location
                })
        else:
            unique_key = (job_role, 'N/A', 'N/A')
            if unique_key not in seen:
                seen.add(unique_key)
                recommended_jobs.append({
                    'Role': job_role,
                    'Experience': 'N/A',
                    'Location': 'N/A'
                })
    return recommended_jobs


jobs_dict=pickle.load(open('jobs_dict.pkl','rb'))

jobs=pd.DataFrame(jobs_dict)

# Load full CSV with all features
jobs_df = pd.read_csv('jobss.csv')

similarity=pickle.load(open('similarity.pkl','rb'))



st.title('Jobs Recommender System')

selected_job_name = st.selectbox(
    "Enter the Job Role that you're looking for:",
    jobs['Role'].values

)

if st.button('Recommend'):
    recommendations=recommend(selected_job_name)
    st.markdown('### Top 10 Recommended Jobs:')
    st.markdown('---')
    for idx, job in enumerate(recommendations, 1):
        st.write(f"{idx}. {job['Role']} | {job['Experience']} | {job['Location']}")
