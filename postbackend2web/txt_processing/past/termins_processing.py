from gpt.gpt_default import gpt
from gpt.API.key import keys as keys
from gpt.prompts.prompts import prompt_termins
from txt_processing.pre.allocate_token_text import allocate
from txt_processing.pre.sentence_maker import sentense
from .try_json_refactor import str2list
def post_gpt_termins(data, count=0):

    text_new = allocate(data)
    text_new = [{"role": "system", "content": fragment} for fragment in text_new]

    return gpt(keys[0],text_new,prompt_termins[1])

def termins_processing(txt, count=0):
    if count >= 10:
        return ['Exceeded attempts']

    result = post_gpt_termins(txt)

    result = str2list(result)
    if result != ['BadType']:
        return result
    else:
        count += 1
        return post_gpt_termins(txt, count)
def termins_processing_old(txt):
    result = post_gpt_termins(txt)
    return result
