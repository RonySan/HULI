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

import shutil
import os
from datetime import datetime

PASTA_BACKUP = os.path.join(os.getcwd(), "backup")


def criar_backup():
    if not os.path.exists(PASTA_BACKUP):
        os.makedirs(PASTA_BACKUP)

    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(PASTA_BACKUP, f"huli_backup_{agora}")
    os.makedirs(destino, exist_ok=True)

    arquivos = [
        os.path.join("modules", "rotinas.json"),
        os.path.join("modules", "agendamentos.json"),
        os.path.join("modules", "custom_commands.json"),
    ]

    copiados = []

    for arq in arquivos:
        if os.path.exists(arq):
            shutil.copy(arq, destino)
            copiados.append(arq)

    if not copiados:
        return "Nenhum arquivo de dados foi encontrado para backup."

    return f"Backup criado com sucesso em: {destino}"


def listar_backups():
    if not os.path.exists(PASTA_BACKUP):
        return []

    itens = []
    for nome in os.listdir(PASTA_BACKUP):
        caminho = os.path.join(PASTA_BACKUP, nome)
        if os.path.isdir(caminho):
            itens.append(nome)

    return sorted(itens, reverse=True)