from faster_whisper import WhisperModel
import torch
import random
import string

print(torch.cuda.is_available())
def seconds_to_hms(seconds):  # Подтягивает время
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"

def audio_to_text(audio):

    model_size = "small"
    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio, beam_size=5, language='ru')
    name=generate_random_name()
    file_result = open(name, 'w', encoding='utf-8')

    txt_result = []
    onl_txt = []
    for segment in segments:
        start_time = seconds_to_hms(float(segment.start))
        end_time = seconds_to_hms(float(segment.end))
        text = segment.text
        onl_txt.append(text)
        stroke = f'{start_time} - {end_time}    {text}'
        txt_result.append(stroke)


    file_result.write(str(txt_result))
    file_result.write(str(onl_txt))
    print(txt_result,onl_txt)
    return [txt_result, onl_txt]
def generate_random_name():
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    return random_name + ".txt"


#print(audio_to_text("audio1.mp3"))

