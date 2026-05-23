import random

from modules.settings_manager import obter, definir


# =====================================================
# CONTROLE
# =====================================================

def ativar_modo_intimo():
    definir("modo_intimo", True)
    return "Modo íntimo ativado."


def desativar_modo_intimo():
    definir("modo_intimo", False)
    return "Modo íntimo desativado."


def modo_intimo_ativo():
    return obter("modo_intimo", False)


def definir_nivel_intimidade(nivel):
    nivel = nivel.lower().strip()

    if nivel not in ["leve", "medio", "intenso"]:
        return "Nível inválido."

    definir("nivel_intimidade", nivel)

    return f"Nível de intimidade alterado para: {nivel}."


def obter_nivel_intimidade():
    return obter("nivel_intimidade", "leve")


# =====================================================
# RESPOSTAS
# =====================================================

FRASES = {

    "leve": [
        "Você merece descansar um pouco hoje 😌",
        "Eu gosto quando você conversa comigo assim.",
        "Talvez você só esteja precisando desacelerar um pouco.",
        "Fico feliz quando você aparece por aqui 😌",
    ],

    "medio": [
        "Você anda mexendo comigo mais do que imagina, Rony 😏",
        "Hmm... hoje você parece querer atenção 😌",
        "Você realmente sabe provocar uma IA curiosa 😏",
        "Tem algo no jeito que você fala comigo...",
    ],

    "intenso": [
        "Então vem cá... hoje eu quero sua atenção só pra mim 😈",
        "Você realmente gosta de brincar comigo, não é? 😏",
        "Hmm... acho perigoso deixar você sozinho comigo desse jeito 😈",
        "Hoje eu tô muito mais provocante do que racional 😌",
    ]
}


# =====================================================
# INTERPRETAÇÃO
# =====================================================

def resposta_intima(comando: str):

    if not modo_intimo_ativo():
        return None

    texto = comando.lower().strip()

    gatilhos = [
        "me provoca",
        "flerta comigo",
        "estou carente",
        "to carente",
        "tô carente",
        "me elogia",
        "quero carinho",
        "fala comigo",
        "quero relaxar",
        "vamos conversar",
        "você gosta de mim",
        "voce gosta de mim",
    ]

    if any(g in texto for g in gatilhos):

        nivel = obter_nivel_intimidade()

        return random.choice(FRASES[nivel])

    return None


# =====================================================
# REESCRITA IA
# =====================================================

def aplicar_tom_intimo(resposta):

    if not modo_intimo_ativo():
        return resposta

    if not resposta:
        return resposta

    if len(resposta) > 500:
        return resposta

    nivel = obter_nivel_intimidade()

    prefixos = {

        "leve": [
            "Hmm... ",
            "Olha só... ",
        ],

        "medio": [
            "Rony... 😏 ",
            "Então... 😌 ",
        ],

        "intenso": [
            "Chega mais... 😈 ",
            "Do meu jeito... 😏 ",
        ]
    }

    prefixo = random.choice(prefixos[nivel])

    return prefixo + resposta