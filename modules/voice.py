import pyttsx3
import speech_recognition as sr
import re


def falar(texto: str):
    try:
        print(f"H.U.L.I (voz): {texto}")

        engine = pyttsx3.init()
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)

        engine.say(texto)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print(f"[ERRO VOZ] {e}")


def limpar_texto_voz(texto: str) -> str:
    texto = texto.lower().strip()

    # normalização de variações comuns da palavra "huli"
    ativacoes_erradas = [
        "rolê",
        "role",
        "rule",
        "ruli",
        "vôlei",
        "volei",
        "hully",
        "hully",
    ]

    for termo in ativacoes_erradas:
        if texto.startswith(termo + " "):
            texto = texto.replace(termo, "huli", 1)

    # correções simples de comandos comuns
    correcoes = {
        "listar programa": "listar programas",
        "lista programa": "lista programas",
        "abre navegador": "abrir navegador",
        "abre edge": "abrir edge",
        "abre ajuda": "ajuda",
    }

    if texto in correcoes:
        texto = correcoes[texto]

    return texto


def ouvir():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎙️ Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        texto = limpar_texto_voz(texto)
        print(f"Você disse: {texto}")
        return texto.lower()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""