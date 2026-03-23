import tkinter as tk
from tkinter import scrolledtext
import threading

from modules.commands import processar_comando
from modules.routines import listar_rotinas
from modules.scheduler import listar_agendamentos
from modules.custom_commands import listar_comandos_personalizados
from modules.missions import listar_missoes
from modules.backup import listar_backups
from modules.logger import ler_logs


class HuliPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("H.U.L.I - Painel Interativo")
        self.root.geometry("1050x700")

        titulo = tk.Label(
            root,
            text="H.U.L.I - Painel Interativo",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=10)

        subtitulo = tk.Label(
            root,
            text="Você pode usar o painel e o terminal ao mesmo tempo.",
            font=("Arial", 10)
        )
        subtitulo.pack()

        # Área superior de comando
        frame_comando = tk.Frame(root)
        frame_comando.pack(fill="x", padx=10, pady=10)

        self.entry_comando = tk.Entry(frame_comando, font=("Arial", 12))
        self.entry_comando.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_comando.bind("<Return>", self.executar_comando_evento)

        btn_executar = tk.Button(
            frame_comando,
            text="Executar",
            width=15,
            command=self.executar_comando
        )
        btn_executar.pack(side="left")

        # Botões rápidos
        frame_botoes = tk.Frame(root)
        frame_botoes.pack(fill="x", padx=10, pady=5)

        botoes = [
            ("Ajuda", lambda: self.preencher_e_executar("ajuda")),
            ("Status Sistema", lambda: self.preencher_e_executar("status sistema")),
            ("Listar Rotinas", lambda: self.mostrar_rotinas()),
            ("Agendamentos", lambda: self.mostrar_agendamentos()),
            ("Comandos", lambda: self.mostrar_comandos()),
            ("Missões", lambda: self.mostrar_missoes()),
            ("Backups", lambda: self.mostrar_backups()),
            ("Logs", lambda: self.mostrar_logs()),
            ("Limpar Tela", self.limpar_tela),
        ]

        for i, (texto, comando) in enumerate(botoes):
            tk.Button(frame_botoes, text=texto, width=18, command=comando).grid(
                row=0,
                column=i,
                padx=4,
                pady=4
            )

        # Área principal dividida
        frame_principal = tk.Frame(root)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

        # Console do painel
        frame_console = tk.Frame(frame_principal)
        frame_console.pack(side="left", fill="both", expand=True, padx=(0, 5))

        lbl_console = tk.Label(frame_console, text="Console H.U.L.I", font=("Arial", 12, "bold"))
        lbl_console.pack(anchor="w")

        self.console = scrolledtext.ScrolledText(
            frame_console,
            wrap="word",
            font=("Consolas", 11)
        )
        self.console.pack(fill="both", expand=True)

        # Painel lateral
        frame_lateral = tk.Frame(frame_principal, width=300)
        frame_lateral.pack(side="right", fill="y", padx=(5, 0))

        lbl_lateral = tk.Label(frame_lateral, text="Resumo", font=("Arial", 12, "bold"))
        lbl_lateral.pack(anchor="w")

        self.resumo = scrolledtext.ScrolledText(
            frame_lateral,
            wrap="word",
            font=("Consolas", 10),
            height=20,
            width=35
        )
        self.resumo.pack(fill="both", expand=True)

        # Rodapé
        frame_rodape = tk.Frame(root)
        frame_rodape.pack(fill="x", padx=10, pady=5)

        btn_logs_auto = tk.Button(
            frame_rodape,
            text="Logs ao vivo",
            width=18,
            command=self.logs_ao_vivo
        )
        btn_logs_auto.pack(side="left", padx=5)

        btn_atualizar_resumo = tk.Button(
            frame_rodape,
            text="Atualizar Resumo",
            width=18,
            command=self.atualizar_resumo
        )
        btn_atualizar_resumo.pack(side="left", padx=5)

        self.escrever_console("H.U.L.I painel iniciado.")
        self.escrever_console("Você pode continuar usando o terminal normalmente.")
        self.atualizar_resumo()

    def escrever_console(self, texto):
        self.console.insert(tk.END, texto + "\n")
        self.console.see(tk.END)

    def limpar_tela(self):
        self.console.delete("1.0", tk.END)

    def executar_comando_evento(self, event):
        self.executar_comando()

    def executar_comando(self):
        comando = self.entry_comando.get().strip()

        if not comando:
            return

        self.entry_comando.delete(0, tk.END)
        self.escrever_console(f"Você: {comando}")

        def rodar():
            try:
                resposta = processar_comando(comando)

                if resposta == "ENCERRAR":
                    resposta = "Encerrando operações. Até logo, Rony."

                if not resposta:
                    resposta = "(sem resposta)"

                self.root.after(0, lambda: self.escrever_console(f"H.U.L.I: {resposta}"))
                self.root.after(0, self.atualizar_resumo)

            except Exception as e:
                self.root.after(0, lambda: self.escrever_console(f"[ERRO] {e}"))

        threading.Thread(target=rodar, daemon=True).start()

    def preencher_e_executar(self, comando):
        self.entry_comando.delete(0, tk.END)
        self.entry_comando.insert(0, comando)
        self.executar_comando()

    def mostrar_rotinas(self):
        itens = listar_rotinas()
        self.escrever_console("\n=== ROTINAS ===")
        if not itens:
            self.escrever_console("Nenhuma rotina cadastrada.")
            return
        for item in itens:
            self.escrever_console(f"- {item}")

    def mostrar_agendamentos(self):
        itens = listar_agendamentos()
        self.escrever_console("\n=== AGENDAMENTOS ===")
        if not itens:
            self.escrever_console("Nenhum agendamento cadastrado.")
            return
        for item in itens:
            self.escrever_console(
                f"{item['id']}. [{item['tipo']}] {item['valor']} às {item['horario']} ({item.get('recorrencia', 'uma vez')})"
            )

    def mostrar_comandos(self):
        dados = listar_comandos_personalizados()
        self.escrever_console("\n=== COMANDOS PERSONALIZADOS ===")
        if not dados:
            self.escrever_console("Nenhum comando personalizado cadastrado.")
            return
        for nome, comando in dados.items():
            self.escrever_console(f"- {nome} => {comando}")

    def mostrar_missoes(self):
        itens = listar_missoes()
        self.escrever_console("\n=== MISSÕES ===")
        if not itens:
            self.escrever_console("Nenhuma missão cadastrada.")
            return
        for item in itens:
            self.escrever_console(f"- {item}")

    def mostrar_backups(self):
        itens = listar_backups()
        self.escrever_console("\n=== BACKUPS ===")
        if not itens:
            self.escrever_console("Nenhum backup encontrado.")
            return
        for item in itens:
            self.escrever_console(f"- {item}")

    def mostrar_logs(self):
        linhas = ler_logs(50)
        self.escrever_console("\n=== LOGS ===")
        if not linhas:
            self.escrever_console("Nenhum log disponível.")
            return
        for linha in linhas:
            self.escrever_console(linha.rstrip())

    def logs_ao_vivo(self):
        self.mostrar_logs()
        self.root.after(5000, self.logs_ao_vivo)

    def atualizar_resumo(self):
        self.resumo.delete("1.0", tk.END)

        rotinas = listar_rotinas()
        agendamentos = listar_agendamentos()
        comandos = listar_comandos_personalizados()
        missoes = listar_missoes()
        backups = listar_backups()

        self.resumo.insert(tk.END, "RESUMO GERAL\n")
        self.resumo.insert(tk.END, "============\n\n")

        self.resumo.insert(tk.END, f"Rotinas: {len(rotinas)}\n")
        self.resumo.insert(tk.END, f"Agendamentos: {len(agendamentos)}\n")
        self.resumo.insert(tk.END, f"Comandos personalizados: {len(comandos)}\n")
        self.resumo.insert(tk.END, f"Missões: {len(missoes)}\n")
        self.resumo.insert(tk.END, f"Backups: {len(backups)}\n\n")

        self.resumo.insert(tk.END, "Últimos logs:\n")
        self.resumo.insert(tk.END, "------------\n")

        for linha in ler_logs(10):
            self.resumo.insert(tk.END, linha)


if __name__ == "__main__":
    root = tk.Tk()
    app = HuliPanel(root)
    root.mainloop()