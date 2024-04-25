from .gpt_new_default_db import gpt
from .API.key import keys as keys
from .gigaprompts.prompts import prompt_test,template_test


def test(data):

    return gpt(data,prompt_test[0],template_test)

