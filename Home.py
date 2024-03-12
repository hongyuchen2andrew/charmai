import streamlit as st
import base64
from streamlit_extras.switch_page_button import switch_page
import os

st.session_state.api_key = st.secrets["API_KEY"]
st.session_state.perplexity_key = st.secrets["PERPLEXITY_KEY"]
st.session_state.google_key = st.secrets["GOOGLE_KEY"]
st.session_state.llama_key = st.secrets["LLAMA_KEY"]
st.session_state.langChain_key = st.secrets["LANGCHAIN_KEY"]
st.session_state.gemini_key = st.secrets["GEMINI_API_KEY"]

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
bin_str = get_base64("back4.jpg")
background = """
                <style>
                .stApp {
                    background-image: url("data:image/png;base64,%s");
                    background-size: cover; /* 调整背景图像的大小以覆盖整个屏幕 */
                }
                </style>
             """% bin_str
st.markdown(background, unsafe_allow_html=True)
st.markdown(
    """
    <style>
    .fixed-box {
        position: fixed; /* 将框固定在页面上方 */
        top: 0; /* 距离页面顶部位置 */
        width: 50%; /* 宽度占满整个页面 */
        height: 205px;
        padding: 10px; /* 内边距 */
    }
    </style>
    <p style='font: serif; text-shadow: 2px 2px 4px #c1e6f5; color: #4abded; font-size: 130px; text-align:center; margin-bottom: -20px; margin-top: -80px'><b>CharmAI</b></p>
    """
    , unsafe_allow_html=True
)

# 添加固定框内容
st.markdown(
    """
    <div style='border: 2px solid #ebf6fc; height: 300px; margin-bottom: 40px; border-radius: 20px; padding: 10px; background-color: rgba(255, 255, 255, 0.45);'>
        <h2 style='color: black;'>About</h2>
        <p style='font: serif; font-size: 22px;'><b>CharmAI</b> is a cutting-edge GenAI-powered chatbot designed to navigate you through the dating journey,\
            offering expert advice and consultation, while also as a supportive friend during love's challenging moments.<br>\
            <b>CharmAI</b> is your personal love consultant and friend, accompany you every step of the way to find love!</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
        <style>
        .stButton > button {
            height: 60px;
            width: 200px;
            padding-top: 10px !important;
            padding-bottom: 10px !important;
        }
        </style>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([2.3,1])
with col1:
    if st.button("Let's start!"):
        switch_page("Account")

with col2:
    if st.button("Tutorial"):
        switch_page("Tutorial")


# 在侧边栏添加小部件和内容
st.sidebar.title("Contact us")
st.sidebar.header("Email")
st.sidebar.write("chenhongyuXXXX@gmail.com")
st.sidebar.header("Phone")
st.sidebar.write("(+1) 206-3XX-0XXX")
st.sidebar.header("Address")
st.sidebar.write("University of Washington")
st.sidebar.header("LinkedIn")
st.sidebar.write("https://www.linkedin.com/in/hongyuchenuw/")
