import io
import os
from konlpy.tag import Okt

# Imports the Google Cloud client library
from google.cloud import speech

client = speech.SpeechClient()

# Loads the audio into memory
with io.open('test.wav', "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding='LINEAR16',
    language_code="ko-KR",
    sample_rate_hertz=44100,
    audio_channel_count=2,
    enable_automatic_punctuation=True
)

# Detects speech in the audio file
response = client.recognize(config=config, audio=audio)

text = ""
okt = Okt()
for idx, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print(okt.morphs(alternative.transcript))
# [END speech_quickstart]