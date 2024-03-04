import os
import openai
import json
import time

class Profile:
    def __init__(self, prompt, api_key):
        self.prompt = prompt
        self.api_key = api_key
        # self.age = 'unknown'
        # self.gender = 'unknown'
        # self.career = 'unknown'
        # self.personality = 'unknown'
        # self.hobby = 'unknown'
        # self.situation = 'unknown'
        self.max_try = 0

    def questionAnswering(self, question, answer_format):
        openai.api_key = self.api_key
        completion = openai.chat.completions.create(
        model="gpt-4",
        messages=[
          {"role": "system", "content": f'You\'re a bot that\'s really good at answering questions based on the information user given.'},
          {"role": "system", "content": f'You should answer the following question based on the prompt user input:{question}'},
          {"role": "system", "content": f'Your answer should follow the format:{answer_format}'},
          {"role": "system", "content": f'Your answer must strictly follow the format mentioned above.'},
          {"role": "user", "content": f"{self.prompt}"}
        ]
        )
        return completion.choices[0].message.content

    def getAge(self):
        question = 'What is the age?'
        answer_format = 'Age should be an integer, you can only return an integer.\
                         For example, return 15 but not he is 15 years old.'
        age = self.questionAnswering(question, answer_format)
        try:
            age = int(age)
            self.max_try = 0
            return age
        except:
            age = self.questionAnswering(question, answer_format)
            self.max_try += 1
            if self.max_try == 5:
                return 'unknown'

    def getGender(self):
        question = 'What is the gender of the person that was mentioned in the prompt?'
        answer_format = 'Although gender can not only be female or male, please return a single word.\
                         For example, return \'male\' \'female\' or \'non-binary\'.'
        gender = self.questionAnswering(question, answer_format)
        if len(gender.split(' ')) <= 4:
            self.max_try = 0
            return gender
        else:
            gender = self.questionAnswering(question, answer_format)
            self.max_try += 1
            if self.max_try == 5:
                return 'unknown'
        return gender

    def getCareer(self):
        question = 'What is the career of the person that was mentioned in the prompt?'
        answer_format = 'Career should strictly less than ten English words.\
                         If it has more than ten words, please return the most important ten keywords.\
                         For example, return \'student\' or \'machine learning engineer\'.'
        career = self.questionAnswering(question, answer_format)
        if len(career.split(' ')) <= 10:
            self.max_try = 0
            return career
        else:
            career = self.questionAnswering(question, answer_format)
            self.max_try += 1
            if self.max_try == 5:
                return 'unknown'
            
    def getPersonality(self):
        question = 'What are the personalities of the person that was mentioned in the prompt?'
        answer_format = 'You can only return at most five personality related keywords which are seperated by a comma. \
                        If there is less than five personalities, just return them. \
                        Please not output a whole sentence or even a paragraph.\
                        For example, return \'outgoing, humour\''
        personality = self.questionAnswering(question, answer_format)
        if len(personality.split(',')) <= 5:
            self.max_try = 0
            return personality
        else:
            personality = self.questionAnswering(question, answer_format)
            self.max_try += 1
            if self.max_try == 5:
                return 'unknown'
            
    def getHobby(self):
        question = 'What are the hobbies of the person that was mentioned in the prompt?'
        answer_format = 'You can only return at most five hobby related keywords which are seperated by a comma.\
                         If there is less than five hobbies, just return them.\
                         Please not output a whole sentence or even a paragraph.\
                         For example, return \'swim, reading, video games.\''
        hobby = self.questionAnswering(question, answer_format)
        if len(hobby.split(',')) <= 5:
            self.max_try = 0
            return hobby
        else:
            hobby = self.questionAnswering(question, answer_format)
            self.max_try += 1
            if self.max_try == 5:
                return 'unknown'

    def returnProfile(self):
        age = self.getAge()
        gender = self.getGender()
        career = self.getCareer()
        personality = self.getPersonality()
        hobby = self.getHobby()

        return age, gender, career, personality, hobby

# introduction = 'Hi, my name is Andrew. I have lived in China for 20 years. Last year, I went to MIT for my master degree. So as you can see, I am twenty one years old\
#                 I love coding, playing basketball, singing, going hiking. Nice to meet you.'  
# p = Profile(introduction)
# age, gender, career, personality, hobby = p.returnProfile()
# print('age:', age)
# print('gender:', gender)
# print('career:', career)
# print('personality:', personality)
# print('hobby:', hobby)
