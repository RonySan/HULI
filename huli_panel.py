import tkinter as tk
from modules.scheduler import listar_agendamentos
from modules.routines import listar_rotinas

root = tk.Tk()

root.title("H.U.L.I Control Panel")

root.geometry("500x500")

titulo = tk.Label(root, text="H.U.L.I Painel", font=("Arial", 18))
titulo.pack(pady=10)


def mostrar_rotinas():

    rotinas = listar_rotinas()

    texto.delete(1.0, tk.END)

    texto.insert(tk.END, "ROTINAS:\n\n")

    for r in rotinas:
        texto.insert(tk.END, f"- {r}\n")


def mostrar_agendamentos():

    ag = listar_agendamentos()

    texto.delete(1.0, tk.END)

    texto.insert(tk.END, "AGENDAMENTOS:\n\n")

    for item in ag:
        texto.insert(tk.END, f"{item['id']} - {item['valor']} às {item['horario']}\n")


btn1 = tk.Button(root, text="Mostrar Rotinas", command=mostrar_rotinas)
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Mostrar Agendamentos", command=mostrar_agendamentos)
btn2.pack(pady=5)

texto = tk.Text(root)
texto.pack(fill="both", expand=True)

root.mainloop()