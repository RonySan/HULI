import json
import os

ARQUIVO = os.path.join(os.path.dirname(__file__), "habits.json")


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
        json.dump(dados, f, indent=4, ensure_ascii=False)


def registrar_sequencia(comando_anterior, comando_atual):
    if not comando_anterior or not comando_atual:
        return

    comando_anterior = comando_anterior.strip().lower()
    comando_atual = comando_atual.strip().lower()

    dados = carregar()

    if comando_anterior not in dados:
        dados[comando_anterior] = {}

    if comando_atual not in dados[comando_anterior]:
        dados[comando_anterior][comando_atual] = 0

    dados[comando_anterior][comando_atual] += 1
    salvar(dados)


def prever_proximo(comando, minimo=2):
    comando = comando.strip().lower()
    dados = carregar()

    if comando not in dados:
        return None

    proximos = dados[comando]
    if not proximos:
        return None

    sugestao = max(proximos, key=proximos.get)

    if proximos[sugestao] >= minimo:
        return sugestao

    return None


def listar_habitos():
    return carregar()


def limpar_habitos():
    salvar({})
    return "Memória de hábitos limpa com sucesso."