import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import Canvas, Label  # Importar Label do tkinter

# Função de validação de login (exemplo simples)
def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "admin" and password == "1234":
        print("Login bem-sucedido!")
    else:
        print("Usuário ou senha incorretos!")

# Função para criar uma nova conta (exemplo simples)
def create_account():
    print("Criar conta clicado!")  # Placeholder para a funcionalidade de criar conta

# Função para criar bordas arredondadas em um Canvas
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Configuração da janela principal
root = ttk.Window(themename="flatly")
root.title("SODGA")
root.geometry("900x500")
root.configure(bg='#d4e4f7')

# Frame principal para alinhar os elementos (agora à esquerda)
main_frame = ttk.Frame(root, bootstyle="light")
main_frame.place(relx=0, rely=0.5, anchor="w", relwidth=0.5, relheight=0.8)  # Alinhado à esquerda

# Título (centralizado horizontalmente no espaço à esquerda)
title_label = Label(main_frame, text="SODGA", font=("Helvetica", 20, "bold"), fg="black", bg="#d4e4f7")
title_label.pack(anchor="center", pady=(20, 0))  # Centralizado horizontalmente

# Subtítulo (centralizado horizontalmente no espaço à esquerda)
subtitle_label = Label(main_frame, text="Software desenvolvido para Gestão Acadêmica", 
                       font=("Helvetica", 16), fg="black", bg="#d4e4f7")
subtitle_label.pack(anchor="center", pady=10)  # Centralizado horizontalmente

# Frame do login (com bordas arredondadas)
login_frame = Canvas(main_frame, bg="#d4e4f7", highlightthickness=0)
login_frame.pack(anchor="center", padx=20, pady=20)  # Centralizado no espaço à esquerda
create_rounded_rectangle(login_frame, 0, 0, 400, 300, radius=20, fill="#ffffff", outline="#ccc")  # Ajustei o tamanho do frame
login_frame.config(width=400, height=300)

# Label de login
login_label = ttk.Label(login_frame, text="Login", font=("Helvetica", 16, "bold"), bootstyle="success")
login_label.place(relx=0.5, rely=0.1, anchor="center")  # Centralizado horizontalmente

# Label e entrada para o nome de usuário (com bordas arredondadas)
username_label = ttk.Label(login_frame, text="Usuário:", font=("Helvetica", 14), bootstyle="success")
username_label.place(relx=0.1, rely=0.25, anchor="w")  # Alinhado à esquerda
username_entry = ttk.Entry(login_frame, font=("Helvetica", 14))
username_entry.place(relx=0.1, rely=0.35, relwidth=0.8, height=35)  # Aumentei a altura da entrada

# Label e entrada para a senha (com bordas arredondadas)
password_label = ttk.Label(login_frame, text="Senha:", font=("Helvetica", 14), bootstyle="success")
password_label.place(relx=0.1, rely=0.55, anchor="w")  # Alinhado à esquerda
password_entry = ttk.Entry(login_frame, font=("Helvetica", 14), show="*")
password_entry.place(relx=0.1, rely=0.65, relwidth=0.8, height=35)  # Aumentei a altura da entrada

# Botão de acesso (com bordas arredondadas) - Tamanho reduzido
access_button = ttk.Button(login_frame, text="Acessar", bootstyle="success", command=validate_login)
access_button.place(relx=0.3, rely=0.85, anchor="center", width=100, height=30)  # Posicionado à esquerda

# Botão "Criar Conta" (com bordas arredondadas) - Tamanho reduzido
create_account_button = ttk.Button(login_frame, text="Criar Conta", bootstyle="info", command=create_account)
create_account_button.place(relx=0.6, rely=0.85, anchor="center", width=100, height=30)  # Posicionado à esquerda

# Executa a aplicação
root.mainloop()