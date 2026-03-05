import json
import os
from datetime import datetime
from uuid import uuid4


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

        # Compatibilidade com registros antigos
        for item in self.memorias:
            if isinstance(item, dict) and "categoria" not in item:
                item["categoria"] = "geral"

            if isinstance(item, dict) and item.get("categoria") == "lembretes":
                item.setdefault("id", str(uuid4()))
                item.setdefault("executado", False)

    def _salvar_arquivo(self):
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(self.memorias, f, ensure_ascii=False, indent=4)

    def salvar(self, conteudo, categoria="geral"):
        for item in self.memorias:
            if item.get("conteudo") == conteudo and item.get("categoria", "geral") == categoria:
                return

        agora = datetime.now()
        nova_memoria = {
            "categoria": categoria,
            "conteudo": conteudo,
            "data": agora.strftime("%d/%m/%Y"),
            "hora": agora.strftime("%H:%M:%S"),
        }

        self.memorias.append(nova_memoria)
        self._salvar_arquivo()

    def salvar_lembrete(self, conteudo, quando_dt: datetime):
        quando_str = quando_dt.strftime("%Y-%m-%d %H:%M:%S")

        # evita duplicado (mesmo conteúdo e mesmo horário)
        for item in self.memorias:
            if (
                item.get("categoria") == "lembretes"
                and item.get("conteudo") == conteudo
                and item.get("quando") == quando_str
            ):
                return False

        novo = {
            "id": str(uuid4()),
            "categoria": "lembretes",
            "conteudo": conteudo,
            "quando": quando_str,
            "executado": False,
            "data": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M:%S"),
        }
        self.memorias.append(novo)
        self._salvar_arquivo()
        return True

    def listar(self):
        if not self.memorias:
            return "Ainda não tenho memórias registradas."
        return self.memorias

    def listar_por_categoria(self, categoria):
        filtradas = [m for m in self.memorias if m.get("categoria", "geral") == categoria]
        if not filtradas:
            return f"Não tenho registros na categoria '{categoria}'."
        return filtradas

    def listar_lembretes_pendentes(self):
        pendentes = []
        for m in self.memorias:
            if m.get("categoria") == "lembretes" and m.get("executado") is False and m.get("quando"):
                pendentes.append(m)
        return pendentes

    def marcar_lembrete_executado(self, lembrete_id: str):
        for m in self.memorias:
            if m.get("categoria") == "lembretes" and m.get("id") == lembrete_id:
                m["executado"] = True
                self._salvar_arquivo()
                return True
        return False

    def limpar_lembretes_executados(self):
        self.memorias = [
            m for m in self.memorias
            if not (m.get("categoria") == "lembretes" and m.get("executado") is True)
        ]
        self._salvar_arquivo()

    def apagar_lembretes(self):
        self.memorias = [m for m in self.memorias if m.get("categoria") != "lembretes"]
        self._salvar_arquivo()