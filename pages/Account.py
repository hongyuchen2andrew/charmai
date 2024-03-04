import streamlit as st
from profiles import Profile

st.markdown("<h2 style='color:pink; font-size: 60px; text-align:left; margin-top: -40px'>Account</h2>", unsafe_allow_html=True) 

userName = st.text_input(label = 'Name', placeholder = 'Please enter your name...')
age = st.select_slider('Age:', options=list(range(18, 121)))
gender = st.text_input(label = 'Gender', placeholder = 'Please enter your gender...')
job = st.text_input(label = 'Job', placeholder = 'Please enter your job...')
personality = st.text_input(label = 'Personality (Personality can be a description or several keywords)', placeholder = 'Please enter your personalities...')
hobby = st.text_input(label = 'Hobby (Hobby can be a description or several keywords)', placeholder = 'Please enter your hobbies...')

prompt = f'Hi, my name is {userName}, my age is {age}, my gender is {gender}, my job is {job}, my personalities are {personality}, my hobbies are {hobby}.'

profile = Profile(prompt)
userAge, userGender, userCareer, userPersonality, userHobby = profile.returnProfile()

st.session_state.userName = userName
st.session_state.userAge = userAge
st.session_state.userGender = userGender
st.session_state.userCareer = userCareer
st.session_state.userPersonality = userPersonality
st.session_state.userHobby = userHobby
