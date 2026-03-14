import os
import subprocess
from pathlib import Path
import webbrowser
import urllib.parse


PASTAS_MENU_INICIAR = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs"),
]


def normalizar_nome(nome: str) -> str:
    return (
        nome.lower()
        .replace(".lnk", "")
        .replace(".url", "")
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def escanear_programas():
    apps = {}

    for pasta in PASTAS_MENU_INICIAR:
        if not os.path.exists(pasta):
            continue

        for raiz, _, arquivos in os.walk(pasta):
            for arquivo in arquivos:
                if arquivo.endswith(".lnk") or arquivo.endswith(".url"):
                    nome_original = Path(arquivo).stem
                    nome_normalizado = normalizar_nome(nome_original)
                    caminho_completo = os.path.join(raiz, arquivo)

                    if nome_normalizado not in apps:
                        apps[nome_normalizado] = {
                            "nome": nome_original,
                            "caminho": caminho_completo,
                        }

    return apps


def listar_programas():
    apps = escanear_programas()
    if not apps:
        return []
    return sorted([dados["nome"] for dados in apps.values()])


def abrir_programa(nome_programa: str):
    apps = escanear_programas()
    busca = normalizar_nome(nome_programa)

    # 1. correspondência exata
    if busca in apps:
        caminho = apps[busca]["caminho"]
        os.startfile(caminho)
        return True, f"Abrindo {apps[busca]['nome']}."

    # 2. correspondência parcial
    correspondencias = []
    for chave, dados in apps.items():
        if busca in chave:
            correspondencias.append(dados)

    if len(correspondencias) == 1:
        os.startfile(correspondencias[0]["caminho"])
        return True, f"Abrindo {correspondencias[0]['nome']}."

    if len(correspondencias) > 1:
        nomes = ", ".join([c["nome"] for c in correspondencias[:5]])
        return False, f"Encontrei vários programas parecidos: {nomes}"

    # 3. fallback para apps comuns do Windows
    atalhos = {
        "chrome": "start chrome",
        "google chrome": "start chrome",
        "edge": "start msedge",
        "vscode": "start code",
        "visual studio code": "start code",
        "bloco de notas": "start notepad",
        "notepad": "start notepad",
        "calculadora": "start calc",
        "calc": "start calc",
        "explorador": "start explorer",
        "explorer": "start explorer",
        "powershell": "start powershell",
        "cmd": "start cmd",
    }

    if busca in atalhos:
        subprocess.Popen(atalhos[busca], shell=True)
        return True, f"Abrindo {nome_programa}."

    return False, f"Não encontrei o programa '{nome_programa}'."

SITES_RAPIDOS = {
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
    "google": "https://www.google.com",
    "whatsapp": "https://web.whatsapp.com",
}


def abrir_site(nome_site: str):
    nome = normalizar_nome(nome_site)

    if nome in SITES_RAPIDOS:
        webbrowser.open(SITES_RAPIDOS[nome])
        return True, f"Abrindo {nome_site}."

    return False, f"Não encontrei o site '{nome_site}'."


def pesquisar_web(termo: str):
    if not termo.strip():
        return False, "O que você quer pesquisar?"

    query = urllib.parse.quote_plus(termo)
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return True, f"Pesquisando por: {termo}"


def abrir_pasta(caminho: str):
    try:
        if not os.path.exists(caminho):
            return False, f"Não encontrei a pasta '{caminho}'."

        os.startfile(caminho)
        return True, f"Abrindo pasta: {caminho}"
    except Exception:
        return False, f"Não consegui abrir a pasta '{caminho}'."


def executar_comando_terminal(comando: str):
    try:
        subprocess.Popen(comando, shell=True)
        return True, f"Executando comando: {comando}"
    except Exception:
        return False, "Não consegui executar o comando."
    
def abrir_arquivo(caminho: str):
    try:
        if not os.path.exists(caminho):
            return False, f"Não encontrei o arquivo '{caminho}'."

        os.startfile(caminho)
        return True, f"Abrindo arquivo: {caminho}"
    except Exception:
        return False, f"Não consegui abrir o arquivo '{caminho}'."