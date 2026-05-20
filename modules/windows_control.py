import subprocess
import time

from modules.vision_actions import aguardar_e_clicar_texto
from modules.logger import registrar_log


def abrir_bluetooth():
    try:
        subprocess.Popen("start ms-settings:bluetooth", shell=True)
        time.sleep(3)
        return "Abrindo configurações de Bluetooth."
    except Exception as e:
        registrar_log("erro", f"abrir_bluetooth: {e}")
        return "Não consegui abrir o Bluetooth."


def conectar_bluetooth(nome: str):
    nome = nome.strip()

    if not nome:
        return "Informe o nome do dispositivo Bluetooth."

    abrir_bluetooth()

    resultado = aguardar_e_clicar_texto(nome, tentativas=6, intervalo=2)

    time.sleep(2)

    aguardar_e_clicar_texto("Conectar", tentativas=3, intervalo=1)

    return f"Tentei conectar ao Bluetooth: {nome}."


def conectar_bluetooth_padrao():
    from modules.settings_manager import obter

    nome = obter("bluetooth_dispositivo_padrao", "MUNDIAL")
    return conectar_bluetooth(nome)


def abrir_som():
    subprocess.Popen("start ms-settings:sound", shell=True)
    return "Abrindo configurações de som."


def abrir_wifi():
    subprocess.Popen("start ms-settings:network-wifi", shell=True)
    return "Abrindo configurações de Wi-Fi."