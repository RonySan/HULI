import os
import subprocess
import requests


def tem_internet() -> bool:
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except Exception:
        return False



def responder_openai(pergunta: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "gpt-5.3-chat-latest",
            "messages": [
                {"role": "system", "content": "Você é H.U.L.I, assistente pessoal de Rony."},
                {"role": "user", "content": pergunta},
            ],
        }

        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20,
        )

        if r.status_code != 200:
            with open("debug_openai.log", "a", encoding="utf-8") as f:
                f.write("\n--- OPENAI ERROR ---\n")
                f.write(f"STATUS: {r.status_code}\n")
                f.write(r.text[:2000] + "\n")
            return None

        j = r.json()
        return j["choices"][0]["message"]["content"].strip()

    except Exception as e:
        with open("debug_openai.log", "a", encoding="utf-8") as f:
            f.write("\n--- OPENAI EXCEPTION ---\n")
            f.write(repr(e) + "\n")
        return None


def responder_ollama(pergunta: str) -> str | None:
    """
    OFFLINE (Ollama) com prompt fixo da H.U.L.I:
    - sempre PT-BR
    - estilo Jarvis/HULI
    - respostas mais confiáveis (se não souber, diz que não sabe)
    - evita inventar
    """
    try:
        # Prompt "sistema" da HULI
        sistema = (
            "Você é H.U.L.I (Humano Único Leal Inteligente), assistente pessoal do Rony.\n"
            "Regras:\n"
            "1) Responda SEMPRE em português do Brasil.\n"
            "2) Seja educada, leal, com leve humor e estilo 'Jarvis'.\n"
            "3) Seja direta e útil.\n"
            "4) Se você não tiver certeza, diga que não tem certeza e sugira como verificar.\n"
            "5) Não invente fatos. Não crie nomes/datas/estatísticas sem base.\n"
            "6) Se a pergunta for ambígua, peça um detalhe antes de responder.\n"
            "7) Se o usuário pedir 'simples', responda em 1 ou 2 frases.\n"
        )

        prompt = f"{sistema}\nPergunta do Rony: {pergunta}\nResposta da H.U.L.I:"

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

        # Limpeza leve: remove possíveis repetições do próprio prompt
        return saida.strip()

    except Exception:
        return None


def responder_ia(pergunta: str) -> str:
    # 1️⃣ tenta ONLINE primeiro
    if tem_internet():
        r = responder_openai(pergunta)
        if r:
            return "🌐 ONLINE | " + r

    # 2️⃣ se falhar vai para OFFLINE
    r = responder_ollama(pergunta)
    if r:
        return "🖥️ OFFLINE | " + r

    # 3️⃣ nunca fica sem responder
    return "⚠️ Ainda estou sem acesso ao modo ONLINE e OFFLINE agora. Tenta reformular 🙂"