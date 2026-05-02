import time
import threading
from datetime import datetime

from modules.identity import HULIIdentity
from modules.commands import processar_comando
from modules.memory import HULIMemory
from modules.voice import falar
from modules.voice_listener import ouvir_um_comando
from modules.voice_natural import ouvir_natural, ouvir_com_ativacao
from modules.scheduler import verificar_agendamentos
from modules.history import registrar as registrar_historico
from modules.logger import registrar_log
from modules.habits import registrar_sequencia, prever_proximo
from modules.autopilot import obter_autoexecucao, ativar_autoexecucao
from modules.voice_mode import deve_falar

encerrar_programa = False
ultimo_comando = None
sugestao_pendente = None
escuta_continua_ativa = False


def monitor_agendamentos(stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            verificar_agendamentos(executar_agendamento)
        except Exception as e:
            registrar_log("erro", f"monitor_agendamentos: {e}")

        time.sleep(30)


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
                    registrar_log("lembrete", texto)
                    print(f"\nH.U.L.I: 🔔 {texto}\n")
                    falar(texto)
                    memoria.marcar_lembrete_executado(lembrete.get("id"))

        except Exception as e:
            registrar_log("erro", f"monitor_lembretes: {e}")

        time.sleep(1)


def executar_agendamento(tipo: str, valor: str):
    if tipo == "rotina":
        registrar_log("agendamento", f"Executando rotina agendada: {valor}")
        print(f"\nH.U.L.I: ⏰ Executando rotina agendada: {valor}")
        executar_comando(f"abrir {valor}")

    elif tipo == "comando":
        registrar_log("agendamento", f"Executando comando agendado: {valor}")
        print(f"\nH.U.L.I: ⏰ Executando comando agendado: {valor}")
        executar_comando(valor)


def falar_se_permitido(texto):
    if deve_falar(texto):
        falar(texto)




def executar_comando(comando: str):
    global encerrar_programa, ultimo_comando, sugestao_pendente

    if not comando:
        return

    comando_limpo = comando.strip().lower()
    registrar_log("comando", comando)
    registrar_historico(comando)

    if sugestao_pendente and comando_limpo in ["sim", "s", "ok", "pode", "claro"]:
        comando_base = sugestao_pendente["base"]
        proximo = sugestao_pendente["proximo"]

        resposta_auto = ativar_autoexecucao(comando_base, proximo)
        registrar_log("autopilot", resposta_auto)

        print(f"H.U.L.I: {resposta_auto}")
        falar_se_permitido(resposta_auto)

        sugestao_pendente = None
        return

    if sugestao_pendente and comando_limpo in ["nao", "não", "n", "deixa", "deixa pra la", "deixa pra lá"]:
        print("H.U.L.I: Entendido. Não vou automatizar isso.")
        falar_se_permitido("Entendido. Não vou automatizar isso.")
        registrar_log("autopilot", "Usuário recusou sugestão de autoexecução.")
        sugestao_pendente = None
        return

    if comando_limpo in ["sair", "encerrar", "fechar huli"]:
        registrar_log("sistema", "Encerrando H.U.L.I por comando do usuário.")
        print("H.U.L.I: Encerrando operações. Até logo, Rony.")
        falar_se_permitido("Encerrando operações. Até logo, Rony.")
        encerrar_programa = True
        return

    resposta = processar_comando(comando)

    if resposta == "ENCERRAR":
        registrar_log("sistema", "Encerrando H.U.L.I por retorno ENCERRAR.")
        print("H.U.L.I: Encerrando operações. Até logo, Rony.")
        falar_se_permitido("Encerrando operações. Até logo, Rony.")
        encerrar_programa = True
        return

    if resposta:
        registrar_log("resposta", resposta)
        print(f"H.U.L.I: {resposta}")
        falar_se_permitido(resposta)

    registrar_sequencia(ultimo_comando, comando)

    sugestao = prever_proximo(comando)
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
            falar_se_permitido("Você costuma fazer isso depois. Quer que eu execute automaticamente da próxima vez?")

    ultimo_comando = comando

def modo_escuta_continua(stop_event: threading.Event):
    global escuta_continua_ativa

    print("🎙️ Escuta contínua ativada. Diga 'huli' + comando.")

    while not stop_event.is_set() and escuta_continua_ativa:
        try:
            comando_voz = ouvir_com_ativacao(
                timeout=6,
                phrase_time_limit=6
            )

            if comando_voz:
                print(f"\n🎤 Você disse: {comando_voz}")
                executar_comando(comando_voz)

        except Exception as e:
            registrar_log("erro", f"modo_escuta_continua: {e}")

        time.sleep(0.5)

    print("🎙️ Escuta contínua encerrada.")

def iniciar():
    global encerrar_programa, escuta_continua_ativa

    identidade = HULIIdentity()

    saudacao = identidade.apresentar()
    print(saudacao)
    falar_se_permitido(saudacao)

    print("H.U.L.I iniciado.")
    print("Modo seguro ativado: teclado + voz manual.")
    print("Comandos:")
    print(" - digite normalmente para usar teclado")
    print(" - digite 'voz' para falar um comando")
    print(" - digite 'ouvir' para falar com ativação")
    print(" - digite 'ouvir natural' para voz natural")
    print(" - digite 'sair' para encerrar\n")

    registrar_log("sistema", "H.U.L.I iniciada com sucesso.")

    stop_event = threading.Event()

    t_lembretes = threading.Thread(
        target=monitor_lembretes,
        args=(stop_event,),
        daemon=True
    )
    t_lembretes.start()

    t_agendamentos = threading.Thread(
        target=monitor_agendamentos,
        args=(stop_event,),
        daemon=True
    )
    t_agendamentos.start()

    while not encerrar_programa:
        try:
            comando = input("Você: ").strip()

            if not comando:
                continue

            # -------------------------
            # ESCUTA CONTÍNUA
            # -------------------------
            if comando.lower() in ["modo escuta", "ativar escuta", "escuta continua", "escuta contínua"]:
                if escuta_continua_ativa:
                    print("H.U.L.I: A escuta contínua já está ativa.")
                    falar_se_permitido("A escuta contínua já está ativa.")
                    continue

                escuta_continua_ativa = True

                print("H.U.L.I: Escuta contínua ativada.")
                falar_se_permitido("Escuta contínua ativada.")

                t_escuta = threading.Thread(
                    target=modo_escuta_continua,
                    args=(stop_event,),
                    daemon=True
                )
                t_escuta.start()
                continue

            if comando.lower() in ["parar escuta", "desativar escuta", "encerrar escuta"]:
                escuta_continua_ativa = False

                print("H.U.L.I: Escuta contínua desativada.")
                falar_se_permitido("Escuta contínua desativada.")
                continue

            # -------------------------
            # VOZ MANUAL
            # -------------------------
            if comando.lower() == "voz":
                print("🎤 Fale agora...")
                comando_voz = ouvir_um_comando()

                if not comando_voz:
                    print("H.U.L.I: Não consegui entender o comando de voz.")
                    falar_se_permitido("Não consegui entender o comando de voz.")
                    continue

                print(f"Você disse: {comando_voz}")
                executar_comando(comando_voz)
                continue

            if comando.lower() == "ouvir":
                print("🎙️ Modo voz com ativação...")
                comando_voz = ouvir_com_ativacao()

                if not comando_voz:
                    print("H.U.L.I: Não ouvi nenhum comando válido com ativação.")
                    falar_se_permitido("Não ouvi nenhum comando válido com ativação.")
                    continue

                print(f"Você disse: {comando_voz}")
                executar_comando(comando_voz)
                continue

            if comando.lower() == "ouvir natural":
                comando_voz = ouvir_natural()

                if not comando_voz:
                    print("H.U.L.I: Não consegui entender pela voz natural.")
                    falar_se_permitido("Não consegui entender pela voz natural.")
                    continue

                print(f"Você disse: {comando_voz}")
                executar_comando(comando_voz)
                continue

            # -------------------------
            # EXECUÇÃO NORMAL
            # -------------------------
            executar_comando(comando)

        except (KeyboardInterrupt, EOFError):
            registrar_log("sistema", "Encerrando H.U.L.I por teclado.")
            print("\nH.U.L.I: Encerrando pelo teclado.")
            falar_se_permitido("Encerrando pelo teclado.")
            break

        except Exception as e:
            registrar_log("erro", f"loop principal: {e}")
            print(f"H.U.L.I: Ocorreu um erro: {e}")

    stop_event.set()

if __name__ == "__main__":
    iniciar()