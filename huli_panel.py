import tkinter as tk
from tkinter import scrolledtext

from modules.routines import listar_rotinas
from modules.scheduler import listar_agendamentos
from modules.custom_commands import listar_comandos_personalizados
from modules.missions import listar_missoes
from modules.backup import listar_backups
from modules.logger import ler_logs

root = tk.Tk()
root.title("H.U.L.I Control Panel")
root.geometry("950x600")

titulo = tk.Label(root, text="H.U.L.I - Painel de Controle", font=("Arial", 20, "bold"))
titulo.pack(pady=10)

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=5)

texto = scrolledtext.ScrolledText(root, wrap="word", font=("Consolas", 11))
texto.pack(fill="both", expand=True, padx=10, pady=10)


def limpar():
    texto.delete("1.0", tk.END)


def escrever_titulo(nome):
    texto.insert(tk.END, f"{nome}\n")
    texto.insert(tk.END, "=" * len(nome) + "\n\n")


def mostrar_rotinas():
    limpar()
    escrever_titulo("ROTINAS")
    itens = listar_rotinas()
    if not itens:
        texto.insert(tk.END, "Nenhuma rotina cadastrada.\n")
        return
    for item in itens:
        texto.insert(tk.END, f"- {item}\n")


def mostrar_agendamentos():
    limpar()
    escrever_titulo("AGENDAMENTOS")
    itens = listar_agendamentos()
    if not itens:
        texto.insert(tk.END, "Nenhum agendamento cadastrado.\n")
        return

    for item in itens:
        texto.insert(
            tk.END,
            f"{item['id']}. [{item['tipo']}] {item['valor']} às {item['horario']} ({item.get('recorrencia', 'uma vez')})\n"
        )


def mostrar_comandos():
    limpar()
    escrever_titulo("COMANDOS PERSONALIZADOS")
    dados = listar_comandos_personalizados()
    if not dados:
        texto.insert(tk.END, "Nenhum comando personalizado cadastrado.\n")
        return

    for nome, comando in dados.items():
        texto.insert(tk.END, f"- {nome} => {comando}\n")


def mostrar_missoes():
    limpar()
    escrever_titulo("MISSÕES")
    itens = listar_missoes()
    if not itens:
        texto.insert(tk.END, "Nenhuma missão cadastrada.\n")
        return

    for item in itens:
        texto.insert(tk.END, f"- {item}\n")


def mostrar_backups():
    limpar()
    escrever_titulo("BACKUPS")
    itens = listar_backups()
    if not itens:
        texto.insert(tk.END, "Nenhum backup encontrado.\n")
        return

    for item in itens:
        texto.insert(tk.END, f"- {item}\n")


def mostrar_logs():
    limpar()
    escrever_titulo("LOGS")
    linhas = ler_logs(200)

    if not linhas:
        texto.insert(tk.END, "Nenhum log disponível.\n")
        return

    for linha in linhas:
        texto.insert(tk.END, linha)


def atualizar_logs_auto():
    mostrar_logs()
    root.after(5000, atualizar_logs_auto)


tk.Button(frame_botoes, text="Rotinas", width=18, command=mostrar_rotinas).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Agendamentos", width=18, command=mostrar_agendamentos).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botoes, text="Comandos", width=18, command=mostrar_comandos).grid(row=0, column=2, padx=5, pady=5)
tk.Button(frame_botoes, text="Missões", width=18, command=mostrar_missoes).grid(row=0, column=3, padx=5, pady=5)
tk.Button(frame_botoes, text="Backups", width=18, command=mostrar_backups).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_botoes, text="Logs", width=18, command=mostrar_logs).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_botoes, text="Logs ao vivo", width=18, command=atualizar_logs_auto).grid(row=1, column=2, padx=5, pady=5)

root.mainloop()