import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas, Label, PhotoImage, BooleanVar
import json

# Arquivo para armazenar credenciais
CREDENTIALS_FILE = "credentials.json"

# Função para salvar credenciais
def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump({"username": username, "password": password}, file)

# Função para carregar credenciais
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Função de validação de login
def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "admin" and password == "1234":
        print("Login bem-sucedido!")
        if remember_me_var.get():
            save_credentials(username, password)
    else:
        print("Usuário ou senha incorretos!")

# Função para criar uma nova conta
def create_account():
    print("Criar conta clicado!")

# Configuração da janela principal
root = ttk.Window(themename="flatly")
root.title("SODGA")
root.geometry("1800x1000")

# Adicionando imagem de fundo
bg_image = PhotoImage(file="resources/img/Home.png")
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Frame do login
login_frame = Canvas(root, bg="#d4e4f7", highlightthickness=500)
login_frame.place(relx=0.1, rely=0.6, anchor="w", width=600, height=400)

# Label de login
login_label = ttk.Label(login_frame, text="Login", font=("TT Norms", 30, "bold"), bootstyle="success")
login_label.place(relx=0.5, rely=0.1, anchor="center")

# Entrada para o nome de usuário
username_label = ttk.Label(login_frame, text="Email:", font=("TT Norms", 16), bootstyle="success")
username_label.place(relx=0.1, rely=0.25, anchor="w")
username_entry = ttk.Entry(login_frame, font=("Helvetica", 14))
username_entry.place(relx=0.1, rely=0.35, relwidth=0.8, height=50)

# Entrada para a senha
password_label = ttk.Label(login_frame, text="Senha:", font=("TT Norms", 16), bootstyle="success")
password_label.place(relx=0.1, rely=0.55, anchor="w")
password_entry = ttk.Entry(login_frame, font=("Helvetica", 14), show="*")
password_entry.place(relx=0.1, rely=0.65, relwidth=0.8, height=50)

# Checkbox para lembrar login
remember_me_var = BooleanVar()
remember_me_checkbox = ttk.Checkbutton(login_frame, text="Lembrar login", bootstyle="success-round-toggle", variable=remember_me_var)
remember_me_checkbox.place(relx=0.1, rely=0.83, anchor="w")

# Botões de acesso e criação de conta
access_button = ttk.Button(login_frame, text="Acessar", bootstyle="success", command=validate_login)
access_button.place(relx=0.3, rely=0.92, anchor="center", width=100, height=30)

create_account_button = ttk.Button(login_frame, text="Criar Conta", bootstyle="info", command=create_account)
create_account_button.place(relx=0.6, rely=0.92, anchor="center", width=100, height=30)

# Carregar credenciais salvas
dados = load_credentials()
if "username" in dados and "password" in dados:
    username_entry.insert(0, dados["username"])
    password_entry.insert(0, dados["password"])
    remember_me_var.set(True)

# Executa a aplicação
root.mainloop()