from core_system.skill_manager import listar_skills, obter_skill
from core_system.kernel import obter_kernel
from core_system.context import resumo_contexto


def gerar_ajuda():
    kernel = obter_kernel().status()
    ctx = resumo_contexto()
    skills = listar_skills()

    resposta = "🧠 H.U.L.I — Central de Ajuda Inteligente\n\n"

    resposta += "📌 Status rápido:\n"
    resposta += f"• Usuário: {kernel.get('usuario')}\n"
    resposta += f"• Proprietário: {kernel.get('proprietario')}\n"
    resposta += f"• Voz: {kernel.get('voz')}\n"
    resposta += f"• Jarvis: {kernel.get('jarvis')}\n"
    resposta += f"• Skills registradas: {len(skills)}\n\n"

    resposta += "🧩 Áreas disponíveis:\n"

    for nome in skills:
        skill = obter_skill(nome)

        if not skill:
            continue

        resposta += f"\n### {nome.upper()}\n"
        resposta += f"{skill.get('descricao')}\n"

        comandos = skill.get("comandos", [])

        if comandos:
            resposta += "Comandos principais:\n"
            for cmd in comandos[:5]:
                resposta += f"• {cmd}\n"

    resposta += "\n💡 Dicas:\n"
    resposta += "• Digite: skill nome_da_skill\n"
    resposta += "• Digite: status skills\n"
    resposta += "• Digite: o que voce sabe fazer\n"
    resposta += "• Digite: relatorio neural\n"
    resposta += "• Digite: resumo da sessao\n"

    return resposta


def gerar_novidades():
    resposta = "🚀 Novidades recentes da H.U.L.I\n\n"

    novidades = [
        "Kernel central operacional",
        "Contexto global sincronizado",
        "Event Bus",
        "Session Memory",
        "Skill Manager expandido",
        "Planner Service",
        "Diagnóstico completo",
        "Relatório Neural",
        "Personality Engine",
        "Conversational Brain",
        "Reflection Engine",
        "Auto Help Engine",
        "H.U.L.I 5.0 Orchestrator",
        "Task Queue",
        "Intent Analyzer",
    ]

    for item in novidades:
        resposta += f"• {item}\n"

    resposta += "\nDigite 'ajuda' para ver tudo que a H.U.L.I sabe fazer."

    return resposta