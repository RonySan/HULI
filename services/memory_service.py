from modules.smart_memory import (
    lembrar_pessoa,
    buscar_pessoa,
    listar_pessoas,
    lembrar_preferencia,
    listar_memoria_inteligente,
)


def salvar_pessoa(nome, relacao):
    return lembrar_pessoa(nome, relacao)


def procurar_pessoa(nome):
    return buscar_pessoa(nome)


def pessoas():
    return listar_pessoas()


def salvar_preferencia(chave, valor):
    return lembrar_preferencia(chave, valor)


def memoria():
    return listar_memoria_inteligente()