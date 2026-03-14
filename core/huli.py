import time
import threading
from datetime import datetime

from modules.identity import HULIIdentity
from modules.commands import processar_comando
from modules.memory import HULIMemory
from modules.voice import falar
from modules.voice_listener import ouvir_um_comando
from modules.scheduler import verificar_agendamentos


encerrar_programa = False


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

        except Exception:
            pass

        time.sleep(1)


def executar_comando(comando: str):
    global encerrar_programa

    if not comando:
        return

    comando_limpo = comando.strip().lower()

    if comando_limpo in ["sair", "encerrar", "fechar huli"]:
        print("H.U.L.I: Encerrando operações. Até logo, Rony.")
        falar("Encerrando operações. Até logo, Rony.")
        encerrar_programa = True
        return

    resposta = processar_comando(comando)

    if resposta == "ENCERRAR":
        print("H.U.L.I: Encerrando operações. Até logo, Rony.")
        falar("Encerrando operações. Até logo, Rony.")
        encerrar_programa = True
        return

    if resposta:
        print(f"H.U.L.I: {resposta}")
        falar(resposta)


def executar_agendamento(tipo: str, valor: str):
    if tipo == "rotina":
        print(f"\nH.U.L.I: ⏰ Executando rotina agendada: {valor}")
        executar_comando(f"abrir {valor}")

    elif tipo == "comando":
        print(f"\nH.U.L.I: ⏰ Executando comando agendado: {valor}")
        executar_comando(valor)


def iniciar():
    identidade = HULIIdentity()

    print(identidade.apresentar())
    falar(identidade.apresentar())

    print("H.U.L.I iniciado.")
    print("Modo seguro ativado: teclado + voz manual.")
    print("Comandos:")
    print(" - digite normalmente para usar teclado")
    print(" - digite 'voz' para falar um comando")
    print(" - digite 'sair' para encerrar\n")

    stop_event = threading.Event()

    t_lembretes = threading.Thread(
        target=monitor_lembretes,
        args=(stop_event,),
        daemon=True
    )
    t_lembretes.start()

    while not encerrar_programa:
        verificar_agendamentos(executar_agendamento)

        try:
            comando = input("Você: ").strip()

            if not comando:
                continue

            if comando.lower() == "voz":
                print("🎤 Fale agora...")
                comando_voz = ouvir_um_comando()

                if not comando_voz:
                    print("H.U.L.I: Não consegui entender o comando de voz.")
                    falar("Não consegui entender o comando de voz.")
                    continue

                print(f"Você disse: {comando_voz}")
                executar_comando(comando_voz)
                continue

            executar_comando(comando)

        except (KeyboardInterrupt, EOFError):
            print("\nH.U.L.I: Encerrando pelo teclado.")
            falar("Encerrando pelo teclado.")
            break

    stop_event.set()


if __name__ == "__main__":
    iniciar()