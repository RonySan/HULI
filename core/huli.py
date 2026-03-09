import time
import threading
from datetime import datetime

from modules.identity import HULIIdentity
from modules.commands import processar_comando
from modules.memory import HULIMemory
from modules.voice import ouvir, falar


def monitor_lembretes(stop_event: threading.Event):
    memoria = HULIMemory()

    while not stop_event.is_set():
        try:
            memoria.carregar()
            pendentes = memoria.listar_lembretes_pendentes()
            agora = datetime.now()

            for lembrete in pendentes:
                quando_str = lembrete.get("quando")
                if not quando_str:
                    continue

                try:
                    quando_dt = datetime.strptime(quando_str, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue

                if agora >= quando_dt and not lembrete.get("executado", False):
                    texto = f"Rony, lembrete: {lembrete['conteudo']}"
                    print(f"\nH.U.L.I: 🔔 {texto}\n")
                    falar(texto)
                    memoria.marcar_lembrete_executado(lembrete.get("id"))
                    print("Aguardando comando...\n")
        except Exception:
            pass

        time.sleep(1)


def iniciar():
    identidade = HULIIdentity()

    print(identidade.apresentar())
    falar(identidade.apresentar())

    print("H.U.L.I iniciado.")
    print("Aguardando comando...")

    stop_event = threading.Event()
    t = threading.Thread(target=monitor_lembretes, args=(stop_event,), daemon=True)
    t.start()

    while True:
        modo = input("Digite [1] texto ou [2] voz: ").strip()

        if modo == "2":
            comando = ouvir()
            if not comando:
                print("H.U.L.I: Não consegui entender.")
                falar("Não consegui entender.")
                continue
        else:
            comando = input("Você: ").strip().lower()

        resposta = processar_comando(comando)

        if resposta == "ENCERRAR":
            print("H.U.L.I: Encerrando operações. Até logo, Rony.")
            falar("Encerrando operações. Até logo, Rony.")
            stop_event.set()
            break

        if resposta == "":
            continue

        print(f"H.U.L.I: {resposta}")
        falar(resposta)


if __name__ == "__main__":
    iniciar()