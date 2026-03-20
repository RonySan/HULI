import json
import os
import time

from modules.pc_control import abrir_site, abrir_programa
from modules.automation import digitar_texto, pressionar_tecla
from modules.vision_advanced import clicar_texto_na_tela

ARQUIVO_MISSOES = os.path.join(os.path.dirname(__file__), "missions.json")


def carregar_missoes():
    if not os.path.exists(ARQUIVO_MISSOES):
        return {}

    try:
        with open(ARQUIVO_MISSOES, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salvar_missoes(dados):
    with open(ARQUIVO_MISSOES, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def salvar_missao(nome, passos):
    dados = carregar_missoes()
    dados[nome.lower().strip()] = passos
    salvar_missoes(dados)
    return f"Missão '{nome}' salva com sucesso."


def listar_missoes():
    return list(carregar_missoes().keys())


def apagar_missao(nome):
    dados = carregar_missoes()
    chave = nome.lower().strip()

    if chave not in dados:
        return False, f"Não encontrei a missão '{nome}'."

    del dados[chave]
    salvar_missoes(dados)
    return True, f"Missão '{nome}' removida com sucesso."


def executar_passos(passos):
    for passo in passos:
        acao = passo.get("acao", "").strip().lower()
        valor = passo.get("valor", "")

        if acao == "abrir_site":
            abrir_site(valor)
            time.sleep(2)

        elif acao == "abrir_programa":
            abrir_programa(valor)
            time.sleep(2)

        elif acao == "digitar":
            digitar_texto(valor)
            time.sleep(1)

        elif acao == "tecla":
            pressionar_tecla(valor)
            time.sleep(1)

        elif acao == "clicar_texto":
            clicar_texto_na_tela(valor)
            time.sleep(2)

    return "Missão executada com sucesso."


def executar_missao_salva(nome):
    dados = carregar_missoes()
    chave = nome.lower().strip()

    if chave not in dados:
        return False, f"Não encontrei a missão '{nome}'."

    resposta = executar_passos(dados[chave])
    return True, resposta


def criar_missao_pesquisa(nome, termo):
    passos = [
        {"acao": "abrir_site", "valor": "google"},
        {"acao": "digitar", "valor": termo},
        {"acao": "tecla", "valor": "enter"},
    ]
    return salvar_missao(nome, passos)


def criar_missao_simples(nome, destino):
    destino = destino.strip().lower()

    if destino in ["github", "gmail", "youtube", "chatgpt", "google", "netflix"]:
        passos = [{"acao": "abrir_site", "valor": destino}]
    else:
        passos = [{"acao": "abrir_programa", "valor": destino}]

    return salvar_missao(nome, passos)


def interpretar_missao_rapida(texto):
    texto = texto.lower().strip()

    if texto.startswith("missao pesquisar "):
        termo = texto.replace("missao pesquisar ", "", 1).strip()
        return [
            {"acao": "abrir_site", "valor": "google"},
            {"acao": "digitar", "valor": termo},
            {"acao": "tecla", "valor": "enter"},
        ]

    if texto == "missao abrir github":
        return [{"acao": "abrir_site", "valor": "github"}]

    if texto == "missao abrir gmail":
        return [{"acao": "abrir_site", "valor": "gmail"}]

    if texto == "missao abrir youtube":
        return [{"acao": "abrir_site", "valor": "youtube"}]

    if texto == "missao abrir chatgpt":
        return [{"acao": "abrir_site", "valor": "chatgpt"}]

    if texto == "missao abrir netflix":
        return [{"acao": "abrir_site", "valor": "netflix"}]

    if texto.startswith("missao clicar "):
        alvo = texto.replace("missao clicar ", "", 1).strip()
        return [{"acao": "clicar_texto", "valor": alvo}]

    return None


def interpretar_missao_multietapa(texto):
    texto = texto.lower().strip()

    # normaliza vírgulas para facilitar
    texto = texto.replace(",", "")

    # google + pesquisa + clique
    if texto.startswith("abra o google e pesquise ") and " e clique em " in texto:
        resto = texto.replace("abra o google e pesquise ", "", 1)
        termo, clique = resto.split(" e clique em ", 1)
        return [
            {"acao": "abrir_site", "valor": "google"},
            {"acao": "digitar", "valor": termo.strip()},
            {"acao": "tecla", "valor": "enter"},
            {"acao": "clicar_texto", "valor": clique.strip()},
        ]

    # github/gmail/youtube/chatgpt/netflix + clique
    gatilhos_site = {
        "abra o github e clique em ": "github",
        "abra o gmail e clique em ": "gmail",
        "abra o youtube e clique em ": "youtube",
        "abra o chatgpt e clique em ": "chatgpt",
        "abra o netflix e clique em ": "netflix",
    }

    for gatilho, site in gatilhos_site.items():
        if texto.startswith(gatilho):
            alvo = texto.replace(gatilho, "", 1).strip()
            return [
                {"acao": "abrir_site", "valor": site},
                {"acao": "clicar_texto", "valor": alvo},
            ]

    # youtube + pesquisar
    if texto.startswith("abra o youtube e pesquise "):
        termo = texto.replace("abra o youtube e pesquise ", "", 1).strip()
        return [
            {"acao": "abrir_site", "valor": "youtube"},
            {"acao": "digitar", "valor": termo},
            {"acao": "tecla", "valor": "enter"},
        ]

    return None


def executar_missao_rapida(texto):
    passos = interpretar_missao_multietapa(texto)

    if not passos:
        passos = interpretar_missao_rapida(texto)

    if not passos:
        return "Missão não reconhecida."

    return executar_passos(passos)