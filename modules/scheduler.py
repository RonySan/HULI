import json
import os
from datetime import datetime

ARQUIVO_AGENDAMENTOS = os.path.join(os.path.dirname(__file__), "agendamentos.json")


def carregar_agendamentos():
    if not os.path.exists(ARQUIVO_AGENDAMENTOS):
        return []

    try:
        with open(ARQUIVO_AGENDAMENTOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def salvar_agendamentos(dados):
    with open(ARQUIVO_AGENDAMENTOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def adicionar_agendamento(tipo: str, valor: str, horario: str):
    agendamentos = carregar_agendamentos()

    novo = {
        "id": len(agendamentos) + 1,
        "tipo": tipo,
        "valor": valor,
        "horario": horario,
        "executado_hoje": False,
        "ultima_data": ""
    }

    agendamentos.append(novo)
    salvar_agendamentos(agendamentos)

    return f"Agendamento criado: {tipo} '{valor}' às {horario}."


def listar_agendamentos():
    return carregar_agendamentos()


def remover_agendamento(agendamento_id: int):
    agendamentos = carregar_agendamentos()
    novos = [a for a in agendamentos if a.get("id") != agendamento_id]

    if len(novos) == len(agendamentos):
        return False, f"Não encontrei o agendamento {agendamento_id}."

    # reorganiza IDs
    for i, item in enumerate(novos, 1):
        item["id"] = i

    salvar_agendamentos(novos)
    return True, f"Agendamento {agendamento_id} removido com sucesso."


def verificar_agendamentos(executar_callback):
    agendamentos = carregar_agendamentos()
    agora = datetime.now()
    data_hoje = agora.strftime("%Y-%m-%d")
    hora_atual = agora.strftime("%H:%M")

    alterado = False

    for item in agendamentos:
        horario = item.get("horario", "")
        ultima_data = item.get("ultima_data", "")

        if horario == hora_atual and ultima_data != data_hoje:
            executar_callback(item["tipo"], item["valor"])
            item["ultima_data"] = data_hoje
            alterado = True

    if alterado:
        salvar_agendamentos(agendamentos)