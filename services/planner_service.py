from datetime import datetime

from modules.memory import HULIMemory
from modules.scheduler import listar_agendamentos
from modules.routines import listar_rotinas
from modules.missions import listar_missoes
from core_system.session_memory import obter_memoria_sessao


def _linha(titulo, itens):
    resposta = f"{titulo}\n"

    if not itens:
        resposta += "• Nada encontrado.\n"
        return resposta

    if isinstance(itens, str):
        resposta += f"• {itens}\n"
        return resposta

    for item in itens:
        resposta += f"• {item}\n"

    return resposta


def resumo_do_dia():
    hoje = datetime.now().strftime("%d/%m/%Y")

    memoria = HULIMemory()

    try:
        agenda = memoria.listar_por_categoria("agenda")
        if isinstance(agenda, str):
            agenda = []
    except Exception:
        agenda = []

    try:
        tarefas = memoria.listar_por_categoria("tarefas")
        if isinstance(tarefas, str):
            tarefas = []
    except Exception:
        tarefas = []

    try:
        ideias = memoria.listar_por_categoria("ideias")
        if isinstance(ideias, str):
            ideias = []
    except Exception:
        ideias = []

    try:
        agendamentos = listar_agendamentos()
    except Exception:
        agendamentos = []

    try:
        rotinas = listar_rotinas()
    except Exception:
        rotinas = []

    try:
        missoes = listar_missoes()
    except Exception:
        missoes = []

    memoria_sessao = obter_memoria_sessao()
    sessao = memoria_sessao.resumo()

    resposta = f"📅 Resumo de hoje — {hoje}\n\n"

    resposta += "🗓️ Agenda registrada:\n"
    if agenda:
        for item in agenda:
            resposta += f"• {item.get('conteudo', item)}\n"
    else:
        resposta += "• Nenhum compromisso registrado na memória.\n"

    resposta += "\n✅ Tarefas:\n"
    if tarefas:
        for item in tarefas:
            resposta += f"• {item.get('conteudo', item)}\n"
    else:
        resposta += "• Nenhuma tarefa registrada.\n"

    resposta += "\n⏰ Agendamentos automáticos:\n"
    if agendamentos:
        for item in agendamentos:
            resposta += f"• {item}\n"
    else:
        resposta += "• Nenhum agendamento automático encontrado.\n"

    resposta += "\n🚀 Rotinas disponíveis:\n"
    if rotinas:
        for item in rotinas:
            resposta += f"• {item}\n"
    else:
        resposta += "• Nenhuma rotina cadastrada.\n"

    resposta += "\n🧠 Missões salvas:\n"
    if missoes:
        for item in missoes:
            resposta += f"• {item}\n"
    else:
        resposta += "• Nenhuma missão salva.\n"

    resposta += "\n💬 Sessão atual:\n"
    resposta += f"• Último tópico: {sessao.get('ultimo_topico')}\n"
    resposta += f"• Última pergunta: {sessao.get('ultima_pergunta')}\n"

    resposta += "\n📌 Recomendação do Petrus:\n"
    if tarefas:
        resposta += "• Comece pelas tarefas registradas e depois execute a rotina de trabalho.\n"
    elif rotinas:
        resposta += "• Você pode iniciar uma rotina disponível, como: modo trabalho.\n"
    else:
        resposta += "• Registre tarefas ou compromissos para a H.U.L.I organizar seu dia melhor.\n"

    return resposta


def resumo_pendencias():
    memoria = HULIMemory()

    try:
        tarefas = memoria.listar_por_categoria("tarefas")
        if isinstance(tarefas, str):
            tarefas = []
    except Exception:
        tarefas = []

    try:
        missoes = listar_missoes()
    except Exception:
        missoes = []

    resposta = "📌 Pendências encontradas:\n\n"

    resposta += "✅ Tarefas:\n"
    if tarefas:
        for item in tarefas:
            resposta += f"• {item.get('conteudo', item)}\n"
    else:
        resposta += "• Nenhuma tarefa registrada.\n"

    resposta += "\n🧠 Missões salvas:\n"
    if missoes:
        for item in missoes:
            resposta += f"• {item}\n"
    else:
        resposta += "• Nenhuma missão salva.\n"

    return resposta