import streamlit as st
from streamlit_chatbox import *

from perplexity import perplexity

chat_box = ChatBox()
chat_box.init_session()
chat_box.output_messages()

format = '**Name of the hot pot**\
          Description:\
          Price:\
          Location:'

if query := st.chat_input('Chat with CharmAI...'):
    chat_box.user_say(query)
    text  = perplexity(query, format)
    chat_box.ai_say(
        [
            Markdown(text, expanded=True, state='complete', title="CharmAI"),
        ]
    )