from modules.pc_control import abrir_site, pesquisar_web


def abrir_google_e_pesquisar(termo: str):
    abrir_site("google")
    return pesquisar_web(termo)[1]


def pesquisar_no_google(termo: str):
    return pesquisar_web(termo)[1]


def abrir_destino_ou_pesquisar(destino: str):
    ok, resposta = abrir_site(destino)
    if ok:
        return resposta

    return pesquisar_web(destino)[1]