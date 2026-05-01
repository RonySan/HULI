import speech_recognition as sr

ATIVACOES = ["huli", "ruli", "rule", "role", "holy", "holi", "uli"]


def ouvir_natural(timeout=8, phrase_time_limit=8):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎙️ Fale naturalmente...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            texto = recognizer.recognize_google(audio, language="pt-BR").lower().strip()
            return texto
        except Exception:
            return ""


def ouvir_com_ativacao(timeout=8, phrase_time_limit=8):
    texto = ouvir_natural(timeout=timeout, phrase_time_limit=phrase_time_limit)

    if not texto:
        return ""

    palavras = texto.split()
    if not palavras:
        return ""

    if palavras[0] in ATIVACOES:
        return " ".join(palavras[1:]).strip()

    return ""