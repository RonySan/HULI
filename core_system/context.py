from datetime import datetime

from modules.settings_manager import listar_config, obter
from modules.voice_mode import voz_esta_ativa
from modules.jarvis_mode import modo_jarvis_ativo
from modules.protection import status_protecao


class HULIContext:
    def __init__(self):
        self.usuario_atual = None
        self.proprietario = False
        self.visitante = True
        self.ultima_intencao = None
        self.ultimo_comando = None
        self.ultima_resposta = None
        self.iniciado_em = datetime.now()

    def definir_usuario(self, usuario, proprietario=False):
        self.usuario_atual = usuario
        self.proprietario = proprietario
        self.visitante = not proprietario

    def registrar_interacao(self, comando, resposta=None, intencao=None):
        self.ultimo_comando = comando
        self.ultima_resposta = resposta
        self.ultima_intencao = intencao

    def resumo(self):
        configs = listar_config()

        return {
            "usuario_atual": self.usuario_atual,
            "proprietario": self.proprietario,
            "visitante": self.visitante,
            "empresa": configs.get("empresa"),
            "assistente": configs.get("assistente_nome"),
            "voz_ativa": voz_esta_ativa(),
            "modo_jarvis": modo_jarvis_ativo(),
            "modo_protecao": status_protecao(),
            "personalidade": configs.get("personalidade"),
            "bluetooth_padrao": configs.get("bluetooth_dispositivo_padrao"),
            "ultimo_comando": self.ultimo_comando,
            "ultima_intencao": self.ultima_intencao,
            "iniciado_em": self.iniciado_em.strftime("%d/%m/%Y %H:%M:%S"),
        }


contexto_huli = HULIContext()


def obter_contexto():
    return contexto_huli


def resumo_contexto():
    return contexto_huli.resumo()