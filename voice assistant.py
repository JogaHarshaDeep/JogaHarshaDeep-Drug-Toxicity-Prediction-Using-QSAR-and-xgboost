import speech_recognition as sr
import wikipedia
import pyttsx3
engine = pyttsx3.init()
language = "en"

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)

result = wikipedia.summary(audio, sentences=2)
print(result)
engine.say(result)
engine.runAndWait()
    