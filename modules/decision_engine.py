def decidir_abrir_ou_pesquisar(destino, abrir_site_func, abrir_programa_func, pesquisar_web_func):
    destino = destino.strip().lower()

    ok_site, resposta_site = abrir_site_func(destino)
    if ok_site:
        return resposta_site

    ok_prog, resposta_prog = abrir_programa_func(destino)
    if ok_prog:
        return resposta_prog

    _, resposta_web = pesquisar_web_func(destino)
    return resposta_web


def precisa_busca_web(texto: str):
    texto = texto.lower().strip()

    gatilhos = [
        " no google",
        "pesquise ",
        "pesquisar ",
        "procure ",
        "procurar ",
    ]

    return any(g in texto for g in gatilhos)