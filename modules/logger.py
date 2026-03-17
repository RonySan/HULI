import os
from datetime import datetime

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

ARQUIVO_LOG = os.path.join(LOG_DIR, "huli.log")


def registrar_log(tipo, mensagem):

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linha = f"[{agora}] [{tipo.upper()}] {mensagem}\n"

    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linha)