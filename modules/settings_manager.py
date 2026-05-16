import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")
ARQUIVO = os.path.join(CONFIG_DIR, "settings.json")


PADRAO = {
    "usuario": "Rony",
    "empresa": "Impulso Digital",
    "assistente_nome": "H.U.L.I",
    "voz_ativa": True,
    "limite_fala": 250,
    "escuta_continua": False,
    "modo_conversa": False,
    "personalidade": "huli",
    "debug": True,
    "modo_protecao": False,
    "bluetooth_dispositivo_padrao": "MUNDIAL",
    "iniciar_com_windows": False
}


def garantir_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)

    if not os.path.exists(ARQUIVO):
        salvar_config(PADRAO)

    return True


def carregar_config():
    garantir_config()

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            dados = json.load(f)

        for chave, valor in PADRAO.items():
            if chave not in dados:
                dados[chave] = valor

        salvar_config(dados)
        return dados

    except Exception:
        salvar_config(PADRAO)
        return PADRAO.copy()


def salvar_config(dados):
    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def obter(chave, padrao=None):
    dados = carregar_config()
    return dados.get(chave, padrao)


def definir(chave, valor):
    dados = carregar_config()
    dados[chave] = valor
    salvar_config(dados)
    return f"Configuração atualizada: {chave} = {valor}"


def listar_config():
    return carregar_config()


def ativar(chave):
    return definir(chave, True)


def desativar(chave):
    return definir(chave, False)