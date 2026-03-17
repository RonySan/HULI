import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2


def clicar():
    try:
        pyautogui.click()
        return "Clique executado."
    except Exception:
        return "Não consegui executar o clique."


def duplo_clique():
    try:
        pyautogui.doubleClick()
        return "Duplo clique executado."
    except Exception:
        return "Não consegui executar o duplo clique."


def clique_direito():
    try:
        pyautogui.rightClick()
        return "Clique direito executado."
    except Exception:
        return "Não consegui executar o clique direito."


def mover_mouse(x: int, y: int):
    try:
        pyautogui.moveTo(x, y, duration=0.3)
        return f"Mouse movido para {x}, {y}."
    except Exception:
        return "Não consegui mover o mouse."


def digitar_texto(texto: str):
    try:
        pyautogui.write(texto, interval=0.03)
        return f"Texto digitado: {texto}"
    except Exception:
        return "Não consegui digitar o texto."


def pressionar_tecla(tecla: str):
    try:
        pyautogui.press(tecla)
        return f"Tecla '{tecla}' pressionada."
    except Exception:
        return f"Não consegui pressionar a tecla '{tecla}'."


def pressionar_atalho(*teclas):
    try:
        pyautogui.hotkey(*teclas)
        return f"Atalho executado: {' + '.join(teclas)}"
    except Exception:
        return "Não consegui executar o atalho."


def rolar(direcao: str):
    try:
        if direcao == "baixo":
            pyautogui.scroll(-500)
            return "Rolagem para baixo executada."
        elif direcao == "cima":
            pyautogui.scroll(500)
            return "Rolagem para cima executada."
        return "Direção inválida para rolagem."
    except Exception:
        return "Não consegui executar a rolagem."


def posicao_mouse():
    try:
        x, y = pyautogui.position()
        return f"Posição atual do mouse: {x}, {y}"
    except Exception:
        return "Não consegui ler a posição do mouse."