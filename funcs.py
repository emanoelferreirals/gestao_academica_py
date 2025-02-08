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

def salvar_dados_academicos(curso, instituicao, qtd_periodos, notas_bimestre, qtd_notas_periodo, carga_horaria):
    dados = {
        "curso": curso,
        "instituicao": instituicao,
        "qtd_periodos": qtd_periodos,
        "notas_bimestre": notas_bimestre,
        "qtd_notas_periodo": qtd_notas_periodo,  # Corrigido o erro de digitação
        "carga_horaria": carga_horaria,
        "materias": []  # Garante que a estrutura base já tenha uma lista de matérias
    }
    
    usuario = ler_login()["email"]
    caminho_arquivo = os.path.join(DATA_PATH, usuario, "notas.json")
    
    banco = acessar_bd("r", caminho_arquivo)
    banco["dados_academicos"] = dados  # Substitui/Cria os dados acadêmicos corretamente
    
    acessar_bd("w", caminho_arquivo, banco)
    print("Dados acadêmicos salvos com sucesso!")

def salvar_materia(nome, descricao, periodo, carga_horaria, conteudos, qtd_aulas, duracao_aulas_min, horario_aula):
    dados = {
        "nome": nome,  # Adicionando nome na estrutura para facilitar busca
        "descricao": descricao,
        "periodo": periodo,
        "carga_horaria": carga_horaria,
        "qtd_aulas": qtd_aulas,  
        "duracao_aulas_min": duracao_aulas_min,
        "horario_aula": horario_aula,  # Lista de horários
        "conteudos": conteudos  # Lista de conteúdos
    }
    
    usuario = ler_login()["email"]
    caminho_arquivo = os.path.join(DATA_PATH, usuario, "notas.json")
    
    banco = acessar_bd("r", caminho_arquivo)
    
    # Garante que "dados_academicos" e "materias" existem
    if not isinstance(banco, dict):
        banco = {}
    if "dados_academicos" not in banco or not isinstance(banco["dados_academicos"], dict):
        banco["dados_academicos"] = {}
    if "materias" not in banco["dados_academicos"] or not isinstance(banco["dados_academicos"]["materias"], dict):
        banco["dados_academicos"]["materias"] = {}

    materias = banco["dados_academicos"]["materias"]

    # Atualiza ou adiciona a matéria
    materias[nome] = dados
    
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
