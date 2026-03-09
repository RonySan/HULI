import subprocess
import webbrowser
import os

ROTINAS = {

    "trabalho": [
        {"tipo": "programa", "nome": "vscode"},
        {"tipo": "programa", "nome": "chrome"},
        {"tipo": "site", "url": "https://github.com"},
        {"tipo": "site", "url": "https://mail.google.com"},
    ],

    "estudo": [
        {"tipo": "site", "url": "https://youtube.com"},
        {"tipo": "site", "url": "https://chatgpt.com"},
        {"tipo": "programa", "nome": "vscode"},
    ],

    "projeto huli": [
        {"tipo": "programa", "nome": "vscode"},
        {"tipo": "programa", "nome": "powershell"},
        {"tipo": "site", "url": "https://github.com"},
    ],

}


def executar_rotina(nome_rotina, abrir_programa_func):
    nome = nome_rotina.lower()

    if nome not in ROTINAS:
        return False, f"Não encontrei a rotina '{nome_rotina}'."

    tarefas = ROTINAS[nome]

    for tarefa in tarefas:

        if tarefa["tipo"] == "programa":
            abrir_programa_func(tarefa["nome"])

        elif tarefa["tipo"] == "site":
            webbrowser.open(tarefa["url"])

        elif tarefa["tipo"] == "comando":
            subprocess.Popen(tarefa["cmd"], shell=True)

    return True, f"Executando rotina '{nome_rotina}'."