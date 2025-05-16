import speech_recognition as sr

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"👂 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        print("⚠️ Speech service error.")
        return ""
