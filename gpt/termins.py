from .gpt_new_default_db import gpt

from .gigaprompts.prompts import prompt_termins,template_termins

data=[{'role': 'system', 'content': '00:00:5.80 -00:00:11.36 Ролик получился достаточно длинный, поэтому перед началом давайте обговорим, что в этом ролике будет.'}, {'role': 'system', 'content': '00:00:11.36 - 00:00:16.44 В ходе ролика будем работать с REST API, спроектируем грамотную...'}]


def termins(data):
    return gpt(data,prompt_termins[0],template_termins)



