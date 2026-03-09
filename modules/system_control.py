import os
import subprocess


def desligar_pc():
    subprocess.Popen("shutdown /s /t 0", shell=True)
    return "Desligando o computador."


def reiniciar_pc():
    subprocess.Popen("shutdown /r /t 0", shell=True)
    return "Reiniciando o computador."


def bloquear_pc():
    subprocess.Popen("rundll32.exe user32.dll,LockWorkStation", shell=True)
    return "Bloqueando o computador."


def cancelar_desligamento():
    subprocess.Popen("shutdown /a", shell=True)
    return "Cancelando desligamento agendado."