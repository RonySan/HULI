from modules.voice_mode import (
    ativar_voz,
    desativar_voz,
    voz_esta_ativa,
)


def ativar():
    return ativar_voz()


def desativar():
    return desativar_voz()


def status():
    return "ATIVA" if voz_esta_ativa() else "DESATIVADA"