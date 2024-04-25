from openai import OpenAI
from .API.key import keys as keys
import asyncio
def gpt(api_key,data,prompt):

    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=data+[{"role": "user","content": prompt}],
        model="gpt-3.5-turbo-1106",
    )

    #print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


