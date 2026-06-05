import importlib
import json
import os
from datetime import datetime
from core_system.session_memory import obter_memoria_sessao


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


MODULOS_CRITICOS = {
    "kernel": "core_system.kernel",
    "context": "core_system.context",
    "event_bus": "core_system.event_bus",
    "skill_manager": "core_system.skill_manager",
    "router": "core_system.router",
    "brain": "core_system.brain",

    "commands": "modules.commands",
    "memory": "modules.memory",
    "smart_memory": "modules.smart_memory",
    "missions": "modules.missions",
    "routines": "modules.routines",
    "logger": "modules.logger",
    "voice": "modules.voice",
    "voice_mode": "modules.voice_mode",
    "automation": "modules.automation",
    "vision": "modules.vision",
    "vision_ai": "modules.vision_ai",
    "windows_control": "modules.windows_control",
    "medication": "modules.medication",
    "settings_manager": "modules.settings_manager",
    "jarvis_mode": "modules.jarvis_mode",
    "protection": "modules.protection",
    "ai": "modules.ai",

    "system_service": "services.system_service",
    "voice_service": "services.voice_service",
    "vision_service": "services.vision_service",
    "automation_service": "services.automation_service",
    "memory_service": "services.memory_service",
    "ai_service": "services.ai_service",
}


ARQUIVOS_JSON = [
    "modules/missions.json",
    "modules/routines.json",
    "modules/habits.json",
    "modules/smart_memory.json",
    "modules/reminders.json",
    "config/settings.json",
]


def ok(msg="OK"):
    return {"status": "OK", "detalhe": msg}


def erro(msg):
    return {"status": "ERRO", "detalhe": str(msg)}


def alerta(msg):
    return {"status": "ALERTA", "detalhe": str(msg)}


def testar_imports():
    resultado = {}

    for nome, caminho in MODULOS_CRITICOS.items():
        try:
            importlib.import_module(caminho)
            resultado[nome] = ok("Importado com sucesso.")
        except Exception as e:
            resultado[nome] = erro(e)

    return resultado


def testar_jsons():
    resultado = {}

    for arquivo in ARQUIVOS_JSON:
        caminho = os.path.join(BASE_DIR, arquivo)

        if not os.path.exists(caminho):
            resultado[arquivo] = alerta("Arquivo não encontrado.")
            continue

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                json.load(f)

            resultado[arquivo] = ok("JSON válido.")

        except Exception as e:
            resultado[arquivo] = erro(e)

    return resultado


def testar_kernel():
    try:
        from core_system.kernel import obter_kernel

        kernel = obter_kernel()
        status = kernel.status()

        obrigatorios = [
            "usuario",
            "proprietario",
            "modo_conversa",
            "escuta_continua",
            "jarvis",
            "voz",
            "ultimo_comando",
            "threads",
            "uptime",
        ]

        faltando = [k for k in obrigatorios if k not in status]

        if faltando:
            return erro(f"Campos ausentes no kernel: {faltando}")

        return ok(f"Kernel ativo. Threads: {status.get('threads')}")

    except Exception as e:
        return erro(e)


def testar_contexto():
    try:
        from core_system.context import resumo_contexto

        ctx = resumo_contexto()

        obrigatorios = [
            "usuario_atual",
            "proprietario",
            "visitante",
            "empresa",
            "voz_ativa",
            "modo_jarvis",
            "modo_conversa",
            "escuta_continua",
        ]

        faltando = [k for k in obrigatorios if k not in ctx]

        if faltando:
            return erro(f"Campos ausentes no contexto: {faltando}")

        return ok("Contexto sincronizado com kernel.")

    except Exception as e:
        return erro(e)


def testar_event_bus():
    try:
        from core_system.event_bus import emitir_evento, listar_eventos

        emitir_evento(
            "diagnostico_teste",
            origem="diagnostic",
            dados={"data": datetime.now().isoformat()}
        )

        eventos = listar_eventos()

        if not eventos:
            return erro("Evento não foi registrado.")

        return ok(f"Event Bus funcionando. Eventos recentes: {len(eventos)}")

    except Exception as e:
        return erro(e)


def testar_skill_manager():
    try:
        from core_system.skill_manager import listar_skills, obter_skill, status_skills

        skills = listar_skills()
        status = status_skills()

        if not skills:
            return erro("Nenhuma skill registrada.")

        if status.get("total_skills", 0) != len(skills):
            return alerta("Quantidade de skills inconsistente.")

        essenciais = ["core", "voz", "visao", "automacao", "sistema", "ia", "memoria"]

        faltando = [s for s in essenciais if not obter_skill(s)]

        if faltando:
            return alerta(f"Skills essenciais ausentes: {faltando}")

        return ok(f"{len(skills)} skills registradas.")

    except Exception as e:
        return erro(e)


def testar_memoria():
    try:
        from modules.memory import HULIMemory

        memoria = HULIMemory()
        dados = memoria.carregar()

        return ok("Memória carregada com sucesso.")

    except Exception as e:
        return erro(e)


def testar_smart_memory():
    try:
        from modules.smart_memory import carregar

        dados = carregar()

        if not isinstance(dados, dict):
            return erro("Smart memory não retornou dicionário.")

        return ok("Smart memory carregada.")

    except Exception as e:
        return erro(e)


def testar_missoes():
    try:
        from modules.missions import carregar_missoes, listar_missoes

        dados = carregar_missoes()
        missoes = listar_missoes()

        if not isinstance(dados, dict):
            return erro("missions.json inválido.")

        return ok(f"{len(missoes)} missões registradas.")

    except Exception as e:
        return erro(e)


def testar_rotinas():
    try:
        from modules.routines import listar_rotinas

        rotinas = listar_rotinas()

        if rotinas is None:
            return alerta("Nenhuma rotina retornada.")

        return ok(f"{len(rotinas)} rotinas registradas.")

    except Exception as e:
        return erro(e)


def testar_configuracoes():
    try:
        from modules.settings_manager import listar_config

        configs = listar_config()

        if not isinstance(configs, dict):
            return erro("Configurações não retornaram dicionário.")

        essenciais = ["usuario", "empresa", "personalidade"]

        faltando = [c for c in essenciais if c not in configs]

        if faltando:
            return alerta(f"Configurações ausentes: {faltando}")

        return ok("Configurações carregadas.")

    except Exception as e:
        return erro(e)


def testar_logs():
    try:
        from modules.logger import registrar_log, ler_logs

        registrar_log("diagnostico", "Teste de log automático.")
        logs = ler_logs(5)

        if logs is None:
            return erro("Logs não retornaram dados.")

        return ok("Logger funcionando.")

    except Exception as e:
        return erro(e)


def testar_medicamentos():
    try:
        from modules.medication import processar_pedido_medicamento

        resposta = processar_pedido_medicamento(
            "remedio de 8 em 8 horas a partir das 6:30 por 1 dias"
        )

        if "06:30" not in resposta:
            return alerta("Medicamento respondeu, mas horário esperado não apareceu.")

        return ok("Módulo de medicamentos funcionando.")

    except Exception as e:
        return erro(e)


def testar_services():
    resultado = {}

    testes = {
        "system_service": ("services.system_service", "status"),
        "voice_service": ("services.voice_service", "status"),
        "vision_service": ("services.vision_service", None),
        "automation_service": ("services.automation_service", None),
        "memory_service": ("services.memory_service", None),
        "ai_service": ("services.ai_service", "online"),
    }

    for nome, dados in testes.items():
        modulo_nome, funcao = dados

        try:
            modulo = importlib.import_module(modulo_nome)

            if funcao:
                getattr(modulo, funcao)()

            resultado[nome] = ok("Service carregado.")

        except Exception as e:
            resultado[nome] = erro(e)

    return resultado


def testar_ia():
    try:
        from modules.ai import tem_internet

        internet = tem_internet()

        if internet:
            return ok("Internet disponível para IA online.")
        else:
            return alerta("Internet indisponível ou IA online sem conexão.")

    except Exception as e:
        return erro(e)


def diagnostico_completo():
    relatorio = {
        "imports": testar_imports(),
        "jsons": testar_jsons(),
        "kernel": testar_kernel(),
        "contexto": testar_contexto(),
        "event_bus": testar_event_bus(),
        "skill_manager": testar_skill_manager(),
        "memoria": testar_memoria(),
        "smart_memory": testar_smart_memory(),
        "missoes": testar_missoes(),
        "rotinas": testar_rotinas(),
        "configuracoes": testar_configuracoes(),
        "logs": testar_logs(),
        "medicamentos": testar_medicamentos(),
        "services": testar_services(),
        "ia": testar_ia(),
    }

    return relatorio


def calcular_saude(relatorio):
    total = 0
    ok_count = 0
    alertas = 0
    erros = 0

    def contar(item):
        nonlocal total, ok_count, alertas, erros

        if isinstance(item, dict) and "status" in item:
            total += 1

            if item["status"] == "OK":
                ok_count += 1
            elif item["status"] == "ALERTA":
                alertas += 1
            else:
                erros += 1

        elif isinstance(item, dict):
            for v in item.values():
                contar(v)

    contar(relatorio)

    porcentagem = 0

    if total:
        porcentagem = round((ok_count / total) * 100, 2)

    return {
        "total_testes": total,
        "ok": ok_count,
        "alertas": alertas,
        "erros": erros,
        "saude": porcentagem,
    }


def formatar_diagnostico(relatorio):
    saude = calcular_saude(relatorio)

    resposta = "🩺 DIAGNÓSTICO COMPLETO DA H.U.L.I\n\n"

    resposta += f"Saúde geral: {saude['saude']}%\n"
    resposta += f"Testes: {saude['total_testes']}\n"
    resposta += f"OK: {saude['ok']}\n"
    resposta += f"Alertas: {saude['alertas']}\n"
    resposta += f"Erros: {saude['erros']}\n\n"

    for categoria, dados in relatorio.items():
        resposta += f"📌 {categoria.upper()}\n"

        if isinstance(dados, dict) and "status" in dados:
            status = dados["status"]
            detalhe = dados["detalhe"]
            resposta += f"• {status}: {detalhe}\n\n"
            continue

        if isinstance(dados, dict):
            for nome, item in dados.items():
                if isinstance(item, dict):
                    resposta += f"• {nome}: {item['status']} - {item['detalhe']}\n"
                else:
                    resposta += f"• {nome}: {item}\n"

        resposta += "\n"

    return resposta


def diagnosticar():
    return diagnostico_completo()


def diagnosticar_formatado():
    relatorio = diagnostico_completo()
    texto = formatar_diagnostico(relatorio)

    memoria = obter_memoria_sessao()
    memoria.registrar_diagnostico(relatorio, texto)

    return texto