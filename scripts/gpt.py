import os
from dotenv import *
import openai

load_dotenv()
api_key = os.environ.get("key")
openai.api_key = api_key


def chatApiCall(prompt, tokens=200):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                f"content": prompt,
            },
        ],
        temperature=0,
        max_tokens=200,
    )


"write a summuray of the key enviromental points in 1 scentance, avoid using introductions like 'The key environmental points':{string}"
