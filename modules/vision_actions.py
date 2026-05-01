import time

from modules.vision_advanced import procurar_texto_na_tela, clicar_texto_na_tela
from modules.automation import digitar_texto, pressionar_tecla


def aguardar_texto(texto_alvo, tentativas=5, intervalo=1.5):
    for _ in range(tentativas):
        ok, resposta, pos = procurar_texto_na_tela(texto_alvo)
        if ok:
            return True, resposta, pos
        time.sleep(intervalo)

    return False, f"Não encontrei o texto '{texto_alvo}' após {tentativas} tentativas.", None


def aguardar_e_clicar_texto(texto_alvo, tentativas=5, intervalo=1.5):
    for _ in range(tentativas):
        resultado = clicar_texto_na_tela(texto_alvo)
        if "Clique realizado" in resultado:
            return resultado
        time.sleep(intervalo)

    return f"Não consegui clicar no texto '{texto_alvo}'."


def digitar_e_confirmar(texto):
    digitar_texto(texto)
    time.sleep(0.5)
    pressionar_tecla("enter")
    return f"Texto digitado e confirmado: {texto}"