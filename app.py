
import streamlit as st
import pickle
import pandas as pd

def recommend(role):
    role_index=jobs[jobs['Role']==role].index[0]
    dist=similarity[role_index]
    job_list=sorted(list(enumerate(dist)),reverse=True,key=lambda x:x[1])[1:11]
    recommended_roles=[]
    for i in job_list:
        recommended_roles.append(jobs.iloc[i[0]].Role)
    return recommended_roles


jobs_dict=pickle.load(open('jobs_dict.pkl','rb'))

jobs=pd.DataFrame(jobs_dict)

similarity=pickle.load(open('similarity.pkl','rb'))



st.title('Jobs Recommender System')

selected_job_name = st.selectbox(
    "Enter the Job Role that you're looking for:",
    jobs['Role'].values

)

if st.button('Recommend'):
    recommendations=recommend(selected_job_name)
    for i in recommendations:
        st.write(i)
