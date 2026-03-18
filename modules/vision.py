import pyautogui
import pytesseract
import mss
import cv2
import numpy as np
from datetime import datetime
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def screenshot():

    img = pyautogui.screenshot()

    nome = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    img.save(nome)

    return f"Screenshot salvo como {nome}"


def localizar_imagem(caminho):

    try:

        pos = pyautogui.locateCenterOnScreen(caminho, confidence=0.8)

        if pos:
            return f"Imagem encontrada em {pos}"
        else:
            return "Não encontrei essa imagem na tela."

    except Exception:
        return "Erro ao procurar imagem."


def clicar_imagem(caminho):

    try:

        pos = pyautogui.locateCenterOnScreen(caminho, confidence=0.8)

        if pos:
            pyautogui.click(pos)
            return "Clique realizado na imagem."

        return "Não encontrei a imagem."

    except Exception:
        return "Erro ao clicar na imagem."


def ler_tela():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)

        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

        texto = pytesseract.image_to_string(img)

        if not texto.strip():
            return "Não consegui ler texto na tela."

        return texto[:500]