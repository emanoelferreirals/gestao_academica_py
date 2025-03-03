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
        return {"email": None}

login_data = ler_login()
USUARIO = login_data.get("email")

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

def gerar_novo_id(materias):
    lista_ids = [int(k) for k in materias.keys() if k.strip().isdigit()]
    print("Lista de IDs extraídos:", lista_ids)
    return max(lista_ids, default=0) + 1

def salvar_materia(nome, descricao, periodo, carga_horaria, conteudos, qtd_aulas, duracao_aulas_min, horario_aula, materia_id):
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    
    if "dados_academicos" not in banco:
        banco["dados_academicos"] = {}
    if "materias" not in banco["dados_academicos"]:
        banco["dados_academicos"]["materias"] = {}
    
    materias = banco["dados_academicos"]["materias"]
    print("keysss:", materias.keys())
    
    if not materia_id:  
        materia_id = str(gerar_novo_id(materias))

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

def salvar_dados_academicos(curso, instituicao, qtd_periodos, notas_bimestre, qtd_notas_periodo, carga_horaria):
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    
    if "dados_academicos" not in banco:
        banco["dados_academicos"] = {}
    
    dados_academicos = {
        "curso": curso,
        "instituicao": instituicao,
        "qtd_periodos": qtd_periodos,
        "notas_bimestre": notas_bimestre,
        "qtd_notas_periodo": qtd_notas_periodo,
        "carga_horaria": carga_horaria,
    }
    
    banco["dados_academicos"] = dados_academicos
    acessar_bd("w", caminho_arquivo, banco)
    print(banco)

def acessar_lista(name_lista):
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    return banco.get(name_lista, [])

def on_close(root):
    apagar_login()
    root.destroy()

def iniciar_sessao(nome, email):
    os.makedirs('temp', exist_ok=True)
    login_data = {'nome': nome, 'email': email}
    with open(TEMP_LOG_PATH, 'w') as f:
        json.dump(login_data, f)
    print("ssss")

def apagar_login():
    try:
        os.remove(TEMP_LOG_PATH)
    except FileNotFoundError:
        pass

def abrir_nova_tela(tela_atual, tela, destroy_atual):
    if destroy_atual:
        tela_atual.destroy()
    subprocess.run(["python", tela])

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def cadastrar_usuario(nome, email, senha):
    dados = {
        "cadastro": {
            "nome": nome,
            "email": email,
            "senha": senha
        }   
    }
    if not validar_email(email):
        return "Email inválido!"
    caminho_arquivo = os.path.join(DATA_PATH, email, "notas.json")
    if os.path.exists(caminho_arquivo):
        return "Usuário já cadastrado!"
    os.makedirs(os.path.join(DATA_PATH, email), exist_ok=True)
    acessar_bd("w", caminho_arquivo, dados)
    return "Usuário Cadastrado com Sucesso!"

def login_usuario(email, senha):
    caminho_arquivo = os.path.join(DATA_PATH, email, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    if not banco:
        return "Usuário não encontrado!"
    if banco.get("cadastro", {}).get("senha") != senha:
        return "Senha incorreta!"
    iniciar_sessao(banco["cadastro"]["nome"], email)
    global USUARIO
    USUARIO = email  # Atualiza a variável global USUARIO
    return True

def carregar_dados():
    usuario = ler_login().get("email")
    if not usuario:
        return {}
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
    return acessar_bd("r", caminho_arquivo).get("registro_notas", {})

def salvar_dados(novos_dados):
    usuario = ler_login().get("email")
    if not usuario:
        return
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    banco["registro_notas"] = novos_dados
    acessar_bd("w", caminho_arquivo, banco)

def carregar_materias_registradas():
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
    dados = acessar_bd("r", caminho_arquivo)
    if isinstance(dados, dict):
        materias_registradas = dados.get("dados_academicos", {}).get("materias", {})
    else:
        materias_registradas = {}
    print(materias_registradas)
    return materias_registradas

def carregar_lista_materias():
    materias = carregar_materias_registradas()
    nomes_materias = []
    for id_materia, dados_materia in materias.items():
        nomes_materias.append(dados_materia["nome"])
        print("Opções: ", nomes_materias)
    return nomes_materias

def carregar_periodos():
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
    dados = acessar_bd("r", caminho_arquivo)
    periodos = []
    qtd_periodos = dados.get("dados_academicos", {}).get("qtd_periodos", {})
    if int(qtd_periodos) == 0:
        periodos = ["1", "2", "3", "4", "5", "6", "7", "8"]
    else:
        for i in range(1, qtd_periodos + 1):
            periodos.append(f"{i}")
    print(periodos)
    return periodos