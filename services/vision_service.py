from modules.vision_ai import (
    encontrar_na_tela,
    clicar_quando_aparecer,
    ler_e_resumir_tela,
    preencher_campo_por_texto,
)


def ler_tela():
    return ler_e_resumir_tela()


def encontrar(texto):
    ok, resposta = encontrar_na_tela(texto)
    return resposta


def clicar_texto(texto):
    return clicar_quando_aparecer(texto)


def preencher(campo, valor):
    return preencher_campo_por_texto(campo, valor)