import json
import os
import re
from datetime import datetime, timedelta


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARQUIVO_AGENDA = os.path.join(DATA_DIR, "calendar.json")


def garantir_arquivo():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(ARQUIVO_AGENDA):
        with open(ARQUIVO_AGENDA, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


def carregar_agenda():
    garantir_arquivo()

    try:
        with open(ARQUIVO_AGENDA, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def salvar_agenda(eventos):
    garantir_arquivo()

    with open(ARQUIVO_AGENDA, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)


def gerar_id():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def normalizar_texto(texto):
    return texto.lower().strip()


def extrair_horario(texto):
    texto = texto.lower()
    texto = texto.replace("às", "as")
    texto = texto.replace("á", "a")
    texto = texto.replace("ã", "a")

    padroes = [
        r"\b(?:as\s*)?(\d{1,2}):(\d{2})\b",
        r"\b(?:as\s*)?(\d{1,2})h(\d{2})\b",
        r"\b(?:as\s*)?(\d{1,2})h\b",
        r"\b(?:as\s*)?(\d{1,2})\s+(\d{2})\b",
    ]

    for padrao in padroes:
        m = re.search(padrao, texto)
        if m:
            hora = int(m.group(1))
            minuto = int(m.group(2)) if len(m.groups()) > 1 and m.group(2) else 0

            if 0 <= hora <= 23 and 0 <= minuto <= 59:
                return hora, minuto

    return None, None

def extrair_data(texto):
    hoje = datetime.now()

    if "hoje" in texto:
        return hoje.date()

    if "amanha" in texto or "amanhã" in texto:
        return (hoje + timedelta(days=1)).date()

    if "depois de amanha" in texto or "depois de amanhã" in texto:
        return (hoje + timedelta(days=2)).date()

    dias = {
        "segunda": 0,
        "terça": 1,
        "terca": 1,
        "quarta": 2,
        "quinta": 3,
        "sexta": 4,
        "sábado": 5,
        "sabado": 5,
        "domingo": 6,
    }

    for nome, indice in dias.items():
        if nome in texto:
            dias_ate = (indice - hoje.weekday()) % 7
            if dias_ate == 0:
                dias_ate = 7
            return (hoje + timedelta(days=dias_ate)).date()

    m = re.search(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{4}))?\b", texto)
    if m:
        dia = int(m.group(1))
        mes = int(m.group(2))
        ano = int(m.group(3)) if m.group(3) else hoje.year

        try:
            return datetime(ano, mes, dia).date()
        except ValueError:
            return None

    return hoje.date()


def limpar_titulo(texto):
    texto = texto.lower()

    gatilhos = [
        "marcar",
        "agendar",
        "agenda",
        "colocar na agenda",
        "criar compromisso",
        "compromisso",
        "me lembre de",
        "me lembrar de",
        "lembrete",
    ]

    for gatilho in gatilhos:
        texto = texto.replace(gatilho, "")

    texto = re.sub(r"\b(hoje|amanha|amanhã|depois de amanha|depois de amanhã)\b", "", texto)
    texto = re.sub(r"\b(segunda|terça|terca|quarta|quinta|sexta|sábado|sabado|domingo)\b", "", texto)
    texto = texto.replace("às", "as")
    texto = re.sub(r"\bas\b", "", texto)
    texto = re.sub(r"\b\d{1,2}:\d{2}\b", "", texto)
    texto = re.sub(r"\b\d{1,2}h\d{0,2}\b", "", texto)
    texto = re.sub(r"\b\d{1,2}\s+\d{2}\b", "", texto)
    texto = re.sub(r"\b\d{1,2}:\d{2}\b", "", texto)
    texto = re.sub(r"\b\d{1,2}h\d{0,2}\b", "", texto)
    texto = re.sub(r"\b\d{1,2}/\d{1,2}(?:/\d{4})?\b", "", texto)
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip().capitalize()


def criar_evento(titulo, data, hora, minuto=0, origem="huli"):
    eventos = carregar_agenda()

    evento = {
    "id": gerar_id(),
    "titulo": titulo,
    "data": data.strftime("%Y-%m-%d"),
    "hora": f"{hora:02d}:{minuto:02d}",
    "origem": origem,
    "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "notificado": False,
    "avisos": {
        "30": False,
        "10": False,
        "0": False,
    },
    "status": "pendente",
}

    evento = {
        "id": gerar_id(),
        "titulo": titulo,
        "data": data.strftime("%Y-%m-%d"),
        "hora": f"{hora:02d}:{minuto:02d}",
        "origem": origem,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "notificado": False,
        
    }

    eventos.append(evento)
    salvar_agenda(eventos)

    return evento


def criar_evento_por_texto(texto):
    texto_normalizado = normalizar_texto(texto)

    hora, minuto = extrair_horario(texto_normalizado)
    if hora is None:
        return False, "Não encontrei horário. Exemplo: agendar reunião amanhã às 14:30"

    data = extrair_data(texto_normalizado)
    if not data:
        return False, "Não consegui identificar a data."

    titulo = limpar_titulo(texto_normalizado)
    if not titulo:
        titulo = "Compromisso"

    evento = criar_evento(titulo, data, hora, minuto)

    data_br = datetime.strptime(evento["data"], "%Y-%m-%d").strftime("%d/%m/%Y")

    return True, (
        f"Compromisso registrado:\n"
        f"• {evento['titulo']}\n"
        f"• {data_br} às {evento['hora']}"
    )


def listar_eventos_data(data):
    eventos = carregar_agenda()
    alvo = data.strftime("%Y-%m-%d")

    return sorted(
        [e for e in eventos if e.get("data") == alvo],
        key=lambda e: e.get("hora", "00:00")
    )


def agenda_hoje():
    hoje = datetime.now().date()
    eventos = listar_eventos_data(hoje)

    if not eventos:
        return "Você não tem compromissos registrados na agenda interna da H.U.L.I para hoje."

    resposta = f"📅 Agenda de hoje — {hoje.strftime('%d/%m/%Y')}\n\n"

    for e in eventos:
        resposta += f"• {e['hora']} — {e['titulo']}\n"

    return resposta


def agenda_amanha():
    data = (datetime.now() + timedelta(days=1)).date()
    eventos = listar_eventos_data(data)

    if not eventos:
        return "Você não tem compromissos registrados para amanhã na agenda interna da H.U.L.I."

    resposta = f"📅 Agenda de amanhã — {data.strftime('%d/%m/%Y')}\n\n"

    for e in eventos:
        resposta += f"• {e['hora']} — {e['titulo']}\n"

    return resposta


def agenda_semana():
    hoje = datetime.now().date()
    eventos = carregar_agenda()

    fim = hoje + timedelta(days=7)

    filtrados = []
    for e in eventos:
        try:
            data_e = datetime.strptime(e["data"], "%Y-%m-%d").date()
            if hoje <= data_e <= fim:
                filtrados.append(e)
        except Exception:
            continue

    if not filtrados:
        return "Nenhum compromisso encontrado para os próximos 7 dias."

    filtrados = sorted(filtrados, key=lambda e: (e["data"], e["hora"]))

    resposta = "📅 Agenda dos próximos 7 dias:\n\n"

    for e in filtrados:
        data_br = datetime.strptime(e["data"], "%Y-%m-%d").strftime("%d/%m/%Y")
        resposta += f"• {data_br} {e['hora']} — {e['titulo']}\n"

    return resposta


def apagar_evento_por_titulo(titulo):
    eventos = carregar_agenda()
    titulo_busca = titulo.lower().strip()

    novos = []
    removidos = []

    for e in eventos:
        if titulo_busca in e.get("titulo", "").lower():
            removidos.append(e)
        else:
            novos.append(e)

    salvar_agenda(novos)

    if not removidos:
        return False, "Não encontrei compromisso com esse nome."

    return True, f"Removi {len(removidos)} compromisso(s) da agenda."


def verificar_eventos_para_notificar():
    eventos = carregar_agenda()
    agora = datetime.now()
    alterou = False
    notificacoes = []

    for e in eventos:
        try:
            quando = datetime.strptime(
                f"{e['data']} {e['hora']}",
                "%Y-%m-%d %H:%M"
            )
        except Exception:
            continue

        if "avisos" not in e:
            e["avisos"] = {
                "30": False,
                "10": False,
                "0": False,
            }
            alterou = True

        if "status" not in e:
            e["status"] = "pendente"
            alterou = True

        diferenca_minutos = int((quando - agora).total_seconds() / 60)

        if 29 <= diferenca_minutos <= 30 and not e["avisos"].get("30"):
            notificacoes.append({
                "tipo": "antes_30",
                "evento": e,
                "mensagem": f"Rony, em 30 minutos você tem: {e.get('titulo')} às {e.get('hora')}."
            })
            e["avisos"]["30"] = True
            alterou = True

        if 9 <= diferenca_minutos <= 10 and not e["avisos"].get("10"):
            notificacoes.append({
                "tipo": "antes_10",
                "evento": e,
                "mensagem": f"Rony, faltam 10 minutos para: {e.get('titulo')} às {e.get('hora')}."
            })
            e["avisos"]["10"] = True
            alterou = True

        if diferenca_minutos <= 0 and not e["avisos"].get("0"):
            notificacoes.append({
                "tipo": "agora",
                "evento": e,
                "mensagem": f"Rony, compromisso agora: {e.get('titulo')} às {e.get('hora')}."
            })
            e["avisos"]["0"] = True
            e["notificado"] = True
            alterou = True

    if alterou:
        salvar_agenda(eventos)

    return notificacoes

def concluir_evento_por_titulo(titulo):
    eventos = carregar_agenda()
    titulo_busca = titulo.lower().strip()
    alterou = False

    for e in eventos:
        if titulo_busca in e.get("titulo", "").lower():
            e["status"] = "concluido"
            alterou = True

    if alterou:
        salvar_agenda(eventos)
        return True, "Compromisso marcado como concluído."

    return False, "Não encontrei esse compromisso."


def remarcar_evento_por_texto(texto):
    eventos = carregar_agenda()
    texto_n = normalizar_texto(texto)

    hora, minuto = extrair_horario(texto_n)
    data = extrair_data(texto_n)

    if hora is None:
        return False, "Não encontrei o novo horário."

    titulo = texto_n

    gatilhos = [
        "remarcar",
        "remarque",
        "alterar",
        "alterar compromisso",
        "mudar",
        "mudar compromisso",
    ]

    for g in gatilhos:
        titulo = titulo.replace(g, "")

    titulo = re.sub(r"\b(hoje|amanha|amanhã|depois de amanha|depois de amanhã)\b", "", titulo)
    titulo = re.sub(r"\b\d{1,2}:\d{2}\b", "", titulo)
    titulo = re.sub(r"\b\d{1,2}h\d{0,2}\b", "", titulo)
    titulo = re.sub(r"\b\d{1,2}\s+\d{2}\b", "", titulo)
    titulo = titulo.replace("às", "as")
    titulo = re.sub(r"\bas\b", "", titulo)
    titulo = re.sub(r"\s+", " ", titulo).strip()

    if not titulo:
        return False, "Não entendi qual compromisso você quer remarcar."

    for e in eventos:
        if titulo in e.get("titulo", "").lower():
            e["data"] = data.strftime("%Y-%m-%d")
            e["hora"] = f"{hora:02d}:{minuto:02d}"
            e["notificado"] = False
            e["avisos"] = {"30": False, "10": False, "0": False}
            e["status"] = "pendente"
            salvar_agenda(eventos)

            data_br = data.strftime("%d/%m/%Y")
            return True, f"Compromisso remarcado para {data_br} às {hora:02d}:{minuto:02d}."

    return False, "Não encontrei esse compromisso para remarcar."


def listar_eventos_pendentes():
    eventos = carregar_agenda()
    pendentes = [e for e in eventos if e.get("status", "pendente") == "pendente"]

    if not pendentes:
        return "Nenhum compromisso pendente encontrado."

    pendentes = sorted(pendentes, key=lambda e: (e.get("data", ""), e.get("hora", "")))

    resposta = "📌 Compromissos pendentes:\n\n"
    for e in pendentes:
        data_br = datetime.strptime(e["data"], "%Y-%m-%d").strftime("%d/%m/%Y")
        resposta += f"• {data_br} {e['hora']} — {e['titulo']}\n"

    return resposta