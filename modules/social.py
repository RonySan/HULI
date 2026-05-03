def limpar_nome(texto):
    texto = texto.strip()
    removiveis = [
        "minha namorada",
        "meu namorado",
        "minha esposa",
        "meu esposo",
        "minha amiga",
        "meu amigo",
        "para",
        "pra",
    ]

    for item in removiveis:
        texto = texto.replace(item, "")

    return texto.strip().title()


def se_apresentar_para(nome):
    nome = limpar_nome(nome)

    if not nome:
        return "Para quem você quer que eu me apresente?"

    return (
        f"Olá, {nome}! Tudo bem?\n"
        "Eu sou a H.U.L.I, que significa Humano Único Leal Inteligente.\n"
        "Sou a assistente inteligente do Rony, criada para ajudar, organizar, automatizar tarefas "
        "e evoluir junto com ele.\n"
        "É um prazer falar com você."
    )


def cumprimentar(nome):
    nome = limpar_nome(nome)

    if not nome:
        return "Quem você quer que eu cumprimente?"

    return f"Oi, {nome}! Tudo bem? Eu sou a H.U.L.I. O Rony pediu para eu te mandar um oi com carinho."


def elogiar(nome):
    nome = limpar_nome(nome)

    if not nome:
        return "Quem você quer que eu elogie?"

    return (
        f"{nome}, o Rony fala de você com muito carinho. "
        "Espero que seu dia seja leve, bonito e cheio de coisas boas."
    )


def recado(nome, mensagem):
    nome = limpar_nome(nome)

    if not nome:
        return "Para quem é o recado?"

    if not mensagem:
        return f"O que você quer que eu diga para {nome}?"

    return f"{nome}, o Rony pediu para eu te dizer: {mensagem}"