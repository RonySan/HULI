import time

from modules.vision_advanced import listar_textos_tela, procurar_texto_na_tela, clicar_texto_na_tela
from modules.automation import pressionar_tecla, digitar_texto


def encontrar_na_tela(texto):
    ok, resposta, dados = procurar_texto_na_tela(texto)

    if ok:
        return True, resposta

    return False, f"Não encontrei '{texto}' na tela."


def clicar_quando_aparecer(texto, tentativas=8, intervalo=1.5):
    for _ in range(tentativas):
        try:
            resposta = clicar_texto_na_tela(texto)

            if "clic" in resposta.lower() or "sucesso" in resposta.lower():
                return resposta

        except Exception:
            pass

        time.sleep(intervalo)

    return f"Não consegui clicar em '{texto}'."


def ler_e_resumir_tela():
    try:
        return listar_textos_tela()
    except Exception:
        return "Não consegui ler os textos da tela."


def preencher_campo_por_texto(nome_campo, valor):
    clique = clicar_quando_aparecer(nome_campo)

    time.sleep(1)

    digitar_texto(valor)
    pressionar_tecla("enter")

    return f"Tentei preencher '{nome_campo}' com '{valor}'."