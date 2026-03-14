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


def adicionar_agendamento(tipo: str, valor: str, horario: str, recorrencia: str = "uma vez"):
    agendamentos = carregar_agendamentos()

    novo = {
        "id": len(agendamentos) + 1,
        "tipo": tipo,
        "valor": valor,
        "horario": horario,
        "recorrencia": recorrencia,
        "ultima_execucao": ""
    }

    agendamentos.append(novo)
    salvar_agendamentos(agendamentos)

    return f"Agendamento criado: {tipo} '{valor}' às {horario} ({recorrencia})."


def listar_agendamentos():
    return carregar_agendamentos()


def remover_agendamento(agendamento_id: int):
    agendamentos = carregar_agendamentos()
    novos = [a for a in agendamentos if a.get("id") != agendamento_id]

    if len(novos) == len(agendamentos):
        return False, f"Não encontrei o agendamento {agendamento_id}."

    for i, item in enumerate(novos, 1):
        item["id"] = i

    salvar_agendamentos(novos)
    return True, f"Agendamento {agendamento_id} removido com sucesso."


def recorrencia_valida_hoje(recorrencia: str, agora: datetime) -> bool:
    dia_semana = agora.weekday()  # 0=segunda ... 6=domingo

    if recorrencia == "uma vez":
        return True
    if recorrencia == "todo dia":
        return True
    if recorrencia == "segunda a sexta":
        return dia_semana <= 4
    if recorrencia == "fim de semana":
        return dia_semana >= 5

    return False


def verificar_agendamentos(executar_callback):
    agendamentos = carregar_agendamentos()
    agora = datetime.now()
    data_hora_atual = agora.strftime("%Y-%m-%d %H:%M")
    hora_atual = agora.strftime("%H:%M")

    alterado = False
    novos_agendamentos = []

    for item in agendamentos:
        horario = item.get("horario", "")
        recorrencia = item.get("recorrencia", "uma vez")
        ultima_execucao = item.get("ultima_execucao", "")

        if (
            horario == hora_atual
            and ultima_execucao != data_hora_atual
            and recorrencia_valida_hoje(recorrencia, agora)
        ):
            executar_callback(item["tipo"], item["valor"])
            item["ultima_execucao"] = data_hora_atual
            alterado = True

            if recorrencia == "uma vez":
                continue

        novos_agendamentos.append(item)

    if alterado:
        for i, item in enumerate(novos_agendamentos, 1):
            item["id"] = i
        salvar_agendamentos(novos_agendamentos)