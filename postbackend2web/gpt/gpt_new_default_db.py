from openai import OpenAI
import openai
#from .API.key import keys as keys_list
#from .API.key_change import shift_keys,del_key
from tenacity import retry, stop_after_attempt, wait_random_exponential,retry_if_not_exception_type,retry_if_result,TryAgain
import asyncio
import time
import importlib
from .db.db import Database
import random
import httpx
import httpx_socks
from fake_useragent import UserAgent
from .db.tg import send_message_to_users
import json

@retry
def gpt( data, prompt,template_json):
   db=Database()
   try:
       #что если не будет свободных ключей?
       print('aaasfs')
       keys=db.read_active()
       if keys!='No keys':
           key=keys[random.randint(0, (len(keys)-1))]
           db.create_log("API", f"Api keys закончились")
           db.change_time(key)
           if len(keys)<=1:
               db.create_log("API", f"{len(keys)} Api keys осталось")
       else:
           while keys=="No keys":
               keys = db.read_active()
           key = keys[random.randint(0, (len(keys) - 1))]
           db.change_time(key)


       print('Wait...Keys:',keys)


       proxies=db.read_active_proxy()
       if proxies!='No proxies':
           proxy=proxies[random.randint(0, (len(keys)-1))]

           if len(proxies)<2:
               db.create_log("proxy",f"{len(proxies)} Proxy осталось")

       else:
           db.create_log("proxy","Proxy ЗАКОНЧИЛИСЬ!!!")

       ua = UserAgent()
       user_agent = str(ua.chrome)
       headers = {'User-Agent': user_agent}

       if proxy[2]=='socks5':
           if proxy[1]=='None':
               proxy_use="socks5://"+proxy[0]
              #Дальше прикрепить если с паролем прокси
           else:

               proxy_use="socks5://"+proxy[1]+"@"+ proxy[0]
           transport = httpx_socks.SyncProxyTransport.from_url(proxy_use)
           http_client = httpx.Client(transport=transport, headers=headers)
       elif proxy[2]=='https':
           if proxy[1] == 'None':
               proxy_use = "http://" + proxy[0]
           # Дальше прикрепить если с паролем прокси
           else:

               proxy_use = "http://" + proxy[1] + "@" + proxy[0]

           http_client = httpx.Client(proxies=proxy_use, headers=headers)
       print(proxy_use)
       client = OpenAI(api_key=key, http_client=http_client)

       if template_json!='None':

           chat_completion = client.chat.completions.create(
               messages=[
               {"role": "system","content": "Provide output in valid JSON. The data schema should be like this: "+ json.dumps(template_json)
                }]+data+[{"role": "user","content": prompt}],
               model="gpt-3.5-turbo-1106",
               response_format={"type": "json_object"},
           )
           res=chat_completion.choices[0].message.content
           print(res)
           print("TYPE +++++++",type(res))
           res="["+res[16:-1].replace("/t","")
           print(res)

           return res
       else:
           chat_completion = client.chat.completions.create(
               messages=data + [{"role": "user", "content": prompt}],
               model="gpt-3.5-turbo-1106",
           )
           return chat_completion.choices[0].message.content

   except Exception as e:
       print(f'Exception: ',e)
       if '401' in str(e):

           db.change_state(key,"0")
           raise TryAgain
       elif '429' in str(e):

           db.turn_off_30(key)
           raise TryAgain
       elif 'Why have I been blocked?' in str(e):
           db.change_state_proxy(proxy[0],"0")
           print('Exception: прокси dead')
           raise TryAgain
       else:

           raise TryAgain