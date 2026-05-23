from datetime import datetime


class HULIKernel:

    def __init__(self):

        self.iniciado_em = datetime.now()

        self.encerrar_programa = False

        self.modo_conversa = False

        self.escuta_continua = False

        self.jarvis_ativo = False

        self.voz_ativa = False

        self.usuario_atual = None

        self.proprietario = False

        self.ultimo_comando = None

        self.ultima_resposta = None

        self.threads_ativas = []

    # =====================================================
    # ESTADO
    # =====================================================

    def desligar(self):
        self.encerrar_programa = True

    def esta_ativo(self):
        return not self.encerrar_programa

    # =====================================================
    # MODOS
    # =====================================================

    def ativar_conversa(self):
        self.modo_conversa = True

    def desativar_conversa(self):
        self.modo_conversa = False

    def ativar_escuta(self):
        self.escuta_continua = True

    def desativar_escuta(self):
        self.escuta_continua = False

    # =====================================================
    # INTERAÇÃO
    # =====================================================

    def registrar_interacao(self, comando, resposta=None):

        self.ultimo_comando = comando

        self.ultima_resposta = resposta

    # =====================================================
    # USUÁRIO
    # =====================================================

    def definir_usuario(self, nome, proprietario=False):

        self.usuario_atual = nome

        self.proprietario = proprietario

    # =====================================================
    # THREADS
    # =====================================================

    def registrar_thread(self, nome):

        if nome not in self.threads_ativas:
            self.threads_ativas.append(nome)

    def remover_thread(self, nome):

        if nome in self.threads_ativas:
            self.threads_ativas.remove(nome)

    # =====================================================
    # STATUS
    # =====================================================

    def status(self):

        return {

            "usuario": self.usuario_atual,

            "proprietario": self.proprietario,

            "modo_conversa": self.modo_conversa,

            "escuta_continua": self.escuta_continua,

            "jarvis": self.jarvis_ativo,

            "voz": self.voz_ativa,

            "ultimo_comando": self.ultimo_comando,

            "threads": self.threads_ativas,

            "uptime": str(datetime.now() - self.iniciado_em)
        }


kernel_huli = HULIKernel()


def obter_kernel():
    return kernel_huli