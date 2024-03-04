import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from bokeh.models.widgets import Button

background = """
                <style>
                body {
                    background-color: #f0f2f6; /* 设置背景颜色 */
                    background-size: cover; /* 调整背景图像的大小以覆盖整个屏幕 */
                }
                </style>
             """
st.markdown(background, unsafe_allow_html=True)
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

st.markdown("<h1 style='color:pink; font-size: 80px; text-align:center; margin-top: -40px'>CharmAI</h1>", unsafe_allow_html=True) 
st.markdown("<h2 style='color:lightskyblue; font-size: 40px; text-align:left; margin-top: -20px'>About</h2>", unsafe_allow_html=True) 
st.markdown("<h3 style='color:grey; font-size: 20px; text-align:left; margin-top: -20px'>About</h3>", unsafe_allow_html=True) 

if st.button("Quick start"):
    switch_page("Chatbot")

if st.button("Tutorial"):
    switch_page("Tutorial")

if st.button("Complete your profile"):
    switch_page("Account")