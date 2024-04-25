from gpt.gpt_default import gpt

from gpt.API.key import keys as keys
from gpt.prompts.prompts import prompt_test
from txt_processing.pre.allocate_token_text import allocate
from txt_processing.pre.sentence_maker import sentense
from .try_json_refactor import str2list

def post_gpt_test(data,count=0):
    text_new = allocate(data)

    text_new = [{"role": "system", "content": fragment} for fragment in text_new]

    return gpt(keys[0],text_new,prompt_test[1])

def test_post_process(txt, count=0):
    if count >= 10:
        return ['Exceeded attempts']

    #result = post_gpt_test(txt)
    result = str2list(txt)
    if result != ['BadType']:
        return result
    else:
        count += 1
        return test_post_process(txt, count)

