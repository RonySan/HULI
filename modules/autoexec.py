from modules.habits import prever_proximo


def sugerir_proxima_acao(comando):
    proximo = prever_proximo(comando)

    if not proximo:
        return None

    return f"Rony, você costuma executar '{proximo}' depois disso. Deseja continuar?"


def auto_executar(comando, processar_func):
    proximo = prever_proximo(comando)

    if not proximo:
        return None

    # Só executa automaticamente se for MUITO frequente
    return processar_func(proximo)