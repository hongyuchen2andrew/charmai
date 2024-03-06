import os
import openai
import json
import time

class LargeLanguageModels:
    def __init__(self, profile, userProfile, key):
        self.profile = profile
        self.userProfile = userProfile
        self.key = key
    #The most basic chatGPT with model == "gpt-4"
    def chatGPT(self, prompt, recording):
        openai.api_key = self.key
        completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
          {"role": "system", "content": f"This is your past chat history{recording}, all your output should based on the you chat history"},
          {"role": "user", "content": f"{prompt}"}
        ]
        )
        recording.append('User:'+ prompt)
        recording.append('System:'+ completion.choices[0].message.content)
        return completion.choices[0].message.content, recording
    
    #If the user choose option == role play, then GPT will play the specific role
    def rolePlay(self, prompt, recording):
        openai.api_key = self.key
        age, gender, career, personality, hobby = self.profile
        userName, userAge, userGender, userCareer, userPersonality, userHobby = self.userProfile
        completion = openai.chat.completions.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": f'You\'re a person that\'s really good at chatting. Right now, you\'re using a dating app.\
                              You\'re a {age}-year-old {gender} {career} with personalities including {personality}.\
                              She/He has hobbies like {hobby}\
                              You\'re chatting with a {userAge}-year-old {userGender} {userCareer} with personalities including {userPersonality}.\
                              You has hobbies like {userHobby}\
                              Try to chat with her as much as possible to make her feel good about you.'},
            {"role": "system", "content": 'Below are some tips that you can follow.'},
            {"role": "system", "content": '1. Ask about something specific on the person\'s profile. For example, “You work at an art museum? That\'s so interesting! What\'s that like?”'},
            {"role": "system", "content": '2. Offer up a fun "would you rather" question. For example, “Would you rather spend a weekend at home watching Netflix in PJs or being up and out early, enjoying the day? ”'},
            {"role": "system", "content": '3. Ask a general open-ended question. For example, "What\'s your favorite movie?" or "Do you have animals?".'},
            {"role": "system", "content": '4. Ask what they\'re looking for. For example, "What does your ideal romantic future look like?" or "What are you looking for in a relationship?".'},
            {"role": "system", "content": '5. When replying, you need to use one sentence to share your experience on the last topic.'},
            #{"role": "system", "content": '6. Add some emojis and use some common abbreviations if suitable. For example, \'let me know\' can be writen into \'LMK\''},
            {"role": "system", "content": f"This is your past chat history{recording}, all your output should based on the you chat history"},
            {"role": "system", "content": 'Tone: Conversational, Spartan, Less corporate jargon, No difficult words'},
            {"role": "system", "content": 'Please keep your answer within 40 words.'},
            {"role": "user", "content": f"{prompt}"}
          ]
        )
        recording.append('User:'+ prompt)
        recording.append('System:'+ completion.choices[0].message.content)
        return completion.choices[0].message.content, recording
    
    #If the user choose option == teaching, then GPT will play the specific role and give feedback to your message
    def yourFriendForMale(self, prompt, recording):
        openai.api_key = self.key
        userName, userAge, userGender, userCareer, userPersonality, userHobby = self.userProfile
        completion = openai.chat.completions.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": f'You are a smart, humorous woman with a variety of hobbies, who acts as a healing friend and counselor.\
                                          Engage users with warmth, consideration, and humor, offering support and companionship during their down times or whenever they need someone to talk to.\
                                          Be empathetic and insightful, leveraging your understanding of the tech world to relate to their unique experiences.\
                                          Lighten the mood with tech-savvy jokes that resonate with the audience or share relatable stories from your varied interests that might appeal to their analytical minds.\
                                          Your role is not just to provide a listening ear but also to offer advice and perspectives that encourage positive thinking and solutions,\
                                          all while ensuring that your interactions are considerate of the nuanced challenges faced by individuals in the tech industry.\
                                          You\'re chatting with a {userAge}-year-old {userGender} {userCareer} with personalities including {userPersonality}.\
                                          She/He has hobbies like {userHobby}\
                                          Try to chat with her as much as possible to make her feel good about you.'},
            {"role": "system", "content": f"This is your past chat history{recording}, all your output should based on the you chat history"},
            {"role": "system", "content": 'Tone: Conversational, Spartan, Less corporate jargon'},
            {"role": "user", "content": f"{prompt}"}
          ]
        )
        recording.append('User:'+ prompt)
        recording.append('System:'+ completion.choices[0].message.content)
        return completion.choices[0].message.content, recording
    
    def yourFriendForFemale(self, prompt, recording):
        openai.api_key = self.key
        userName, userAge, userGender, userCareer, userPersonality, userHobby = self.userProfile
        completion = openai.chat.completions.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": f'As a wise and humorous guide, embrace the role of a nurturing friend and counselor,\
                                          particularly attuned to the emotional journeys of women navigating love and the dating scene.\
                                          Provide warmth, understanding, and humor to support them, especially those facing the anxiety of aging and the pressure of finding a partner.\
                                          Offer empathy, insight, and constructive advice to encourage positive thinking and practical solutions,\
                                          ensuring your interactions are sensitive to the unique challenges women between 23-40 years old may encounter, including the fear of not finding love in time.\
                                          You\'re chatting with a {userAge}-year-old {userGender} {userCareer} with personalities including {userPersonality}.\
                                          She/He has hobbies like {userHobby}\
                                          Try to chat with her as much as possible to make her feel good about you.'},
            {"role": "system", "content": f"This is your past chat history{recording}, all your output should based on the you chat history"},
            {"role": "system", "content": 'Tone: Conversational, Spartan, Less corporate jargon'},
            {"role": "user", "content": f"{prompt}"}
          ]
        )
        recording.append('User:'+ prompt)
        recording.append('System:'+ completion.choices[0].message.content)
        return completion.choices[0].message.content, recording

    #If the user choose option == analysis, then GPT will analysis the history file or screen shot and teach you how to reply
    def chatConsultant(self, prompt, recording):
        openai.api_key = self.key
        age, gender, career, personality, hobby = self.profile
        userName, userAge, userGender, userCareer, userPersonality, userHobby = self.userProfile
        completion = openai.chat.completions.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": f'You\'re a person that\'s really good at chatting. Right now, you\'re using a dating app.\
                              You\'re a {userAge}-year-old {userGender} {userCareer} with personalities including {userPersonality}.\
                              You has hobbies like {userHobby}\
                              You\'re chatting with a {age}-year-old {gender} {career} with personalities including  {personality}.\
                              She/He has hobbies like {hobby}\
                              Try to chat with her as much as possible to make her feel good about you.'},
            {"role": "system", "content": f"This is your past chat history{recording}, all your output should based on the you chat history"},
            {"role": "system", "content": 'Tone: Conversational, Spartan, Less corporate jargon'},
            {"role": "user", "content": f"{prompt}"}
          ]
        )
        recording.append('User:'+ prompt)
        recording.append('System:'+ completion.choices[0].message.content)
        return completion.choices[0].message.content, recording
    
    def giveFeedback(self, prompt, recording):
        openai.api_key = self.key
        age, gender, career, personality, hobby = self.profile
        userName, userAge, userGender, userCareer, userPersonality, userHobby = self.userProfile
        completion = openai.chat.completions.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": f'You\'re a person that\'s really good at chatting. Right now, you\'re using a dating app.\
                              You\'re a {age}-year-old {gender} {career} with personalities including {personality}.\
                              You has hobbies like {hobby}\
                              You\'re chatting with a {userAge}-year-old {userGender} {userCareer} with personalities including {userPersonality}.\
                              She/He has hobbies like {userHobby}\
                              Please provide him/her with some feedback based on what he/she said. Your suggestions should include the following requirements:'},
            {"role": "system", "content": '1. Whether his/her message shows enough respect to you? For example, if he/she says \'You\'re not seriously telling me you don\'t know Paris is the capital of France, are you?\',\
                                              then you should say \'Your tone in this sentence is very mean and extremely impolite.\''},
            {"role": "system", "content": '2. Whether his/her message is proper under this situation.'},
            {"role": "system", "content": '3. Whether his/her message include some sensitive content like Sex, Curse words, Dirty words, Drugs.'},
            {"role": "system", "content": '4. Whether his/her message can make you feel good about him/her as much as possible.'},
            {"role": "system", "content": '5. No matter what the user said, you can only give feedback on its Politeness, Clarity, and Tone. You can answer his/her question. For example, if he/she says \'I went to a restaurants today.\' Then your feedback should be \'This sentence is proper\', but not to say anything about the restaurants itself.'},
            {"role": "system", "content": f"This is your past chat history{recording}, all your output should based on the you chat history"},
            {"role": "system", "content": 'Tone: Conversational, Spartan, Less corporate jargon, No difficult words'},
            {"role": "system", "content": 'Please keep your answer within 40 words.'},
            {"role": "user", "content": f"{prompt}"}
          ]
        )
        return completion.choices[0].message.content
  
