import os
import re

from datetime import datetime, timedelta

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet


# =====================================================
# EXTRAÇÃO DE DADOS
# =====================================================

def extrair_intervalo_horas(texto: str):
    texto = texto.lower()

    padroes = [
        r"(\d{1,2})\s*em\s*\1\s*horas",
        r"(\d{1,2})\s*em\s*\1\s*hora",
        r"(\d{1,2})\s*e\s*\1\s*horas",
        r"(\d{1,2})\s*e\s*\1\s*hora",
        r"de\s*(\d{1,2})\s*em\s*\1",
        r"a cada\s*(\d{1,2})\s*horas",
        r"a cada\s*(\d{1,2})\s*hora",
        r"(\d{1,2})h\s*em\s*\1h",
    ]

    for padrao in padroes:
        m = re.search(padrao, texto)

        if m:
            return int(m.group(1))

    return None


def extrair_horario_inicio(texto: str):
    texto = texto.lower()

    # 06:30
    m = re.search(r"\b(\d{1,2}):(\d{2})\b", texto)
    if m:
        hora = int(m.group(1))
        minuto = int(m.group(2))

        if 0 <= hora <= 23 and 0 <= minuto <= 59:
            return f"{hora:02d}:{minuto:02d}"

    # 6 30 / 06 30
    m = re.search(r"\b(\d{1,2})\s+(\d{2})\b", texto)
    if m:
        hora = int(m.group(1))
        minuto = int(m.group(2))

        if 0 <= hora <= 23 and 0 <= minuto <= 59:
            return f"{hora:02d}:{minuto:02d}"

    # 6h30
    m = re.search(r"\b(\d{1,2})h(\d{2})\b", texto)
    if m:
        hora = int(m.group(1))
        minuto = int(m.group(2))

        if 0 <= hora <= 23 and 0 <= minuto <= 59:
            return f"{hora:02d}:{minuto:02d}"

    # 6h
    m = re.search(r"\b(\d{1,2})h\b", texto)
    if m:
        hora = int(m.group(1))

        if 0 <= hora <= 23:
            return f"{hora:02d}:00"

    # às 6 da manhã / as 6 da tarde
    m = re.search(
        r"\b(?:as|às)\s*(\d{1,2})(?:\s*da\s*(manhã|manha|tarde|noite))?\b",
        texto
    )
    if m:
        hora = int(m.group(1))
        periodo = m.group(2)

        if periodo in ["tarde", "noite"] and hora < 12:
            hora += 12

        if 0 <= hora <= 23:
            return f"{hora:02d}:00"

    return None

def extrair_quantidade_dias(texto: str):
    texto = texto.lower()

    m = re.search(r"por\s*(\d{1,3})\s*dias", texto)

    if m:
        return int(m.group(1))

    m = re.search(r"durante\s*(\d{1,3})\s*dias", texto)

    if m:
        return int(m.group(1))

    return 1


# =====================================================
# GERAÇÃO DE HORÁRIOS
# =====================================================

def gerar_horarios(inicio: str, intervalo_horas: int, dias: int = 1):
    try:
        hora, minuto = map(int, inicio.split(":"))

        agora = datetime.now()

        base = agora.replace(
            hour=hora,
            minute=minuto,
            second=0,
            microsecond=0
        )

    except Exception:
        return False, "Horário inválido. Use HH:MM."

    if intervalo_horas <= 0:
        return False, "Intervalo inválido."

    total_doses = int((24 / intervalo_horas) * dias)

    horarios = []
    atual = base

    for i in range(total_doses):

        horarios.append({
            "dose": i + 1,
            "data": atual.strftime("%d/%m"),
            "hora": atual.strftime("%H:%M"),
        })

        atual += timedelta(hours=intervalo_horas)

    return True, horarios


# =====================================================
# FORMATAÇÃO
# =====================================================

def formatar_horarios(horarios, intervalo, dias):

    resposta = (
        f"Horários do medicamento de "
        f"{intervalo} em {intervalo} horas "
        f"por {dias} dia(s):\n\n"
    )

    dia_atual = None

    for item in horarios:

        if item["data"] != dia_atual:

            dia_atual = item["data"]

            resposta += f"\n📅 Dia {dia_atual}\n"

        resposta += (
            f"• Dose {item['dose']}: "
            f"{item['hora']}\n"
        )

    resposta += (
        "\n⚠️ Observação: confirme sempre "
        "com médico ou farmacêutico "
        "em caso de dúvida."
    )

    return resposta


# =====================================================
# PROCESSAMENTO PRINCIPAL
# =====================================================

def processar_pedido_medicamento(comando: str):

    intervalo = extrair_intervalo_horas(comando)
    inicio = extrair_horario_inicio(comando)
    dias = extrair_quantidade_dias(comando)

    if not intervalo:

        return (
            "Entendi que é sobre medicamento, "
            "mas não encontrei o intervalo.\n"
            "Exemplo: remédio de 8 em 8 horas "
            "começando às 06:30 por 10 dias."
        )

    if not inicio:

        return (
            "Entendi que é sobre medicamento, "
            "mas não encontrei o horário inicial.\n"
            "Exemplo: remédio de 8 em 8 horas "
            "começando às 06:30 por 10 dias."
        )

    ok, horarios = gerar_horarios(
        inicio,
        intervalo,
        dias
    )

    if not ok:
        return horarios

    return formatar_horarios(
        horarios,
        intervalo,
        dias
    )


# =====================================================
# LEMBRETES
# =====================================================

def criar_lembretes_medicamento(memoria, comando: str):

    intervalo = extrair_intervalo_horas(comando)
    inicio = extrair_horario_inicio(comando)
    dias = extrair_quantidade_dias(comando)

    if not intervalo or not inicio:
        return False, (
            "Não consegui identificar "
            "intervalo ou horário inicial."
        )

    ok, horarios = gerar_horarios(
        inicio,
        intervalo,
        dias
    )

    if not ok:
        return False, horarios

    total = 0

    agora = datetime.now()

    for item in horarios:

        hora, minuto = map(
            int,
            item["hora"].split(":")
        )

        quando = agora.replace(
            hour=hora,
            minute=minuto,
            second=0,
            microsecond=0
        )

        memoria.salvar_lembrete(
            f"Dar medicamento - "
            f"dose {item['dose']} "
            f"({item['hora']})",
            quando
        )

        total += 1

    return True, (
        f"{total} lembretes criados "
        f"com sucesso."
    )


# =====================================================
# EXPORTAÇÃO
# =====================================================

def abrir_arquivo_exportado(caminho: str):

    try:
        os.startfile(caminho)
        return True

    except Exception:
        return False


def exportar_horarios_txt(comando: str):

    intervalo = extrair_intervalo_horas(comando)
    inicio = extrair_horario_inicio(comando)
    dias = extrair_quantidade_dias(comando)

    if not intervalo or not inicio:
        return False, (
            "Não consegui identificar "
            "intervalo ou horário inicial."
        )

    ok, horarios = gerar_horarios(
        inicio,
        intervalo,
        dias
    )

    if not ok:
        return False, horarios

    resposta = formatar_horarios(
        horarios,
        intervalo,
        dias
    )

    pasta = os.path.join(
        os.getcwd(),
        "exports"
    )

    os.makedirs(
        pasta,
        exist_ok=True
    )

    caminho = os.path.join(
        pasta,
        "horarios_medicamento.txt"
    )

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(resposta)

    abrir_arquivo_exportado(caminho)

    return True, (
        f"TXT criado com sucesso em:\n"
        f"{caminho}"
    )


def exportar_horarios_pdf(comando: str):

    intervalo = extrair_intervalo_horas(comando)
    inicio = extrair_horario_inicio(comando)
    dias = extrair_quantidade_dias(comando)

    if not intervalo or not inicio:
        return False, (
            "Não consegui identificar "
            "intervalo ou horário inicial."
        )

    ok, horarios = gerar_horarios(
        inicio,
        intervalo,
        dias
    )

    if not ok:
        return False, horarios

    pasta = os.path.join(
        os.getcwd(),
        "exports"
    )

    os.makedirs(
        pasta,
        exist_ok=True
    )

    caminho = os.path.join(
        pasta,
        "horarios_medicamento.pdf"
    )

    doc = SimpleDocTemplate(
        caminho,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph(
            "<b>Horários de Medicamento</b>",
            styles["Title"]
        )
    )

    elementos.append(
        Spacer(1, 12)
    )

    elementos.append(
        Paragraph(
            f"""
            Intervalo:
            de {intervalo} em {intervalo} horas
            <br/>
            Período:
            {dias} dia(s)
            <br/>
            Horário inicial:
            {inicio}
            """,
            styles["BodyText"]
        )
    )

    elementos.append(
        Spacer(1, 16)
    )

    dia_atual = None

    for item in horarios:

        if item["data"] != dia_atual:

            dia_atual = item["data"]

            elementos.append(
                Spacer(1, 10)
            )

            elementos.append(
                Paragraph(
                    f"<b>Dia {dia_atual}</b>",
                    styles["Heading2"]
                )
            )

        elementos.append(
            Paragraph(
                f"""
                Dose {item['dose']}:
                {item['hora']}
                """,
                styles["BodyText"]
            )
        )

    elementos.append(
        Spacer(1, 18)
    )

    elementos.append(
        Paragraph(
            """
            Observação:
            confirme sempre com médico
            ou farmacêutico em caso
            de dúvida.
            """,
            styles["Italic"]
        )
    )

    doc.build(elementos)

    abrir_arquivo_exportado(caminho)

    return True, (
        f"PDF criado com sucesso em:\n"
        f"{caminho}"
    )