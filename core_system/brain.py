from modules.intent_engine import detectar_intencao
from services import system_service
from services import voice_service
from services import vision_service
from services import automation_service
from services import memory_service
from services import ai_service


def processar_intencao_local(comando, base=""):
    intencao = detectar_intencao(comando)

    if not intencao:
        return None

    intent = intencao.get("intent")
    valor = intencao.get("valor", "")
    texto = intencao.get("texto", comando)

    if intent == "hora":
        from datetime import datetime
        return f"{base} Agora são {datetime.now().strftime('%H:%M:%S')}."

    if intent == "data":
        from datetime import datetime
        return f"{base} Hoje é {datetime.now().strftime('%d/%m/%Y')}."

    if intent == "status_sistema":
        return system_service.status()

    if intent == "clicar":
        return automation_service.clique()

    if intent == "duplo_clique":
        return automation_service.clique_duplo()

    if intent == "clique_direito":
        return automation_service.clique_direito_mouse()

    if intent == "digitar":
        return automation_service.digitar(valor)

    if intent == "pressionar":
        return automation_service.pressionar(valor)

    if intent == "pesquisar":
        from modules.pc_control import pesquisar_web
        _, resposta = pesquisar_web(valor)
        return resposta

    if intent == "abrir_site":
        from modules.pc_control import abrir_site
        ok, resposta = abrir_site(valor)
        if ok:
            return resposta

    return None