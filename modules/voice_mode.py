from modules.settings_manager import obter, definir


def ativar_voz():
    definir("voz_ativa", True)
    return "Voz ativada."


def desativar_voz():
    definir("voz_ativa", False)
    return "Voz desativada."


def voz_esta_ativa():
    return obter("voz_ativa", True)


def deve_falar(texto):
    if not obter("voz_ativa", True):
        return False

    if not texto:
        return False

    limite = obter("limite_fala", 250)

    if len(texto) > limite:
        return False

    return True