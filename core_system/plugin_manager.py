import importlib
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGINS_DIR = os.path.join(BASE_DIR, "plugins")


def garantir_pasta_plugins():
    if not os.path.exists(PLUGINS_DIR):
        os.makedirs(PLUGINS_DIR)


def descobrir_plugins():
    garantir_pasta_plugins()

    plugins = []

    for arquivo in os.listdir(PLUGINS_DIR):
        if not arquivo.endswith(".py"):
            continue

        if arquivo == "__init__.py":
            continue

        nome = arquivo.replace(".py", "")
        plugins.append(nome)

    return plugins


def carregar_plugin(nome):
    try:
        modulo = importlib.import_module(f"plugins.{nome}")

        info = {}

        if hasattr(modulo, "PLUGIN_INFO"):
            info = modulo.PLUGIN_INFO

        return {
            "nome": nome,
            "status": "OK",
            "info": info,
            "modulo": modulo,
        }

    except Exception as e:
        return {
            "nome": nome,
            "status": "ERRO",
            "erro": str(e),
        }


def listar_plugins():
    nomes = descobrir_plugins()
    resultado = []

    for nome in nomes:
        resultado.append(carregar_plugin(nome))

    return resultado


def status_plugins():
    plugins = listar_plugins()

    total = len(plugins)
    ok = len([p for p in plugins if p.get("status") == "OK"])
    erros = len([p for p in plugins if p.get("status") == "ERRO"])

    return {
        "total": total,
        "ok": ok,
        "erros": erros,
        "plugins": plugins,
    }


def formatar_plugins():
    status = status_plugins()

    resposta = "🔌 Plugins da H.U.L.I\n\n"
    resposta += f"Total: {status['total']}\n"
    resposta += f"OK: {status['ok']}\n"
    resposta += f"Erros: {status['erros']}\n\n"

    if not status["plugins"]:
        resposta += "Nenhum plugin encontrado."
        return resposta

    for plugin in status["plugins"]:
        resposta += f"• {plugin['nome']} — {plugin['status']}\n"

        info = plugin.get("info", {})

        if info:
            resposta += f"  Descrição: {info.get('descricao', 'sem descrição')}\n"
            resposta += f"  Versão: {info.get('versao', '0.0.1')}\n"

        if plugin.get("erro"):
            resposta += f"  Erro: {plugin['erro']}\n"

    return resposta