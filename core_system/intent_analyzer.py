def analisar_intencao(texto):
    comando = texto.lower().strip()

    if any(x in comando for x in [
        "começar a trabalhar",
        "comecar a trabalhar",
        "iniciar trabalho",
        "modo trabalho",
        "quero trabalhar",
    ]):
        return {
            "intencao": "trabalho",
            "confianca": 0.95,
            "dados": {"rotina": "trabalho"}
        }

    if any(x in comando for x in [
        "gerar documentação",
        "gerar documentacao",
        "documentar projeto",
        "documentar huli",
    ]):
        return {
            "intencao": "documentacao",
            "confianca": 0.9,
            "dados": {}
        }

    if any(x in comando for x in [
        "como esta o projeto",
        "como está o projeto",
        "estado do projeto",
        "status do projeto",
    ]):
        return {
            "intencao": "reflexao_projeto",
            "confianca": 0.9,
            "dados": {}
        }

    if any(x in comando for x in [
        "o que temos hoje",
        "o que temos pra fazer hoje",
        "agenda de hoje",
        "pendencias",
        "pendências",
    ]):
        return {
            "intencao": "planejamento_dia",
            "confianca": 0.9,
            "dados": {}
        }

    return {
        "intencao": "desconhecida",
        "confianca": 0.0,
        "dados": {}
    }