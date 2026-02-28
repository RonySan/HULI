from modules.personality import HULIPersonality
from datetime import datetime


def processar_comando(comando):

    personalidade = HULIPersonality()
    comando = comando.lower().strip()


    if comando == "status":
        base = personalidade.gerar_resposta_base()
        return f"{base} Sistemas operacionais funcionando normalmente."

    elif comando == "hora":
        agora = datetime.now()
        base = personalidade.gerar_resposta_base()
        return f"{base} Agora são {agora.strftime('%H:%M:%S')}."

    elif comando == "sair":
        return "ENCERRAR"

    else:
        return "Comando não reconhecido."
