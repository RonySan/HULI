import re
from datetime import datetime, timedelta


def extrair_intervalo_horas(texto: str):
    texto = texto.lower()

    padroes = [
        r"(\d{1,2})\s*em\s*\1\s*horas",
        r"de\s*(\d{1,2})\s*em\s*\1",
        r"a cada\s*(\d{1,2})\s*horas",
        r"(\d{1,2})h\s*em\s*\1h",
    ]

    for padrao in padroes:
        m = re.search(padrao, texto)
        if m:
            return int(m.group(1))

    return None


def extrair_horario_inicio(texto: str):
    texto = texto.lower()

    padroes = [
        r"(\d{1,2}):(\d{2})",
        r"(\d{1,2})h(\d{2})?",
        r"às\s*(\d{1,2})(?:\s*da\s*manhã|\s*da\s*tarde|\s*da\s*noite)?",
        r"as\s*(\d{1,2})(?:\s*da\s*manhã|\s*da\s*tarde|\s*da\s*noite)?",
    ]

    for padrao in padroes:
        m = re.search(padrao, texto)
        if m:
            hora = int(m.group(1))
            minuto = int(m.group(2) or 0) if len(m.groups()) > 1 else 0

            if "tarde" in texto and hora < 12:
                hora += 12

            if "noite" in texto and hora < 12:
                hora += 12

            if 0 <= hora <= 23 and 0 <= minuto <= 59:
                return f"{hora:02d}:{minuto:02d}"

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


def gerar_horarios(inicio: str, intervalo_horas: int, dias: int = 1):
    try:
        base = datetime.strptime(inicio, "%H:%M")
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


def formatar_horarios(horarios, intervalo, dias):
    resposta = (
        f"Horários do medicamento de {intervalo} em {intervalo} horas "
        f"por {dias} dia(s):\n\n"
    )

    dia_atual = None

    for item in horarios:
        if item["data"] != dia_atual:
            dia_atual = item["data"]
            resposta += f"\n📅 Dia {dia_atual}\n"

        resposta += f"• Dose {item['dose']}: {item['hora']}\n"

    resposta += (
        "\n⚠️ Observação: confirme sempre com o médico ou farmacêutico "
        "em caso de dúvida sobre dose, atraso ou troca de medicamento."
    )

    return resposta


def processar_pedido_medicamento(comando: str):
    intervalo = extrair_intervalo_horas(comando)
    inicio = extrair_horario_inicio(comando)
    dias = extrair_quantidade_dias(comando)

    if not intervalo:
        return (
            "Entendi que é sobre medicamento, mas não encontrei o intervalo.\n"
            "Exemplo: remédio de 8 em 8 horas começando às 06:30 por 10 dias."
        )

    if not inicio:
        return (
            "Entendi que é sobre medicamento, mas não encontrei o horário inicial.\n"
            "Exemplo: remédio de 8 em 8 horas começando às 06:30 por 10 dias."
        )

    ok, horarios = gerar_horarios(inicio, intervalo, dias)

    if not ok:
        return horarios

    return formatar_horarios(horarios, intervalo, dias)



def criar_lembretes_medicamento(memoria, comando: str):
    intervalo = extrair_intervalo_horas(comando)
    inicio = extrair_horario_inicio(comando)
    dias = extrair_quantidade_dias(comando)

    if not intervalo or not inicio:
        return False, "Não consegui identificar intervalo ou horário inicial."

    ok, horarios = gerar_horarios(inicio, intervalo, dias)

    if not ok:
        return False, horarios

    total = 0

    for item in horarios:
        horario = item["hora"]

        hoje = datetime.now()
        hora, minuto = map(int, horario.split(":"))

        quando = hoje.replace(hour=hora, minute=minuto, second=0, microsecond=0)

        # se o horário já passou hoje, joga para o próximo dia
        if quando <= hoje:
            quando += timedelta(days=1)

        memoria.salvar_lembrete(
            f"Dar medicamento - dose {item['dose']} ({item['hora']})",
            quando
        )
        total += 1

    return True, f"{total} lembretes de medicamento criados com sucesso."

import os


def exportar_horarios_txt(comando: str):
    intervalo = extrair_intervalo_horas(comando)
    inicio = extrair_horario_inicio(comando)
    dias = extrair_quantidade_dias(comando)

    if not intervalo or not inicio:
        return False, "Não consegui identificar intervalo ou horário inicial."

    ok, horarios = gerar_horarios(inicio, intervalo, dias)

    if not ok:
        return False, horarios

    resposta = formatar_horarios(horarios, intervalo, dias)

    pasta = os.path.join(os.getcwd(), "exports")
    os.makedirs(pasta, exist_ok=True)

    caminho = os.path.join(pasta, "horarios_medicamento.txt")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(resposta)

    return True, f"Arquivo criado com sucesso em: {caminho}"