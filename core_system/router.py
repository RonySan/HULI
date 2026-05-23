from core_system.brain import processar_intencao_local


def rotear(comando, base=""):
    resposta = processar_intencao_local(comando, base)

    if resposta:
        return resposta

    return None