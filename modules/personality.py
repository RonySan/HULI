import random


class HULIPersonality:

    def __init__(self):
        self.modos = {
            "normal": [
                "Entendido.",
                "Certo.",
                "Perfeito.",
                "Já estou verificando."
            ],
            "humor": [
                "Deixa comigo, chefe 😎",
                "Já resolvo isso antes do café acabar.",
                "Missão aceita."
            ]
        }

    def gerar_resposta_base(self):
        escolha = random.choice(["normal", "humor"])
        return random.choice(self.modos[escolha])
import random


class HULIPersonality:

    def __init__(self):
        self.modos = {
            "normal": [
                "Entendido.",
                "Certo.",
                "Perfeito.",
                "Já estou verificando."
            ],
            "humor": [
                "Deixa comigo, chefe 😎",
                "Já resolvo isso antes do café acabar.",
                "Missão aceita."
            ]
        }

    def gerar_resposta_base(self):
        escolha = random.choice(["normal", "humor"])
        return random.choice(self.modos[escolha])
