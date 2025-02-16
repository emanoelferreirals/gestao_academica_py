import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import messagebox
from funcs import cadastrar_usuario, login_usuario, abrir_nova_tela, on_close


def fazer_login():
    email = campos['email'].get().strip()
    senha = campos['senha'].get().strip()
    if not email or not senha:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return
    resultado = login_usuario({"email": email, "senha": senha})
    if resultado is True:
        abrir_nova_tela(root, "menu_tela.py", True)
    else:
        messagebox.showerror("Erro", resultado)


def fazer_cadastro():
    nome = campos['nome'].get().strip()
    email = campos['email_cd'].get().strip()
    senha = campos['senha_cd'].get().strip()
    confirmar_senha = campos['conf_senha'].get().strip()
    if not nome or not email or not senha or not confirmar_senha:
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return
    if senha != confirmar_senha:
        messagebox.showerror("Erro", "As senhas não coincidem!")
        return
    resultado = cadastrar_usuario({"cadastro": {"nome": nome, "email": email, "senha": senha}})
    if resultado is True:
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        mostrar_tela('login')
    else:
        messagebox.showerror("Erro", resultado)


def mostrar_tela(tela):
    for widget in frame.winfo_children():
        widget.grid_forget()
    for nome, config in telas[tela].items():
        config.grid(row=config.grid_info()['row'], column=config.grid_info()['column'], columnspan=1, pady=5, sticky="w")
    root.title(tela.replace('_', ' ').title() + " SODGA")


# Configurações da Janela
style = Style(theme="darkly")
root = style.master
root.title("Login SODGA")
root.geometry("600x350")
root.resizable(False, False)

# Frame principal
frame = ttk.Frame(root, padding=30)
frame.pack(pady=50)

# Campos de entrada
campos = {
    'email': ttk.Entry(frame, width=25),
    'senha': ttk.Entry(frame, width=25, show="*"),
    'nome': ttk.Entry(frame, width=25),
    'email_cd': ttk.Entry(frame, width=25),
    'senha_cd': ttk.Entry(frame, width=25, show="*"),
    'conf_senha': ttk.Entry(frame, width=25, show="*"),
}

# Telas
telas = {
    'login': {
        ttk.Label(frame, text="Email:").grid(row=0, column=0),
        campos['email'].grid(row=0, column=1),
        ttk.Label(frame, text="Senha:").grid(row=1, column=0),
        campos['senha'].grid(row=1, column=1),
        ttk.Button(frame, text="Login", command=fazer_login, bootstyle="success").grid(row=2, column=0, columnspan=2),
        ttk.Button(frame, text="Criar Conta", command=lambda: mostrar_tela('cadastro'), bootstyle="info").grid(row=3, column=0, columnspan=2),
    },
    'cadastro': {
        ttk.Label(frame, text="Nome Completo:").grid(row=0, column=0),
        campos['nome'].grid(row=0, column=1),
        ttk.Label(frame, text="Email:").grid(row=1, column=0),
        campos['email_cd'].grid(row=1, column=1),
        ttk.Label(frame, text="Senha:").grid(row=2, column=0),
        campos['senha_cd'].grid(row=2, column=1),
        ttk.Label(frame, text="Confirmar Senha:").grid(row=3, column=0),
        campos['conf_senha'].grid(row=3, column=1),
        ttk.Button(frame, text="Cadastrar", command=fazer_cadastro, bootstyle="success").grid(row=4, column=1),
        ttk.Button(frame, text="Voltar", command=lambda: mostrar_tela('login'), bootstyle="danger").grid(row=4, column=0),
    }
}

# Exibir a tela inicial
mostrar_tela('login')

# Vincular a função de fechamento
ttk.protocol(root, "WM_DELETE_WINDOW", lambda: on_close(root))
root.mainloop()
