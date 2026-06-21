from modules.settings_manager import obter, definir


def definir_modo_personalidade(modo):
    modo = modo.lower().strip()

    modos_validos = [
        "normal",
        "jarvis",
        "petrus",
        "tecnico",
        "amigo",
        "trabalho",
        "silencioso",
    ]

    if modo not in modos_validos:
        return f"Modo inválido. Modos disponíveis: {', '.join(modos_validos)}"

    definir("modo_personalidade", modo)
    return f"Modo de personalidade alterado para: {modo}."


def obter_modo_personalidade():
    return obter("modo_personalidade", "normal")


def aplicar_personalidade(resposta):
    modo = obter_modo_personalidade()

    if not resposta:
        return resposta

    if modo == "silencioso":
        if len(resposta) > 250:
            return "Resposta grande demais para leitura. Deixei na tela para você ler."

    if modo == "jarvis":
        return f"Entendido, Rony. {resposta}"

    if modo == "petrus":
        return f"Petrus analisando: {resposta}"

    if modo == "tecnico":
        return f"Análise técnica: {resposta}"

    if modo == "amigo":
        return f"Fechado, Rony. {resposta}"

    if modo == "trabalho":
        return f"Modo trabalho: {resposta}"

    return resposta


def status_personalidade():
    return f"Personalidade atual: {obter_modo_personalidade()}"