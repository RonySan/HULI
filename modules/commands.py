import re
from datetime import datetime

from modules.personality import HULIPersonality
from modules.memory import HULIMemory

memoria = HULIMemory()


def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    # troca pontuação por espaço (mantém letras/números/acentos e espaços)
    texto = re.sub(r"[^\w\sáàâãéêíóôõúç]", " ", texto)
    # remove espaços duplicados
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
        "quem e voce",
    ]):
        return "Eu sou H.U.L.I. Humano Único Leal Inteligente. Seu parceiro digital."

    # Bem-estar
    elif any(frase in comando for frase in [
        "voce esta bem",
        "tudo bem",
        "como voce ta",
        "como voce esta",
        "voce ta bem",
    ]):
        base = personalidade.gerar_resposta_base()
        return f"{base} Estou bem sim, Rony. Operando 100%. E você, como está?"
    
    elif any(frase in comando for frase in [
        "estou otimo",
        "estou ótimo",
        "to otimo",
        "tô ótimo",
        "to bem",
        "tô bem",
        "tudo certo",
        "beleza",
        "tranquilo",
        "suave"
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

    # Status
    elif comando == "status":
        base = personalidade.gerar_resposta_base()
        return f"{base} Sistemas operacionais funcionando normalmente."

    # Lembretes naturais
    elif any(comando.startswith(g) for g in [
        "lembrar que",
        "lembra de",
        "preciso lembrar de",
        "anota",
        "guarda isso",
        "guardar",
        "lembrar que",
        "lembra de",
        "preciso lembrar de",
        "anota",
        "guarda isso",
        "guardar",
        "me lembra",
        "me lembre",
        "me lembrar"
    ]):
        gatilhos = [
            "lembrar que",
            "lembra de",
            "preciso lembrar de",
            "anota",
            "guarda isso",
            "guardar",
            "lembrar que",
            "lembra de",
            "preciso lembrar de",
            "anota",
            "guarda isso",
            "guardar",
            "me lembra",
            "me lembre",
            "me lembrar"
        ]

        conteudo = ""
        for gatilho in gatilhos:
            if comando.startswith(gatilho):
                conteudo = comando.replace(gatilho, "").strip()
                break

        if conteudo:
            memoria.salvar(conteudo)
            return "Informação armazenada com sucesso."
        else:
            return "O que você quer que eu registre?"

    # Listar memórias
    elif comando == "o que voce lembra":
        lembrancas = memoria.listar()
        if isinstance(lembrancas, str):
            return lembrancas

        resposta = "Eu lembro:\n"
        for i, item in enumerate(lembrancas, 1):
            resposta += (
                f"{i}. {item['conteudo']} "
                f"(Registrado em {item['data']} às {item['hora']})\n"
            )
        return resposta

    elif comando == "sair":
        return "ENCERRAR"

    else:
        return "Comando não reconhecido."
