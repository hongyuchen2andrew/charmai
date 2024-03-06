from openai import OpenAI
import openai

def perplexity(prompt, perplexity_key):
    messages = [
        {
            "role": "system",
            "content": 
                "You are an artificial intelligence assistant and you need to "
                "give precise and accurate answer to the user.",
        },
        # {
        #     "role": "system",
        #     "content": 
        #         f"Your answer should follow the following format:{format}",
        # },
        {
            "role": "user",
            "content": (prompt),
        },
    ]

    client = OpenAI(api_key=perplexity_key, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-medium-online",
        messages=messages,
    )
    return response.choices[0].message.content

