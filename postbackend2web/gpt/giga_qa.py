from langchain_community.chat_models import GigaChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .apiGetter import api_getters
from .gigaprompts import QA_CREATOR, WRONG_A_GENERTOR, REGENERATOR_1
from .document_loaders import text_splitter
import ast
import asyncio
# from temp.tests import TEST_LEC


def regenerator(chunk, first_output):
    token = api_getters()["access_token"]
    print(f'\nНовый токен для регенирации:\n{token}')

    llm = GigaChat(access_token=token, verify_ssl_certs=False)
    regen_template = REGENERATOR_1
    regen_prompt = PromptTemplate.from_template(regen_template)

    regen_chain = LLMChain(llm=llm, prompt=regen_prompt)
    res = regen_chain.invoke({"chunk": chunk, "question": first_output})
    print(f"\nПосле регена:\n{res['text']}")

    return res['text']


def check_questions_and_answers(input_strings):
    questions_only = True
    for string in input_strings:
        if '?' not in string:
            questions_only = False
            break
    return not questions_only


def string_to_sets(string, chunk):
    final_qa_list = []
    if "\n" in string:
        substrings = string.split('\n')
        for substring in substrings:
            listed_string = ast.literal_eval(substring)
            if check_questions_and_answers(listed_string):
                final_qa_list.append(listed_string)
    else:
        listed_string = ast.literal_eval(string)
        if check_questions_and_answers(listed_string):
            final_qa_list.extend(listed_string)
        else:
            answers = regenerator(chunk, string)
            index = answers.find('[')
            subanswers = answers[index:]
            if "\n" in subanswers:
                listed_answers = ast.literal_eval(subanswers.replace("\n", ","))
                for i in range(len(listed_string)):
                    pair = [listed_string[i], listed_answers[i][0]]
                    final_qa_list.append(pair)
            else:
                listed_answers = ast.literal_eval(subanswers)

                for i in range(len(listed_string)):
                    pair = [listed_string[i], listed_answers[i]]
                    final_qa_list.append(pair)

    return final_qa_list


def string_to_sets_wa(string):
    pre_string = string.strip("[]")
    pre_string = pre_string.strip("''")
    if "','" in pre_string:
        segments = pre_string.split("','")
    elif "',\n'" in pre_string:
        segments = pre_string.split("',\n'")
    else:
        segments = pre_string.split("', '")
    return segments


def wa_validation(set_a, set_wa):
    new_set = []
    count = 0
    for segments_wa, segments_a in zip(set_wa, set_a):
        count += 1
        valid_segment = {f"question": segments_a[0], "variant1": segments_a[1], "variant2": segments_wa[0],
                         "variant3": segments_wa[1], "variant4": segments_wa[2], "answer": 'variant1'}
        new_set.append(valid_segment)

    valid_set = []
    for segm in new_set:
        if segm["variant1"] != segm["variant2"] != segm["variant3"]:
            valid_set.append(segm)

    return valid_set


def qa_generator(text):
    # Делим на чанки
    chunks = text_splitter(text)

    token = api_getters()["access_token"]
    print(f'Новый токен:\n{token}')
    llm = GigaChat(access_token=token, verify_ssl_certs=False)

    qa_creator_template = QA_CREATOR
    qa_creator_prompt = PromptTemplate.from_template(qa_creator_template)
    # Сет с вопросами и ответами для всех чанков
    qa_sets = []
    for chunk in chunks:
        qa_chain = LLMChain(llm=llm, prompt=qa_creator_prompt)
        answers = qa_chain.invoke({"chunk": chunk})
        if answers['text'].startswith(("Не люблю менять тему разговора",
                                       "Что-то в вашем вопросе меня смущает",
                                       "Как у нейросетевой языковой модели у меня не может быть настроения")):
            return {"status_code": 401, "Blacklisted chunk": chunk}

        print(f"\nВходной чанк:\n{answers['chunk']}\nОтвет llm:\n{answers['text']}\n")

        qa_sets.extend(string_to_sets(answers['text'], chunk))

    print(f"Отформатированное множество:\n{qa_sets}\n")
    wrong_answers_template = WRONG_A_GENERTOR
    wrong_answers_prompt = PromptTemplate.from_template(wrong_answers_template)

    worng_a_chain = LLMChain(llm=llm, prompt=wrong_answers_prompt)
    # Сет с неверными ответами
    wa_sets = []
    for qa in qa_sets:
        q = qa[0]
        a = qa[1]
        variant = worng_a_chain.invoke({"question": q, "answer": a})
        print(f"Входной вопрос:\n{variant['question']}\nОтвет: {variant['answer']}\nОтвет llm:\n{variant['text']}\n")
        wa = string_to_sets_wa(variant['text'])
        wa_sets.append(wa)
    print(f"Множество ответов:\n{wa_sets}\n\n")

    validated_test = wa_validation(qa_sets, wa_sets)
    print(validated_test)
    return str(validated_test)


# qa_generator(TEST_LEC)