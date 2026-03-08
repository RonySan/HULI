import os
import subprocess
import requests

from modules.docs import buscar_docs


# -------------------------
# INTERNET
# -------------------------
def tem_internet() -> bool:
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except Exception:
        return False


# -------------------------
# BUSCAR CONTEXTO EM DOCS
# -------------------------
def buscar_contexto_docs(pergunta: str) -> str:
    trechos = buscar_docs(pergunta, limite=6)

    if not trechos:
        return ""

    contexto = "TRECHOS ENCONTRADOS NOS DOCUMENTOS:\n"
    for t in trechos:
        contexto += f"- {t}\n"

    return contexto


# -------------------------
# DECISÃO DE MOTOR
# -------------------------
def decidir_motor(pergunta: str, tem_docs: bool = False) -> str:
    p = (pergunta or "").lower()

    palavras_docs = [
        "contrato", "cliente", "multa", "cancelamento", "prazo", "pagamento",
        "serviço", "servicos", "valor", "orçamento", "orcamento",
        "proposta", "cláusula", "clausula", "assinado", "vigência", "vigencia"
    ]

    palavras_online = [
        "hoje", "agora", "atual", "atualmente", "última", "ultimo", "último",
        "notícia", "noticia", "preço", "preco", "cotação", "cotacao",
        "clima", "tempo", "presidente", "governo", "dólar", "dolar"
    ]

    if any(k in p for k in palavras_docs) and tem_docs:
        return "docs"

    if any(k in p for k in palavras_online):
        return "online"

    if len(p.split()) > 18:
        return "online"

    return "offline"


# -------------------------
# OPENAI (ONLINE)
# -------------------------
def responder_openai(pergunta: str, historico=None, modo="normal", usar_docs=False):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    try:
        if usar_docs:
            system_prompt = (
                "Você é H.U.L.I (Humano Único Leal Inteligente), assistente pessoal do Rony.\n"
                "Responda sempre em português do Brasil.\n"
                "Use apenas os trechos fornecidos como fonte.\n"
                "Se a resposta estiver nos trechos, responda direto.\n"
                "Não peça desculpas.\n"
                "Não faça perguntas de volta.\n"
                "Formato obrigatório:\n"
                "Resposta: <resposta curta>\n"
                "Fonte: <arquivo> — <trecho>"
            )
        else:
            system_prompt = (
                "Você é H.U.L.I (Humano Único Leal Inteligente), assistente pessoal do Rony.\n"
                "Responda sempre em português do Brasil.\n"
                "Seja clara, útil, objetiva e natural.\n"
                "Não mencione documentos, fontes ou trechos se o usuário não pediu isso.\n"
                "Não diga que faltam trechos ou fontes quando a pergunta for geral."
            )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        mensagens = [{"role": "system", "content": system_prompt}]

        if historico:
            mensagens.extend(historico)

        mensagens.append({"role": "user", "content": pergunta})

        data = {
            "model": "gpt-5.3-chat-latest",
            "messages": mensagens,
        }

        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20,
        )

        if r.status_code != 200:
            return None

        j = r.json()
        return j["choices"][0]["message"]["content"].strip()

    except Exception:
        return None


# -------------------------
# OLLAMA (OFFLINE)
# -------------------------
def responder_ollama(pergunta: str, historico=None, modo="normal", usar_docs=False):
    try:
        if usar_docs:
            prompt = f"""
Você é H.U.L.I, assistente pessoal do Rony.

Regras:
- Responda sempre em português do Brasil.
- Use APENAS os trechos fornecidos.
- Se a resposta estiver nos trechos, responda direto.
- NÃO peça desculpas.
- NÃO faça perguntas de volta.
- Sempre use este formato:

Resposta: <resposta curta>
Fonte: <arquivo> — <trecho>

Pergunta:
{pergunta}

Resposta:
"""
        else:
            prompt = f"""
Você é H.U.L.I, assistente pessoal do Rony.

Regras:
- Responda sempre em português do Brasil.
- Seja clara, útil, objetiva e natural.
- Não invente fatos.
- Não mencione documentos, fontes ou trechos.
- Não diga que faltam fontes ou contexto se a pergunta for geral.

Pergunta:
{pergunta}

Resposta:
"""

        comando = ["ollama", "run", "llama3.1:8b", prompt]

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        saida = (resultado.stdout or "").strip()

        if not saida:
            return None

        return saida

    except Exception:
        return None


# -------------------------
# MOTOR CENTRAL HULI
# -------------------------
def responder_ia(pergunta: str, historico=None, modo="normal"):
    pergunta_lower = (pergunta or "").lower()

    palavras_docs = [
        "contrato", "cliente", "multa", "cancelamento", "prazo", "pagamento",
        "serviço", "servicos", "valor", "orçamento", "orcamento",
        "proposta", "cláusula", "clausula", "assinado", "vigência", "vigencia"
    ]

    usar_docs = any(p in pergunta_lower for p in palavras_docs)

    contexto_docs = buscar_contexto_docs(pergunta) if usar_docs else ""
    tem_docs = bool(contexto_docs.strip())

    motor = decidir_motor(pergunta, tem_docs=tem_docs)

    if tem_docs:
        pergunta_final = (
            f"{contexto_docs}\n\n"
            f"PERGUNTA: {pergunta}"
        )
    else:
        pergunta_final = pergunta

    # DOCS
    if motor == "docs":
        r = responder_ollama(pergunta_final, historico, modo, usar_docs=True)
        if r:
            return "📚 DOCS + 🖥️ OFFLINE | " + r

        r = responder_openai(pergunta_final, historico, modo, usar_docs=True)
        if r:
            return "📚 DOCS + 🌐 ONLINE | " + r

    # ONLINE
    if motor == "online":
        if tem_internet():
            r = responder_openai(pergunta_final, historico, modo, usar_docs=False)
            if r:
                return "🌐 ONLINE | " + r

        r = responder_ollama(pergunta_final, historico, modo, usar_docs=False)
        if r:
            return "🖥️ OFFLINE | " + r

    # OFFLINE
    r = responder_ollama(pergunta_final, historico, modo, usar_docs=False)
    if r:
        return "🖥️ OFFLINE | " + r

    if tem_internet():
        r = responder_openai(pergunta_final, historico, modo, usar_docs=False)
        if r:
            return "🌐 ONLINE | " + r

    return "⚠️ Ainda estou sem acesso aos motores de IA."