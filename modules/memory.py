import json
import os
from datetime import datetime

ARQUIVO = os.path.join(os.path.dirname(__file__), "memory.json")


class HULIMemory:
    def __init__(self):
        self.dados = self.carregar()

    def carregar(self):
        if not os.path.exists(ARQUIVO):
            return []

        try:
            with open(ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def salvar_arquivo(self):
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)

    def salvar(self, conteudo, categoria="geral"):
        item = {
            "id": len(self.dados) + 1,
            "conteudo": conteudo,
            "categoria": categoria,
            "data": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M:%S"),
        }

        self.dados.append(item)
        self.salvar_arquivo()

    def listar(self):
        return self.dados if self.dados else "Nada salvo."

    def listar_por_categoria(self, categoria):
        filtrado = [x for x in self.dados if x.get("categoria") == categoria]
        return filtrado if filtrado else []

    # -------------------------
    # LEMBRETES
    # -------------------------
    def salvar_lembrete(self, conteudo, quando):
        item = {
            "id": len(self.dados) + 1,
            "conteudo": conteudo,
            "categoria": "lembretes",
            "quando": quando.strftime("%Y-%m-%d %H:%M:%S"),
            "executado": False,
        }

        self.dados.append(item)
        self.salvar_arquivo()
        return True

    def listar_lembretes_pendentes(self):
        return [x for x in self.dados if x.get("categoria") == "lembretes"]

    def marcar_lembrete_executado(self, id_lembrete):
        for item in self.dados:
            if item.get("id") == id_lembrete:
                item["executado"] = True
        self.salvar_arquivo()

    def apagar_lembretes(self):
        self.dados = [x for x in self.dados if x.get("categoria") != "lembretes"]
        self.salvar_arquivo()

    def limpar_lembretes_executados(self):
        self.dados = [
            x for x in self.dados
            if not (x.get("categoria") == "lembretes" and x.get("executado"))
        ]
        self.salvar_arquivo()