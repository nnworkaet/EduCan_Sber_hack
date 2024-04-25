import requests
from .urls2serv import url_for_server
from .types_of_requests import transcription, glossary, test,summary
import os
import time
def trans2serv(identity,txt,text_time):

    url = url_for_server
    post_data = transcription
    post_data["identity"] = identity
    post_data["text"] = txt
    post_data["textTime"] = text_time

    get_params = {
        'appendTranscriptionText': ''
    }

    # Sending the request
    response = requests.post(url, data=post_data, params=get_params)
    print(response.text)

def glos2serv(identity,txt):

    url = url_for_server
    post_data = glossary
    post_data["identity"] = identity
    post_data["text"] = txt


    get_params = {
        'appendGlossaryText': ''
    }

    # Sending the request
    response = requests.post(url, data=post_data, params=get_params)
    print(response.text)

def sum2serv(identity,txt,path_to_docs):
    url = url_for_server
    post_data = summary
    post_data["identity"] = identity
    post_data["text"] = txt



    get_params = {
        'appendSummary': ''
    }

    with open(path_to_docs, 'rb') as file:
        files = {'file': file}
        # Ваш код для отправки файла и дальнейших операций
        response = requests.post(url, data=post_data, params=get_params, files=files)



    time.sleep(3)
    if os.path.exists(path_to_docs):
        os.remove(path_to_docs)
        print(f"Файл {path_to_docs} успешно удален.")
    else:
        print(f"Файл {path_to_docs} не существует.")
    print(response.text)

def test2serv(identity,txt):

    url = url_for_server
    post_data = test
    post_data["identity"] = identity
    post_data["text"] = txt


    get_params = {
        'appendTestText': ''
    }

    # Sending the request
    response = requests.post(url, data=post_data, params=get_params)
    print(response.text)
