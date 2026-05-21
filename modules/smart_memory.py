import json
import os
from datetime import datetime

ARQUIVO = os.path.join(os.path.dirname(__file__), "smart_memory.json")


def carregar():
    if not os.path.exists(ARQUIVO):
        return {
            "pessoas": {},
            "preferencias": {},
            "eventos": [],
            "observacoes": []
        }

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "pessoas": {},
            "preferencias": {},
            "eventos": [],
            "observacoes": []
        }


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def lembrar_pessoa(nome, relacao="conhecido", observacao=""):
    dados = carregar()

    nome = nome.lower().strip()

    dados["pessoas"][nome] = {
        "nome": nome.title(),
        "relacao": relacao,
        "observacao": observacao,
        "registrado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    salvar(dados)

    return f"Aprendi quem é {nome.title()}."


def buscar_pessoa(nome):
    dados = carregar()
    nome = nome.lower().strip()

    return dados["pessoas"].get(nome)


def listar_pessoas():
    dados = carregar()

    if not dados["pessoas"]:
        return "Ainda não conheço nenhuma pessoa registrada."

    resposta = "Pessoas que eu conheço:\n"

    for pessoa in dados["pessoas"].values():
        resposta += f"- {pessoa['nome']} ({pessoa['relacao']})"

        if pessoa.get("observacao"):
            resposta += f": {pessoa['observacao']}"

        resposta += "\n"

    return resposta


def lembrar_preferencia(chave, valor):
    dados = carregar()

    dados["preferencias"][chave.lower().strip()] = valor.strip()

    salvar(dados)

    return f"Preferência salva: {chave} = {valor}"


def listar_memoria_inteligente():
    dados = carregar()

    resposta = "Memória inteligente:\n\n"

    resposta += "Pessoas:\n"
    if dados["pessoas"]:
        for pessoa in dados["pessoas"].values():
            resposta += f"- {pessoa['nome']} ({pessoa['relacao']})\n"
    else:
        resposta += "- Nenhuma pessoa registrada.\n"

    resposta += "\nPreferências:\n"
    if dados["preferencias"]:
        for k, v in dados["preferencias"].items():
            resposta += f"- {k}: {v}\n"
    else:
        resposta += "- Nenhuma preferência registrada.\n"

    return resposta