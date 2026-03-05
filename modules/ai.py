import os
import subprocess
import requests


def tem_internet() -> bool:
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except Exception:
        return False


def responder_openai(pergunta: str, historico: list[dict] | None = None) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        mensagens = [{"role": "system", "content": "Você é H.U.L.I (Humano Único Leal Inteligente), assistente pessoal do Rony. Responda em PT-BR."}]
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
            # salva erro para diagnóstico (ex.: 429 quota)
            try:
                with open("debug_openai.log", "a", encoding="utf-8") as f:
                    f.write("\n--- OPENAI FAIL ---\n")
                    f.write(f"STATUS: {r.status_code}\n")
                    f.write(r.text[:2000] + "\n")
            except Exception:
                pass
            return None

        j = r.json()
        return j["choices"][0]["message"]["content"].strip()

    except Exception:
        return None


def responder_ollama(pergunta: str, historico: list[dict] | None = None) -> str | None:
    """
    OFFLINE (Ollama) com:
    - PT-BR
    - estilo Jarvis/HULI
    - contexto da conversa (histórico)
    - menos alucinação
    """
    try:
        sistema = (
            "Você é H.U.L.I (Humano Único Leal Inteligente), assistente pessoal do Rony.\n"
            "Regras:\n"
            "1) Responda SEMPRE em português do Brasil.\n"
            "2) Seja educada, leal, com leve humor e estilo 'Jarvis'.\n"
            "3) Seja direta e útil.\n"
            "4) Se não tiver certeza, diga que não tem certeza e sugira como verificar.\n"
            "5) Não invente fatos.\n"
            "6) Se a pergunta for ambígua, peça 1 detalhe.\n"
            "7) Se o usuário pedir 'simples', responda em 1 ou 2 frases.\n"
        )

        contexto_txt = ""
        if historico:
            # transforma o histórico em texto pro modelo manter contexto
            linhas = []
            for m in historico[-10:]:  # mantém só as últimas 10 mensagens pra não ficar enorme
                role = "Rony" if m.get("role") == "user" else "H.U.L.I"
                linhas.append(f"{role}: {m.get('content','')}")
            contexto_txt = "\n".join(linhas)

        prompt = (
            f"{sistema}\n"
            f"Contexto recente da conversa (se houver):\n{contexto_txt}\n\n"
            f"Pergunta do Rony: {pergunta}\n"
            f"Resposta da H.U.L.I:"
        )

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
        return saida.strip()

    except Exception:
        return None


def responder_ia(pergunta: str, historico: list[dict] | None = None) -> str:
    # ONLINE primeiro
    if tem_internet():
        r = responder_openai(pergunta, historico=historico)
        if r:
            return "🌐 ONLINE | " + r

    # OFFLINE por último
    r = responder_ollama(pergunta, historico=historico)
    if r:
        return "🖥️ OFFLINE | " + r

    return "⚠️ Ainda estou sem acesso ao modo ONLINE e OFFLINE agora. Tenta reformular 🙂"  