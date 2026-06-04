from datetime import datetime

from modules.settings_manager import listar_config
from modules.protection import status_protecao
from core_system.kernel import obter_kernel


class HULIContext:
    def __init__(self):
        self.ultima_intencao = None
        self.ultimo_comando = None
        self.ultima_resposta = None
        self.iniciado_em = datetime.now()

    def registrar_interacao(self, comando, resposta=None, intencao=None):
        self.ultimo_comando = comando
        self.ultima_resposta = resposta
        self.ultima_intencao = intencao

    def resumo(self):
        configs = listar_config()
        kernel = obter_kernel()
        status_kernel = kernel.status()

        proprietario = bool(status_kernel.get("proprietario"))

        return {
            "usuario_atual": status_kernel.get("usuario"),
            "proprietario": proprietario,
            "visitante": not proprietario,
            "empresa": configs.get("empresa"),
            "assistente": configs.get("assistente_nome"),
            "voz_ativa": status_kernel.get("voz"),
            "modo_jarvis": status_kernel.get("jarvis"),
            "modo_conversa": status_kernel.get("modo_conversa"),
            "escuta_continua": status_kernel.get("escuta_continua"),
            "modo_protecao": status_protecao(),
            "personalidade": configs.get("personalidade"),
            "bluetooth_padrao": configs.get("bluetooth_dispositivo_padrao"),
            "ultimo_comando": self.ultimo_comando or status_kernel.get("ultimo_comando"),
            "ultima_resposta": self.ultima_resposta,
            "ultima_intencao": self.ultima_intencao,
            "iniciado_em": self.iniciado_em.strftime("%d/%m/%Y %H:%M:%S"),
            "uptime_kernel": status_kernel.get("uptime"),
            "threads": status_kernel.get("threads"),
        }


contexto_huli = HULIContext()


def obter_contexto():
    return contexto_huli


def resumo_contexto():
    return contexto_huli.resumo()