import streamlit as st
from profiles import Profile
from streamlit_extras.switch_page_button import switch_page

st.markdown("<h2 style='color:pink; font-size: 60px; text-align:left; margin-top: -40px'>Account</h2>", unsafe_allow_html=True) 
# api_key = st.text_input(label = 'OpenAI API Key (Required)', placeholder = 'Please enter your OpenAI API Keys...')
# perplexity_key = st.text_input(label = 'Perplexity API Key', placeholder = 'Please enter your Perplexity API key...')
# google_key = st.text_input(label = 'Google API Key', placeholder = 'Please enter your Google API key...')
# if not(("api_key" in st.session_state) and ("perplexity_key" in st.session_state) and ("google_key" in st.session_state) and ("llama_key" in st.session_state) and ("langChain_key" in st.session_state)):
#     st.error("Please input your API Key in the box.\
#               Don't have a OpenAI key? Click here: https://openai.com/blog/openai-api\
#               Don't have a Perplexity key? Click here: https://www.perplexity.ai/settings/api\
#               Don't have a Google key? Click here: https://serpapi.com/.)\
#               Don't have a Llama key? Click here: https://replicate.com/account/api-tokens.)\
#               Don't have a LangChain key? Click here: https://python.langchain.com/docs/get_started/quickstart.")
#     st.stop() 
# st.write('**API Key verified! Let\'s start to complete your profile! You can also complete it later.**')
userName = st.text_input(label = '**Name** (Optinal)', placeholder = 'Please enter your name...')
age = st.select_slider('**Age** (Optinal)', options=list(range(18, 121)))
gender = st.text_input(label = '**Gender** (Optinal)', placeholder = 'Please enter your gender...')
job = st.text_input(label = '**Job** (Optinal)', placeholder = 'Please enter your job...')
personality = st.text_input(label = '**Personality** (Personality can be a description or several keywords) (Optinal)', placeholder = 'Please enter your personalities...')
hobby = st.text_input(label = '**Hobby** (Hobby can be a description or several keywords) (Optinal)', placeholder = 'Please enter your hobbies...')

col1, col2 = st.columns(2)
with col2:
    if st.button("Not Now"):
        switch_page("Chatbot")
if userName or gender or job or personality or hobby:
    prompt = f'Hi, my name is {userName}, my age is {age}, my gender is {gender}, my job is {job}, my personalities are {personality}, my hobbies are {hobby}.'
    profile = Profile(prompt, api_key)
    userAge, userGender, userCareer, userPersonality, userHobby = profile.returnProfile()
    st.session_state.userName = userName
    st.session_state.userAge = userAge
    st.session_state.userGender = userGender
    st.session_state.userCareer = userCareer
    st.session_state.userPersonality = userPersonality
    st.session_state.userHobby = userHobby
    with col1:
        if st.button("Save"):
            switch_page("Chatbot")

