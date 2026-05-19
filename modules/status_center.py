from modules.settings_manager import listar_config
from modules.system_monitor import status_sistema
from modules.reminder_engine import listar_lembretes
from modules.logger import ler_logs


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
    logs = ler_logs(10)

    if logs:
        for linha in logs:
            resposta += linha
    else:
        resposta += "Nenhum log recente."

    return resposta