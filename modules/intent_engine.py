def interpretar_intencao(texto: str):
    texto = texto.lower().strip()

    # -------------------------
    # Pesquisa composta
    # -------------------------
    gatilhos_pesquisa_composta = [
        "abra o google e pesquise ",
        "abrir o google e pesquise ",
        "abrir o google e pesquisar ",
        "abre o google e pesquise ",
        "abre o google e pesquisar ",
        "huli abrir o google e pesquise ",
        "huli abrir o google e pesquisar ",
    ]

    for gatilho in gatilhos_pesquisa_composta:
        if texto.startswith(gatilho):
            termo = texto.replace(gatilho, "", 1).strip()
            if termo:
                return {"tipo": "pesquisa", "valor": termo}

    # -------------------------
    # Pesquisa tipo "abrir netflix no google"
    # -------------------------
    gatilhos_google = [
        "abrir ",
        "abra ",
        "abre ",
        "abrir a ",
        "abrir o ",
        "abra a ",
        "abra o ",
        "abre a ",
        "abre o ",
        "huli abrir ",
        "huli abra ",
        "huli abre ",
    ]

    for gatilho in gatilhos_google:
        if texto.startswith(gatilho) and " no google" in texto:
            termo = texto.replace(gatilho, "", 1).replace(" no google", "").strip()
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
    if texto in ["abra o github", "abrir github", "abre github", "abrir o github", "abre o github", "huli abrir github"]:
        return {"tipo": "site", "valor": "github"}

    if texto in ["abra o gmail", "abrir gmail", "abre gmail", "abrir o gmail", "abre o gmail", "huli abrir gmail"]:
        return {"tipo": "site", "valor": "gmail"}

    if texto in ["abra o youtube", "abrir youtube", "abre youtube", "abrir o youtube", "abre o youtube", "huli abrir youtube"]:
        return {"tipo": "site", "valor": "youtube"}

    if texto in ["abra o chatgpt", "abrir chatgpt", "abre chatgpt", "abrir o chatgpt", "abre o chatgpt", "huli abrir chatgpt"]:
        return {"tipo": "site", "valor": "chatgpt"}

    if texto in ["abra o google", "abrir google", "abre google", "abrir o google", "abre o google", "huli abrir google"]:
        return {"tipo": "site", "valor": "google"}

    if texto in ["abra o netflix", "abrir netflix", "abre netflix", "abrir o netflix", "abre o netflix", "huli abrir netflix"]:
        return {"tipo": "site", "valor": "netflix"}

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