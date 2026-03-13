import re


def normalizar_comando_natural(texto: str) -> str:
    texto = texto.lower().strip()

    # remove pontuação leve
    texto = re.sub(r"[^\w\sáàâãéêíóôõúç]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()

    # frases comuns -> comandos diretos
    substituicoes = {
        "que horas sao agora": "que horas sao",
        "que horas sao": "que horas sao",
        "que horas e": "que horas sao",
        "que horas e agora": "que horas sao",
        "me mostra os programas": "listar programas",
        "mostra os programas": "listar programas",
        "quais programas voce conhece": "listar programas",
        "lista de programas": "listar programas",
        "abre o navegador": "abrir navegador",
        "abre navegador": "abrir navegador",
        "pode abrir o navegador": "abrir navegador",
        "pode abrir o navegador pra mim": "abrir navegador",
        "abre meu github": "abrir github",
        "abre o github": "abrir github",
        "abre o gmail": "abrir gmail",
        "abre o youtube": "abrir youtube",
        "abre o vscode": "abrir vscode",
        "pode abrir o vscode": "abrir vscode",
        "me ajuda": "ajuda",
        "pode me ajudar": "ajuda",
    }

    if texto in substituicoes:
        return substituicoes[texto]

    # padrões genéricos
    texto = re.sub(r"^pode abrir o ", "abrir ", texto)
    texto = re.sub(r"^pode abrir a ", "abrir ", texto)
    texto = re.sub(r"^pode abrir ", "abrir ", texto)
    texto = re.sub(r"^abre o ", "abrir ", texto)
    texto = re.sub(r"^abre a ", "abrir ", texto)
    texto = re.sub(r"^abre meu ", "abrir ", texto)
    texto = re.sub(r"^abre minha ", "abrir ", texto)
    texto = re.sub(r"^me mostra os ", "listar ", texto)
    texto = re.sub(r"^me mostra ", "mostrar ", texto)

    # limpeza final
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto