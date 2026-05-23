from modules.reminder_engine import (
    criar_lembrete,
    listar_lembretes,
    apagar_lembretes,
)


def criar(texto, horario):
    return criar_lembrete(texto, horario)


def listar():
    return listar_lembretes()


def apagar():
    return apagar_lembretes()