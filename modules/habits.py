import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "habitos.json")


def carregar():
    if not os.path.exists(ARQUIVO):
        return {}

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def registrar_sequencia(anterior, atual):
    if not anterior or not atual:
        return

    dados = carregar()

    if anterior not in dados:
        dados[anterior] = {}

    if atual not in dados[anterior]:
        dados[anterior][atual] = 0

    dados[anterior][atual] += 1

    salvar(dados)


def sugerir_proximo(comando):
    dados = carregar()

    if comando not in dados:
        return None

    proximos = dados[comando]

    if not proximos:
        return None

    # pega o mais usado
    sugestao = max(proximos, key=proximos.get)

    if proximos[sugestao] >= 2:
        return sugestao

    return None


def listar_habitos():
    return carregar()


def limpar_habitos():
    salvar({})
    return "Memória de hábitos limpa."