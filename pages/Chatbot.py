import streamlit as st
from streamlit_chatbox import *
import time
import base64
import simplejson as json
from streamlit_modal import Modal
import streamlit.components.v1 as components

from gpt import LargeLanguageModels
from profiles import Profile
from duckduckgo import restaurantRecommendation

introduction = 'Hi, my name is Andrew. I have lived in China for 20 years. Last year, I went to MIT for my master degree. So as you can see, I am twenty one years old\
                I love coding, playing basketball, singing, going hiking. Nice to meet you.'  

st.title("CharmAI")
profile = Profile
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
    api_key = st.text_area(label = 'API Key', placeholder = 'Please enter your OpenAI API key...')
    st.divider()

    btns = st.container()

    image = st.file_uploader(
        "Chat history screenshot"
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
print(len(chat_box.history))
if "api_key" in st.session_state:
    api_key = st.session_state.api_key
if not api_key:
    st.error("Please input your OpenAI API Key in the sidebar.\
              Don't have a key? Click here: https://openai.com/blog/openai-api")
    st.stop() 
profile = Profile(introduction, api_key)
if option == "Role Play":
    # st.session_state.your_friend = 0
    # st.session_state.chat_consultant = 0
    # st.session_state.date_expert = 0
    
    if st.session_state.role_play == 0:
        chat_box.init_session(clear=True)
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
        if len(chat_box.history) <= 4:
            career = 'unknown'
            userCareer = 'unknown'
        if len(chat_box.history) <= 8:
            personality, hobby = 'unknown', 'unknown'
            userHobby = 'unknown'
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
    # btns.download_button(
    #     "Export Markdown",
    #     "".join(chat_box.export2md()),
    #     file_name=f"chat_history.md",
    #     mime="text/markdown",
    # )

    # btns.download_button(
    #     "Export Json",
    #     chat_box.to_json(),
    #     file_name="chat_history.json",
    #     mime="text/json",
    # )

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
    # st.session_state.chat_consultant = 0
    # st.session_state.date_expert = 0
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
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
    # btns.download_button(
    #     "Export Markdown",
    #     "".join(chat_box.export2md()),
    #     file_name=f"chat_history.md",
    #     mime="text/markdown",
    # )

    # btns.download_button(
    #     "Export Json",
    #     chat_box.to_json(),
    #     file_name="chat_history.json",
    #     mime="text/json",
    # )

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
    # st.session_state.your_friend = 0
    # st.session_state.date_expert = 0
    if st.session_state.chat_consultant == 0:
        chat_box.ai_say(
            [
                Markdown('Please give me a file or screen shot that contains the chat you want me to analysis so that I can give you some suggestion about how to reply!', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.chat_consultant += 1
        st.image('chat_history.jpg')
    # if image:
    #     chat_box.ai_say(
    #         [
    #             Markdown('File successfully uploaded!', 
    #                         in_expander=in_expander,
    #                         expanded=True, state='complete', title="CharmAI"),
    #         ]
    #     )

    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        if st.session_state.chat_consultant == 1:
            chat_box.ai_say(
                [
                    Markdown('Hi Andrew,<br>\
                            From your reply, Camila might think that you are not interested in her.<br>\
                            She brought the topic- He even wanted to ask me out 😡 seems like she wants to gain your attention and see your respond,<br>\
                            More aggressviely, this might be a chance to ask her out.', 
                                in_expander=in_expander,
                                expanded=True, state='complete', title="CharmAI"),
                ]
            )
            st.session_state.chat_consultant += 1
        else:
            chat_box.ai_say(
                [
                    Markdown('Practice makes perfect! Why not to use our <b>Role Play</b> mode to practice you communication skills?', 
                                in_expander=in_expander,
                                expanded=True, state='complete', title="CharmAI"),
                ]
            )

    # profile = Profile(introduction, api_key)
    # age, gender, career, personality, hobby = profile.returnProfile()
    # if len(chat_box.history) <= 4:
    #     career = 'unknown'
    # if len(chat_box.history) <= 8:
    #     personality, hobby = 'unknown', 'unknown'
    # LLM = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby), api_key)

    # if query := st.chat_input('Chat with CharmAI...'):
    #     chat_box.user_say(query)
    #     text, st.session_state.recording = LLM.chatConsultant(query, st.session_state.recording)
    #     chat_box.ai_say(
    #         [
    #             Markdown(text, in_expander=in_expander,
    #                         expanded=True, state='complete', title="CharmAI"),
    #         ]
    #     )
    # btns.download_button(
    #     "Export Markdown",
    #     "".join(chat_box.export2md()),
    #     file_name=f"chat_history.md",
    #     mime="text/markdown",
    # )

    # btns.download_button(
    #     "Export Json",
    #     chat_box.to_json(),
    #     file_name="chat_history.json",
    #     mime="text/json",
    # )

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
    # st.session_state.your_friend = 0
    # st.session_state.chat_consultant = 0
    if st.session_state.date_expert == 0:
        chat_box.ai_say(
            [
                Markdown('Please give me a file or screen shot that contains the chat you want me to analysis so that I can give you some suggestion about how to reply!', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.date_expert += 1
    profile = Profile(introduction, api_key)
    age, gender, career, personality, hobby = profile.returnProfile()


    # btns.download_button(
    #     "Export Markdown",
    #     "".join(chat_box.export2md()),
    #     file_name=f"chat_history.md",
    #     mime="text/markdown",
    # )

    # btns.download_button(
    #     "Export Json",
    #     chat_box.to_json(),
    #     file_name="chat_history.json",
    #     mime="text/json",
    # )

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
    # st.session_state.your_friend = 0
    # st.session_state.chat_consultant = 0
    # st.session_state.date_expert = 0
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
    # btns.download_button(
    #     "Export Markdown",
    #     "".join(chat_box.export2md()),
    #     file_name=f"chat_history.md",
    #     mime="text/markdown",
    # )

    # btns.download_button(
    #     "Export Json",
    #     chat_box.to_json(),
    #     file_name="chat_history.json",
    #     mime="text/json",
    # )

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
