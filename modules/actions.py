import subprocess
import json
import os

PROGRAMAS_PATH = "programas.json"

PROGRAMAS_PADRAO = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": r"C:\Users\ronys\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "bloco de notas": "notepad.exe",
    "notepad": "notepad.exe",
    "calculadora": "calc.exe",
}


def carregar_programas():
    if not os.path.exists(PROGRAMAS_PATH):
        salvar_programas(PROGRAMAS_PADRAO)
        return PROGRAMAS_PADRAO.copy()

    try:
        with open(PROGRAMAS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return PROGRAMAS_PADRAO.copy()


def salvar_programas(programas):
    with open(PROGRAMAS_PATH, "w", encoding="utf-8") as f:
        json.dump(programas, f, ensure_ascii=False, indent=4)


def abrir_programa(nome: str):
    programas = carregar_programas()
    nome = nome.lower().strip()

    if nome in programas:
        try:
            subprocess.Popen(programas[nome], shell=True)
            return f"Abrindo {nome}."
        except Exception:
            return f"Não consegui abrir {nome}."

    return None


def aprender_programa(nome: str, caminho: str):
    nome = nome.lower().strip()
    caminho = caminho.strip()

    # se for caminho com barra invertida, valida existência
    if "\\" in caminho and not os.path.exists(caminho):
        return f"O caminho '{caminho}' não existe."

    programas = carregar_programas()
    programas[nome] = caminho
    salvar_programas(programas)

    return f"Aprendi o programa '{nome}'."