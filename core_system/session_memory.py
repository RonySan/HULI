from datetime import datetime


class SessionMemory:
    def __init__(self):
        self.interacoes = []
        self.ultimo_diagnostico = None
        self.ultimo_relatorio_texto = None
        self.ultimo_topico = None
        self.ultima_resposta = None
        self.ultima_pergunta = None

    def registrar_interacao(self, pergunta, resposta=None, topico=None):
        item = {
            "pergunta": pergunta,
            "resposta": resposta,
            "topico": topico,
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        self.interacoes.append(item)

        if len(self.interacoes) > 30:
            self.interacoes = self.interacoes[-30:]

        self.ultima_pergunta = pergunta
        self.ultima_resposta = resposta

        if topico:
            self.ultimo_topico = topico

    def registrar_diagnostico(self, relatorio, texto):
        self.ultimo_diagnostico = relatorio
        self.ultimo_relatorio_texto = texto
        self.ultimo_topico = "diagnostico"

    def obter_ultimo_diagnostico(self):
        return self.ultimo_diagnostico

    def obter_ultimo_relatorio_texto(self):
        return self.ultimo_relatorio_texto

    def resumo(self):
        return {
            "total_interacoes": len(self.interacoes),
            "ultimo_topico": self.ultimo_topico,
            "ultima_pergunta": self.ultima_pergunta,
            "ultima_resposta": self.ultima_resposta,
            "tem_diagnostico": self.ultimo_diagnostico is not None,
        }

    def ultimas_interacoes(self, limite=5):
        return self.interacoes[-limite:]


session_memory = SessionMemory()


def obter_memoria_sessao():
    return session_memory