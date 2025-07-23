import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(f"[Assistant]: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error with pyttsx3: {e}")
