from modules.ai import responder_ia, tem_internet, extrair_conhecimento


def online():
    return tem_internet()


def responder(comando, historico=None, modo="normal"):
    return responder_ia(comando, historico=historico, modo=modo)


def extrair_memoria(comando):
    return extrair_conhecimento(comando)