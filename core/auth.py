from core.config import OWNER_NAME, OWNER_PASSWORD

def autenticar(usuario, senha):
    if usuario == OWNER_NAME and senha == OWNER_PASSWORD:
        return True
    return False