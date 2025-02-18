import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas, Label, PhotoImage, BooleanVar, StringVar
import json
from renderizer.centralizar_janela import centralizar_janela
from funcs import cadastrar_usuario,login_usuario,abrir_nova_tela

# Arquivo para armazenar credenciais
CREDENTIALS_FILE = "data/credentials.json"

# Função para salvar credenciais
def salvar_login(usuario, senha):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump({"usuario": usuario, "senha": senha}, file)

# Função para carregar credenciais
def carregar_dados_login():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Função de validação de login
def verificar_login(usuario_var, senha_var, remember_var, mensagem_var, mensagem_label):
    # Limpar mensagem anterior
    limpar_mensagem(mensagem_label)

    usuario = usuario_var.get()
    senha = senha_var.get()

    if login_usuario(usuario,senha) == True:
        set_mensagem("Login bem-sucedido!", "success", mensagem_var, mensagem_label)
        if remember_var.get():
            salvar_login(usuario, senha)
        abrir_nova_tela(root, "menu_tela.py",True)
    else:
        set_mensagem("Usuário ou senha incorretos!", "danger", mensagem_var, mensagem_label)

# Função para criar uma nova conta
def cadastrar_usuario(nome_var, email_var, senha_var, confirm_senha_var, mensagem_var, mensagem_label):
    # Limpar mensagem anterior
    limpar_mensagem(mensagem_label)

    nome = nome_var.get()
    email = email_var.get()
    senha = senha_var.get()
    confirm_senha = confirm_senha_var.get()

    if not nome or not email or not senha or not confirm_senha:
        set_mensagem("Preencha todos os campos!", "danger", mensagem_var, mensagem_label)
        return
    if senha != confirm_senha:
        set_mensagem("As senhas não coincidem!", "danger", mensagem_var, mensagem_label)
        return
    
    mensagem = cadastrar_usuario(nome, email, senha)
    # set_mensagem(f"Conta criada para {nome} com email {email}.", "success", mensagem_var, mensagem_label)
    set_mensagem(mensagem, "success", mensagem_var, mensagem_label)

# Função para definir a mensagem e a cor do label de mensagem
def set_mensagem(mensagem, style, mensagem_var, mensagem_label):
    mensagem_var.set(mensagem)
    mensagem_label.config(bootstyle=style, width=40, wraplength=400)
    mensagem_label.pack(pady=(10, 0))

    # Ocultar a mensagem após 5 segundos
    mensagem_label.after(5000, lambda: limpar_mensagem(mensagem_label))

# Função para limpar a mensagem
def limpar_mensagem(mensagem_label):
    mensagem_label.pack_forget()

largura_janela = 1800
altura_janela =  980

# Criando a janela principal
root = ttk.Window(themename="flatly")
root.title("SODGA")
root.iconbitmap("resources/icones/logo_sodga.ico")  # Arquivo ICO
centralizar_janela(root, largura_janela, altura_janela)

# Adicionando imagem de fundo
bg_image = PhotoImage(file="resources/img/login_fundo.png")
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Variáveis para armazenar os dados dos campos
usuario_var = StringVar()
senha_var = StringVar()
remember_var = BooleanVar()

nome_var = StringVar()
email_var = StringVar()
confirm_senha_var = StringVar()

mensagem_var = StringVar()

def criar_frame():
    frame = Canvas(root, bg="#d4e4f7")
    frame.place(relx=0.4, rely=0.60, anchor="e", width=500, height=600) 
    return frame

# Criando a tela de login
def criar_tela_login():
    frame = criar_frame()

    ttk.Label(frame, text="Login", font=("TT Norms", 20, "bold"), bootstyle="success").pack(pady=(30,5))
    ttk.Label(frame, text="Email:", font=("Segoe UI", 11,"normal")).pack(anchor="w",fill="x", padx=50, pady=(10, 5))
    ttk.Entry(frame, textvariable=usuario_var,width=35, font=("Segoe UI", 11)).pack(padx=10, pady=(10, 5))

    ttk.Label(frame, text="Senha:", font=("Segoe UI", 11,"normal")).pack(anchor="w", fill="x", padx=50, pady=(25,0))
    ttk.Entry(frame, textvariable=senha_var,width=35, font=("Segoe UI", 11), show="*").pack(pady=(10,5))
    ttk.Checkbutton(frame, text="Lembrar login", bootstyle="success-round-toggle", variable=remember_var).pack(anchor="w", padx=67,pady=(25,20))

    ttk.Button(frame, text="Acessar", bootstyle="success", width=40, command=lambda: verificar_login(usuario_var, senha_var, remember_var, mensagem_var, mensagem_label)).pack(pady=10)
    ttk.Button(frame, text="Criar Conta", bootstyle="info",  width=40, command=criar_tela_cadastro).pack()

    # Label para exibir mensagens
    mensagem_label = ttk.Label(frame, textvariable=mensagem_var, font=("Segoe UI", 11, "normal"), width=40, wraplength=400,anchor="center")

# Criando a tela de cadastro
def criar_tela_cadastro():
    frame = criar_frame()

    ttk.Label(frame, text="Cadastro", font=("TT Norms", 20, "bold"), bootstyle="info").pack(pady=(30,5))
    ttk.Label(frame, text="Nome Completo:", font=("Segoe UI", 11,"normal")).pack(anchor="w",fill="x", padx=50, pady=(10, 5))
    ttk.Entry(frame, textvariable=nome_var,width=35, font=("Segoe UI", 11)).pack(padx=10, pady=(5, 5))

    ttk.Label(frame, text="Email:", font=("Segoe UI", 11,"normal")).pack(anchor="w",fill="x", padx=50, pady=(10,0))
    ttk.Entry(frame, textvariable=email_var,width=35, font=("Segoe UI", 11)).pack(padx=5, pady=(5, 5))

    ttk.Label(frame, text="Senha:", font=("Segoe UI", 11,"normal")).pack(anchor="w",fill="x", padx=50, pady=(10,0))
    ttk.Entry(frame, textvariable=senha_var,width=35, font=("Segoe UI", 11), show="*").pack(padx=5, pady=(5, 5))

    ttk.Label(frame, text="Confirmar Senha:", font=("Segoe UI", 11,"normal")).pack(anchor="w",fill="x", padx=50, pady=(10,0))
    ttk.Entry(frame, textvariable=confirm_senha_var,width=35, font=("Segoe UI", 11), show="*").pack(padx=10, pady=(5, 0))

    ttk.Button(frame, text="Cadastrar", bootstyle="success", width=40, command=lambda: cadastrar_usuario(nome_var, email_var, senha_var, confirm_senha_var, mensagem_var, mensagem_label)).pack(pady=(30,5))
    ttk.Button(frame, text="Voltar", bootstyle="danger", width=40, command=criar_tela_login).pack()

    # Label para exibir mensagens
    mensagem_label = ttk.Label(frame, textvariable=mensagem_var, font=("Segoe UI", 11, "normal"), width=40, wraplength=400, anchor="center")

# Carregar credenciais salvas
dados = carregar_dados_login()
if "usuario" in dados and "senha" in dados:
    usuario_var.set(dados["usuario"])
    senha_var.set(dados["senha"])
    remember_var.set(True)

# Exibir tela inicial
criar_tela_login()

# Executa a aplicação
root.mainloop()