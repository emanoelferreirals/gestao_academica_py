# funcs.py
import json
import os
import re
import subprocess
import tkinter as tk
import ttkbootstrap as tb

DATABASE_PATH = "database/alunos/"
TEMP_LOG_PATH = "temp/log.json"

def salvar_materia(nome, descricao, conteudos, periodo):
    dados = {
        "Nome": nome,
        "Descricao": descricao,
        "Conteudo": conteudos,
        "Periodo": periodo
    }

    usuario = ler_login()["email"]
    caminho_arquivo = os.path.join(DATABASE_PATH, f"{usuario}.json")
    
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            banco = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        banco = {"dados_academicos": {"Materias": []}}
    
    banco["dados_academicos"].setdefault("Materias", []).append(dados)
    
    with open(caminho_arquivo, "w", encoding="utf-8") as file:
        json.dump(banco, file, indent=4, ensure_ascii=False)
    
    print("Matéria salva com sucesso!")

def acessar_lista(name_lista):
    aluno = ler_login()["email"]
    caminho_arquivo = os.path.join(DATABASE_PATH, f"{aluno}.json")
    
    try:
        with open(caminho_arquivo, "r") as ls:
            lista = json.load(ls)
            return lista["dados_academicos"].get(name_lista, [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def on_close(root):
    apagar_login()
    root.destroy()

def salvar_login(nome, email):
    os.makedirs('temp', exist_ok=True)
    login_data = {'nome': nome, 'email': email}
    with open(TEMP_LOG_PATH, 'w') as f:
        json.dump(login_data, f)

def ler_login():
    try:
        with open(TEMP_LOG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def apagar_login():
    try:
        os.remove(TEMP_LOG_PATH)
    except FileNotFoundError:
        pass

def abrir_nova_tela(tela_atual, tela):
    tela_atual.destroy()
    subprocess.run(["python", tela])

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\\.[^@]+", email)

def cadastrar_usuario(dados):
    email = dados["cadastro"]["email"]
    senha = dados["cadastro"]["senha"]

    if not email or not senha or not dados["cadastro"].get("nome"):
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

def carregar_dados():
    login_data = ler_login()
    if not login_data:
        return {}

    email = login_data["email"]
    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")

    try:
        with open(caminho_arquivo, "r") as f:
            return json.load(f).get("dados_academicos", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_dados(novos_dados):
    login_data = ler_login()
    if not login_data:
        return

    email = login_data["email"]
    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")

    try:
        with open(caminho_arquivo, "r") as f:
            dados_usuario = json.load(f)
        dados_usuario["dados_academicos"] = novos_dados
        with open(caminho_arquivo, "w") as f:
            json.dump(dados_usuario, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
