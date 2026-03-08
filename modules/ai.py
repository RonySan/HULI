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

    if tem_docs:
        return "docs"

    palavras_online = [
        "hoje",
        "agora",
        "atual",
        "última",
        "ultimo",
        "último",
        "notícia",
        "noticia",
        "preço",
        "preco",
        "cotação",
        "cotacao",
        "clima",
        "tempo",
        "presidente",
    ]

    if any(k in p for k in palavras_online):
        return "online"

    if len(p.split()) > 18:
        return "online"

    return "offline"


# -------------------------
# OPENAI (ONLINE)
# -------------------------
def responder_openai(pergunta: str, historico=None, modo="normal"):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    try:

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        mensagens = [
            {
                "role": "system",
                "content": (
                    "Você é H.U.L.I (Humano Único Leal Inteligente), assistente pessoal do Rony.\n"
                    "Responda sempre em português do Brasil.\n"
                    "Seja clara, educada e direta."
                ),
            }
        ]

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
def responder_ollama(pergunta: str, historico=None, modo="normal"):

    try:

        prompt = f"""
Você é H.U.L.I, assistente pessoal do Rony.

Responda sempre em português do Brasil.
Seja clara e útil.

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

    contexto_docs = buscar_contexto_docs(pergunta)

    tem_docs = bool(contexto_docs.strip())

    pergunta_final = pergunta

    if tem_docs:

        pergunta_final = f"""
Use as informações abaixo se forem relevantes.

{contexto_docs}

Pergunta:
{pergunta}
"""

    motor = decidir_motor(pergunta, tem_docs)

    # -------------------------
    # DOCS
    # -------------------------
    if motor == "docs":

        r = responder_ollama(pergunta_final, historico, modo)

        if r:
            return "📚 DOCS + 🖥️ OFFLINE | " + r

        r = responder_openai(pergunta_final, historico, modo)

        if r:
            return "📚 DOCS + 🌐 ONLINE | " + r

    # -------------------------
    # ONLINE
    # -------------------------
    if motor == "online":

        if tem_internet():

            r = responder_openai(pergunta_final, historico, modo)

            if r:
                return "🌐 ONLINE | " + r

        r = responder_ollama(pergunta_final, historico, modo)

        if r:
            return "🖥️ OFFLINE | " + r

    # -------------------------
    # OFFLINE
    # -------------------------
    r = responder_ollama(pergunta_final, historico, modo)

    if r:
        return "🖥️ OFFLINE | " + r

    if tem_internet():

        r = responder_openai(pergunta_final, historico, modo)

        if r:
            return "🌐 ONLINE | " + r

    return "⚠️ Ainda estou sem acesso aos motores de IA."