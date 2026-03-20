def interpretar_intencao(texto: str):
    texto = texto.lower().strip()

    # -------------------------
    # Pesquisa composta (tem prioridade máxima)
    # -------------------------
    gatilhos_pesquisa_composta = [
        "abra o google e pesquise ",
        "abrir o google e pesquise ",
        "abrir o google e pesquisar ",
        "abre o google e pesquise ",
        "abre o google e pesquisar ",
    ]

    for gatilho in gatilhos_pesquisa_composta:
        if texto.startswith(gatilho):
            termo = texto.replace(gatilho, "", 1).strip()
            if termo:
                return {"tipo": "pesquisa", "valor": termo}

    # -------------------------
    # Pesquisa simples
    # -------------------------
    gatilhos_pesquisa = [
        "pesquise ",
        "pesquisar ",
        "procure ",
        "procurar ",
    ]

    for gatilho in gatilhos_pesquisa:
        if texto.startswith(gatilho):
            termo = texto.replace(gatilho, "", 1).strip()
            if termo:
                return {"tipo": "pesquisa", "valor": termo}

    # -------------------------
    # Abrir site direto
    # -------------------------
    if texto in ["abra o github", "abrir github", "abre github", "abrir o github", "abre o github"]:
        return {"tipo": "site", "valor": "github"}

    if texto in ["abra o gmail", "abrir gmail", "abre gmail", "abrir o gmail", "abre o gmail"]:
        return {"tipo": "site", "valor": "gmail"}

    if texto in ["abra o youtube", "abrir youtube", "abre youtube", "abrir o youtube", "abre o youtube"]:
        return {"tipo": "site", "valor": "youtube"}

    if texto in ["abra o chatgpt", "abrir chatgpt", "abre chatgpt", "abrir o chatgpt", "abre o chatgpt"]:
        return {"tipo": "site", "valor": "chatgpt"}

    if texto in ["abra o google", "abrir google", "abre google", "abrir o google", "abre o google"]:
        return {"tipo": "site", "valor": "google"}

    # -------------------------
    # Abrir genérico
    # -------------------------
    gatilhos_abrir = [
        "abra o ",
        "abra a ",
        "abrir o ",
        "abrir a ",
        "abre o ",
        "abre a ",
        "abra ",
        "abrir ",
        "abre ",
    ]

    for gatilho in gatilhos_abrir:
        if texto.startswith(gatilho):
            destino = texto.replace(gatilho, "", 1).strip()
            if destino:
                return {"tipo": "abrir", "valor": destino}

    return None