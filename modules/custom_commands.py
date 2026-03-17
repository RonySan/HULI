import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "custom_commands.json")


def carregar_comandos_personalizados():
    if not os.path.exists(ARQUIVO):
        return {}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salvar_comandos_personalizados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def criar_comando_personalizado(nome: str, comando: str):
    dados = carregar_comandos_personalizados()
    dados[nome.lower().strip()] = comando.strip().lower()
    salvar_comandos_personalizados(dados)
    return f"Comando personalizado '{nome}' criado com sucesso."


def listar_comandos_personalizados():
    return carregar_comandos_personalizados()


def apagar_comando_personalizado(nome: str):
    dados = carregar_comandos_personalizados()
    chave = nome.lower().strip()

    if chave not in dados:
        return False, f"Não encontrei o comando personalizado '{nome}'."

    del dados[chave]
    salvar_comandos_personalizados(dados)
    return True, f"Comando personalizado '{nome}' removido com sucesso."


def resolver_comando_personalizado(texto: str):
    dados = carregar_comandos_personalizados()
    return dados.get(texto.lower().strip())