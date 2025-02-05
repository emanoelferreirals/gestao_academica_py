import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from funcs import cadastrar_usuario, login_usuario, abrir_tela_notas, on_close
import subprocess

def fazer_login():
    email = campos['email']['widget'].get().strip()
    senha = campos['senha']['widget'].get().strip()
    if not email or not senha:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return
    resultado = login_usuario({"email": email, "senha": senha})
    if resultado is True:
        abrir_tela_notas(root,"menu.py")
        # messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
    else:
        messagebox.showerror("Erro", resultado)

def fazer_cadastro():
    nome = campos['nome']['widget'].get().strip()
    email = campos['email_cd']['widget'].get().strip()
    senha = campos['senha_cd']['widget'].get().strip()
    confirmar_senha = campos['conf_senha']['widget'].get().strip()
    if not nome or not email or not senha or not confirmar_senha:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return
    if senha != confirmar_senha:
        messagebox.showerror("Erro", "As senhas não coincidem!")
        return
    resultado = cadastrar_usuario({
        "cadastro": {
            "nome": nome,
            "email": email,
            "senha": senha
        }
    })
    if resultado is True:
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        mostrar_tela('login')
    else:
        messagebox.showerror("Erro", resultado)

def mostrar_tela(tela):
    for widget in frame.winfo_children():
        widget.grid_forget()
    for nome, config in telas[tela].items():
        config['widget'].grid(row=config['row'], column=config['column'], columnspan=config.get('columnspan', 1), pady=5, sticky="w")
    root.title(tela.replace('_', ' ').title() + " SODGA")

# Configurações da Janela
largura_tela, altura_tela = 600, 350
style = Style(theme="darkly")
root = style.master
root.title("Login SODGA")
root.geometry(f"{largura_tela}x{altura_tela}")
root.resizable(False, False)

# Imagem de fundo da janela
fundo = Image.open("resources/img/wallpaper.png").resize((largura_tela, altura_tela))
fundo = ImageTk.PhotoImage(fundo)
lbl_fundo = ttk.Label(root, image=fundo)
lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Frame principal
frame = ttk.Frame(root, padding=30)
frame.grid(row=0, column=0, padx=20, pady=50)

"""# Logo ao lado do frame
logo = Image.open("resources/img/logo_if.png").resize((100, 150))
logo = ImageTk.PhotoImage(logo)
lbl_logo = tk.Label(root, image=logo)
lbl_logo.grid(row=0, column=1, padx=20)"""

# Campos de entrada
campos = { 
    'email': {'widget': ttk.Entry(frame, width=25), 'row': 0, 'column': 1},
    'senha': {'widget': ttk.Entry(frame, width=25, show="*"), 'row': 1, 'column': 1},
    'nome': {'widget': ttk.Entry(frame, width=25), 'row': 0, 'column': 1},
    'email_cd': {'widget': ttk.Entry(frame, width=25), 'row': 1, 'column': 1},
    'senha_cd': {'widget': ttk.Entry(frame, width=25, show="*"), 'row': 2, 'column': 1},
    'conf_senha': {'widget': ttk.Entry(frame, width=25, show="*"), 'row': 3, 'column': 1}
}

# Telas
telas = {
    'login': {
        'lbl_email': {'widget': ttk.Label(frame, text="Email:"), 'row': 0, 'column': 0},
        'email': campos['email'],
        'lbl_senha': {'widget': ttk.Label(frame, text="Senha:"), 'row': 1, 'column': 0},
        'senha': campos['senha'],
        'btn_login': {'widget': ttk.Button(frame, text="Login", command=fazer_login, bootstyle="success"), 'row': 2, 'column': 0, 'columnspan': 2},
        'btn_cadastro': {'widget': ttk.Button(frame, text="Criar Conta", command=lambda: mostrar_tela('cadastro'), bootstyle="info"), 'row': 3, 'column': 0, 'columnspan': 2}
    },
    'cadastro': {
        'lbl_nome': {'widget': ttk.Label(frame, text="Nome Completo:"), 'row': 0, 'column': 0},
        'nome': campos['nome'],
        'lbl_email_cd': {'widget': ttk.Label(frame, text="Email:"), 'row': 1, 'column': 0},
        'email_cd': campos['email_cd'],
        'lbl_senha_cd': {'widget': ttk.Label(frame, text="Senha:"), 'row': 2, 'column': 0},
        'senha_cd': campos['senha_cd'],
        'lbl_conf_senha': {'widget': ttk.Label(frame, text="Confirmar Senha:"), 'row': 3, 'column': 0},
        'conf_senha': campos['conf_senha'],
        'btn_cadastrar': {'widget': ttk.Button(frame, text="Cadastrar", command=fazer_cadastro, bootstyle="success"), 'row': 4, 'column': 1},
        'btn_voltar': {'widget': ttk.Button(frame, text="Voltar", command=lambda: mostrar_tela('login'), bootstyle="danger"), 'row': 4, 'column': 0}
    }
}

# Exibir a tela inicial
mostrar_tela('login')

# Vinculando a função on_close ao evento de fechar a janela
root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))  # Chamando a função on_close

root.mainloop()
