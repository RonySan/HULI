import time
import threading
from datetime import datetime
from modules.habits import registrar_sequencia, sugerir_proximo
from modules.identity import HULIIdentity
from modules.commands import processar_comando
from modules.memory import HULIMemory
from modules.voice import falar
from modules.voice_listener import ouvir_um_comando
from modules.scheduler import verificar_agendamentos
from modules.history import registrar as registrar_historico
from modules.logger import registrar_log
from modules.autopilot import obter_autoexecucao, ativar_autoexecucao


encerrar_programa = False
ultimo_comando = None
sugestao_pendente = None


def monitor_agendamentos(stop_event):
    while not stop_event.is_set():
        try:
            verificar_agendamentos(executar_agendamento)
        except Exception:
            pass

        time.sleep(30)  # verifica a cada 30 segundos

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
        t_agendamentos = threading.Thread(
        target=monitor_agendamentos,
        args=(stop_event,),
        daemon=True
    )
    t_agendamentos.start()



def executar_comando(comando: str):
    global encerrar_programa, ultimo_comando, sugestao_pendente

    if not comando:
        return

    comando_limpo = comando.strip().lower()
    registrar_log("comando", comando)

    # confirma autoexecução sugerida
    if sugestao_pendente and comando_limpo in ["sim", "s", "ok", "pode", "claro"]:
        comando_base = sugestao_pendente["base"]
        proximo = sugestao_pendente["proximo"]

        resposta_auto = ativar_autoexecucao(comando_base, proximo)
        registrar_log("autopilot", resposta_auto)

        print(f"H.U.L.I: {resposta_auto}")
        falar(resposta_auto)

        sugestao_pendente = None
        return

    if sugestao_pendente and comando_limpo in ["nao", "não", "n", "deixa", "deixa pra la", "deixa pra lá"]:
        print("H.U.L.I: Entendido. Não vou automatizar isso.")
        falar("Entendido. Não vou automatizar isso.")
        registrar_log("autopilot", "Usuário recusou sugestão de autoexecução.")
        sugestao_pendente = None
        return

    if comando_limpo in ["sair", "encerrar", "fechar huli"]:
        registrar_log("sistema", "Encerrando H.U.L.I por comando do usuário.")
        print("H.U.L.I: Encerrando operações. Até logo, Rony.")
        falar("Encerrando operações. Até logo, Rony.")
        encerrar_programa = True
        return

    resposta = processar_comando(comando)

    if resposta == "ENCERRAR":
        registrar_log("sistema", "Encerrando H.U.L.I por retorno ENCERRAR.")
        print("H.U.L.I: Encerrando operações. Até logo, Rony.")
        falar("Encerrando operações. Até logo, Rony.")
        encerrar_programa = True
        return

    if resposta:
        registrar_log("resposta", resposta)
        print(f"H.U.L.I: {resposta}")
        falar(resposta)

    # memória operacional
    registrar_sequencia(ultimo_comando, comando)

    sugestao = sugerir_proximo(comando)

    if sugestao:
        auto = obter_autoexecucao(comando)

        if auto:
            registrar_log("autopilot", f"Executando automaticamente após '{comando}': '{auto}'")
            print(f"H.U.L.I: ⚡ Executando automaticamente: {auto}")
            falar("Executando automaticamente.")
            executar_comando(auto)
        else:
            sugestao_pendente = {
                "base": comando,
                "proximo": sugestao,
            }
            print(f"H.U.L.I: 💡 Você costuma fazer isso depois: '{sugestao}'. Quer que eu execute automaticamente da próxima vez?")
            falar("Você costuma fazer isso depois. Quer que eu execute automaticamente da próxima vez?")

    ultimo_comando = comando


def executar_agendamento(tipo: str, valor: str):
    from modules.logger import registrar_log

    if tipo == "rotina":
        registrar_log("agendamento", f"Executando rotina agendada: {valor}")
        print(f"\nH.U.L.I: ⏰ Executando rotina agendada: {valor}")
        executar_comando(f"abrir {valor}")

    elif tipo == "comando":
        registrar_log("agendamento", f"Executando comando agendado: {valor}")
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