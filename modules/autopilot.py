import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "autopilot.json")


def carregar_autopilot():
    if not os.path.exists(ARQUIVO):
        return {}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salvar_autopilot(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def ativar_autoexecucao(comando_base: str, proximo_comando: str):
    dados = carregar_autopilot()
    dados[comando_base.strip().lower()] = proximo_comando.strip().lower()
    salvar_autopilot(dados)

    return f"Autoexecução ativada: depois de '{comando_base}', vou executar '{proximo_comando}'."


def desativar_autoexecucao(comando_base: str):
    dados = carregar_autopilot()
    chave = comando_base.strip().lower()

    if chave not in dados:
        return False, f"Não existe autoexecução cadastrada para '{comando_base}'."

    del dados[chave]
    salvar_autopilot(dados)
    return True, f"Autoexecução removida para '{comando_base}'."


def obter_autoexecucao(comando_base: str):
    dados = carregar_autopilot()
    return dados.get(comando_base.strip().lower())


def listar_autoexecucoes():
    return carregar_autopilot()


def limpar_autoexecucoes():
    salvar_autopilot({})
    return "Todas as autoexecuções foram removidas."