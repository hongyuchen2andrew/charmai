import streamlit as st
from streamlit_chatbox import *
import time
import base64
from PIL import Image
from io import BytesIO
import simplejson as json
from streamlit_modal import Modal
import streamlit.components.v1 as components

from gpt import LargeLanguageModels
from profiles import Profile
from duckduckgo import restaurantRecommendation
from vision import Vision

api_key = st.secrets["API_KEY"]
perplexity_key = st.secrets["PERPLEXITY_KEY"]
google_key = st.secrets["GOOGLE_KEY"]
llama_key = st.secrets["LLAMA_KEY"]
langChain_key = st.secrets["LANGCHAIN_KEY"]
gemini_key = st.secrets["GEMINI_API_KEY"]

introduction = 'Hi, my name is Andrew. I have lived in China for 20 years. Last year, I went to MIT for my master degree. So as you can see, I am twenty one years old\
                I love coding, playing basketball, singing, going hiking. Nice to meet you.'  

st.title("CharmAI")
chat_box = ChatBox()

if "recording" not in st.session_state:
    st.session_state.recording = []

#init the userName
if "userName" not in st.session_state:
    userName = 'User'
else:
    userName = st.session_state.userName

#init the userName
if "userAge" not in st.session_state:
    userAge = 'unknown'
else:
    userAge = st.session_state.userAge

#init the userCareer
if "userCareer" not in st.session_state:
    userCareer = 'unknown'
else:
    userCareer = st.session_state.userCareer

#init the userGender
if "userGender" not in st.session_state:
    userGender = 'unknown'
else:
    userGender = st.session_state.userGender

#init the userPersonality
if "userPersonality" not in st.session_state:
    userPersonality = 'unknown'
else:
    userPersonality = st.session_state.userPersonality

#init the userHobby
if "userHobby" not in st.session_state:
    userHobby = 'unknown'
else:
    userHobby = st.session_state.userHobby

#st.write(userName, userAge, userGender, userCareer, userPersonality, userHobby)
with st.sidebar:
    st.subheader('Start to chat with CharmAI!')
    in_expander = st.checkbox('show messages in expander', True)
    show_history = st.checkbox('show history', False)
    option = st.selectbox(
        "Please choose the mode:",
        ("Your Friend", "Chat Consultant", "Role Play", "Date Expert"),
        index=None,
        placeholder="Select the mode...",
        )
    if option == "Role Play":
        give_feedback = st.checkbox('Recieve feedback regarding your message from CharmAI.', False)
    introduction = st.text_area(label = 'Description', placeholder = 'Please enter the description...')
    st.divider()

    btns = st.container()

    img = st.file_uploader(
        "Upload File"
    )


chat_box.init_session()
chat_box.output_messages()

if "role_play" not in st.session_state:
    st.session_state.role_play = 0
if "your_friend" not in st.session_state:
    st.session_state.your_friend = 0
if "chat_consultant" not in st.session_state:
    st.session_state.chat_consultant = 0
if "date_expert" not in st.session_state:
    st.session_state.date_expert = 0

if "guidance" not in st.session_state:
    st.session_state.guidance = 0
    
if st.session_state.guidance == 0:
    chat_box.ai_say(
        [
            Markdown('What do you need?<br>\
                    Pick one mode from left side bar- \"Please choose the mode\"<br>\
                    **Your Friend**:<br>\
                    Feeling sad, lonely, or in need of a chat? CharmAI is here for you—a smart, warmth and humor woman to keep you company.<br>\
                    **Chat Consultant**:<br>\
                    Need tips on what to say next? CharmAI offers advice and insights to keep your conversations engaging and forward-moving<br>\
                    **Role Play**:<br>\
                    Want to charm someone special? Practice together to spark engaging conversations, where CharmAI is the person you\'re drawn to.<br>\
                    **Date Expert**:<br>\
                    Anxious about your upcoming date? Date Expert provides tailored guidance to help you plan dates that leave a lasting impression<br>\
                    ***Notice:** If you choose none of the above, GPT4 will be used as your default assistant.*',
                    in_expander=in_expander,
                    expanded=True, state='complete', title="CharmAI"),
        ]
    )
    st.session_state.guidance += 1
  
profile = Profile(introduction, api_key)
if option == "Role Play":
    st.session_state.your_friend = 0
    st.session_state.chat_consultant = 0
    st.session_state.date_expert = 0
    
    if st.session_state.role_play == 0:
        chat_box.ai_say(
            [
                Markdown('Please give me a breif description of the role you want me to play in the sidebar! Try to include some key information like age, gender, careers, and also personality.\
                         For example, \'Her name is Camila, a beautiful 27-year-old girl from Taiwan, pursuing her Master\'s in Information System at the University of Washington.\
                         She loves yoga, movies, and outdoor activities. She\'s currently learning to ski.\'', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.role_play += 1
    if st.session_state.role_play >= 1:
        age, gender, career, personality, hobby = profile.returnProfile()
        #-------------------------------------------------#
        if len(chat_box.history) <= 4:
            career = 'unknown'
            userCareer = 'unknown'
        if len(chat_box.history) <= 8:
            personality, hobby = 'unknown', 'unknown'
            userHobby = 'unknown'
        #-------------------------------------------------#
        LLM = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby), api_key)
        if query := st.chat_input('Chat with CharmAI...'):
            chat_box.user_say(query)
            text, st.session_state.recording = LLM.rolePlay(query, st.session_state.recording)
            if give_feedback:
                feedback = LLM.giveFeedback(query, st.session_state.recording)
                chat_box.ai_say(
                    [
                        Markdown(feedback, in_expander=in_expander,
                                    expanded=True, state='complete', title="CharmAI"),
                    ]
                )
            chat_box.ai_say(
                [
                    Markdown(text, in_expander=in_expander,
                                expanded=True, state='complete', title="CharmAI"),
                ]
            )

    if btns.button("Clear history"):
        chat_box.init_session(clear=True)
        st.rerun()

    if btns.button("Start a new conversation"):
        chat_box.init_session(clear=True)
        st.session_state.recording = []
        st.rerun()

    if show_history:
        st.write(chat_box.history)

elif option == "Your Friend":
    st.session_state.role_play = 0
    st.session_state.chat_consultant = 0
    st.session_state.date_expert = 0
    if st.session_state.your_friend == 0:
        chat_box.ai_say(
            [
                Markdown('Hey there! I\'m your best friend! You can talk everything you want to me!', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.your_friend += 1
    age = gender = career = personality = hobby = 'unkown'
    if len(chat_box.history) <= 4:
        career = 'unknown'
    if len(chat_box.history) <= 8:
        personality, hobby = 'unknown', 'unknown'
    LLM = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby), api_key)
    male = ['male', 'man', 'boy', 'gentleman', 'sir']
    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        if userGender.lower() in male:
            text, st.session_state.recording = LLM.yourFriendForMale(query, st.session_state.recording)
        else:
            text, st.session_state.recording = LLM.yourFriendForFemale(query, st.session_state.recording)
        text += ' By the way, if you can upload a screenshot of the chat history, our **Chat Consultant** feature might be able to help you.'
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )

    if btns.button("Clear history"):
        chat_box.init_session(clear=True)
        st.rerun()

    if btns.button("Start a new conversation"):
        chat_box.init_session(clear=True)
        st.session_state.recording = []
        st.rerun()

    if show_history:
        st.write(chat_box.history)

elif option == "Chat Consultant":
    st.session_state.role_play = 0
    st.session_state.your_friend = 0
    st.session_state.date_expert = 0
    age, gender, career, personality, hobby = profile.returnProfile()
    LLM_1 = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby), api_key)
    if st.session_state.chat_consultant == 0:
        if 'analysis' in st.session_state:
            st.session_state.analysis = ''
        if not img:
            chat_box.ai_say(
                [
                    Markdown('Please give me a file or screen shot that contains the chat you want me to analysis so that I can give you some suggestion about how to reply!', 
                                in_expander=in_expander,
                                expanded=True, state='complete', title="CharmAI"),
                ]
            )
        else:
            bytes_data = img.read()
            im = Image.open(BytesIO(bytes_data))
            if img:
                st.image(bytes_data)
            st.session_state.chat_consultant += 1

            gemini = Vision(im)
            chat_history = gemini.chatHistoryScreenshot()
            analysis = LLM_1.chatConsultant(chat_history)
            if 'analysis' not in st.session_state:
                st.session_state.analysis = analysis

            #Here, GPT need to role play the user, so we exchange the positions of the two profiles
            LLM = LargeLanguageModels((userAge, userGender, userCareer, userPersonality, userHobby), ('', age, gender, career, personality, hobby), api_key)
            prompt = f'This is the situation: {analysis}. Please reply to \'A\' based on the situation and the chatting history.'
            text, _ = LLM.consultantReply(prompt, chat_history, list(analysis))
            chat_box.ai_say(
                [
                    Markdown(analysis, 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="Analysis"),
                ]
            )
            chat_box.ai_say(
                [
                    Markdown(text, 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
                ]
            )

    if query := st.chat_input('Ask something about the screenshot...'):
        chat_box.user_say(query)
        text = LLM_1.qustionAnsweringBot(prompt = query, additional_information = st.session_state.analysis)
        chat_box.ai_say(
            [
                Markdown(text, 
                        in_expander=in_expander,
                        expanded=True, state='complete', title="Chat Consultant"),
            ]
        )


    if btns.button("Clear history"):
        chat_box.init_session(clear=True)
        st.rerun()

    if btns.button("Start a new conversation"):
        chat_box.init_session(clear=True)
        st.session_state.recording = []
        st.rerun()

    if show_history:
        st.write(chat_box.history)

elif option == "Date Expert":
    st.session_state.role_play = 0
    st.session_state.your_friend = 0
    st.session_state.chat_consultant = 0
    if st.session_state.date_expert == 0:
        chat_box.ai_say(
            [
                Markdown('Please briefly describe what kind of date you would like. Romantic? Thrilling? Or artistic?', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.date_expert += 1
    profile = Profile(introduction, api_key)
    age, gender, career, personality, hobby = profile.returnProfile()
    LLM = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby), api_key)
    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        date_plan = LLM.customizeDate(query)
        chat_box.ai_say(
            [
                Markdown(date_plan, 
                        in_expander=in_expander,
                        expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.date_expert += 1
        recommendation = restaurantRecommendation(date_plan, api_key, google_key, perplexity_key)
        for rec in recommendation:
            if rec == 'unknown':
                continue
            try:
                title = rec[0]['title']
                st.write('**Name:** ', title)
                #print('Name: ', title)
            except:
                st.write('**Address:** ', 'unknown')
                #print('Name: ', 'unknown')

            try:
                address = rec[0]['address']
                st.write('**Address:** ', address)
                #print('Address: ', address)
            except:
                st.write('**Address:** ', 'unknown')
                #print('Address: ', 'unknown')

            try:
                phone = rec[0]['phone']
                st.write('**Phone:** ', phone)
                #print('Phone: ', phone)
            except:
                st.write('**Phone:** ', 'unknown')
                #print('Phone: ', 'unknown')

            try:
                website = rec[0]['website']
                st.write('**Website:** ', website)
                #print('Website: ', website)
            except:
                st.write('**Website:** ', 'unknown')
                #print('Website: ', 'unknown')

            try:
                link = rec[0]['link']
                st.write('**Link:** ', link)
                #print('Link: ', link)
            except:
                st.write('**Link:** ', 'unknown')
                #print('Link: ', 'unknown')

    if btns.button("Clear history"):
        chat_box.init_session(clear=True)
        st.rerun()

    if btns.button("Start a new conversation"):
        chat_box.init_session(clear=True)
        st.session_state.recording = []
        st.rerun()

    if show_history:
        st.write(chat_box.history)

else:
    st.session_state.role_play = 0
    st.session_state.your_friend = 0
    st.session_state.chat_consultant = 0
    st.session_state.date_expert = 0
    profile = ''
    userProfile = ''
    LLM = LargeLanguageModels(profile, userProfile, api_key)
    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        text, st.session_state.recording = LLM.chatGPT(query, st.session_state.recording)
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )

    if btns.button("Clear history"):
        chat_box.init_session(clear=True)
        st.rerun()

    if btns.button("Start a new conversation"):
        chat_box.init_session(clear=True)
        st.session_state.recording = []
        st.rerun()

    if show_history:
        st.write(chat_box.history)

# cols = st.columns(2)
# if cols[0].button('show me the multimedia'):
#     chat_box.ai_say(Image(
#         'https://tse4-mm.cn.bing.net/th/id/OIP-C.cy76ifbr2oQPMEs2H82D-QHaEv?w=284&h=181&c=7&r=0&o=5&dpr=1.5&pid=1.7'))
#     time.sleep(0.5)
#     chat_box.ai_say(
#         Video('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))
#     time.sleep(0.5)
#     chat_box.ai_say(
#         Audio('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))

# if cols[1].button('run agent'):
#     chat_box.user_say('run agent')
#     agent = FakeAgent()
#     text = ""

#     # streaming:
#     chat_box.ai_say() # generate a blank placeholder to render messages
#     for d in agent.run_stream():
#         if d["type"] == "complete":
#             chat_box.update_msg(expanded=False, state="complete")
#             chat_box.insert_msg(d["llm_output"])
#             break

#         if d["status"] == 1:
#             chat_box.update_msg(expanded=False, state="complete")
#             text = ""
#             chat_box.insert_msg(Markdown(text, title=d["text"], in_expander=True, expanded=True))
#         elif d["status"] == 2:
#             text += d["llm_output"]
#             chat_box.update_msg(text, streaming=True)
#         else:
#             chat_box.update_msg(text, streaming=False)

