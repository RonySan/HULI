import json
import os

ARQUIVO = "knowledge.json"


def carregar():
    if not os.path.exists(ARQUIVO):
        return {}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def aprender(chave, valor):
    dados = carregar()
    dados[chave.lower().strip()] = valor.strip()
    salvar(dados)


def buscar(chave):
    dados = carregar()
    return dados.get(chave.lower().strip())


def listar_tudo():
    return carregar()