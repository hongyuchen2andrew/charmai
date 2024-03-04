import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json
from streamlit_modal import Modal
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder

from gpt import LargeLanguageModels
from profiles import Profile

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
    serName = st.session_state.userName

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
        ("Role Play", "Teaching", "Analysis"),
        index=None,
        placeholder="Select the mode...",
        )
    introduction = st.text_area(label = 'Description', placeholder = 'Please enter the description...')
    st.divider()

    btns = st.container()

    file = st.file_uploader(
        "chat history json",
        type=["json"]
    )
    # audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=41_000)
    # if audio_bytes:
    #     st.audio(audio_bytes, format="audio/wav")

    if st.button("Load Json") and file:
        data = json.load(file)
        chat_box.from_dict(data)

chat_box.init_session()
chat_box.output_messages()

if "role_play" not in st.session_state:
    st.session_state.role_play = 0
if "teach" not in st.session_state:
    st.session_state.teach = 0
if "analysis" not in st.session_state:
    st.session_state.analysis = 0

if option == "Role Play":
    st.session_state.analysis = 0
    st.session_state.teach = 0
    
    if st.session_state.role_play == 0:
        chat_box.ai_say(
            [
                Markdown('Please give me a breif description of the role you want me to play in the sidebar! Try to include some key information like age, gender, careers, and also personality.\
                         For example, She is a beautiful girl, currently 25 years old, pursuing a master\'s degree at UW. She enjoys skiing, singing, and hiking. She is cheerful, confident, and full of youthful energy.', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.role_play += 1
    if st.session_state.role_play >= 1:
        profile = Profile(introduction)
        age, gender, career, personality, hobby = profile.returnProfile()
        if len(chat_box.history) <= 4:
            career = 'unknown'
            userCareer = 'unknown'
        if len(chat_box.history) <= 8:
            personality, hobby = 'unknown', 'unknown'
            userHobby = 'unknown'
        LLM = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby))

        if query := st.chat_input('Chat with CharmAI...'):
            chat_box.user_say(query)
            text, st.session_state.recording = LLM.rolePlay(query, st.session_state.recording)
            chat_box.ai_say(
                [
                    Markdown(text, in_expander=in_expander,
                                expanded=True, state='complete', title="CharmAI"),
                ]
            )
    btns.download_button(
        "Export Markdown",
        "".join(chat_box.export2md()),
        file_name=f"chat_history.md",
        mime="text/markdown",
    )

    btns.download_button(
        "Export Json",
        chat_box.to_json(),
        file_name="chat_history.json",
        mime="text/json",
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

elif option == "Teaching":
    st.session_state.role_play = 0
    st.session_state.analysis = 0
    if st.session_state.teach == 0:
        chat_box.ai_say(
            [
                Markdown('Please give me a breif description of the person that you will chat in the sidebar with so that I can guide you how to efficiently communicate with them! Try to include some key information like age, gender, careers, and also personality.', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.teach += 1
    profile = Profile(introduction)
    age, gender, career, personality, hobby = profile.returnProfile()
    if len(chat_box.history) <= 4:
        career = 'unknown'
    if len(chat_box.history) <= 8:
        personality, hobby = 'unknown', 'unknown'
    LLM = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby))
    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        text, st.session_state.recording = LLM.teaching(query, st.session_state.recording)
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
    btns.download_button(
        "Export Markdown",
        "".join(chat_box.export2md()),
        file_name=f"chat_history.md",
        mime="text/markdown",
    )

    btns.download_button(
        "Export Json",
        chat_box.to_json(),
        file_name="chat_history.json",
        mime="text/json",
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

elif option == "Analysis":
    st.session_state.role_play = 0
    st.session_state.teach = 0
    if st.session_state.analysis == 0:
        chat_box.ai_say(
            [
                Markdown('Please give me a file or screen shot that contains the chat you want me to analysis so that I can give you some suggestion about how to reply!', 
                            in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
        st.session_state.analysis += 1
    profile = Profile(introduction)
    age, gender, career, personality, hobby = profile.returnProfile()
    if len(chat_box.history) <= 4:
        career = 'unknown'
    if len(chat_box.history) <= 8:
        personality, hobby = 'unknown', 'unknown'
    LLM = LargeLanguageModels((age, gender, career, personality, hobby), (userName, userAge, userGender, userCareer, userPersonality, userHobby))

    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        text, st.session_state.recording = LLM.analysis(query, st.session_state.recording)
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
    btns.download_button(
        "Export Markdown",
        "".join(chat_box.export2md()),
        file_name=f"chat_history.md",
        mime="text/markdown",
    )

    btns.download_button(
        "Export Json",
        chat_box.to_json(),
        file_name="chat_history.json",
        mime="text/json",
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

else:
    st.session_state.role_play = 0
    st.session_state.teach = 0
    st.session_state.analysis = 0
    profile = ''
    userProfile = ''
    LLM = LargeLanguageModels(profile, userProfile)
    if query := st.chat_input('Chat with CharmAI...'):
        chat_box.user_say(query)
        text, st.session_state.recording = LLM.chatGPT(query, st.session_state.recording)
        chat_box.ai_say(
            [
                Markdown(text, in_expander=in_expander,
                            expanded=True, state='complete', title="CharmAI"),
            ]
        )
    btns.download_button(
        "Export Markdown",
        "".join(chat_box.export2md()),
        file_name=f"chat_history.md",
        mime="text/markdown",
    )

    btns.download_button(
        "Export Json",
        chat_box.to_json(),
        file_name="chat_history.json",
        mime="text/json",
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
