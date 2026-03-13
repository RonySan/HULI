import pyttsx3
import threading

falando_agora = False
_lock_fala = threading.Lock()


def esta_falando():
    return falando_agora


def falar(texto: str):
    global falando_agora

    with _lock_fala:
        try:
            falando_agora = True
            print(f"H.U.L.I (voz): {texto}")

            engine = pyttsx3.init()
            engine.setProperty("rate", 175)
            engine.setProperty("volume", 1.0)

            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)

            engine.say(texto)
            engine.runAndWait()
            engine.stop()

        except Exception as e:
            print(f"[ERRO VOZ] {e}")

        finally:
            falando_agora = False