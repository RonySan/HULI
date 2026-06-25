import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

BASE = r"C:\HULI"


def rodar_terminal(comando):
    subprocess.Popen(f'start cmd /k "{comando}"', cwd=BASE, shell=True)


def iniciar_huli():
    rodar_terminal("cd /d C:\\HULI && python -m core.huli")


def modo_trabalho():
    rodar_terminal("cd /d C:\\HULI && python -m core.huli")


def abrir_pasta():
    os.startfile(BASE)


def abrir_docs():
    pasta = os.path.join(BASE, "docs")
    if os.path.exists(pasta):
        os.startfile(pasta)
    else:
        messagebox.showinfo("H.U.L.I", "Pasta docs ainda não existe.")


def atualizar_git():
    rodar_terminal("cd /d C:\\HULI && git pull --rebase origin main")


janela = tk.Tk()
janela.title("H.U.L.I 5.0 Desktop")
janela.geometry("460x430")
janela.resizable(False, False)

titulo = tk.Label(janela, text="H.U.L.I 5.0", font=("Arial", 26, "bold"))
titulo.pack(pady=15)

subtitulo = tk.Label(
    janela,
    text="Humano Único Leal Inteligente",
    font=("Arial", 11)
)
subtitulo.pack()

status = tk.Label(
    janela,
    text=f"Online para Rony • {datetime.now().strftime('%d/%m/%Y %H:%M')}",
    font=("Arial", 10)
)
status.pack(pady=10)

tk.Button(janela, text="🚀 Iniciar H.U.L.I", width=35, height=2, command=iniciar_huli).pack(pady=6)
tk.Button(janela, text="💼 Abrir Modo Trabalho", width=35, height=2, command=modo_trabalho).pack(pady=6)
tk.Button(janela, text="📁 Abrir Pasta C:\\HULI", width=35, height=2, command=abrir_pasta).pack(pady=6)
tk.Button(janela, text="📄 Abrir Documentação", width=35, height=2, command=abrir_docs).pack(pady=6)
tk.Button(janela, text="🔄 Atualizar pelo Git", width=35, height=2, command=atualizar_git).pack(pady=6)
tk.Button(janela, text="Sair", width=35, command=janela.destroy).pack(pady=15)

janela.mainloop()