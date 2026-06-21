import os
from datetime import datetime

from core_system.skill_manager import listar_skills, obter_skill, status_skills
from core_system.kernel import obter_kernel
from core_system.context import resumo_contexto


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def garantir_pasta_docs():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)


def gerar_documentacao_md():
    garantir_pasta_docs()

    caminho = os.path.join(DOCS_DIR, "HULI_DOCUMENTACAO.md")

    kernel = obter_kernel().status()
    contexto = resumo_contexto()
    skills_status = status_skills()
    skills = listar_skills()

    texto = "# H.U.L.I — Documentação Automática\n\n"
    texto += "Humano Único Leal Inteligente\n\n"
    texto += f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"

    texto += "## 1. Status do Kernel\n\n"
    for chave, valor in kernel.items():
        texto += f"- **{chave}**: {valor}\n"

    texto += "\n## 2. Contexto Atual\n\n"
    for chave, valor in contexto.items():
        texto += f"- **{chave}**: {valor}\n"

    texto += "\n## 3. Skills Registradas\n\n"
    texto += f"Total de skills: {skills_status.get('total_skills')}\n\n"

    for nome in skills:
        skill = obter_skill(nome)

        if not skill:
            continue

        texto += f"### {nome.upper()}\n\n"
        texto += f"{skill.get('descricao')}\n\n"

        texto += "**Módulos:**\n"
        for modulo in skill.get("modulos", []):
            texto += f"- {modulo}\n"

        texto += "\n**Comandos principais:**\n"
        for comando in skill.get("comandos", []):
            texto += f"- `{comando}`\n"

        texto += "\n"

    texto += "\n## 4. Arquitetura Atual\n\n"
    texto += "- Kernel\n"
    texto += "- Context\n"
    texto += "- Event Bus\n"
    texto += "- Session Memory\n"
    texto += "- Skill Manager\n"
    texto += "- Planner Service\n"
    texto += "- Personality Engine\n"
    texto += "- Conversational Brain\n"
    texto += "- Reflection Engine\n"
    texto += "- Auto Help Engine\n"
    texto += "- Neural Scanner\n"

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)

    return f"Documentação gerada com sucesso em: {caminho}"