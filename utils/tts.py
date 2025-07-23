from gtts import gTTS
import os
from playsound import playsound

def speak(text):
    print(f"[Assistant]: {text}")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")
    except Exception as e:
        print(f"Error with gTTS: {e}")
