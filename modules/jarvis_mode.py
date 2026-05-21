from modules.settings_manager import obter, definir


def ativar_modo_jarvis():
    definir("modo_jarvis", True)
    definir("voz_ativa", True)
    definir("escuta_continua", True)
    return "Modo Jarvis ativado."


def desativar_modo_jarvis():
    definir("modo_jarvis", False)
    definir("escuta_continua", False)
    return "Modo Jarvis desativado."


def modo_jarvis_ativo():
    return obter("modo_jarvis", False)


def status_jarvis():
    ativo = modo_jarvis_ativo()
    return "ATIVO" if ativo else "DESATIVADO"