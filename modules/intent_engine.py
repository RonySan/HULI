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

def contem(texto, palavras):
    return any(p in texto for p in palavras)


def extrair_depois(texto, gatilho):
    if gatilho not in texto:
        return ""
    return texto.split(gatilho, 1)[1].strip()


def detectar_intencao(comando: str):
    texto = comando.lower().strip()

    # mantém compatibilidade com o motor antigo
    antiga = interpretar_intencao(texto)
    if antiga:
        tipo = antiga.get("tipo")

        if tipo == "site":
            return {
                "intent": "abrir_site",
                "valor": antiga.get("valor", "")
            }

        if tipo == "pesquisa":
            return {
                "intent": "pesquisar",
                "valor": antiga.get("valor", "")
            }

        if tipo == "abrir":
            return {
                "intent": "abrir",
                "valor": antiga.get("valor", "")
            }

    # lembrete vem antes de medicamento
    if contem(texto, ["me lembra", "me lembre", "lembrete", "lembra de"]):
        return {
            "intent": "lembrete",
            "texto": texto
        }

    if contem(texto, ["remedio", "remédio", "medicamento", "dose"]):
        return {
            "intent": "medicamento",
            "texto": texto
        }

    if texto in ["hora", "horas", "que horas", "que horas sao", "que horas são", "qual a hora", "qual e a hora"]:
        return {"intent": "hora"}

    if texto in ["que dia e hoje", "que dia é hoje", "data de hoje", "qual a data"]:
        return {"intent": "data"}

    if texto == "status":
        return {"intent": "status"}

    if texto in ["status sistema", "diagnostico", "diagnóstico"]:
        return {"intent": "status_sistema"}

    if texto in ["status ia", "modo ia", "online ou offline"]:
        return {"intent": "status_ia"}

    if texto in ["ajuda", "help", "socorro", "o que voce faz", "o que você faz"]:
        return {"intent": "ajuda"}

    if texto in ["sair", "encerrar", "fechar huli"]:
        return {"intent": "sair"}

    if texto in ["clicar", "clique"]:
        return {"intent": "clicar"}

    if texto in ["duplo clique", "clicar duas vezes"]:
        return {"intent": "duplo_clique"}

    if texto in ["clique direito", "botao direito", "botão direito"]:
        return {"intent": "clique_direito"}

    if texto.startswith("mover mouse para "):
        return {
            "intent": "mover_mouse",
            "texto": texto
        }

    if texto.startswith("digitar "):
        return {
            "intent": "digitar",
            "valor": texto.replace("digitar ", "", 1).strip()
        }

    if texto.startswith("pressionar "):
        return {
            "intent": "pressionar",
            "valor": texto.replace("pressionar ", "", 1).strip()
        }

    if texto in ["mostrar logs", "ver logs", "listar logs"]:
        return {"intent": "mostrar_logs"}

    if texto in ["limpar logs", "apagar logs"]:
        return {"intent": "limpar_logs"}

    if texto in ["criar backup", "backup"]:
        return {"intent": "criar_backup"}

    if texto in ["listar backups", "mostrar backups"]:
        return {"intent": "listar_backups"}

    return None