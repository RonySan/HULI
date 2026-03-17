import json
import os

ARQUIVO = "history.json"


def carregar():
    if not os.path.exists(ARQUIVO):
        return []

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar(hist):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=4, ensure_ascii=False)


def registrar(comando):

    hist = carregar()

    hist.append(comando)

    hist = hist[-100:]

    salvar(hist)


def listar():

    return carregar()