from modules.settings_manager import listar_config
from modules.system_monitor import status_sistema
from modules.reminder_engine import listar_lembretes
from modules.logger import ler_logs


def limpar_linha_log(linha: str, limite: int = 140):
    linha = linha.strip()

    if not linha:
        return ""

    linha = linha.replace("\n", " ")

    if len(linha) > limite:
        linha = linha[:limite] + "..."

    return linha


def status_geral():
    configs = listar_config()

    resposta = "🧠 STATUS GERAL DA H.U.L.I\n\n"

    resposta += "⚙️ Configurações:\n"
    resposta += f"- Usuário: {configs.get('usuario')}\n"
    resposta += f"- Empresa: {configs.get('empresa')}\n"
    resposta += f"- Voz ativa: {configs.get('voz_ativa')}\n"
    resposta += f"- Personalidade: {configs.get('personalidade')}\n"
    resposta += f"- Bluetooth padrão: {configs.get('bluetooth_dispositivo_padrao')}\n\n"

    resposta += "🖥️ Sistema:\n"
    resposta += status_sistema()
    resposta += "\n\n"

    resposta += "🔔 Lembretes:\n"
    resposta += listar_lembretes()
    resposta += "\n\n"

    resposta += "📜 Logs recentes:\n"

    logs = ler_logs(20)

    if not logs:
        resposta += "Nenhum log recente."
        return resposta

    limpos = []

    for linha in logs:
        if "[COMANDO]" in linha or "[ERRO]" in linha or "[SISTEMA]" in linha:
            linha_limpa = limpar_linha_log(linha)
            if linha_limpa:
                limpos.append(linha_limpa)

    if not limpos:
        resposta += "Nenhum comando recente."
    else:
        for linha in limpos[-10:]:
            resposta += f"- {linha}\n"

    return resposta