import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from funcs import *

def login():
    email = campos['email']['widget'].get()
    senha = campos['senha']['widget'].get()
    print(f"Email: {email}, Senha: {senha}")
    messagebox.showinfo("Aviso", f"Email: {email}, Senha: {senha}")

def cadastro():
    nome = campos['nome']['widget'].get()
    email = campos['email_cd']['widget'].get()
    senha = campos['senha_cd']['widget'].get()
    confirmar_senha = campos['conf_senha']['widget'].get()

    dados = {
        "cadastro": {
            "nome": nome,
            "email": email,
            "senha": senha
        }
    }

    print(f"Cadastro - Nome: {nome}, Email: {email}, Senha: {senha}, Confirmar Senha: {confirmar_senha}")

    if cadastrar_user(dados):
        messagebox.showinfo("Aviso", "Usuário cadastrado com sucesso!")
    else:
        messagebox.showinfo("Erro", "Erro ao cadastrar")

def mostrar_tela(tela):
    for widget in frame.winfo_children():
        widget.grid_forget()
    
    for nome, config in telas[tela].items():
        config['widget'].grid(row=config['row'], column=config['column'], columnspan=config.get('columnspan', 1), pady=5, sticky="w")
    
    root.title(tela.replace('_', ' ').title() + " SODGA")

largura_tela = 600
altura_tela = 350

root = tk.Tk()
root.title("Login SODGA") 
root.geometry(f"{largura_tela}x{altura_tela}") # 500x300
root.resizable(False, False) # impede redimencionamento


# Imagem de fundo
fundo = Image.open("resources/img/wallpaper.png").resize((largura_tela, altura_tela)) #importa imagem
fundo = ImageTk.PhotoImage(fundo) #abre no padrão

lbl_fundo = tk.Label(root, image=fundo)
lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)

frame = ttk.Frame(root, padding=30)
frame.grid(row=0, column=0, padx=20, pady=50)

# Campos
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
        'btn_login': {'widget': ttk.Button(frame, text="Login", command=login), 'row': 2, 'column': 0, 'columnspan': 2},
        'btn_cadastro': {'widget': ttk.Button(frame, text="Criar Conta", command=lambda: mostrar_tela('cadastro')), 'row': 3, 'column': 0, 'columnspan': 2}
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
        'btn_cadastrar': {'widget': ttk.Button(frame, text="Cadastrar", command=cadastro), 'row': 4, 'column': 1},
        'btn_voltar': {'widget': ttk.Button(frame, text="Voltar", command=lambda: mostrar_tela('login')), 'row': 4, 'column': 0}
    }
}

# Exibir a tela inicial
mostrar_tela('login')
root.mainloop()
