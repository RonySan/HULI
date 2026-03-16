import json
import os
import subprocess
import webbrowser

ARQUIVO_ROTINAS = os.path.join(os.path.dirname(__file__), "rotinas.json")

def apagar_rotina(nome):
    rotinas = carregar_rotinas()

    nome = nome.lower()

    if nome not in rotinas:
        return False, f"Não encontrei a rotina '{nome}'."

    del rotinas[nome]

    salvar_rotinas(rotinas)

    return True, f"Rotina '{nome}' removida."

def carregar_rotinas():
    if not os.path.exists(ARQUIVO_ROTINAS):
        return {}

    try:
        with open(ARQUIVO_ROTINAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def salvar_rotinas(rotinas):
    with open(ARQUIVO_ROTINAS, "w", encoding="utf-8") as f:
        json.dump(rotinas, f, indent=4, ensure_ascii=False)


def listar_rotinas():
    rotinas = carregar_rotinas()
    return list(rotinas.keys())


def criar_rotina(nome, itens):
    rotinas = carregar_rotinas()
    tarefas = []

    for item in itens:
        item = item.strip().lower()

        if item in ["github", "gmail", "youtube", "chatgpt", "google"]:
            tarefas.append({"tipo": "site", "valor": item})
        elif item.startswith("http"):
            tarefas.append({"tipo": "site", "valor": item})
        elif ":\\" in item or item.startswith("\\"):
            if any(item.endswith(ext) for ext in [".pdf", ".docx", ".xlsx", ".txt", ".pptx"]):
                tarefas.append({"tipo": "arquivo", "valor": item})
            else:
                tarefas.append({"tipo": "pasta", "valor": item})
        else:
            tarefas.append({"tipo": "programa", "valor": item})

    rotinas[nome.lower().strip()] = tarefas
    salvar_rotinas(rotinas)

    return f"Rotina '{nome}' criada com sucesso."


def executar_rotina(
    nome_rotina,
    abrir_programa_func,
    abrir_site_func,
    abrir_pasta_func,
    executar_comando_func,
    abrir_arquivo_func
):
    rotinas = carregar_rotinas()
    nome = nome_rotina.lower().strip()

    if nome not in rotinas:
        return False, f"Não encontrei a rotina '{nome_rotina}'."

    tarefas = rotinas[nome]

    for tarefa in tarefas:
        tipo = tarefa.get("tipo", "").strip().lower()
        valor = tarefa.get("valor")

        # compatibilidade com formato antigo
        if not valor:
            if tipo == "programa":
                valor = tarefa.get("nome")
            elif tipo == "site":
                valor = tarefa.get("url")
            elif tipo == "comando":
                valor = tarefa.get("cmd")

        if not valor:
            continue

        if tipo == "programa":
            abrir_programa_func(valor)

        elif tipo == "site":
            if str(valor).startswith("http"):
                webbrowser.open(valor)
            else:
                abrir_site_func(valor)

        elif tipo == "pasta":
            abrir_pasta_func(valor)

        elif tipo == "arquivo":
            abrir_arquivo_func(valor)

        elif tipo == "comando":
            executar_comando_func(valor)

    return True, f"Executando rotina '{nome_rotina}'."
def mostrar_rotina(nome_rotina):
    rotinas = carregar_rotinas()
    nome = nome_rotina.lower().strip()

    if nome not in rotinas:
        return False, f"Não encontrei a rotina '{nome_rotina}'."

    tarefas = rotinas[nome]

    resposta = f"Rotina '{nome}':\n"
    for i, tarefa in enumerate(tarefas, 1):
        tipo = tarefa.get("tipo", "")
        valor = tarefa.get("valor", "")
        if not valor:
            valor = tarefa.get("nome") or tarefa.get("url") or tarefa.get("cmd") or ""
        resposta += f"{i}. [{tipo}] {valor}\n"

    return True, resposta


def adicionar_item_rotina(nome_rotina, item):
    rotinas = carregar_rotinas()
    nome = nome_rotina.lower().strip()

    if nome not in rotinas:
        return False, f"Não encontrei a rotina '{nome_rotina}'."

    item = item.strip()
    item_lower = item.lower()

    if item_lower in ["github", "gmail", "youtube", "chatgpt", "google"]:
        novo_item = {"tipo": "site", "valor": item_lower}
    elif item_lower.startswith("http"):
        novo_item = {"tipo": "site", "valor": item}
    elif ":\\" in item or item.startswith("\\"):
        if any(item_lower.endswith(ext) for ext in [".pdf", ".docx", ".xlsx", ".txt", ".pptx"]):
            novo_item = {"tipo": "arquivo", "valor": item}
        else:
            novo_item = {"tipo": "pasta", "valor": item}
    else:
        novo_item = {"tipo": "programa", "valor": item_lower}

    rotinas[nome].append(novo_item)
    salvar_rotinas(rotinas)

    return True, f"Item '{item}' adicionado na rotina '{nome}'."


def remover_item_rotina(nome_rotina, item):
    rotinas = carregar_rotinas()
    nome = nome_rotina.lower().strip()

    if nome not in rotinas:
        return False, f"Não encontrei a rotina '{nome_rotina}'."

    item = item.lower().strip()
    tarefas = rotinas[nome]
    novas_tarefas = []

    removido = False

    for tarefa in tarefas:
        valor = tarefa.get("valor")
        if not valor:
            valor = tarefa.get("nome") or tarefa.get("url") or tarefa.get("cmd") or ""

        valor_normalizado = str(valor).lower().strip()

        if not removido and valor_normalizado == item:
            removido = True
            continue

        novas_tarefas.append(tarefa)

    if not removido:
        return False, f"Não encontrei o item '{item}' na rotina '{nome}'."

    rotinas[nome] = novas_tarefas
    salvar_rotinas(rotinas)

    return True, f"Item '{item}' removido da rotina '{nome}'."