def iniciar():
    print("H.U.L.I iniciado.")
    print("Aguardando comando...")

    while True:
        comando = input("Você: ")

        if comando.lower() == "sair":
            print("H.U.L.I: Encerrando operações. Até logo, Rony.")
            break

        elif comando.lower() == "status":
            print("H.U.L.I: Sistemas operacionais funcionando normalmente.")

        else:
            print("H.U.L.I: Comando não reconhecido.")


if __name__ == "__main__":
    iniciar()
