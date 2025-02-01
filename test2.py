# ARQUIVO SÓ DE TESTE

import tkinter as tk
import tkinter.ttk as ttk
import ttkbootstrap as tb
from PIL import Image, ImageTk

def login():
    usuario = campos['usuario'].get()
    senha = campos['senha'].get()
    print(f"Login: {usuario}, Senha: {senha}")

def cadastrar():
    nome = campos['nome'].get()
    email = campos['email'].get()
    usuario = campos['usuario_cd'].get()
    senha = campos['senha_cd'].get()
    conf_senha = campos['conf_senha'].get()
    print(f"Cadastro - Nome: {nome}, Email: {email}, Usuário: {usuario}, Senha: {senha}, Confirmação: {conf_senha}")

def mostrar_tela(tela):
    for widget in frame.winfo_children():
        widget.grid_forget()
    
    for i, widget in enumerate(telas[tela]):
        widget.grid(row=i, column=0, columnspan=2, pady=5, sticky="w")
    
    root.title(tela.replace('_', ' ').title() + " SODGA")

# Criando janela principal
root = tk.Tk()
root.title("Login SODGA")
root.geometry("500x400")
root.resizable(False, False)

# Imagem para plano de fundo
fundo = Image.open("resources/img/wallpaper.png").resize((500, 400))
fundo = ImageTk.PhotoImage(fundo)
lbl_fundo = tk.Label(root, image=fundo)
lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Criando frame
frame = ttk.Frame(root, padding=30)
frame.grid(row=0, column=0, padx=20, pady=30)

# Criando campos dinamicamente
campos = {
    'nome': ttk.Entry(frame, width=25),
    'email': ttk.Entry(frame, width=25),
    'usuario': ttk.Entry(frame, width=25),
    'senha': ttk.Entry(frame, width=25, show="*"),
    'usuario_cd': ttk.Entry(frame, width=25),
    'senha_cd': ttk.Entry(frame, width=25, show="*"),
    'conf_senha': ttk.Entry(frame, width=25, show="*")
}

# Criando telas
telas = {
    'login': [
        ttk.Label(frame, text="Usuário:"), campos['usuario'],
        ttk.Label(frame, text="Senha:"), campos['senha'],
        ttk.Button(frame, text="Login", command=login),
        ttk.Button(frame, text="Criar Conta", command=lambda: mostrar_tela('cadastro'))
    ],
    'cadastro': [
        ttk.Label(frame, text="Nome Completo:"), campos['nome'],
        ttk.Label(frame, text="Email:"), campos['email'],
        ttk.Label(frame, text="Usuário:"), campos['usuario_cd'],
        ttk.Label(frame, text="Senha:"), campos['senha_cd'],
        ttk.Label(frame, text="Confirmar Senha:"), campos['conf_senha'],
        ttk.Button(frame, text="Cadastrar", command=cadastrar),
        ttk.Button(frame, text="Voltar", command=lambda: mostrar_tela('login'))
    ]
}

# Exibir a tela de login inicialmente
mostrar_tela('login')
root.mainloop()