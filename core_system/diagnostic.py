import importlib
import inspect
import json
import os
from datetime import datetime

from core_system.session_memory import obter_memoria_sessao


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PASTAS_PY = [
    "core_system",
    "modules",
    "services",
]

FUNCOES_SEGURAS = [
    "status",
    "listar",
    "carregar",
    "resumo",
    "status_skills",
    "listar_skills",
    "listar_missoes",
    "listar_rotinas",
    "listar_config",
    "resumo_contexto",
    "diagnosticar",
]

IGNORAR_ARQUIVOS = [
    "__init__.py",
]

IGNORAR_PASTAS = [
    "__pycache__",
    ".git",
    "venv",
    ".venv",
    "env",
]


def ok(msg="OK"):
    return {"status": "OK", "detalhe": str(msg)}


def erro(msg):
    return {"status": "ERRO", "detalhe": str(msg)}


def alerta(msg):
    return {"status": "ALERTA", "detalhe": str(msg)}


def caminho_para_modulo(caminho):
    rel = os.path.relpath(caminho, BASE_DIR)
    rel = rel.replace("\\", ".").replace("/", ".")

    if rel.endswith(".py"):
        rel = rel[:-3]

    return rel


def descobrir_arquivos_py():
    arquivos = []

    for pasta in PASTAS_PY:
        raiz = os.path.join(BASE_DIR, pasta)

        if not os.path.exists(raiz):
            continue

        for dirpath, dirnames, filenames in os.walk(raiz):
            dirnames[:] = [d for d in dirnames if d not in IGNORAR_PASTAS]

            for filename in filenames:
                if filename in IGNORAR_ARQUIVOS:
                    continue

                if filename.endswith(".py"):
                    arquivos.append(os.path.join(dirpath, filename))

    return arquivos


def descobrir_jsons():
    arquivos = []

    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        dirnames[:] = [d for d in dirnames if d not in IGNORAR_PASTAS]

        for filename in filenames:
            if filename.endswith(".json"):
                arquivos.append(os.path.join(dirpath, filename))

    return arquivos


def testar_imports_auto():
    resultado = {}

    arquivos = descobrir_arquivos_py()

    for caminho in arquivos:
        modulo_nome = caminho_para_modulo(caminho)

        try:
            importlib.import_module(modulo_nome)
            resultado[modulo_nome] = ok("Importado com sucesso.")
        except Exception as e:
            resultado[modulo_nome] = erro(e)

    return resultado


def testar_jsons_auto():
    resultado = {}

    arquivos = descobrir_jsons()

    for caminho in arquivos:
        rel = os.path.relpath(caminho, BASE_DIR)

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                json.load(f)

            resultado[rel] = ok("JSON válido.")

        except Exception as e:
            resultado[rel] = erro(e)

    return resultado


def testar_funcoes_seguras():
    resultado = {}

    arquivos = descobrir_arquivos_py()

    for caminho in arquivos:
        modulo_nome = caminho_para_modulo(caminho)

        try:
            modulo = importlib.import_module(modulo_nome)

            funcoes_encontradas = []

            for nome_funcao in FUNCOES_SEGURAS:
                if hasattr(modulo, nome_funcao):
                    func = getattr(modulo, nome_funcao)

                    if not callable(func):
                        continue

                    try:
                        assinatura = inspect.signature(func)

                        if len(assinatura.parameters) == 0:
                            retorno = func()
                            funcoes_encontradas.append(
                                f"{nome_funcao}(): OK"
                            )
                        else:
                            funcoes_encontradas.append(
                                f"{nome_funcao}(): ignorada, precisa parâmetros"
                            )

                    except Exception as e:
                        funcoes_encontradas.append(
                            f"{nome_funcao}(): ERRO - {e}"
                        )

            if funcoes_encontradas:
                resultado[modulo_nome] = ok("; ".join(funcoes_encontradas))

        except Exception as e:
            resultado[modulo_nome] = erro(e)

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
            "diagnostico_auto_teste",
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

        essenciais = [
            "core",
            "voz",
            "visao",
            "automacao",
            "sistema",
            "ia",
            "memoria",
        ]

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
        memoria.carregar()

        return ok("Memória carregada com sucesso.")

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


def testar_ia():
    try:
        from modules.ai import tem_internet

        internet = tem_internet()

        if internet:
            return ok("Internet disponível para IA online.")

        return alerta("Internet indisponível ou IA online sem conexão.")

    except Exception as e:
        return erro(e)


def diagnostico_completo():
    relatorio = {
        "imports_auto": testar_imports_auto(),
        "jsons_auto": testar_jsons_auto(),
        "funcoes_seguras": testar_funcoes_seguras(),
        "kernel": testar_kernel(),
        "contexto": testar_contexto(),
        "event_bus": testar_event_bus(),
        "skill_manager": testar_skill_manager(),
        "memoria": testar_memoria(),
        "missoes": testar_missoes(),
        "rotinas": testar_rotinas(),
        "medicamentos": testar_medicamentos(),
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

    resposta = "🩺 AUTO DIAGNÓSTICO COMPLETO DA H.U.L.I\n\n"
    resposta += f"Saúde geral: {saude['saude']}%\n"
    resposta += f"Testes: {saude['total_testes']}\n"
    resposta += f"OK: {saude['ok']}\n"
    resposta += f"Alertas: {saude['alertas']}\n"
    resposta += f"Erros: {saude['erros']}\n\n"

    for categoria, dados in relatorio.items():
        resposta += f"📌 {categoria.upper()}\n"

        if isinstance(dados, dict) and "status" in dados:
            resposta += f"• {dados['status']}: {dados['detalhe']}\n\n"
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