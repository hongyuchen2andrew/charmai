import google.generativeai as genai
from pathlib import Path
import PIL.Image
import json
import os
import streamlit as st

GEMINI_API_KEY =  st.secrets["GEMINI_API_KEY"]
genai.configure(api_key = GEMINI_API_KEY)

class Vision:
    def __init__(self, img):
        self.img = img

    #This is used for conversation between two persons 
    def chatHistoryScreenshot(self):

        model = genai.GenerativeModel('gemini-pro-vision')
        img = self.img
        response = model.generate_content(['This is a screenshot of the chatting history between the User and A. The messages shown in the right of the screenshot were sent by the user.\
                                            Please save the chatting history in the format like\
                                            chat_history = [\
                                                            {\
                                                                "sender": "User",\
                                                                "message": "How was your weekend?",\
                                                                "timestamp": "9:35 PM"\
                                                            },\
                                                            {\
                                                                "sender": "A",\
                                                                "message": "It was just ok. I went to my friend\'s bd party.",\
                                                                "timestamp": "9:36 PM"\
                                                            }].', img])
        result = response.text
        while (not '[' in result ) and (not ']' in result ): 
            result = response.text

        position_1 = result.index('[')
        position_2= result.index(']')
        result2 = result[position_1:position_2+1]
        result3 = result2.replace('\n        ', '').replace('\n    ', '').replace('\n', '')

        chat_history_list = eval(result3)
        return chat_history_list
    
# gemini = Vision('chat_history.jpg', 'jpg')
# print(gemini.chatHistoryScreenshot())
