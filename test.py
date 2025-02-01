import tkinter as tk
import tkinter.ttk as ttk
import ttkbootstrap as tb
from PIL import Image, ImageTk

def login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    print(f"Login: {usuario}, Senha: {senha}")
    # Aqui você pode adicionar a lógica de login

def cadastrar():
    nome = entry_nome.get()
    email = entry_email.get()
    usuario = entry_usuario_cd.get()
    senha = entry_senha_cd.get()
    conf_senha = entry_conf_senha.get()
    print(f"Cadastro - Nome: {nome}, Email: {email}, Usuário: {usuario}, Senha: {senha}, Confirmação: {conf_senha}")
    # Aqui você pode adicionar a lógica de cadastro

def mostrar_tela_login():
    # Esconder os elementos da tela de cadastro
    lbl_nome.grid_forget()
    entry_nome.grid_forget()
    lbl_email.grid_forget()
    entry_email.grid_forget()
    lbl_usuario_cd.grid_forget()
    entry_usuario_cd.grid_forget()
    lbl_senha_cd.grid_forget()
    entry_senha_cd.grid_forget()
    lbl_conf_senha.grid_forget()
    entry_conf_senha.grid_forget()
    btn_cadastrar.grid_forget()
    btn_voltar.grid_forget()
    
    # Exibir os elementos da tela de login
    lbl_usuario.grid(row=0, column=0, sticky="w", pady=5)
    entry_usuario.grid(row=0, column=1)
    lbl_senha.grid(row=1, column=0, sticky="w", pady=5)
    entry_senha.grid(row=1, column=1)
    btn_login.grid(row=2, column=0, columnspan=2, pady=10)
    btn_tela_cadastro.grid(row=3, column=0, columnspan=2, pady=10)
    
    root.title("Login SODGA")

def mostrar_tela_cadastro():
    # Esconder os elementos da tela de login
    lbl_usuario.grid_forget()
    entry_usuario.grid_forget()
    lbl_senha.grid_forget()
    entry_senha.grid_forget()
    btn_login.grid_forget()
    btn_tela_cadastro.grid_forget()
    
    # Exibir os elementos da tela de cadastro
    lbl_nome.grid(row=0, column=0, sticky="w", pady=5)
    entry_nome.grid(row=0, column=1)
    lbl_email.grid(row=1, column=0, sticky="w", pady=5)
    entry_email.grid(row=1, column=1)
    lbl_usuario_cd.grid(row=2, column=0, sticky="w", pady=5)
    entry_usuario_cd.grid(row=2, column=1)
    lbl_senha_cd.grid(row=3, column=0, sticky="w", pady=5)
    entry_senha_cd.grid(row=3, column=1)
    lbl_conf_senha.grid(row=4, column=0, sticky="w", pady=5)
    entry_conf_senha.grid(row=4, column=1)
    btn_cadastrar.grid(row=5, column=0, columnspan=2, pady=10)
    btn_voltar.grid(row=6, column=0, columnspan=2, pady=10)
    
    root.title("Cadastro SODGA")

# Criando janela principal
root = tk.Tk()
root.title("Login SODGA")
root.geometry("500x350")
root.resizable(False, False)

# Imagem para plano de fundo
fundo = Image.open("resources/img/wallpaper.png").resize((500, 350))
fundo = ImageTk.PhotoImage(fundo)
lbl_fundo = tk.Label(root, image=fundo)
lbl_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Criando frame
frame = ttk.Frame(root, padding=30)
frame.grid(row=0, column=0, padx=20, pady=30)

# Campos da tela de login
lbl_usuario = ttk.Label(frame, text="Usuário: ")
entry_usuario = ttk.Entry(frame, width=25)
lbl_senha = ttk.Label(frame, text="Senha: ")
entry_senha = ttk.Entry(frame, width=25, show="*")

btn_login = ttk.Button(frame, text="Login", command=login)
btn_tela_cadastro = ttk.Button(frame, text="Criar Conta", command=mostrar_tela_cadastro)

# Campos da tela de cadastro
lbl_nome = ttk.Label(frame, text="Nome Completo:")
entry_nome = ttk.Entry(frame, width=25)
lbl_email = ttk.Label(frame, text="Email:")
entry_email = ttk.Entry(frame, width=25)
lbl_usuario_cd = ttk.Label(frame, text="Usuário:")
entry_usuario_cd = ttk.Entry(frame, width=25)
lbl_senha_cd = ttk.Label(frame, text="Senha:")
entry_senha_cd = ttk.Entry(frame, width=25, show="*")
lbl_conf_senha = ttk.Label(frame, text="Confirmar Senha:")
entry_conf_senha = ttk.Entry(frame, width=25, show="*")

btn_cadastrar = ttk.Button(frame, text="Cadastrar", command=cadastrar)
btn_voltar = ttk.Button(frame, text="Voltar", command=mostrar_tela_login)

# Exibir a tela de login inicialmente
mostrar_tela_login()

root.mainloop()
