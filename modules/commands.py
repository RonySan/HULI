import re
from datetime import datetime

from modules.personality import HULIPersonality
from modules.memory import HULIMemory

memoria = HULIMemory()


def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^\w\sáàâãéêíóôõúç]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def processar_comando(comando: str):
    personalidade = HULIPersonality()
    comando = normalizar_texto(comando)

    # Cumprimentos
    if comando in ["oi", "ola", "olá", "eai", "bom dia", "boa tarde", "boa noite"]:
        base = personalidade.gerar_resposta_base()
        return f"{base} Olá Rony. Como posso ajudar você agora?"

    # Identidade
    elif any(frase in comando for frase in [
        "quem e voce",
        "quem voce e",
        "quem e a huli",
        "quem é a huli",
    ]):
        return "Eu sou H.U.L.I. Humano Único Leal Inteligente. Seu parceiro digital."

    # Bem-estar (perguntas)
    elif any(frase in comando for frase in [
        "voce esta bem",
        "tudo bem",
        "como voce ta",
        "como voce esta",
        "voce ta bem",
    ]):
        base = personalidade.gerar_resposta_base()
        return f"{base} Estou bem sim, Rony. Operando 100%. E você, como está?"

    # Bem-estar (respostas do Rony)
    elif any(frase in comando for frase in [
        "estou otimo",
        "to otimo",
        "to bem",
        "tudo certo",
        "beleza",
        "tranquilo",
        "suave",
    ]):
        base = personalidade.gerar_resposta_base()
        return f"{base} Boa! Quer que eu organize suas prioridades de hoje ou tem algo específico?"

    # Hora (natural)
    elif any(frase in comando for frase in [
        "hora",
        "horas",
        "que horas",
        "que horas sao",
        "qual a hora",
        "qual e a hora",
        "horario",
    ]):
        agora = datetime.now()
        base = personalidade.gerar_resposta_base()
        return f"{base} Agora são {agora.strftime('%H:%M:%S')}."

    # Data de hoje
    elif any(frase in comando for frase in [
        "que dia e hoje",
        "qual o dia de hoje",
        "data de hoje",
        "que data e hoje",
    ]):
        hoje = datetime.now()
        base = personalidade.gerar_resposta_base()
        return f"{base} Hoje é {hoje.strftime('%d/%m/%Y')}."

    # Status
    elif comando == "status":
        base = personalidade.gerar_resposta_base()
        return f"{base} Sistemas operacionais funcionando normalmente."

    # Listagens por categoria (mostra/mostrar)
    elif comando in ["mostra agenda", "mostrar agenda"]:
        itens = memoria.listar_por_categoria("agenda")
        if isinstance(itens, str):
            return itens
        resposta = "Agenda:\n"
        for i, item in enumerate(itens, 1):
            resposta += f"{i}. {item['conteudo']} ({item['data']} {item['hora']})\n"
        return resposta

    elif comando in ["mostra tarefas", "mostrar tarefas"]:
        itens = memoria.listar_por_categoria("tarefas")
        if isinstance(itens, str):
            return itens
        resposta = "Tarefas:\n"
        for i, item in enumerate(itens, 1):
            resposta += f"{i}. {item['conteudo']} ({item['data']} {item['hora']})\n"
        return resposta

    elif comando in ["mostra ideias", "mostrar ideias"]:
        itens = memoria.listar_por_categoria("ideias")
        if isinstance(itens, str):
            return itens
        resposta = "Ideias:\n"
        for i, item in enumerate(itens, 1):
            resposta += f"{i}. {item['conteudo']} ({item['data']} {item['hora']})\n"
        return resposta

    # Lembretes naturais + categoria automática
    elif any(comando.startswith(g) for g in [
        "lembrar que",
        "lembra de",
        "preciso lembrar de",
        "anota",
        "anote",
        "guarda isso",
        "guardar",
        "me lembra",
        "me lembre",
        "me lembrar",
    ]):
        gatilhos = [
            "lembrar que",
            "lembra de",
            "preciso lembrar de",
            "anota",
            "anote",
            "guarda isso",
            "guardar",
            "me lembra",
            "me lembre",
            "me lembrar",
        ]

        conteudo = ""
        for gatilho in gatilhos:
            if comando.startswith(gatilho):
                conteudo = comando.replace(gatilho, "").strip()
                break

        if not conteudo:
            return "O que você quer que eu registre?"

        categoria = "geral"
        if "agenda" in comando:
            categoria = "agenda"
        elif "tarefa" in comando:
            categoria = "tarefas"
        elif "ideia" in comando:
            categoria = "ideias"

        memoria.salvar(conteudo, categoria=categoria)
        return "Informação armazenada com sucesso."

    # Listar tudo
    elif comando in ["o que voce lembra", "o que voce lembra"]:
        lembrancas = memoria.listar()
        if isinstance(lembrancas, str):
            return lembrancas

        resposta = "Eu lembro:\n"
        for i, item in enumerate(lembrancas, 1):
            resposta += (
                f"{i}. [{item.get('categoria','geral')}] {item['conteudo']} "
                f"(Registrado em {item['data']} às {item['hora']})\n"
            )
        return resposta

    elif comando == "sair":
        return "ENCERRAR"

    else:
        return "Comando não reconhecido."