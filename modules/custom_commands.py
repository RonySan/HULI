import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "custom_commands.json")


def carregar():
    if not os.path.exists(ARQUIVO):
        return {}

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def criar_comando(nome, comando):
    dados = carregar()

    dados[nome.lower()] = comando.lower()

    salvar(dados)

    return f"Comando personalizado '{nome}' criado."


def executar_comando_personalizado(texto):
    dados = carregar()

    if texto.lower() in dados:
        return dados[texto.lower()]

    return None


def listar_comandos():
    dados = carregar()

    return dados