import tkinter as tk

from modules.routines import listar_rotinas
from modules.scheduler import listar_agendamentos
from modules.custom_commands import listar_comandos_personalizados

root = tk.Tk()
root.title("H.U.L.I Control Panel")
root.geometry("700x500")

titulo = tk.Label(root, text="H.U.L.I - Painel de Controle", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

texto = tk.Text(root, wrap="word")
texto.pack(fill="both", expand=True, padx=10, pady=10)


def limpar():
    texto.delete("1.0", tk.END)


def mostrar_rotinas():
    limpar()
    texto.insert(tk.END, "ROTINAS:\n\n")
    for nome in listar_rotinas():
        texto.insert(tk.END, f"- {nome}\n")


def mostrar_agendamentos():
    limpar()
    texto.insert(tk.END, "AGENDAMENTOS:\n\n")
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
    texto.insert(tk.END, "COMANDOS PERSONALIZADOS:\n\n")
    dados = listar_comandos_personalizados()
    if not dados:
        texto.insert(tk.END, "Nenhum comando personalizado cadastrado.\n")
        return

    for nome, comando in dados.items():
        texto.insert(tk.END, f"- {nome} => {comando}\n")


frame = tk.Frame(root)
frame.pack(pady=5)

tk.Button(frame, text="Rotinas", width=20, command=mostrar_rotinas).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Agendamentos", width=20, command=mostrar_agendamentos).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Comandos Personalizados", width=20, command=mostrar_comandos).grid(row=0, column=2, padx=5)

root.mainloop()