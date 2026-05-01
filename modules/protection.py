import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "protection.json")

_confirmacao_pendente = None


def carregar_config():
    if not os.path.exists(ARQUIVO):
        return {"ativo": False}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"ativo": False}


def salvar_config(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def ativar_protecao():
    dados = carregar_config()
    dados["ativo"] = True
    salvar_config(dados)
    return "Modo proteção ativado."


def desativar_protecao():
    dados = carregar_config()
    dados["ativo"] = False
    salvar_config(dados)
    return "Modo proteção desativado."


def status_protecao():
    dados = carregar_config()
    return "ATIVO" if dados.get("ativo") else "INATIVO"


def requer_confirmacao(comando: str):
    dados = carregar_config()
    if not dados.get("ativo"):
        return False

    comando = comando.lower().strip()

    comandos_sensiveis = [
        "desligar pc",
        "reiniciar pc",
        "bloquear pc",
        "limpar logs",
        "limpar habitos",
        "limpar autoexecucoes",
        "apagar rotina",
        "apagar missao",
        "apagar comando",
    ]

    return any(comando.startswith(c) for c in comandos_sensiveis)


def registrar_confirmacao_pendente(comando: str):
    global _confirmacao_pendente
    _confirmacao_pendente = comando.strip()
    return f"Comando sensível detectado: '{comando}'. Responda 'sim' para confirmar ou 'nao' para cancelar."


def tem_confirmacao_pendente():
    return _confirmacao_pendente is not None


def resolver_confirmacao(resposta: str):
    global _confirmacao_pendente

    resposta = resposta.lower().strip()

    if _confirmacao_pendente is None:
        return False, None, None

    comando = _confirmacao_pendente

    if resposta in ["sim", "s", "confirmar", "ok"]:
        _confirmacao_pendente = None
        return True, comando, "Confirmado."

    if resposta in ["nao", "não", "n", "cancelar"]:
        _confirmacao_pendente = None
        return True, None, "Operação cancelada."

    return False, None, None