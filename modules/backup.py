import shutil
import os
from datetime import datetime

PASTA_BACKUP = "backup"


def criar_backup():

    if not os.path.exists(PASTA_BACKUP):
        os.makedirs(PASTA_BACKUP)

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")

    destino = os.path.join(PASTA_BACKUP, f"huli_backup_{agora}")

    os.makedirs(destino)

    arquivos = [
        "modules/rotinas.json",
        "modules/agendamentos.json",
        "modules/custom_commands.json",
    ]

    for arq in arquivos:

        if os.path.exists(arq):

            shutil.copy(arq, destino)

    return f"Backup criado em {destino}"