import speech_recognition as sr
import pyttsx3


engine = pyttsx3.init()
engine.setProperty("rate", 180)


def falar(texto: str):
    print(f"H.U.L.I (voz): {texto}")
    engine.say(texto)
    engine.runAndWait()


def ouvir():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎙️ Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {texto}")
        return texto.lower()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""