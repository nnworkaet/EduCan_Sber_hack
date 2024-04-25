from pydub import AudioSegment
import math
import os
from openai import OpenAI
import random
from gpt.db.db import Database
import requests
import re


def remove_timestamps(text):
    # Создаем регулярное выражение для поиска временных меток
    pattern = r'\d{2}:\d{2}:\d{2}\.\d{3} - \d{2}:\d{2}:\d{2}\.\d{3}'

    # Заменяем найденные временные метки на пустую строку
    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text
def downloadin(url):
    file_extension = '.mp3'  # Example .wav
    r = requests.get(url)

    # If extension does not exist in end of url, append it
    if file_extension not in url.split("/")[-1]:
        filename = f'{url}{file_extension}'
    # Else take the last part of the url as filename
    else:
        filename = url.split("/")[-1]

    with open(filename, 'wb') as f:
        # You will get the file in base64 as content
        f.write(r.content)
    return filename
def split_audio(input_file, output_folder, chunk_size_mb=25):
    file_name=downloadin(input_file)
    print(file_name)
    import time
    time.sleep(1)
    if os.path.exists(file_name):
        if os.access(file_name, os.R_OK):
            print("File has read permissions")
        else:
            print("File does not have read permissions")
    else:
        print("File does not exist")

    audio = AudioSegment.from_file(file_name)

    chunk_size_bytes = chunk_size_mb * 1024 * 1024
    num_chunks = math.ceil(len(audio) / chunk_size_bytes)

    chunks = [audio[i * chunk_size_bytes:(i + 1) * chunk_size_bytes] for i in range(num_chunks)]

    output_files = []
    for i, chunk in enumerate(chunks):
        output_file = os.path.join(output_folder, f'chunk_{i+1}.mp3')
        chunk.export(output_file, format="mp3")
        output_files.append(output_file)
    os.remove(file_name)
    return output_files

def res_stroke_output(segments):
    strokes = []
    for segment in segments:
        res_stroke = f'{segment["time"]}    {segment["text"]}'
        strokes.append(res_stroke)
    return strokes

def segmentator(text):
    segments = []
    for row in text.split('\n\n'):
        parts = row.split('\n')
        if len(parts) == 3:
            segments.append({
                'number': parts[0],
                'time': parts[1].replace(' --> ', ' - ').replace(',', '.'),
                'text': parts[2]
            })
    return segments

def texter(audio):
    db = Database()
    keys = db.read_active()
    if keys != 'No keys':
        key = keys[random.randint(0, (len(keys) - 1))]
        db.create_log("API", f"Api keys закончились")
        db.change_time(key)
        if len(keys) <= 1:
            db.create_log("API", f"{len(keys)} Api keys осталось")
    else:
        while keys == "No keys":
            keys = db.read_active()
        key = keys[random.randint(0, (len(keys) - 1))]
        db.change_time(key)
    client = OpenAI(api_key=key)

    output_folder = 'chunks'
    os.makedirs(output_folder, exist_ok=True)

    chunk_files = split_audio(audio, output_folder)

    res_strokes = []
    for chunk_file in chunk_files:
        with open(chunk_file, "rb") as chunk_audio:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=chunk_audio,
                response_format='srt'
            )

            res_strokes.extend(res_stroke_output(segmentator(transcript)))

    return [res_strokes,remove_timestamps(' '.join(res_strokes))]
#print(texter("a.mp3"))
