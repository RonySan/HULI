from modules.automation import (
    clicar,
    duplo_clique,
    clique_direito,
    mover_mouse,
    digitar_texto,
    pressionar_tecla,
    pressionar_atalho,
    rolar,
    posicao_mouse,
)


def clique():
    return clicar()


def clique_duplo():
    return duplo_clique()


def clique_direito_mouse():
    return clique_direito()


def mover(x, y):
    return mover_mouse(x, y)


def digitar(texto):
    return digitar_texto(texto)


def pressionar(texto):
    if " " in texto:
        teclas = texto.split()
        return pressionar_atalho(*teclas)

    return pressionar_tecla(texto)


def scroll(direcao):
    return rolar(direcao)


def posicao():
    return posicao_mouse()