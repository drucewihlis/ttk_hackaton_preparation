# pip install SpeechRecognition
import speech_recognition as sr

r = sr.Recognizer()

harvad = sr.AudioFile("03.03_19.wav")
with harvad as source:
    audio = r.record(source)
val = r.recognize_google(audio, language="ru").lower()

print(val, end='\n')