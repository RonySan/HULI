import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from neural.health_engine import gerar_relatorio_neural

from core_system.skill_manager import listar_skills, obter_skill, status_skills
from core_system.kernel import obter_kernel
from core_system.context import resumo_contexto


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def garantir_pasta_docs():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)


def gerar_documentacao_pdf():
    garantir_pasta_docs()

    nome_arquivo = datetime.now().strftime("HULI_DOCUMENTACAO_%Y%m%d_%H%M%S.pdf")
    caminho = os.path.join(DOCS_DIR, nome_arquivo)

    doc = SimpleDocTemplate(caminho, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    kernel = obter_kernel().status()
    contexto = resumo_contexto()
    skills_status = status_skills()
    skills = listar_skills()
    relatorio_neural = gerar_relatorio_neural()

    story.append(Paragraph("H.U.L.I — Documentação Automática", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Humano Único Leal Inteligente", styles["Heading2"]))
    story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 18))

    story.append(Paragraph("1. Status do Kernel", styles["Heading1"]))
    for chave, valor in kernel.items():
        story.append(Paragraph(f"<b>{chave}</b>: {valor}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("2. Contexto Atual", styles["Heading1"]))
    for chave, valor in contexto.items():
        story.append(Paragraph(f"<b>{chave}</b>: {valor}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("3. Relatório Neural", styles["Heading1"]))
    story.append(Paragraph(f"<b>Saúde neural:</b> {relatorio_neural.get('saude')}%", styles["Normal"]))

    scan = relatorio_neural.get("scan", {})
    story.append(Paragraph(f"<b>Arquivos Python:</b> {scan.get('arquivos_py')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Arquivos JSON:</b> {scan.get('arquivos_json')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Classes:</b> {scan.get('classes')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Funções:</b> {scan.get('funcoes')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Linhas:</b> {scan.get('linhas')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Erros de sintaxe:</b> {scan.get('erros_sintaxe')}", styles["Normal"]))

    story.append(Paragraph("<b>Sugestões:</b>", styles["Normal"]))
    for sugestao in relatorio_neural.get("sugestoes", []):
        story.append(Paragraph(f"• {sugestao}", styles["Normal"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("4. Skills Registradas", styles["Heading1"]))
    story.append(Paragraph(f"Total de skills: {skills_status.get('total_skills')}", styles["Normal"]))

    for nome in skills:
        skill = obter_skill(nome)
        if not skill:
            continue

        story.append(Spacer(1, 10))
        story.append(Paragraph(nome.upper(), styles["Heading2"]))
        story.append(Paragraph(skill.get("descricao", ""), styles["Normal"]))

        story.append(Paragraph("<b>Módulos:</b>", styles["Normal"]))
        for modulo in skill.get("modulos", []):
            story.append(Paragraph(f"• {modulo}", styles["Normal"]))

        story.append(Paragraph("<b>Comandos principais:</b>", styles["Normal"]))
        for comando in skill.get("comandos", []):
            story.append(Paragraph(f"• {comando}", styles["Normal"]))

    doc.build(story)

    return f"PDF gerado com sucesso em: {caminho}"