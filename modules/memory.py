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

        # Compatibilidade: registros antigos podem não ter "categoria"
        for item in self.memorias:
            if isinstance(item, dict) and "categoria" not in item:
                item["categoria"] = "geral"

    def salvar(self, conteudo, categoria="geral"):
        # Evita duplicado baseado no conteúdo + categoria
        for item in self.memorias:
            if item.get("conteudo") == conteudo and item.get("categoria", "geral") == categoria:
                return

        agora = datetime.now()

        nova_memoria = {
            "categoria": categoria,
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

    def listar_por_categoria(self, categoria):
        filtradas = [m for m in self.memorias if m.get("categoria", "geral") == categoria]
        if not filtradas:
            return f"Não tenho registros na categoria '{categoria}'."
        return filtradas

    def _salvar_arquivo(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.memorias, f, ensure_ascii=False, indent=4)