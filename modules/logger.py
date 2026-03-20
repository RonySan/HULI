import os
from datetime import datetime

PASTA_LOGS = os.path.join(os.getcwd(), "logs")
ARQUIVO_LOG = os.path.join(PASTA_LOGS, "huli.log")


def garantir_pasta_logs():
    if not os.path.exists(PASTA_LOGS):
        os.makedirs(PASTA_LOGS)


def registrar_log(tipo: str, mensagem: str):
    garantir_pasta_logs()

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{agora}] [{tipo.upper()}] {mensagem}\n"

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linha)


def ler_logs(quantidade: int = 100):
    garantir_pasta_logs()

    if not os.path.exists(ARQUIVO_LOG):
        return []

    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    return linhas[-quantidade:]


def limpar_logs():
    garantir_pasta_logs()

    with open(ARQUIVO_LOG, "w", encoding="utf-8") as f:
        f.write("")

    return "Logs limpos com sucesso."