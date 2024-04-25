import whisper
import torch

def seconds_to_hms(seconds):  # Подтягивает время
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.2f}"

def texter(audio):  # audio -> txt
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = whisper.load_model("small").to(device)         # ТУТ МОДЕЛЬ

    options = {
        "language": "ru",
        "task": "transcribe",
    }

    result = whisper.transcribe(model, audio, **options)
    result_subset = [{'text': segment['text'], 'start': segment['start'], 'end': segment['end']} for segment in result['segments']]

    strokes = []
    text_mas=[]
    for unit in result_subset:
        start_time = seconds_to_hms(float(unit['start']))
        end_time = seconds_to_hms(float(unit['end']))
        text = unit['text']
        stroke = f'{start_time} - {end_time}   {text}'
        strokes.append(stroke)
        text_mas.append(text)

    return strokes,text_mas


print(texter("audio1.mp3"))