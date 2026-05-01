import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "user_profile.json")


def carregar_perfil():
    if not os.path.exists(ARQUIVO):
        return {}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salvar_perfil(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def definir_valor(chave, valor):
    dados = carregar_perfil()
    dados[chave] = valor
    salvar_perfil(dados)
    return f"Perfil atualizado: {chave} = {valor}"


def obter_valor(chave, padrao=None):
    dados = carregar_perfil()
    return dados.get(chave, padrao)


def listar_perfil():
    return carregar_perfil()


def limpar_perfil():
    salvar_perfil({})
    return "Perfil do usuário limpo com sucesso."