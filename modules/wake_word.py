import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()

model = Model("model")

recognizer = KaldiRecognizer(model, 16000)


def callback(indata, frames, time, status):

    q.put(bytes(indata))


def ouvir():

    with sd.RawInputStream(samplerate=16000, blocksize = 8000, dtype='int16',
                           channels=1, callback=callback):

        while True:

            data = q.get()

            if recognizer.AcceptWaveform(data):

                texto = json.loads(recognizer.Result())

                return texto.get("text", "")