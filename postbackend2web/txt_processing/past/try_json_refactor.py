import json
import re




def wrap_keys_with_double_quotes(json_str):
    def wrap(match):
        # Проверяем, не является ли найденная группа двумя цифрами
        if match.group(1).isdigit() and len(match.group(1)) == 2:
            return f'{match.group(1)}:'
        else:
            return f'"{match.group(1)}":'

    # Уточненное регулярное выражение, исключающее две цифры в формате "число"
    pattern = r'"(\w+)"(?=:)"(?!\d{2})'
    corrected_json_str = re.sub(pattern, wrap, json_str)
    return corrected_json_str
def wrap_keys_with_double_quotes_old(json_str):
    # Ищем все вхождения "ключ:" и оборачиваем "ключ" в двойные кавычки
    def wrap(match):
        return f'"{match.group(1)}":'

    pattern = r'(\w+):'
    corrected_json_str = re.sub(pattern, wrap, json_str)
    return corrected_json_str

def str2list(str_ques):

        corrected_str_ques = wrap_keys_with_double_quotes(str_ques.replace('\n',""))
        print(f"After wrapped: {corrected_str_ques}")
        result_list = json.loads(corrected_str_ques)

        if isinstance(result_list, list) and all(isinstance(item, dict) for item in result_list):
            return result_list
        else:
            return ['BadType']




