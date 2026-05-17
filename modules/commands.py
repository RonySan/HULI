import os
import re
import random
from datetime import datetime, timedelta

from modules.help_system import obter_ajuda

from modules.nlp import normalizar_comando_natural
from modules.ai import responder_ia, tem_internet, extrair_conhecimento
from modules.aliases import ALIASES_APPS
from modules.docs import buscar_docs
from modules.knowledge import aprender, buscar, listar_tudo
from modules.memory import HULIMemory
from modules.personality import HULIPersonality

from modules.backup import criar_backup, listar_backups
from modules.scheduler import adicionar_agendamento, listar_agendamentos, remover_agendamento
from modules.system_monitor import status_sistema
from modules.history import listar as listar_historico
from modules.intent_engine import interpretar_intencao
from modules.logger import ler_logs, limpar_logs, registrar_log
from modules.voice_mode import ativar_voz, desativar_voz, voz_esta_ativa
from modules.social import se_apresentar_para, cumprimentar, elogiar, recado

from modules.settings_manager import listar_config, definir, obter
from modules.medication import processar_pedido_medicamento
from modules.habits import listar_habitos, limpar_habitos
from modules.autopilot import (
    listar_autoexecucoes,
    desativar_autoexecucao,
    limpar_autoexecucoes,
)
from modules.user_profile import definir_valor, listar_perfil, limpar_perfil
from modules.protection import (
    ativar_protecao,
    desativar_protecao,
    status_protecao,
    requer_confirmacao,
    registrar_confirmacao_pendente,
    tem_confirmacao_pendente,
    resolver_confirmacao,
)

from modules.vision import screenshot, localizar_imagem, clicar_imagem
from modules.vision_advanced import (
    tirar_print,
    ler_tela,
    listar_textos_tela,
    procurar_texto_na_tela,
    clicar_texto_na_tela,
)

from modules.custom_commands import (
    criar_comando_personalizado,
    listar_comandos_personalizados,
    apagar_comando_personalizado,
    resolver_comando_personalizado,
)

from modules.routines import (
    apagar_rotina,
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

from modules.automation import (
    clicar,
    duplo_clique,
    clique_direito,
    mover_mouse,
    digitar_texto,
    pressionar_tecla,
    pressionar_atalho,
    rolar,
    posicao_mouse,
)

from modules.missions import (
    listar_missoes,
    apagar_missao,
    executar_missao_salva,
    executar_missao_rapida,
    criar_missao_pesquisa,
    criar_missao_simples,
)

from modules.actions import aprender_programa


memoria = HULIMemory()
historico_conversa: list[dict] = []
MAX_HIST = 12
MODO_RESPOSTA = "normal"  # simples | normal | detalhado


OWNER = "Rony"

def verificar_permissao(usuario):
    if usuario != OWNER:
        return False
    return True

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
    # Controle da voz
    # -------------------------
    if comando in ["ativar voz", "voz on", "ligar voz", "modo falante"]:
        return f"{base} {ativar_voz()}"

    if comando in ["parar voz", "desativar voz", "voz off", "desligar voz", "modo silencioso"]:
        return f"{base} {desativar_voz()}"

    if comando in ["status voz", "voz status"]:
        status = "ATIVA" if voz_esta_ativa() else "DESATIVADA"
        return f"{base} Voz: {status}."

    # -------------------------
    # Comandos personalizados
    # -------------------------
    comando_personalizado = resolver_comando_personalizado(comando)
    if comando_personalizado:
        return processar_comando(comando_personalizado)

    # -------------------------
    # Confirmação do modo proteção
    # -------------------------
    if tem_confirmacao_pendente():
        resolvido, comando_confirmado, mensagem = resolver_confirmacao(comando)

        if resolvido:
            if comando_confirmado:
                return processar_comando(comando_confirmado)
            return f"{base} {mensagem}"

    # -------------------------
    # Modo proteção
    # -------------------------
    if comando in ["protecao on", "proteção on", "ativar protecao", "ativar proteção"]:
        return f"{base} {ativar_protecao()}"

    if comando in ["protecao off", "proteção off", "desativar protecao", "desativar proteção"]:
        return f"{base} {desativar_protecao()}"

    if comando in ["status protecao", "status proteção"]:
        return f"{base} Modo proteção: {status_protecao()}"

    if requer_confirmacao(comando):
        return f"{base} {registrar_confirmacao_pendente(comando)}"

    # -------------------------
    # Missões naturais multietapas
    # -------------------------
    if (
        " e clique em " in comando
        or " e pesquise " in comando
        or ", pesquise " in comando
    ):
        resposta_missao = executar_missao_rapida(comando)
        if resposta_missao != "Missão não reconhecida.":
            return resposta_missao

    # -------------------------
    # Resumo da conversa
    # -------------------------
    if comando in ["resumir conversa", "resumo da conversa"]:
        if not historico_conversa:
            return f"{base} Não há conversa suficiente para resumir."

        resumo = responder_ia(
            "Resuma a conversa até agora.",
            historico=historico_conversa,
            modo="simples"
        )
        return f"{base} {resumo}"

    # -------------------------
    # Intenção natural
    # -------------------------
    intencao = interpretar_intencao(comando)
    if intencao:
        tipo = intencao.get("tipo")
        valor = intencao.get("valor", "").strip()

        if tipo == "site":
            ok, resposta = abrir_site(valor)
            if ok:
                return resposta

        elif tipo == "pesquisa":
            _, resposta = pesquisar_web(valor)
            return resposta

        elif tipo == "abrir":
            ok_rotina, resposta_rotina = executar_rotina(
                valor,
                abrir_programa,
                abrir_site,
                abrir_pasta,
                executar_comando_terminal,
                abrir_arquivo
            )
            if ok_rotina:
                registrar_log("rotina", resposta_rotina)
                return f"{base} {resposta_rotina}"

            ok_site, resposta_site = abrir_site(valor)
            if ok_site:
                return resposta_site

            _, resposta_pc = abrir_programa(valor)
            return resposta_pc

    # -------------------------
    # Conversa dinâmica
    # -------------------------
    if comando in ["kkk", "haha", "rs", "kakak", "lol"]:
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
    # Monitoramento / histórico
    # -------------------------
    if comando in ["status sistema", "diagnostico", "diagnóstico"]:
        return status_sistema()

    if comando in ["historico", "histórico de comandos"]:
        hist = listar_historico()

        if not hist:
            return "Nenhum comando registrado."

        resposta = "Histórico recente:\n"
        for c in hist[-10:]:
            resposta += f"- {c}\n"

        return resposta

    
    # -------------------------
    # Medicamentos / horários
    # -------------------------
    if any(palavra in comando for palavra in ["remedio", "remédio", "medicamento", "dose"]):
        return processar_pedido_medicamento(comando)
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

            if " com " not in texto:
                return f"{base} Use assim: criar rotina trabalho com chrome, vscode"

            nome, itens = texto.split(" com ", 1)
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

    if comando.startswith("apagar rotina "):
        nome = comando.replace("apagar rotina ", "", 1).strip()
        ok, resposta = apagar_rotina(nome)
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
    # Hábitos
    # -------------------------
    if comando in ["mostrar habitos", "mostrar hábitos", "ver habitos", "memoria operacional"]:
        habitos = listar_habitos()

        if not habitos:
            return f"{base} Ainda não aprendi nenhum padrão."

        resposta = "Padrões aprendidos:\n"
        for anterior, proximos in habitos.items():
            resposta += f"\n{anterior} →\n"
            for prox, qtd in proximos.items():
                resposta += f"   - {prox} ({qtd}x)\n"

        return resposta

    if comando in ["limpar habitos", "limpar hábitos", "resetar habitos"]:
        return f"{base} {limpar_habitos()}"

    # -------------------------
    # Ajuda
    # -------------------------
    if comando in ["ajuda", "help", "socorro", "o que voce faz", "o que você faz"]:
        return obter_ajuda()

    # -------------------------
    # Lembretes
    # -------------------------.
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
    # 
    # 
    # 
    # emória categorizada
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
        conhecimento = listar_tudo()

        if not conhecimento:
            return f"{base} Ainda não aprendi nada na memória permanente."

        resposta = "Isto é o que eu aprendi:\n"
        for chave, valor in conhecimento.items():
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
    # Perfil do usuário
    # -------------------------
    if comando.startswith("definir nome "):
        valor = comando.replace("definir nome ", "", 1).strip()
        return f"{base} {definir_valor('nome', valor)}"

    if comando.startswith("definir navegador "):
        valor = comando.replace("definir navegador ", "", 1).strip()
        return f"{base} {definir_valor('navegador_padrao', valor)}"

    if comando.startswith("definir horario trabalho ") or comando.startswith("definir horário trabalho "):
        valor = (
            comando.replace("definir horario trabalho ", "", 1)
            .replace("definir horário trabalho ", "", 1)
            .strip()
        )
        return f"{base} {definir_valor('horario_trabalho', valor)}"

    if comando in ["meu perfil", "mostrar perfil"]:
        perfil = listar_perfil()

        if not perfil:
            return f"{base} Seu perfil ainda está vazio."

        resposta = "Perfil do usuário:\n"
        for k, v in perfil.items():
            resposta += f"- {k}: {v}\n"
        return resposta

    if comando in ["limpar perfil"]:
        return f"{base} {limpar_perfil()}"

    # -------------------------
    # Logs
    # -------------------------
    if comando in ["mostrar logs", "ver logs", "listar logs"]:
        linhas = ler_logs(50)

        if not linhas:
            return f"{base} Ainda não existem logs."

        resposta = "Logs recentes:\n"
        for linha in linhas:
            resposta += linha
        return resposta

    if comando in ["limpar logs", "apagar logs"]:
        return f"{base} {limpar_logs()}"

    # -------------------------
    # Autoexecução
    # -------------------------
    if comando in ["listar autoexecucoes", "listar autoexecuções", "mostrar autoexecucoes", "mostrar autoexecuções"]:
        autos = listar_autoexecucoes()

        if not autos:
            return f"{base} Ainda não existem autoexecuções cadastradas."

        resposta = "Autoexecuções ativas:\n"
        for base_cmd, prox_cmd in autos.items():
            resposta += f"- depois de '{base_cmd}' => '{prox_cmd}'\n"
        return resposta

    if comando.startswith("desativar autoexecucao ") or comando.startswith("desativar autoexecução "):
        nome = (
            comando.replace("desativar autoexecucao ", "", 1)
            .replace("desativar autoexecução ", "", 1)
            .strip()
        )
        ok, resposta = desativar_autoexecucao(nome)
        return f"{base} {resposta}"

    if comando in ["limpar autoexecucoes", "limpar autoexecuções"]:
        return f"{base} {limpar_autoexecucoes()}"

    # -------------------------
    # Sair
    # -------------------------
    if comando == "sair":
        return "ENCERRAR"
    
    resposta_ia = responder_ia(comando, historico=historico_conversa, modo=MODO_RESPOSTA)
    
        # -------------------------
    # Cumprimentos para pessoas
    # -------------------------
    if comando.startswith("cumprimenta "):
        nome = comando.replace("cumprimenta ", "", 1).strip()
        nome = nome.replace("minha namorada ", "").replace("meu namorado ", "")
        nome = nome.replace("minha esposa ", "").replace("meu esposo ", "")
        nome = nome.strip()

        if not nome:
            return f"{base} Quem você quer que eu cumprimente?"

        return f"Olá, {nome.title()}! Tudo bem? Eu sou a H.U.L.I, assistente inteligente do Rony. É um prazer falar com você."

    if comando.startswith("diz oi pra ") or comando.startswith("dis oi pra "):
        nome = (
            comando.replace("diz oi pra ", "", 1)
            .replace("dis oi pra ", "", 1)
            .strip()
        )

        if not nome:
            return f"{base} Para quem você quer que eu diga oi?"

        return f"Oi, {nome.title()}! Eu sou a H.U.L.I. O Rony pediu para eu te mandar um oi com carinho."

    # -------------------------
    # Configurações centrais
    # -------------------------
    if comando in ["mostrar configuracoes", "mostrar configurações", "listar configuracoes", "listar configurações"]:
        configs = listar_config()

        resposta = "Configurações da H.U.L.I:\n"
        for chave, valor in configs.items():
            resposta += f"- {chave}: {valor}\n"

        return resposta

    if comando.startswith("definir usuario "):
        valor = comando.replace("definir usuario ", "", 1).strip()
        return f"{base} {definir('usuario', valor)}"

    if comando.startswith("definir empresa "):
        valor = comando.replace("definir empresa ", "", 1).strip()
        return f"{base} {definir('empresa', valor)}"

    if comando.startswith("definir personalidade "):
        valor = comando.replace("definir personalidade ", "", 1).strip()
        return f"{base} {definir('personalidade', valor)}"

    if comando.startswith("definir limite fala "):
        try:
            valor = int(comando.replace("definir limite fala ", "", 1).strip())
            return f"{base} {definir('limite_fala', valor)}"
        except Exception:
            return f"{base} Use assim: definir limite fala 250"

    if comando.startswith("definir bluetooth padrao ") or comando.startswith("definir bluetooth padrão "):
        valor = (
            comando.replace("definir bluetooth padrao ", "", 1)
            .replace("definir bluetooth padrão ", "", 1)
            .strip()
        )
        return f"{base} {definir('bluetooth_dispositivo_padrao', valor)}"

    if comando in ["qual bluetooth padrao", "qual bluetooth padrão"]:
        return f"{base} Bluetooth padrão: {obter('bluetooth_dispositivo_padrao', 'não definido')}"



    # -------------------------
    # Fallback IA com contexto
    # -------------------------

        # -------------------------
    # Modo social
    # -------------------------
    if comando.startswith("se apresenta para "):
        nome = comando.replace("se apresenta para ", "", 1).strip()
        return se_apresentar_para(nome)

    if comando.startswith("se apresente para "):
        nome = comando.replace("se apresente para ", "", 1).strip()
        return se_apresentar_para(nome)

    if comando.startswith("cumprimenta "):
        nome = comando.replace("cumprimenta ", "", 1).strip()
        return cumprimentar(nome)

    if comando.startswith("diz oi pra ") or comando.startswith("dis oi pra "):
        nome = (
            comando.replace("diz oi pra ", "", 1)
            .replace("dis oi pra ", "", 1)
            .strip()
        )
        return cumprimentar(nome)

    if comando.startswith("elogia "):
        nome = comando.replace("elogia ", "", 1).strip()
        return elogiar(nome)

    if comando.startswith("elogiar "):
        nome = comando.replace("elogiar ", "", 1).strip()
        return elogiar(nome)

    if comando.startswith("mande um recado para ") and " dizendo que " in comando:
        texto = comando.replace("mande um recado para ", "", 1)
        nome, mensagem = texto.split(" dizendo que ", 1)
        return recado(nome.strip(), mensagem.strip())

    if comando.startswith("manda um recado para ") and " dizendo que " in comando:
        texto = comando.replace("manda um recado para ", "", 1)
        nome, mensagem = texto.split(" dizendo que ", 1)
        return recado(nome.strip(), mensagem.strip())


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