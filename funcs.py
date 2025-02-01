import json
import os
import re

DATABASE_PATH = "database/alunos/"

def validar_email(email):
    """Valida se o email tem um formato correto."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def cadastrar_usuario(dados):
    """Cadastra um novo usuário se o email não existir e as senhas coincidirem."""
    email = dados["cadastro"]["email"]
    senha = dados["cadastro"]["senha"]

    # Verificar se algum campo está vazio
    if not email or not senha or not dados["cadastro"]["nome"]:
        return "Preencha todos os campos!"

    # Validar formato do email
    if not validar_email(email):
        return "Email inválido!"

    # Verificar se usuário já existe
    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")
    if os.path.exists(caminho_arquivo):
        return "Usuário já cadastrado!"

    # Criar o arquivo JSON para o usuário
    os.makedirs(DATABASE_PATH, exist_ok=True)
    with open(caminho_arquivo, "w") as arquivo:
        json.dump(dados, arquivo, indent=4)

    return True  # Sucesso

def login_usuario(credenciais):
    """Verifica se o email e a senha estão corretos."""
    email = credenciais["email"]
    senha = credenciais["senha"]

    caminho_arquivo = os.path.join(DATABASE_PATH, f"{email}.json")

    if not os.path.exists(caminho_arquivo):
        return "Usuário não encontrado!"

    # Abrir o arquivo JSON do usuário
    with open(caminho_arquivo, "r") as arquivo:
        dados = json.load(arquivo)

    # Verificar se a senha está correta
    if dados["cadastro"]["senha"] != senha:
        return "Senha incorreta!"

    return True  # Sucesso
