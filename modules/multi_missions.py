def separar_passos(comando: str):
    texto = comando.lower().strip()

    separadores = [
        " depois ",
        " e depois ",
        " em seguida ",
        " aí ",
        " ai ",
    ]

    for sep in separadores:
        texto = texto.replace(sep, " | ")

    return [p.strip() for p in texto.split("|") if p.strip()]


def executar_multi_missao(comando: str, processar_func):
    passos = separar_passos(comando)

    if len(passos) <= 1:
        return "Não encontrei múltiplos passos."

    respostas = "Multi missão executada:\n\n"

    for i, passo in enumerate(passos, 1):
        try:
            resposta = processar_func(passo)
            respostas += f"{i}. {passo} -> {resposta}\n"
        except Exception as e:
            respostas += f"{i}. {passo} -> erro: {e}\n"

    return respostas