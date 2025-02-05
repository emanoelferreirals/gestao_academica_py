# funcs.py
import json
import os
import re
import subprocess
import tkinter as tk
import ttkbootstrap as tb


DATABASE_PATH = "database/alunos/"
TEMP_LOG_PATH = "temp/log.json"

def acessar_lista(name_lista):
    aluno = ler_login()["email"]

    with open(f"{DATABASE_PATH}{aluno}.json","r") as ls:
        lista = json.load(ls)

        if name_lista != "Periodos" and name_lista != "Materias": 
            return []
        
        return lista["listas"][name_lista]

# Função que será chamada para apagar os dados de login e fechar a janela
def on_close(root):
    apagar_login()  # Apagar os dados de login
    root.destroy()  # Fechar a janela

# Função para salvar os dados de login
def salvar_login(nome, email):
    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    login_data = {
        'nome': nome,
        'email': email
    }

    with open(TEMP_LOG_PATH, 'w') as f:
        json.dump(login_data, f)

def ler_login():
    try:
        with open(TEMP_LOG_PATH, 'r') as f:
            login_data = json.load(f)
        return login_data
    except FileNotFoundError:
        return None

def apagar_login():
    try:
        os.remove(TEMP_LOG_PATH)
    except FileNotFoundError:
        pass  # Se o arquivo não existir, não faz nada

# Função para abrir a tela de notas
def abrir_tela_notas(tela_atual, tela):
    tela_atual.destroy()  # Fecha a janela atual
    subprocess.run(["python", tela])  # Executa o outro arquivo

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def cadastrar_usuario(dados):
    email = dados["cadastro"]["email"]
    senha = dados["cadastro"]["senha"]

    if not email or not senha or not dados["cadastro"]["nome"]:
        return "Preencha todos os campos!"

    if not validar_email(email):
        return "Email inválido!"

    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")
    if os.path.exists(caminho_arquivo):
        return "Usuário já cadastrado!"

    os.makedirs(DATABASE_PATH, exist_ok=True)
    with open(caminho_arquivo, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

    return True

def login_usuario(credenciais):
    email = credenciais["email"]
    senha = credenciais["senha"]

    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")

    if not os.path.exists(caminho_arquivo):
        return "Usuário não encontrado!"

    with open(caminho_arquivo, "r") as arquivo:
        dados = json.load(arquivo)

    if dados["cadastro"]["senha"] != senha:
        return "Senha incorreta!"

    salvar_login(dados["cadastro"]["nome"], email)

    return True

# Função para carregar os dados do arquivo JSON
ARQUIVO_DADOS = "database/alunos/aluno.json"

def carregar_dados():
    login_data = ler_login()
    if not login_data:
        return []

    email = login_data["email"]
    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as f:
            try:
                dados_usuario = json.load(f)
                return dados_usuario.get("dados_academicos", [])
            except json.JSONDecodeError:
                return []
    return []


def salvar_dados(novos_dados):
    login_data = ler_login()
    if not login_data:
        return

    email = login_data["email"]
    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")

    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as f:
            dados_usuario = json.load(f)

        # Atualizando os dados acadêmicos do usuário
        dados_usuario["dados_academicos"] = novos_dados

        with open(caminho_arquivo, "w") as f:
            json.dump(dados_usuario, f, indent=4)



"""# Exemplo de criação de janela
def criar_janela():
    root = tb.Window(themename="minty")
    root.title("Menu com Imagens")
    root.geometry("900x500")

    # Definindo a função on_close para ser chamada ao fechar a janela
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))  # Chamando a função on_close ao fechar a janela

    root.mainloop()

if __name__ == "__main__":
    criar_janela()"""
