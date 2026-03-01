import json
import os
from datetime import datetime


class HULIMemory:

    def __init__(self):
        self.arquivo = "memoria.json"
        self.memorias = []
        self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                try:
                    self.memorias = json.load(f)
                except json.JSONDecodeError:
                    self.memorias = []
        else:
            self.memorias = []

    def salvar(self, conteudo):
        for item in self.memorias:
            if item["conteudo"] == conteudo:
                return

        agora = datetime.now()
        nova_memoria = {
            "conteudo": conteudo,
            "data": agora.strftime("%d/%m/%Y"),
            "hora": agora.strftime("%H:%M:%S")
        }

        self.memorias.append(nova_memoria)
        self._salvar_arquivo()

    def listar(self):
        if not self.memorias:
            return "Ainda não tenho memórias registradas."
        return self.memorias

    def _salvar_arquivo(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.memorias, f, ensure_ascii=False, indent=4)
