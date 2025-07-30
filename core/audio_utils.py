from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
import tempfile

model = WhisperModel("base")

# use token from huggingface
HUGGINGFACE_TOKEN = ""
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=HUGGINGFACE_TOKEN)

def transcribe_with_diarization(audio_path):
    # Transcribe with whisper
    segments, _ = model.transcribe(audio_path, beam_size=5, language='en')

    diarization = pipeline(audio_path)

    results = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        text_segment = ""
        for segment in segments:
            if segment.start >= turn.start and segment.end <= turn.end:
                text_segment += segment.text + " "
        results.append({
            "speaker": speaker,
            "start": round(turn.start, 2),
            "end": round(turn.end, 2),
            "text": text_segment.strip()
        })

    return results
