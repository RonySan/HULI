import re
import os
import random
from datetime import datetime, timedelta

from modules.ai import responder_ia, tem_internet
from modules.personality import HULIPersonality
from modules.memory import HULIMemory
from modules.docs import buscar_docs
from modules.actions import abrir_programa, aprender_programa

memoria = HULIMemory()
historico_conversa: list[dict] = []
MAX_HIST = 12
MODO_RESPOSTA = "normal"  # simples | normal | detalhado


# -------------------------
# Utilitários
# -------------------------
def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = re.sub(r"[^\w\sáàâãéêíóôõúç:]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def escolher(lista):
    return random.choice(lista)


def extrair_horario(comando: str):
    m = re.search(r"\b(\d{1,2}):(\d{2})\b", comando)
    if m:
        h = int(m.group(1))
        mi = int(m.group(2))
        if 0 <= h <= 23 and 0 <= mi <= 59:
            return h, mi

    m = re.search(r"\b(\d{1,2})h(\d{2})?\b", comando)
    if m:
        h = int(m.group(1))
        mi = int(m.group(2) or 0)
        if 0 <= h <= 23 and 0 <= mi <= 59:
            return h, mi

    m = re.search(r"\b(?:as|às)\s*(\d{1,2})\b", comando)
    if m:
        h = int(m.group(1))
        if 0 <= h <= 23:
            return h, 0

    return None, None


# -------------------------
# Frases dinâmicas
# -------------------------
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
    global MODO_RESPOSTA

    personalidade = HULIPersonality()
    comando_original = comando.strip()
    comando = normalizar_texto(comando)

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

    if any(frase in comando for frase in ["obrigado", "obrigada", "valeu", "vlw", "obg", "obriado"]):
        return f"{base} {escolher(RESP_AGRADECER)}"

    if comando in ["oi", "ola", "olá", "eai", "bom dia", "boa tarde", "boa noite"]:
        return f"{base} Olá Rony. Como posso ajudar você agora?"

    if any(frase in comando for frase in ["quem e voce", "quem voce e", "quem e a huli", "quem é a huli"]):
        return "Eu sou H.U.L.I. Humano Único Leal Inteligente. Seu parceiro digital."

    if any(frase in comando for frase in ["voce esta bem", "tudo bem", "como voce ta", "como voce esta", "voce ta bem"]):
        return f"{base} Estou bem sim, Rony. Operando 100%. E você, como está?"

    if any(frase in comando for frase in ["estou otimo", "to otimo", "to bem", "tudo certo", "tranquilo", "suave"]):
        return f"{base} Boa! Quer que eu organize suas prioridades de hoje?"

    # ---------
    # Aprender programa
    # ---------
    if comando.startswith("aprender programa"):
        try:
            texto = comando_original.replace("aprender programa", "", 1).strip()

            if " em " not in texto.lower():
                return f"{base} Use assim: aprender programa paint em C:\\Windows\\System32\\mspaint.exe"

            nome, caminho = texto.split(" em ", 1)
            nome = nome.strip().lower()
            caminho = caminho.strip()

            if not nome or not caminho:
                return f"{base} Preciso do nome e do caminho do programa."

            return f"{base} {aprender_programa(nome, caminho)}"
        except Exception:
            return f"{base} Não consegui aprender esse programa."

    # ---------
    # Abrir programas
    # ---------
    if comando.startswith("abrir "):
        nome = comando.replace("abrir ", "").strip()
        r = abrir_programa(nome)
        if r:
            return f"{base} {r}"

    # ---------
    # Sistema
    # ---------
    if any(frase in comando for frase in ["hora", "horas", "que horas", "que horas sao", "qual a hora", "qual e a hora", "horario"]):
        agora = datetime.now()
        return f"{base} Agora são {agora.strftime('%H:%M:%S')}."

    if any(frase in comando for frase in ["que dia e hoje", "qual o dia de hoje", "data de hoje", "que data e hoje"]):
        hoje = datetime.now()
        return f"{base} Hoje é {hoje.strftime('%d/%m/%Y')}."

    if comando == "status":
        return f"{base} Sistemas operacionais funcionando normalmente."

    if comando in ["status ia", "status da ia", "modo ia", "online ou offline"]:
        tem_net = tem_internet()
        tem_key = bool(os.getenv("OPENAI_API_KEY"))
        status = []
        status.append("🌐 INTERNET: OK" if tem_net else "🌐 INTERNET: NÃO")
        status.append("🔑 OPENAI_API_KEY: OK" if tem_key else "🔑 OPENAI_API_KEY: NÃO")
        return f"{base} " + " | ".join(status) + " | (ONLINE depende de cota na OpenAI)"

    # ---------
    # Modos
    # ---------
    if comando in ["modo simples", "modo fácil", "modo facil"]:
        MODO_RESPOSTA = "simples"
        return f"{base} Modo de resposta ajustado para: SIMPLES."

    if comando in ["modo normal", "modo padrão", "modo padrao"]:
        MODO_RESPOSTA = "normal"
        return f"{base} Modo de resposta ajustado para: NORMAL."

    if comando in ["modo detalhado", "modo completo", "modo avançado", "modo avancado"]:
        MODO_RESPOSTA = "detalhado"
        return f"{base} Modo de resposta ajustado para: DETALHADO."

    if comando in ["modo atual", "qual modo", "qual o modo"]:
        return f"{base} Modo atual: {MODO_RESPOSTA.upper()}."

    # ---------
    # Buscar documentos
    # ---------
    if comando.startswith("buscar docs"):
        termo = comando.replace("buscar docs", "").strip()

        if not termo:
            return f"{base} Diga o que você quer buscar nos documentos."

        resultados = buscar_docs(termo)

        if not resultados:
            return f"{base} Não encontrei nada sobre '{termo}' nos documentos."

        resposta = "Encontrei isto nos documentos:\n"
        for r in resultados:
            resposta += f"- {r}\n"
        return resposta

    # ---------
    # Resumir conversa
    # ---------
    if comando in ["resumir conversa", "resumo da conversa", "resumir chat"]:
        if not historico_conversa:
            return f"{base} Ainda não temos conversa suficiente para resumir."

        pedido = (
            "Resuma nossa conversa recente em tópicos curtos (máx 8 linhas). "
            "Depois liste 3 próximos passos recomendados."
        )
        return responder_ia(pedido, historico=historico_conversa, modo="normal")

    # ---------
    # Ajuda
    # ---------
    if comando in ["ajuda", "help", "socorro", "o que voce faz", "o que você faz"]:
        return (
            "Eu posso ajudar com várias coisas, Rony:\n\n"
            "📅 Organização\n"
            "• anota na agenda reunião amanhã\n"
            "• anota tarefa pagar conta\n"
            "• anota ideia criar sistema novo\n\n"
            "⏰ Lembretes\n"
            "• me lembra às 18:30 ligar pro João\n"
            "• me lembra às 22 testar lembrete\n\n"
            "📋 Consultar informações\n"
            "• mostra agenda\n"
            "• mostra tarefas\n"
            "• mostra ideias\n"
            "• o que voce lembra\n"
            "• buscar docs multa\n\n"
            "🕒 Sistema\n"
            "• horas\n"
            "• que dia é hoje\n"
            "• status\n"
            "• status ia\n\n"
            "💻 Ações\n"
            "• abrir chrome\n"
            "• aprender programa paint em C:\\Windows\\System32\\mspaint.exe\n\n"
            "💬 Conversa\n"
            "• oi\n"
            "• como voce esta\n"
            "• quem e voce\n\n"
            "Se quiser registrar algo é só falar naturalmente 😎"
        )

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
    # Lembrete com horário
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
    # Anotações / memórias
    # ---------
    if any(comando.startswith(g) for g in [
        "lembrar que", "lembra de", "preciso lembrar de", "anota", "anote",
        "guarda isso", "guardar", "me lembre", "me lembrar",
    ]):
        gatilhos = [
            "lembrar que", "lembra de", "preciso lembrar de", "anota", "anote",
            "guarda isso", "guardar", "me lembre", "me lembrar",
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
    if comando in ["o que voce lembra"]:
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

    # ---------
    # Limpar contexto
    # ---------
    if comando in ["limpar contexto", "reset conversa", "reiniciar conversa"]:
        historico_conversa.clear()
        return f"{base} Contexto da conversa limpo. Pode falar do zero."

    # ---------
    # Sair
    # ---------
    if comando == "sair":
        return "ENCERRAR"

    # ---------
    # Fallback IA com contexto
    # ---------
    resposta_ia = responder_ia(comando, historico=historico_conversa, modo=MODO_RESPOSTA)

    if resposta_ia:
        historico_conversa.append({"role": "user", "content": comando})
        historico_conversa.append({"role": "assistant", "content": resposta_ia})

        if len(historico_conversa) > MAX_HIST:
            historico_conversa[:] = historico_conversa[-MAX_HIST:]

    return resposta_ia