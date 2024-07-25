import os
import httpx
from dotenv import load_dotenv
from openai import OpenAI

from config import PROXY

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
model_3 = "gpt-3.5-turbo-0125"
model_4 = "gpt-4-turbo"

if api_key is None:
    raise ValueError("Environment variable OPENAI_API_KEY isn't founded")


client = OpenAI(api_key=api_key,
                http_client=httpx.Client(
                    proxy=PROXY
                ))


instruction = ""


def request_to_gpt(request):
    completion = client.chat.completions.create(
        model=model_4,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": request}
        ]
    )

    response = completion.choices[0].message.content

    return response
