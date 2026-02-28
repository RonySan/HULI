from modules.identity import HULIIdentity
from modules.commands import processar_comando


def iniciar():
    identidade = HULIIdentity()
    print(identidade.apresentar())
    print("H.U.L.I iniciado.")
    print("Aguardando comando...")

    while True:
        comando = input("Você: ")

        resposta = processar_comando(comando)

        if resposta == "ENCERRAR":
            print("H.U.L.I: Encerrando operações. Até logo, Rony.")
            break

        print(f"H.U.L.I: {resposta}")


if __name__ == "__main__":
    iniciar()
