import os
from datetime import datetime

import mss
import pyautogui
import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def capturar_tela(caminho_arquivo=None):
    if caminho_arquivo is None:
        caminho_arquivo = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img.save(caminho_arquivo)

    return caminho_arquivo


def tirar_print():
    try:
        caminho = capturar_tela()
        return f"Screenshot salvo como {caminho}"
    except Exception:
        return "Não consegui capturar a tela."


def ler_tela():
    try:
        caminho = capturar_tela()
        img = Image.open(caminho)
        texto = pytesseract.image_to_string(img, lang="por+eng")

        if not texto.strip():
            return "Não consegui ler texto na tela."

        return texto[:1000]
    except Exception:
        return "Não consegui ler a tela."


def listar_textos_tela():
    try:
        caminho = capturar_tela()
        img = Image.open(caminho)

        dados = pytesseract.image_to_data(
            img,
            lang="por+eng",
            output_type=pytesseract.Output.DICT
        )

        encontrados = []
        total = len(dados["text"])

        for i in range(total):
            texto = str(dados["text"][i]).strip()
            conf = dados["conf"][i]

            if texto and conf != "-1":
                encontrados.append(texto)

        if not encontrados:
            return "Não encontrei textos úteis na tela."

        # remove duplicados preservando ordem
        unicos = []
        vistos = set()
        for t in encontrados:
            chave = t.lower()
            if chave not in vistos:
                vistos.add(chave)
                unicos.append(t)

        resposta = "Textos encontrados na tela:\n"
        for item in unicos[:50]:
            resposta += f"- {item}\n"

        return resposta
    except Exception:
        return "Não consegui listar os textos da tela."


def procurar_texto_na_tela(texto_alvo):
    try:
        caminho = capturar_tela()
        img = Image.open(caminho)

        dados = pytesseract.image_to_data(
            img,
            lang="por+eng",
            output_type=pytesseract.Output.DICT
        )

        texto_alvo = texto_alvo.lower().strip()
        total = len(dados["text"])

        for i in range(total):
            texto = str(dados["text"][i]).strip().lower()

            if texto and texto_alvo in texto:
                x = dados["left"][i]
                y = dados["top"][i]
                w = dados["width"][i]
                h = dados["height"][i]

                centro_x = x + w // 2
                centro_y = y + h // 2

                return True, f"Texto '{texto_alvo}' encontrado em {centro_x}, {centro_y}", (centro_x, centro_y)

        return False, f"Não encontrei o texto '{texto_alvo}' na tela.", None
    except Exception:
        return False, "Não consegui procurar o texto na tela.", None


def clicar_texto_na_tela(texto_alvo):
    try:
        ok, resposta, pos = procurar_texto_na_tela(texto_alvo)

        if not ok or not pos:
            return resposta

        x, y = pos
        pyautogui.click(x, y)

        return f"Clique realizado no texto '{texto_alvo}' em {x}, {y}."
    except Exception:
        return f"Não consegui clicar no texto '{texto_alvo}'."