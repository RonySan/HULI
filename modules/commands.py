import os
import re
import random
from datetime import datetime, timedelta
from modules.nlp import normalizar_comando_natural
from modules.ai import responder_ia, tem_internet, extrair_conhecimento
from modules.aliases import ALIASES_APPS
from modules.docs import buscar_docs
from modules.knowledge import aprender, buscar, listar_tudo
from modules.memory import HULIMemory
from modules.personality import HULIPersonality
from modules.scheduler import adicionar_agendamento, listar_agendamentos, remover_agendamento
from modules.routines import (
    executar_rotina,
    listar_rotinas,
    criar_rotina,
    mostrar_rotina,
    adicionar_item_rotina,
    remover_item_rotina,
)
from modules.pc_control import (
    abrir_programa,
    listar_programas,
    abrir_site,
    pesquisar_web,
    abrir_pasta,
    executar_comando_terminal,
    abrir_arquivo,
)
from modules.system_control import (
    desligar_pc,
    reiniciar_pc,
    bloquear_pc,
    cancelar_desligamento,
)
from modules.actions import aprender_programa


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


def limpar_palavra_ativacao(comando: str) -> str:
    comando = normalizar_comando_natural(comando)

    if comando.startswith("huli "):
        comando = comando.replace("huli ", "", 1).strip()

    # limpeza leve sem quebrar comandos importantes
    for termo in [" o ", " a "]:
        comando = comando.replace(termo, " ")

    return re.sub(r"\s+", " ", comando).strip()


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
    comando = limpar_palavra_ativacao(comando)

    if not comando:
        return ""

    base = personalidade.gerar_resposta_base()

    # -------------------------
    # Resumo da conversa
    if comando in ["resumir conversa", "resumo da conversa"]:
        if not historico_conversa:
            return f"{base} Não há conversa suficiente para resumir."
        resumo = responder_ia("Resuma a conversa até agora.", historico=historico_conversa, modo="simples")
        return f"{base} {resumo}"
    # Conversa dinâmicaI
    # -------------------------
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

    # -------------------------
    # Sistema / status / modos
    # -------------------------
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

    if comando in ["limpar contexto", "reset conversa", "reiniciar conversa"]:
        historico_conversa.clear()
        return f"{base} Contexto da conversa limpo. Pode falar do zero."

       # -------------------------
    # Rotinas
    # -------------------------
    if comando in ["listar rotinas", "mostra rotinas", "quais rotinas existem"]:
        rotinas = listar_rotinas()

        if not rotinas:
            return f"{base} Ainda não existem rotinas cadastradas."

        resposta = "Rotinas disponíveis:\n"
        for i, nome in enumerate(rotinas, 1):
            resposta += f"{i}. {nome}\n"
        return resposta

    if comando.startswith("mostrar rotina"):
        nome = comando.replace("mostrar rotina", "", 1).strip()

        if not nome:
            return f"{base} Diga o nome da rotina."

        ok, resposta = mostrar_rotina(nome)
        return f"{base} {resposta}"

    if comando.startswith("criar rotina"):
        try:
            texto = comando.replace("criar rotina", "", 1).strip()

            if "com" not in texto:
                return f"{base} Use assim: criar rotina trabalho com chrome, vscode"

            nome, itens = texto.split("com", 1)
            nome = nome.strip()
            itens = [x.strip() for x in itens.split(",")]

            return f"{base} {criar_rotina(nome, itens)}"
        except Exception:
            return f"{base} Não consegui criar a rotina."

    if comando.startswith("adicionar ") and " na rotina " in comando:
        texto = comando.replace("adicionar ", "", 1)
        item, nome = texto.split(" na rotina ", 1)

        ok, resposta = adicionar_item_rotina(nome.strip(), item.strip())
        return f"{base} {resposta}"

    if comando.startswith("remover ") and " da rotina " in comando:
        texto = comando.replace("remover ", "", 1)
        item, nome = texto.split(" da rotina ", 1)

        ok, resposta = remover_item_rotina(nome.strip(), item.strip())
        return f"{base} {resposta}"

    if comando.startswith("abrir "):
        nome_rotina = comando.replace("abrir ", "", 1).strip()

        ok_rotina, resposta_rotina = executar_rotina(
            nome_rotina,
            abrir_programa,
            abrir_site,
            abrir_pasta,
            executar_comando_terminal,
            abrir_arquivo
        )

        if ok_rotina:
            return f"{base} {resposta_rotina}"
    # -------------------------
    # Web / pesquisa / sites
    # -------------------------
    if comando.startswith("pesquisar "):
        termo = comando.replace("pesquisar ", "", 1).strip()
        _, resposta_web = pesquisar_web(termo)
        return resposta_web

    if comando.startswith("procurar "):
        termo = comando.replace("procurar ", "", 1).strip()
        _, resposta_web = pesquisar_web(termo)
        return resposta_web

    if comando.startswith("abrir "):
        nome_destino = comando.replace("abrir ", "", 1).strip()
        ok_site, resposta_site = abrir_site(nome_destino)
        if ok_site:
            return resposta_site

    # abrir algo no navegador
    if "navegador" in comando:
        if "github" in comando:
            _, resp = abrir_site("github")
            return resp
        if "youtube" in comando:
            _, resp = abrir_site("youtube")
            return resp
        if "gmail" in comando:
            _, resp = abrir_site("gmail")
            return resp
        if "chatgpt" in comando:
            _, resp = abrir_site("chatgpt")
            return resp

    # -------------------------
    # Documentos
    # -------------------------
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

    # -------------------------
    # Ajuda
    # -------------------------
    if comando in ["ajuda", "help", "socorro", "o que voce faz", "o que você faz"]:
        return (
        "Eu posso ajudar com várias coisas, Rony:\n\n"

        "💬 CONVERSA\n"
        "• oi\n"
        "• como voce esta\n"
        "• quem e voce\n"
        "• ajuda\n\n"

        "🕒 SISTEMA\n"
        "• horas\n"
        "• que dia e hoje\n"
        "• status\n"
        "• status ia\n"
        "• modo simples\n"
        "• modo normal\n"
        "• modo detalhado\n"
        "• modo atual\n"
        "• limpar contexto\n"
        "• resumir conversa\n\n"

        "📝 MEMÓRIA E ORGANIZAÇÃO\n"
        "• anota comprar pão\n"
        "• anota na agenda reunião amanhã\n"
        "• anota tarefa pagar conta\n"
        "• anota ideia criar sistema novo\n"
        "• mostra agenda\n"
        "• mostra tarefas\n"
        "• mostra ideias\n"
        "• o que voce lembra\n\n"

        "⏰ LEMBRETES\n"
        "• me lembra às 18:30 ligar pro João\n"
        "• me lembra às 22 estudar\n"
        "• apagar lembretes\n"
        "• limpar lembretes executados\n\n"

        "🧠 CONHECIMENTO PERMANENTE\n"
        "• aprenda que meu cliente principal é a empresa XPTO\n"
        "• o que voce sabe sobre meu cliente principal\n"
        "• o que voce aprendeu\n"
        "• listar conhecimento\n\n"

        "📂 DOCUMENTOS\n"
        "• buscar docs multa\n"
        "• buscar docs contrato\n\n"

        "💻 PROGRAMAS E COMPUTADOR\n"
        "• listar programas\n"
        "• abrir navegador\n"
        "• abrir edge\n"
        "• abrir chrome\n"
        "• abrir vscode\n"
        "• abrir github\n"
        "• abrir gmail\n"
        "• abrir youtube\n"
        "• aprender programa paint em C:\\Windows\\System32\\mspaint.exe\n\n"

        "🧭 COMANDOS NATURAIS\n"
        "• pode abrir o navegador pra mim\n"
        "• abre meu github\n"
        "• que horas são agora\n"
        "• me mostra os programas\n"
        "• pode abrir o vscode\n"
        "• me ajuda\n\n"

        "🌐 PESQUISA E WEB\n"
        "• pesquisar dolar hoje\n"
        "• procurar clima em sao paulo\n"
        "• abrir github\n"
        "• abrir gmail\n"
        "• abrir youtube\n"
        "• abrir chatgpt\n\n"

        "⚙️ CONTROLE DO SISTEMA\n"
        "• bloquear computador\n"
        "• reiniciar computador\n"
        "• desligar computador\n"
        "• cancelar desligamento\n\n"

        "🚀 ROTINAS\n"
        "• abrir trabalho\n"
        "• abrir estudo\n"
        "• abrir projeto huli\n\n"

        "🎤 VOZ\n"
        "• digite: voz\n"
        "• depois fale o comando\n"
        "• exemplo: abrir navegador\n\n"

        "🚪 ENCERRAR\n"
        "• sair\n"
        "• encerrar\n\n"

        "Se quiser, eu também posso executar comandos locais, responder perguntas, "
        "usar IA online/offline e falar com você por voz 😎"
    )

    # -------------------------
    # Lembretes
    # -------------------------
    if comando in ["apagar lembretes", "limpar todos os lembretes"]:
        memoria.apagar_lembretes()
        return f"{base} Ok. Apaguei todos os lembretes."

    if comando in ["limpar lembretes", "limpar lembretes executados"]:
        memoria.limpar_lembretes_executados()
        return f"{base} Ok. Limpei os lembretes executados."

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

    # -------------------------
    # Memória categorizada
    # -------------------------
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
                    f"{i}. [{item.get('categoria', 'geral')}] {item['conteudo']} "
                    f"(Registrado em {item['data']} às {item['hora']})\n"
                )
        return resposta

    # -------------------------
    # Conhecimento permanente
    # -------------------------
    if comando.startswith("aprenda que"):
        texto = comando.replace("aprenda que", "").strip()

        if not texto:
            return f"{base} O que você quer que eu aprenda?"

        gatilhos = [
            " prefere ",
            " gosta de ",
            " usa ",
            " trabalha com ",
            " paga ",
            " vence ",
            " tem ",
            " é ",
            " e ",
        ]

        chave = None
        valor = None

        for gatilho in gatilhos:
            if gatilho in texto:
                parte1, parte2 = texto.split(gatilho, 1)
                chave = parte1.strip()
                valor = (gatilho.strip() + " " + parte2.strip()).strip()
                break

        if not chave or not valor:
            return f"{base} Não entendi o que devo aprender."

        aprender(chave, valor)
        return f"{base} Entendido. Aprendi que {chave} {valor}."

    if comando.startswith("o que voce sabe sobre"):
        chave = comando.replace("o que voce sabe sobre", "").strip()

        if not chave:
            return f"{base} Sobre o que você quer saber?"

        valor = buscar(chave)

        if valor:
            return f"{base} Eu sei que {chave} {valor}."

        return f"{base} Ainda não sei nada sobre isso."

    if comando in ["o que voce aprendeu", "mostra conhecimento", "listar conhecimento"]:
        dados = listar_tudo()

        if not dados:
            return f"{base} Ainda não aprendi nada na memória permanente."

        resposta = "Isto é o que eu aprendi:\n"
        for chave, valor in dados.items():
            resposta += f"- {chave} {valor}\n"

        return resposta

    # -------------------------
    # Aprender programa manualmente
    # -------------------------
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

    # -------------------------
    # Controle do PC
    # -------------------------
    if comando in [
        "listar programas",
        "listar programa",
        "listar apps",
        "quais programas voce conhece",
        "lista programas",
        "lista programa",
        ]:
        programas = listar_programas()
        if not programas:
            return "Não encontrei programas no Menu Iniciar."

        resposta = "Programas encontrados:\n"
        for i, nome in enumerate(programas[:30], 1):
            resposta += f"{i}. {nome}\n"

        if len(programas) > 30:
            resposta += f"\nMostrando 30 de {len(programas)} programas."
        return resposta

    if comando.startswith(("abrir ", "abri ", "abre ")):
        nome_programa = comando.replace("abrir ", "")
        nome_programa = nome_programa.replace("abri ", "")
        nome_programa = nome_programa.replace("abre ", "")
        nome_programa = nome_programa.strip()

        if "navegador" in nome_programa:
            if "edge" in nome_programa:
                nome_programa = "edge"
            elif "chrome" in nome_programa:
                nome_programa = "chrome"
            else:
                nome_programa = "chrome"

        if nome_programa in ALIASES_APPS:
            nome_programa = ALIASES_APPS[nome_programa]

        _, resposta_pc = abrir_programa(nome_programa)
        return resposta_pc

    # -------------------------
    # Controle do sistema
    # -------------------------
    if comando in ["desligar pc", "desligar computador", "desligar o pc", "desligar o computador"]:
        return desligar_pc()

    if comando in ["reiniciar pc", "reiniciar computador", "reiniciar o pc", "reiniciar o computador"]:
        return reiniciar_pc()

    if comando in ["bloquear pc", "bloquear computador", "bloquear o pc", "bloquear o computador"]:
        return bloquear_pc()

    if comando in ["cancelar desligamento", "cancelar reinicio", "cancelar reinício"]:
        return cancelar_desligamento()
       # -------------------------
    # Agendamentos
    # -------------------------
    if comando.startswith("agendar rotina ") and (" às " in comando or " as " in comando):
        try:
            texto = comando.replace("agendar rotina ", "", 1)

            if " às " in texto:
                nome, horario = texto.split(" às ", 1)
            else:
                nome, horario = texto.split(" as ", 1)

            horario = horario.strip().replace(" ", ":")

            return f"{base} {adicionar_agendamento('rotina', nome.strip(), horario)}"
        except Exception:
            return f"{base} Não consegui criar o agendamento da rotina."

    if comando.startswith("agendar comando ") and (" às " in comando or " as " in comando):
        try:
            texto = comando.replace("agendar comando ", "", 1)

            if " às " in texto:
                nome, horario = texto.split(" às ", 1)
            else:
                nome, horario = texto.split(" as ", 1)

            horario = horario.strip().replace(" ", ":")

            return f"{base} {adicionar_agendamento('comando', nome.strip(), horario)}"
        except Exception:
            return f"{base} Não consegui criar o agendamento do comando."

    if comando in ["listar agendamentos", "listar agendamento", "mostrar agendamentos", "mostrar agendamento"]:
        itens = listar_agendamentos()

        if not itens:
            return f"{base} Não existem agendamentos cadastrados."

        resposta = "Agendamentos:\n"
        for item in itens:
            resposta += f"{item['id']}. [{item['tipo']}] {item['valor']} às {item['horario']}\n"
        return resposta

    if comando.startswith("remover agendamento "):
        try:
            agendamento_id = int(comando.replace("remover agendamento ", "", 1).strip())
            ok, resposta = remover_agendamento(agendamento_id)
            return f"{base} {resposta}"
        except Exception:
            return f"{base} Não consegui remover o agendamento."

    # -------------------------
    # Sair
    # -------------------------
    if comando == "sair":
        return "ENCERRAR"

    # -------------------------
    # Fallback IA com contexto
    # -------------------------
    resposta_ia = responder_ia(comando, historico=historico_conversa, modo=MODO_RESPOSTA)

    if resposta_ia:
        historico_conversa.append({"role": "user", "content": comando})
        historico_conversa.append({"role": "assistant", "content": resposta_ia})

        if len(historico_conversa) > MAX_HIST:
            historico_conversa[:] = historico_conversa[-MAX_HIST:]

    # -------------------------
    # Aprendizado automático
    # -------------------------
    try:
        memoria_extraida = extrair_conhecimento(comando)

        if memoria_extraida:
            chave = memoria_extraida.get("chave", "").strip()
            valor = memoria_extraida.get("valor", "").strip()

            if chave and valor:
                aprender(chave, valor)
    except Exception:
        pass

    return resposta_ia