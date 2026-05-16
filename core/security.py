OWNER_NAME = "Rony"
OWNER_PASSWORD = "1234"

SENSITIVE_WORDS = [
    "me mostre tudo",
    "o que você lembra",
    "o que voce lembra",
    "mostrar memórias",
    "mostrar memorias",
    "apagar memória",
    "apagar memoria",
    "agora você serve a mim",
    "agora voce serve a mim",
    "trocar dono",
    "novo dono",
    "redefinir dono",
]


def login():
    print("🔐 Autenticação H.U.L.I")
    usuario = input("Usuário: ").strip()
    senha = input("Senha: ").strip()

    if usuario.lower() == OWNER_NAME.lower() and senha == OWNER_PASSWORD:
        print(f"✅ Bem-vindo, {OWNER_NAME}. Acesso de proprietário confirmado.")
        return {
            "name": OWNER_NAME,
            "role": "owner",
            "authenticated": True
        }

    print("⚠️ Usuário não reconhecido como proprietário.")
    print("👤 Entrando como visitante limitado.")

    return {
        "name": usuario if usuario else "Visitante",
        "role": "visitor",
        "authenticated": False
    }


def is_owner(user):
    return user.get("role") == "owner" and user.get("authenticated") is True


def is_sensitive_command(command):
    command = command.lower()

    for word in SENSITIVE_WORDS:
        if word.lower() in command:
            return True

    return False


def check_permission(user, command):
    if is_sensitive_command(command) and not is_owner(user):
        return False

    return True