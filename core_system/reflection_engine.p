from core_system.session_memory import obter_memoria_sessao
from core_system.kernel import obter_kernel
from core_system.event_bus import listar_eventos
from core_system.skill_manager import status_skills


def resumo_da_sessao():
    memoria = obter_memoria_sessao()
    resumo = memoria.resumo()
    interacoes = memoria.ultimas_interacoes(8)

    resposta = "🧠 Resumo da sessão atual:\n\n"
    resposta += f"• Total de interações: {resumo.get('total_interacoes')}\n"
    resposta += f"• Último tópico: {resumo.get('ultimo_topico')}\n"
    resposta += f"• Tem diagnóstico recente: {resumo.get('tem_diagnostico')}\n\n"

    if interacoes:
        resposta += "Últimas interações:\n"
        for item in interacoes:
            resposta += f"• Você: {item.get('pergunta')}\n"

    return resposta


def estado_do_projeto():
    kernel = obter_kernel().status()
    skills = status_skills()
    eventos = listar_eventos()

    resposta = "🚀 Estado atual do projeto H.U.L.I:\n\n"
    resposta += f"• Kernel ativo: sim\n"
    resposta += f"• Usuário: {kernel.get('usuario')}\n"
    resposta += f"• Proprietário: {kernel.get('proprietario')}\n"
    resposta += f"• Skills registradas: {skills.get('total_skills')}\n"
    resposta += f"• Eventos recentes: {len(eventos)}\n"
    resposta += f"• Threads ativas: {kernel.get('threads')}\n\n"

    resposta += "Arquitetura principal já criada:\n"
    resposta += "• Kernel\n"
    resposta += "• Context\n"
    resposta += "• Event Bus\n"
    resposta += "• Session Memory\n"
    resposta += "• Skill Manager\n"
    resposta += "• Planner Service\n"
    resposta += "• Neural Scanner\n"
    resposta += "• Personality Engine\n"
    resposta += "• Conversational Brain\n"

    return resposta


def proximos_passos():
    resposta = "📌 Próximos passos recomendados:\n\n"
    resposta += "1. Melhorar Conversation Brain para conversas mais naturais.\n"
    resposta += "2. Criar Auto Help baseado em Skills.\n"
    resposta += "3. Criar Auto Documentation.\n"
    resposta += "4. Melhorar Neural Scanner para detectar duplicações.\n"
    resposta += "5. Criar Plugin Manager.\n"

    return resposta


def refletir(comando):
    texto = comando.lower().strip()

    if texto in [
        "resumo da sessao",
        "resumo da sessão",
        "resuma a sessao",
        "resuma a sessão",
        "o que fizemos hoje",
        "o que fizemos agora",
    ]:
        return resumo_da_sessao()

    if texto in [
        "como esta o projeto",
        "como está o projeto",
        "estado do projeto",
        "status do projeto",
        "como esta a huli",
        "como está a huli",
    ]:
        return estado_do_projeto()

    if texto in [
        "o que falta",
        "o que falta fazer",
        "proximos passos",
        "próximos passos",
        "qual o proximo passo",
        "qual o próximo passo",
    ]:
        return proximos_passos()

    return None