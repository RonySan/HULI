import re
import random
from datetime import datetime, timedelta

from modules.personality import HULIPersonality
from modules.memory import HULIMemory

memoria = HULIMemory()


# -------------------------
# Utilitários
# -------------------------
def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    # mantém ":" para horários 18:30
    texto = re.sub(r"[^\w\sáàâãéêíóôõúç:]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def escolher(lista):
    return random.choice(lista)


def extrair_horario(comando: str):
    # 18:30
    m = re.search(r"\b(\d{1,2}):(\d{2})\b", comando)
    if m:
        h = int(m.group(1))
        mi = int(m.group(2))
        if 0 <= h <= 23 and 0 <= mi <= 59:
            return h, mi

    # 20h30 ou 20h
    m = re.search(r"\b(\d{1,2})h(\d{2})?\b", comando)
    if m:
        h = int(m.group(1))
        mi = int(m.group(2) or 0)
        if 0 <= h <= 23 and 0 <= mi <= 59:
            return h, mi

    # às 18 / as 18
    m = re.search(r"\b(?:as|às)\s*(\d{1,2})\b", comando)
    if m:
        h = int(m.group(1))
        if 0 <= h <= 23:
            return h, 0

    return None, None


# -------------------------
# Frases dinâmicas (intenção)
# -------------------------
RESP_OK = [
    "Certo.",
    "Fechado.",
    "Entendido.",
    "Beleza.",
    "Perfeito.",
    "Pode deixar.",
]

RESP_OK_CHEFE = [
    "Fechado, chefe 😎",
    "Entendido, chefe.",
    "Deixa comigo, chefe 😎",
    "Perfeito, chefe.",
    "Já estou nisso 😎",
]

RESP_AGRADECER = [
    "Sempre, chefe 😎",
    "Tamo junto, Rony.",
    "Às ordens. Só mandar.",
    "Disponível e operante ✅",
]

RESP_FALLBACK = [
    "Entendi. Quer que eu anote isso ou você quer uma ação específica?",
    "Certo. Você quer que eu registre isso como tarefa, agenda ou ideia?",
    "Ok. Me diz o que você quer que eu faça com isso.",
    "Posso ajudar melhor se você reformular em uma frase curta 🙂",
]

RESP_RISO = [
    "😂",
    "kkk beleza 😄",
    "Boa 😄",
    "Aí sim 😎",
]


# -------------------------
# Núcleo
# -------------------------
def processar_comando(comando: str):
    personalidade = HULIPersonality()
    comando = normalizar_texto(comando)

    # não responde nada se for ENTER vazio
    if not comando:
        return ""

    base = personalidade.gerar_resposta_base()

    # ---------
    # Conversa dinâmica
    # ---------
    if any(x in comando for x in ["kkk", "haha", "rs", "kakak", "lol"]):
        return escolher(RESP_RISO)

    if comando in ["ok", "blz", "beleza", "fechado", "entendi", "certo", "perfeito"]:
        return f"{base} {escolher(RESP_OK_CHEFE)}"

    if any(frase in comando for frase in [
        "obrigado",
        "obrigada",
        "valeu",
        "vlw",
        "obg",
        "obriado",  # typo comum
    ]):
        return f"{base} {escolher(RESP_AGRADECER)}"

    if comando in ["oi", "ola", "olá", "eai", "bom dia", "boa tarde", "boa noite"]:
        return f"{base} Olá Rony. Como posso ajudar você agora?"

    if any(frase in comando for frase in ["quem e voce", "quem voce e", "quem e a huli", "quem é a huli"]):
        return "Eu sou H.U.L.I. Humano Único Leal Inteligente. Seu parceiro digital."

    if any(frase in comando for frase in [
        "voce esta bem",
        "tudo bem",
        "como voce ta",
        "como voce esta",
        "voce ta bem"
    ]):
        return f"{base} Estou bem sim, Rony. Operando 100%. E você, como está?"

    if any(frase in comando for frase in [
        "estou otimo",
        "to otimo",
        "to bem",
        "tudo certo",
        "tranquilo",
        "suave"
    ]):
        return f"{base} Boa! Quer que eu organize suas prioridades de hoje?"

    # ---------
    # Sistema: hora / data / status
    # ---------
    if any(frase in comando for frase in [
        "hora", "horas", "que horas", "que horas sao", "qual a hora", "qual e a hora", "horario"
    ]):
        agora = datetime.now()
        return f"{base} Agora são {agora.strftime('%H:%M:%S')}."

    if any(frase in comando for frase in [
        "que dia e hoje", "qual o dia de hoje", "data de hoje", "que data e hoje"
    ]):
        hoje = datetime.now()
        return f"{base} Hoje é {hoje.strftime('%d/%m/%Y')}."

    if comando == "status":
        return f"{base} Sistemas operacionais funcionando normalmente."

    # ---------
    # Lembretes: limpeza
    # ---------
    if comando in ["apagar lembretes", "limpar todos os lembretes"]:
        memoria.apagar_lembretes()
        return f"{base} Ok. Apaguei todos os lembretes."

    if comando in ["limpar lembretes", "limpar lembretes executados"]:
        memoria.limpar_lembretes_executados()
        return f"{base} Ok. Limpei os lembretes executados."

    # ---------
    # Mostrar categorias
    # ---------
    if comando in ["mostra agenda", "mostrar agenda"]:
        itens = memoria.listar_por_categoria("agenda")
        if isinstance(itens, str):
            return itens
        resposta = "Agenda:\n"
        for i, item in enumerate(itens, 1):
            resposta += f"{i}. {item['conteudo']} ({item['data']} {item['hora']})\n"
        return resposta

    if comando in ["mostra tarefas", "mostrar tarefas"]:
        itens = memoria.listar_por_categoria("tarefas")
        if isinstance(itens, str):
            return itens
        resposta = "Tarefas:\n"
        for i, item in enumerate(itens, 1):
            resposta += f"{i}. {item['conteudo']} ({item['data']} {item['hora']})\n"
        return resposta

    if comando in ["mostra ideias", "mostrar ideias"]:
        itens = memoria.listar_por_categoria("ideias")
        if isinstance(itens, str):
            return itens
        resposta = "Ideias:\n"
        for i, item in enumerate(itens, 1):
            resposta += f"{i}. {item['conteudo']} ({item['data']} {item['hora']})\n"
        return resposta

    # ---------
    # Lembrete com horário (padrão: "me lembra às 22:10 ...")
    # ---------
    if comando.startswith("me lembra"):
        h, mi = extrair_horario(comando)
        if h is None:
            return f"{base} Me diga o horário, exemplo: 'me lembra às 18:30 comprar pão'."

        conteudo = comando.replace("me lembra", "").strip()
        conteudo = re.sub(r"\b(?:as|às)\s*\d{1,2}(:\d{2})?\b", "", conteudo).strip()
        conteudo = re.sub(r"\b\d{1,2}:\d{2}\b", "", conteudo).strip()
        conteudo = re.sub(r"\b\d{1,2}h(\d{2})?\b", "", conteudo).strip()
        conteudo = re.sub(r"^:\d{2}\s*", "", conteudo).strip()
        conteudo = conteudo.lstrip("que ").strip()

        if not conteudo:
            return f"{base} Certo. O que você quer que eu te lembre?"

        agora = datetime.now()
        quando = agora.replace(hour=h, minute=mi, second=0, microsecond=0)
        if quando <= agora:
            quando = quando + timedelta(days=1)

        ok = memoria.salvar_lembrete(conteudo, quando)
        if ok:
            return f"{base} {escolher(RESP_OK_CHEFE)} Lembrete registrado para {quando.strftime('%d/%m/%Y %H:%M')}."
        return f"{base} Esse lembrete já está registrado."

    # ---------
    # Anotações / memórias (sem horário)
    # ---------
    if any(comando.startswith(g) for g in [
        "lembrar que",
        "lembra de",
        "preciso lembrar de",
        "anota",
        "anote",
        "guarda isso",
        "guardar",
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
            "me lembre",
            "me lembrar",
        ]

        conteudo = ""
        for gatilho in gatilhos:
            if comando.startswith(gatilho):
                conteudo = comando.replace(gatilho, "").strip()
                break

        if not conteudo:
            return f"{base} O que você quer que eu registre?"

        categoria = "geral"
        if "agenda" in comando:
            categoria = "agenda"
        elif "tarefa" in comando:
            categoria = "tarefas"
        elif "ideia" in comando:
            categoria = "ideias"

        memoria.salvar(conteudo, categoria=categoria)
        return f"{base} Informação armazenada com sucesso."

    # ---------
    # Listar tudo
    # ---------
    if comando in ["o que voce lembra", "o que voce lembra"]:
        lembrancas = memoria.listar()
        if isinstance(lembrancas, str):
            return lembrancas

        resposta = "Eu lembro:\n"
        for i, item in enumerate(lembrancas, 1):
            if item.get("categoria") == "lembretes":
                status = "✅" if item.get("executado") else "⏳"
                resposta += f"{i}. [lembrete]{status} {item['conteudo']} (quando: {item.get('quando')})\n"
            else:
                resposta += (
                    f"{i}. [{item.get('categoria','geral')}] {item['conteudo']} "
                    f"(Registrado em {item['data']} às {item['hora']})\n"
                )
        return resposta

    if comando == "sair":
        return "ENCERRAR"

    # ---------
    # Fallback inteligente (dinâmico)
    # ---------
    return f"{base} {escolher(RESP_FALLBACK)}"