from datetime import datetime
import uuid


class Task:
    def __init__(self, nome, descricao="", intencao="", prioridade="normal", dados=None):
        self.id = str(uuid.uuid4())[:8]
        self.nome = nome
        self.descricao = descricao
        self.intencao = intencao
        self.prioridade = prioridade
        self.dados = dados or {}
        self.status = "pendente"
        self.resultado = None
        self.criada_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.iniciada_em = None
        self.finalizada_em = None

    def iniciar(self):
        self.status = "executando"
        self.iniciada_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def concluir(self, resultado=None):
        self.status = "concluida"
        self.resultado = resultado
        self.finalizada_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def falhar(self, erro):
        self.status = "erro"
        self.resultado = str(erro)
        self.finalizada_em = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self):
        return self.__dict__