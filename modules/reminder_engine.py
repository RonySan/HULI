import json
import os
import threading
import time

from datetime import datetime


ARQUIVO = os.path.join(
    os.path.dirname(__file__),
    "reminders.json"
)

rodando = False


# =====================================================
# ARQUIVO
# =====================================================

def carregar():

    if not os.path.exists(ARQUIVO):
        return []

    try:

        with open(
            ARQUIVO,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:
        return []


def salvar(dados):

    with open(
        ARQUIVO,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )


# =====================================================
# LEMBRETES
# =====================================================

def criar_lembrete(texto, horario):

    dados = carregar()

    item = {
        "texto": texto,
        "horario": horario,
        "executado": False,
        "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    dados.append(item)

    salvar(dados)

    return (
        f"✔ Lembrete criado para "
        f"{horario}"
    )


def listar_lembretes():

    dados = carregar()

    if not dados:
        return "Nenhum lembrete cadastrado."

    resposta = "Lembretes:\n\n"

    for i, item in enumerate(dados, 1):

        status = "✅" if item["executado"] else "⏰"

        resposta += (
            f"{i}. {status} "
            f"{item['horario']} -> "
            f"{item['texto']}\n"
        )

    return resposta


def apagar_lembretes():

    salvar([])

    return "Todos os lembretes foram apagados."


# =====================================================
# LOOP
# =====================================================

def verificar_lembretes(falar_callback=None):

    global rodando

    rodando = True

    while rodando:

        agora = datetime.now().strftime("%H:%M")

        dados = carregar()

        alterado = False

        for item in dados:

            if item["executado"]:
                continue

            horario = item["horario"]

            if horario == agora:

                mensagem = (
                    f"🔔 Lembrete: "
                    f"{item['texto']}"
                )

                print("\n" + mensagem)

                if falar_callback:
                    try:
                        falar_callback(mensagem)
                    except Exception:
                        pass

                item["executado"] = True
                alterado = True

        if alterado:
            salvar(dados)

        time.sleep(20)


def iniciar_engine(falar_callback=None):

    thread = threading.Thread(
        target=verificar_lembretes,
        args=(falar_callback,),
        daemon=True
    )

    thread.start()

    return "Reminder Engine iniciado."


def parar_engine():

    global rodando

    rodando = False

    return "Reminder Engine parado."