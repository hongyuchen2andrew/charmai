import json
import re
import string
import openai
from serpapi import GoogleSearch
from perplexity import perplexity

from profiles import Profile
from gpt import LargeLanguageModels

def locationResults(prompt, google_key):
    params = {
    "engine": "google_maps",
    "q": prompt,
    "api_key": google_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    try:
        local_results = results["local_results"]
    except:
        local_results = 'unknown'
    return local_results

def formatAnswer(prompt, place, openai_key):
    openai.api_key = openai_key
    completion = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"Please extract the name of the {place} in the prompt and save them in a python list."},
        {"role": "user", "content": f"{prompt}"}
    ]
    )
    return completion.choices[0].message.content

def restaurantRecommendation(prompt, openai_key, google_key, perplexity_key):
    profile = Profile(prompt, openai_key)
    question = 'What kinds of restaurants this person may like?'
    format = 'A specific kind of restaurant like Korean restaurant, Chinese restaurant, hot pot, and so on.'
    restaurant = profile.questionAnswering(question, format)
    prompt_perplexity = f'recommend 10 {restaurant} in Seattle'
    result = perplexity(prompt_perplexity, perplexity_key)
    while (not '[' in result ) and (not ']' in result ): 
        result = formatAnswer(result, restaurant, openai_key)
    position_1 = result.index('[')
    position_2= result.index(']')
    result = result[position_1+1:position_2].split(', ')
    punctuation = string.punctuation
    Result = []
    for i in result:
        i = i.replace("\n", "")
        i = i.strip()
        i = i.translate(str.maketrans('', '', punctuation))
        prompt = f'{i} in Seattle'
        recommendation = locationResults(prompt, google_key)
        if recommendation == 'unknown':
            continue
        else:
            Result.append(recommendation)
    return Result

# openai_key = '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'
# prompt = '1.Dive-in movie adventure: Considering her love for movies, arrange a special \'outdoor\' movie experience. There are services that offer inflatable movie screens for hire that you can set-up in your backyard. Make sure to choose a movie that she likes or a popular romantic movie. Don\'t forget the popcorn and cozy blankets!\
#           2.Outdoor yoga activity: Since she likes yoga, having a yoga session in the park would be a good idea. You can hire a professional instructor for this private session. This can be both a fun and calming experience.'
# recommendation = recommend(prompt, openai_key)


# r = skiRecommendation(prompt, openai_key)
# print(r)

# place = 'Japanese restaurants'
# city = 'Seattle'
# prompt_perplexity = f'recommend 10 {place} in {city}'
# result = perplexity(prompt_perplexity)
# while (not '[' in result ) and (not ']' in result ): 
#     result = formatAnswer(result, place, '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')

# position_1 = result.index('[')
# position_2= result.index(']')
# result = result[position_1+1:position_2].split(', ')
# print(result)
# name = ['restaurant', 'park', 'cinema', 'ski', 'museum']
# info = ['Name', 'Address', 'Phone', 'Website', 'Link',]
# for place in recommendation:
#     for rec in place:
#         if rec == 'unknown':
#             continue
#         for r

# for recommendation in r:
#     # prompt = f'{i} in Seattle'
#     # recommendation = locationResults(prompt)
#     if recommendation == 'unknown':
#         continue
#     else:
#         print(recommendation[0])
#     try:
#         title = recommendation[0]['title']
#         print('Name: ', title)
#     except:
#         print('Name: ', 'unknown')

#     try:
#         address = recommendation[0]['address']
#         print('Address: ', address)
#     except:
#         print('Address: ', 'unknown')

#     try:
#         phone = recommendation[0]['phone']
#         print('Phone: ', phone)
#     except:
#         print('Phone: ', 'unknown')

#     try:
#         website = recommendation[0]['website']
#         print('Website: ', website)
#     except:
#         print('Website: ', 'unknown')

#     try:
#         link = recommendation[0]['link']
#         print('Link: ', link)
#     except:
#         print('Link: ', 'unknown')


    # print('Address: ', result[0]['address'])
    # print('Phone: ', result[0]['phone'])
    # print('Website: ', result[0]['website'])
    # print('Link: ', result[0]['link'])
