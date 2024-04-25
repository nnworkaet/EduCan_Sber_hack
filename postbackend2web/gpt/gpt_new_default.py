from openai import OpenAI
#from .API.key import keys as keys_list
#from .API.key_change import shift_keys,del_key
from tenacity import retry, stop_after_attempt, wait_random_exponential,retry_if_not_exception_type,retry_if_result,TryAgain
import asyncio
import time
import importlib

keys = [
    "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",
    "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",
    "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",
]
def shift_list():
  global keys
  keys = keys[1:] + keys[:1]

def del_key_list():
   global keys
   keys = keys[1:]


@retry
def gpt( data, prompt):
   try:
       global keys
       client = OpenAI(api_key=keys[0])

       print('ждем')
       print(keys)
       chat_completion = client.chat.completions.create(
           messages=data+[{"role": "user","content": prompt}],
           model="gpt-3.5-turbo-1106",
       )

       return chat_completion.choices[0].message.content

   except Exception as e:
       print(f'OOOOOOASJDHWERROR ',e)
       if '401' in str(e):
           # Удалите ключ API из key.py
           del_key_list()

           time.sleep(0.5)
           raise TryAgain
       elif '429' in str(e):
           # Измените ключ API с помощью shift_keys()
           shift_list()

           time.sleep(0.5)
           raise TryAgain
       elif 'Why have I been blocked?' in str(e):
           print('ERROR: Меняй прокси')
           raise TryAgain
       else:

           raise TryAgain