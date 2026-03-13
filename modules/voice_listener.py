import os
import re
import tempfile

import numpy as np
import scipy.io.wavfile as wav
import sounddevice as sd
from openai import OpenAI

client = OpenAI()

CORRECOES_FRASES = {
    "que hora e sao": "que horas sao",
    "que hora e são": "que horas sao",
    "que horas e sao": "que horas sao",
    "que idade sao": "que horas sao",
    "que idade são": "que horas sao",
    "que horas": "que horas sao",
    "horas sao": "que horas sao",
    "listar programa": "listar programas",
    "lista programa": "listar programas",
    "abre navegador": "abrir navegador",
    "abre edge": "abrir edge",
    "abre chrome": "abrir chrome",
    "abre vscode": "abrir vscode",
}


def gravar_audio(duracao=5, fs=16000):
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()

    volume = np.abs(audio).mean()
    if volume < 120:
        return None

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp.name, fs, audio)
    return temp.name


def transcrever_audio(caminho):
    if not caminho:
        return ""

    with open(caminho, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=f,
            language="pt",
            prompt=(
                "O áudio está em português do Brasil. "
                "O usuário vai falar comandos curtos como: "
                "'abrir navegador', 'abrir vscode', 'que horas sao', "
                "'status', 'ajuda', 'listar programas', 'sair'."
            ),
        )

    try:
        os.unlink(caminho)
    except Exception:
        pass

    return transcript.text.lower().strip()


def limpar_comando(texto):
    texto = texto.lower().strip()
    texto = re.sub(r"[^\w\sáàâãéêíóôõúç]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    if texto in CORRECOES_FRASES:
        texto = CORRECOES_FRASES[texto]

    return texto


def ouvir_um_comando():
    try:
        caminho = gravar_audio(duracao=5)
        texto = transcrever_audio(caminho)

        if not texto:
            return ""

        return limpar_comando(texto)

    except Exception as e:
        print("❌ erro no reconhecimento:", e)
        return ""