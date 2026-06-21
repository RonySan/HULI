from neural.scanner import scanear_projeto


def mapa_dependencias():
    dados = scanear_projeto()
    mapa = {}

    for item in dados:
        mapa[item["arquivo"]] = sorted(set(item["imports"]))

    return mapa


def procurar_imports_suspeitos():
    mapa = mapa_dependencias()
    suspeitos = []

    for arquivo, imports in mapa.items():
        for imp in imports:
            if imp.startswith("modules.commands"):
                suspeitos.append({
                    "arquivo": arquivo,
                    "import": imp,
                    "motivo": "Possível risco de import circular com commands.py"
                })

    return suspeitos


def resumo_dependencias():
    mapa = mapa_dependencias()
    suspeitos = procurar_imports_suspeitos()

    total_imports = sum(len(v) for v in mapa.values())

    return {
        "arquivos_mapeados": len(mapa),
        "total_imports": total_imports,
        "imports_suspeitos": suspeitos,
    }