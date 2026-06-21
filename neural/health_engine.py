import json
import os

from neural.scanner import resumo_scan, listar_jsons
from neural.dependency_map import resumo_dependencias
from core_system.kernel import obter_kernel
from core_system.context import resumo_contexto
from core_system.skill_manager import status_skills
from core_system.event_bus import listar_eventos


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def testar_jsons():
    resultado = []

    for caminho in listar_jsons():
        rel = os.path.relpath(caminho, BASE_DIR)

        try:
            with open(caminho, "r", encoding="utf-8") as f:
                json.load(f)

            resultado.append({
                "arquivo": rel,
                "status": "OK",
                "detalhe": "JSON válido"
            })

        except Exception as e:
            resultado.append({
                "arquivo": rel,
                "status": "ERRO",
                "detalhe": str(e)
            })

    return resultado


def gerar_relatorio_neural():
    scan = resumo_scan()
    deps = resumo_dependencias()
    jsons = testar_jsons()

    kernel = obter_kernel().status()
    contexto = resumo_contexto()
    skills = status_skills()
    eventos = listar_eventos()

    erros_json = [j for j in jsons if j["status"] == "ERRO"]
    imports_suspeitos = deps.get("imports_suspeitos", [])

    pontos = 100

    pontos -= scan["erros_sintaxe"] * 10
    pontos -= len(erros_json) * 5
    pontos -= len(imports_suspeitos) * 3

    if pontos < 0:
        pontos = 0

    return {
        "saude": pontos,
        "scan": scan,
        "dependencias": deps,
        "jsons": {
            "total": len(jsons),
            "erros": erros_json,
        },
        "kernel": kernel,
        "contexto": contexto,
        "skills": skills,
        "eventos_recentes": len(eventos),
        "sugestoes": gerar_sugestoes(scan, deps, erros_json),
    }


def gerar_sugestoes(scan, deps, erros_json):
    sugestoes = []

    if scan["erros_sintaxe"] > 0:
        sugestoes.append("Corrigir arquivos com erro de sintaxe antes de novas evoluções.")

    if erros_json:
        sugestoes.append("Corrigir arquivos JSON inválidos.")

    if deps.get("imports_suspeitos"):
        sugestoes.append("Revisar possíveis imports circulares envolvendo commands.py.")

    if scan["arquivos_py"] > 40:
        sugestoes.append("Projeto grande detectado: manter services, kernel, context e skill manager atualizados.")

    if not sugestoes:
        sugestoes.append("Arquitetura saudável. Próximo passo recomendado: Reflection Engine.")

    return sugestoes


def formatar_relatorio_neural():
    rel = gerar_relatorio_neural()

    resposta = "🧠 RELATÓRIO NEURAL DA H.U.L.I\n\n"

    resposta += f"Saúde neural: {rel['saude']}%\n\n"

    resposta += "📁 Projeto:\n"
    resposta += f"• Arquivos Python: {rel['scan']['arquivos_py']}\n"
    resposta += f"• Arquivos JSON: {rel['scan']['arquivos_json']}\n"
    resposta += f"• Classes: {rel['scan']['classes']}\n"
    resposta += f"• Funções: {rel['scan']['funcoes']}\n"
    resposta += f"• Linhas de código: {rel['scan']['linhas']}\n"
    resposta += f"• Erros de sintaxe: {rel['scan']['erros_sintaxe']}\n\n"

    resposta += "🔗 Dependências:\n"
    resposta += f"• Arquivos mapeados: {rel['dependencias']['arquivos_mapeados']}\n"
    resposta += f"• Total de imports: {rel['dependencias']['total_imports']}\n"
    resposta += f"• Imports suspeitos: {len(rel['dependencias']['imports_suspeitos'])}\n\n"

    resposta += "🧩 Skills:\n"
    resposta += f"• Total: {rel['skills'].get('total_skills')}\n\n"

    resposta += "🧬 Kernel:\n"
    resposta += f"• Usuário: {rel['kernel'].get('usuario')}\n"
    resposta += f"• Proprietário: {rel['kernel'].get('proprietario')}\n"
    resposta += f"• Threads: {rel['kernel'].get('threads')}\n"
    resposta += f"• Uptime: {rel['kernel'].get('uptime')}\n\n"

    resposta += "🧾 JSON:\n"
    resposta += f"• Total: {rel['jsons']['total']}\n"
    resposta += f"• Erros: {len(rel['jsons']['erros'])}\n\n"

    if rel["jsons"]["erros"]:
        for item in rel["jsons"]["erros"]:
            resposta += f"  - {item['arquivo']}: {item['detalhe']}\n"
        resposta += "\n"

    resposta += "💡 Sugestões:\n"
    for sugestao in rel["sugestoes"]:
        resposta += f"• {sugestao}\n"

    return resposta