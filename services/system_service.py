from modules.system_monitor import status_sistema
from modules.windows_control import (
    abrir_bluetooth,
    conectar_bluetooth,
    conectar_bluetooth_padrao,
    abrir_som,
    abrir_wifi,
)
from modules.system_control import (
    desligar_pc,
    reiniciar_pc,
    bloquear_pc,
    cancelar_desligamento,
)


def status():
    return status_sistema()


def bluetooth_abrir():
    return abrir_bluetooth()


def bluetooth_conectar(nome=None):
    if nome:
        return conectar_bluetooth(nome)

    return conectar_bluetooth_padrao()


def som_abrir():
    return abrir_som()


def wifi_abrir():
    return abrir_wifi()


def desligar():
    return desligar_pc()


def reiniciar():
    return reiniciar_pc()


def bloquear():
    return bloquear_pc()


def cancelar_desligar():
    return cancelar_desligamento()