import json
import os
import re
import subprocess
import tkinter as tk
import ttkbootstrap as tb

TEMP_LOG_PATH = "temp/log.json"
DATA_PATH = "data/alunos/"

def ler_login():
    try:
        with open(TEMP_LOG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def acessar_bd(oper, local, dados=None):
    if oper == "r":
        try:
            with open(local, "r", encoding="UTF-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    elif oper == "w" and dados is not None:
        with open(local, "w", encoding="UTF-8") as file:
            json.dump(dados, file, indent=4)
        return "Sucesso"
    return "Erro"

def acessar_bd(modo, caminho, dados=None):
    if modo == "r":
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    elif modo == "w":
        os.makedirs(os.path.dirname(caminho), exist_ok=True)  # Garante que o diretório exista
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

def ler_login():
    return {"email": "emanoel@gmail.com"}  # Simulação de login

def gerar_novo_id(materias):
    if not materias:
        return 1
    return max(map(int, materias.keys())) + 1

def salvar_materia(nome, descricao, periodo, carga_horaria, conteudos, qtd_aulas, duracao_aulas_min, horario_aula, materia_id):
    usuario = ler_login()["email"]
    caminho_arquivo = os.path.join(DATA_PATH, usuario, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    
    if "dados_academicos" not in banco:
        banco["dados_academicos"] = {}
    if "materias" not in banco["dados_academicos"]:
        banco["dados_academicos"]["materias"] = {}
    
    materias = banco["dados_academicos"]["materias"]
    
    # Verifica se a matéria já existe pelo id, Se a matéria for nova, cria um novo ID
    if materia_id == None:
        materia_id = str(gerar_novo_id(materias))
    
    # Salva/atualiza os dados da matéria
    materias[materia_id] = {
        "nome": nome,
        "descricao": descricao,
        "periodo": periodo,
        "carga_horaria": carga_horaria,
        "qtd_aulas": qtd_aulas,
        "duracao_aulas_min": duracao_aulas_min,
        "horario_aula": horario_aula,
        "conteudos": conteudos
    }
    
    banco["dados_academicos"]["materias"] = materias
    acessar_bd("w", caminho_arquivo, banco)
    print(f"Matéria '{nome}' salva com sucesso!")


def acessar_lista(name_lista):
    usuario = ler_login()["email"]
    caminho_arquivo = os.path.join(DATA_PATH, usuario, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    return banco.get(name_lista, [])

def on_close(root):
    apagar_login()
    root.destroy()

def salvar_login(nome, email):
    os.makedirs('temp', exist_ok=True)
    login_data = {'nome': nome, 'email': email}
    with open(TEMP_LOG_PATH, 'w') as f:
        json.dump(login_data, f)

def apagar_login():
    try:
        os.remove(TEMP_LOG_PATH)
    except FileNotFoundError:
        pass

def abrir_nova_tela(tela_atual, tela,destroy_atual):
    if destroy_atual:
        tela_atual.destroy()
    subprocess.run(["python", tela])

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def cadastrar_usuario(dados):
    email = dados["cadastro"]["email"]
    senha = dados["cadastro"]["senha"]
    if not email or not senha or not dados["cadastro"].get("nome"):
        return "Preencha todos os campos!"
    if not validar_email(email):
        return "Email inválido!"
    caminho_arquivo = os.path.join(DATA_PATH, email, "notas.json")
    if os.path.exists(caminho_arquivo):
        return "Usuário já cadastrado!"
    os.makedirs(os.path.join(DATA_PATH, email), exist_ok=True)
    acessar_bd("w", caminho_arquivo, dados)
    return True

def login_usuario(credenciais):
    email = credenciais["email"]
    senha = credenciais["senha"]
    caminho_arquivo = os.path.join(DATA_PATH, email, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    if not banco:
        return "Usuário não encontrado!"
    if banco.get("cadastro", {}).get("senha") != senha:
        return "Senha incorreta!"
    salvar_login(banco["cadastro"]["nome"], email)
    return True

def carregar_dados():
    usuario = ler_login()
    if not usuario:
        return {}
    caminho_arquivo = os.path.join(DATA_PATH, usuario["email"], "notas.json")
    return acessar_bd("r", caminho_arquivo).get("registro_notas", {})

def salvar_dados(novos_dados):
    usuario = ler_login()
    if not usuario:
        return
    caminho_arquivo = os.path.join(DATA_PATH, usuario["email"], "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    banco["registro_notas"] = novos_dados
    acessar_bd("w", caminho_arquivo, banco)
