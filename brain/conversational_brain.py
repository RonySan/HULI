from core_system.session_memory import obter_memoria_sessao
from core_system.personality_engine import aplicar_personalidade


def responder_conversa_local(comando):
    texto = comando.lower().strip()
    memoria = obter_memoria_sessao()

    respostas = {
        "obrigado": "De nada, Rony. Sempre às ordens.",
        "obrigado huli": "De nada, Rony. Estou aqui com você.",
        "valeu": "Tamo junto, Rony.",
        "boa noite": "Boa noite, Rony. Descanse bem. Amanhã continuamos evoluindo.",
        "bom dia": "Bom dia, Rony. Pronto para continuar construindo algo grande?",
        "boa tarde": "Boa tarde, Rony. Estou pronta para te ajudar.",
        "oi": "Oi, Rony. Estou online e pronta.",
        "ola": "Olá, Rony. Sistemas disponíveis.",
        "olá": "Olá, Rony. Sistemas disponíveis.",
    }

    if texto in respostas:
        resposta = aplicar_personalidade(respostas[texto])
        memoria.registrar_interacao(texto, resposta, topico="conversa")
        return resposta

    if any(frase in texto for frase in [
        "estou cansado",
        "to cansado",
        "tô cansado",
        "dia dificil",
        "dia difícil",
    ]):
        resposta = (
            "Entendi, Rony. Pelo que estamos construindo, você tem puxado bastante. "
            "Talvez seja uma boa hora para desacelerar, salvar o progresso e continuar com clareza."
        )
        resposta = aplicar_personalidade(resposta)
        memoria.registrar_interacao(texto, resposta, topico="estado_emocional")
        return resposta

    if any(frase in texto for frase in [
        "o que fizemos hoje",
        "o que fizemos agora",
        "o que avançamos",
    ]):
        resumo = memoria.resumo()
        resposta = (
            "Hoje avançamos na estrutura cognitiva da H.U.L.I. "
            f"O último tópico registrado foi: {resumo.get('ultimo_topico')}. "
            "Também começamos a transformar comandos soltos em arquitetura modular."
        )
        resposta = aplicar_personalidade(resposta)
        memoria.registrar_interacao(texto, resposta, topico="reflexao")
        return resposta

    return None