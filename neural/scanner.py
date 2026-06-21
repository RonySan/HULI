import ast
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PASTAS_ANALISADAS = [
    "core",
    "core_system",
    "modules",
    "services",
    "neural",
]

IGNORAR_PASTAS = [
    "__pycache__",
    ".git",
    "venv",
    ".venv",
    "env",
]


def listar_arquivos_py():
    arquivos = []

    for pasta in PASTAS_ANALISADAS:
        raiz = os.path.join(BASE_DIR, pasta)

        if not os.path.exists(raiz):
            continue

        for dirpath, dirnames, filenames in os.walk(raiz):
            dirnames[:] = [d for d in dirnames if d not in IGNORAR_PASTAS]

            for filename in filenames:
                if filename.endswith(".py"):
                    arquivos.append(os.path.join(dirpath, filename))

    return arquivos


def listar_jsons():
    arquivos = []

    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        dirnames[:] = [d for d in dirnames if d not in IGNORAR_PASTAS]

        for filename in filenames:
            if filename.endswith(".json"):
                arquivos.append(os.path.join(dirpath, filename))

    return arquivos


def analisar_arquivo(caminho):
    rel = os.path.relpath(caminho, BASE_DIR)

    info = {
        "arquivo": rel,
        "classes": [],
        "funcoes": [],
        "imports": [],
        "linhas": 0,
        "erro_sintaxe": None,
    }

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            codigo = f.read()

        info["linhas"] = len(codigo.splitlines())

        arvore = ast.parse(codigo)

        for node in ast.walk(arvore):
            if isinstance(node, ast.ClassDef):
                info["classes"].append(node.name)

            elif isinstance(node, ast.FunctionDef):
                info["funcoes"].append(node.name)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    info["imports"].append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    info["imports"].append(node.module)

    except SyntaxError as e:
        info["erro_sintaxe"] = f"{e}"
    except Exception as e:
        info["erro_sintaxe"] = f"{e}"

    return info


def scanear_projeto():
    arquivos = listar_arquivos_py()
    resultado = []

    for caminho in arquivos:
        resultado.append(analisar_arquivo(caminho))

    return resultado


def resumo_scan():
    dados = scanear_projeto()
    jsons = listar_jsons()

    total_classes = sum(len(item["classes"]) for item in dados)
    total_funcoes = sum(len(item["funcoes"]) for item in dados)
    total_linhas = sum(item["linhas"] for item in dados)
    erros = [item for item in dados if item["erro_sintaxe"]]

    return {
        "arquivos_py": len(dados),
        "arquivos_json": len(jsons),
        "classes": total_classes,
        "funcoes": total_funcoes,
        "linhas": total_linhas,
        "erros_sintaxe": len(erros),
        "arquivos_com_erro": erros,
    }