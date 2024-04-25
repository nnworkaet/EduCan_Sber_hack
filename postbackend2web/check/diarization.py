import torch
from pyannote.audio import Pipeline


def diarizator(audio):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="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")

    # send pipeline to GPU (when available)
    pipeline.to(torch.device("cuda"))

    diarization = pipeline(audio)

    time_speak = []

    for turn, _, speaker in diarization.itertracks(yield_label=True):
        res_str = f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}"
        time_speak.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })

    return time_speak

