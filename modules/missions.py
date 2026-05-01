import json
import os
import time

from modules.pc_control import abrir_site, abrir_programa, pesquisar_web
from modules.automation import digitar_texto, pressionar_tecla
from modules.vision_advanced import clicar_texto_na_tela
from modules.vision_actions import aguardar_e_clicar_texto
from modules.decision_engine import decidir_abrir_ou_pesquisar
from modules.logger import registrar_log

ARQUIVO_MISSOES = os.path.join(os.path.dirname(__file__), "missions.json")


# -------------------------
# ARQUIVO
# -------------------------
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


# -------------------------
# CRUD MISSÕES
# -------------------------
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


# -------------------------
# EXECUÇÃO
# -------------------------
def executar_passos(passos):
    for i, passo in enumerate(passos, 1):
        try:
            acao = passo.get("acao", "").strip().lower()
            valor = passo.get("valor", "")

            registrar_log("missao", f"Passo {i}: {acao} -> {valor}")

            if acao == "abrir_site":
                abrir_site(valor)
                time.sleep(2)

            elif acao == "abrir_programa":
                abrir_programa(valor)
                time.sleep(2)

            elif acao == "abrir_ou_pesquisar":
                resultado = decidir_abrir_ou_pesquisar(
                    valor,
                    abrir_site,
                    abrir_programa,
                    pesquisar_web
                )
                registrar_log("missao", f"Resultado: {resultado}")
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

            elif acao == "aguardar_clicar_texto":
                aguardar_e_clicar_texto(valor)
                time.sleep(2)

            else:
                registrar_log("erro", f"Ação desconhecida: {acao}")

        except Exception as e:
            registrar_log("erro", f"Erro no passo {i}: {str(e)}")
            return f"Erro na missão no passo {i}: {acao}"

    return "Missão executada com sucesso."


def executar_missao_salva(nome):
    dados = carregar_missoes()
    chave = nome.lower().strip()

    if chave not in dados:
        return False, f"Não encontrei a missão '{nome}'."

    resposta = executar_passos(dados[chave])
    return True, resposta


# -------------------------
# CRIAÇÃO DE MISSÕES
# -------------------------
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


# -------------------------
# MISSÃO RÁPIDA
# -------------------------
def interpretar_missao_rapida(texto):
    texto = texto.lower().strip().replace(",", "")

    if texto.startswith("missao pesquisar "):
        termo = texto.replace("missao pesquisar ", "", 1).strip()
        return [
            {"acao": "abrir_site", "valor": "google"},
            {"acao": "digitar", "valor": termo},
            {"acao": "tecla", "valor": "enter"},
        ]

    if texto.startswith("missao clicar "):
        alvo = texto.replace("missao clicar ", "", 1).strip()
        return [{"acao": "clicar_texto", "valor": alvo}]

    if texto.startswith("missao abrir "):
        destino = texto.replace("missao abrir ", "", 1).strip()
        return [{"acao": "abrir_ou_pesquisar", "valor": destino}]

    return None


# -------------------------
# MISSÃO MULTIETAPA
# -------------------------
def interpretar_missao_multietapa(texto):
    texto = texto.lower().strip().replace(",", "")

    if texto.startswith("abra o google e pesquise ") and " e clique em " in texto:
        resto = texto.replace("abra o google e pesquise ", "", 1)
        termo, clique = resto.split(" e clique em ", 1)

        return [
            {"acao": "abrir_site", "valor": "google"},
            {"acao": "digitar", "valor": termo.strip()},
            {"acao": "tecla", "valor": "enter"},
            {"acao": "aguardar_clicar_texto", "valor": clique.strip()},
        ]

    if texto.startswith("abra o youtube e pesquise "):
        termo = texto.replace("abra o youtube e pesquise ", "", 1).strip()

        return [
            {"acao": "abrir_site", "valor": "youtube"},
            {"acao": "digitar", "valor": termo},
            {"acao": "tecla", "valor": "enter"},
        ]

    return None


# -------------------------
# EXECUTOR RÁPIDO
# -------------------------
def executar_missao_rapida(texto):
    passos = interpretar_missao_multietapa(texto)

    if not passos:
        passos = interpretar_missao_rapida(texto)

    if not passos:
        return "Missão não reconhecida."

    return executar_passos(passos)