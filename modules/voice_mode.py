import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "voice_mode.json")


def carregar_config():
    if not os.path.exists(ARQUIVO):
        return {"voz_ativa": True, "limite_caracteres": 250}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"voz_ativa": True, "limite_caracteres": 250}


def salvar_config(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def ativar_voz():
    dados = carregar_config()
    dados["voz_ativa"] = True
    salvar_config(dados)
    return "Voz ativada."


def desativar_voz():
    dados = carregar_config()
    dados["voz_ativa"] = False
    salvar_config(dados)
    return "Voz desativada."


def voz_esta_ativa():
    return carregar_config().get("voz_ativa", True)



def deve_falar(texto):
    dados = carregar_config()

    if not dados.get("voz_ativa", True):
        return False

    if not texto:
        return False

    limite = dados.get("limite_caracteres", 250)

    if len(texto) > limite:
        return False

    return True