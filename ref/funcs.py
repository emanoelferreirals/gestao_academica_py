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

USUARIO = ler_login()

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
    # Filtra chaves que são numéricas e não estão vazias
    # O método .keys() retorna todas as chaves do dicionário materias.
    # O if k.strip().isdigit() garante que só IDs numéricos sejam convertidos para int.
    lista_ids = [int(k) for k in materias.keys() if k.strip().isdigit()]

    # Exibe a lista de IDs extraídos para depuração
    print("Lista de IDs extraídos:", lista_ids)

    # Retorna o maior ID encontrado +1 (para gerar um novo ID único)
    # Se lista_ids estiver vazia, max([], default=0) retorna 0, então o novo ID será 1.
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
    
    # Verifica se a matéria já existe pelo id, Se a matéria for nova, cria um novo ID
    if not materia_id:  
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
     
    caminho_arquivo = os.path.join(DATA_PATH, USUARIO, "notas.json")
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
    caminho_arquivo = os.path.join(DATA_PATH,  USUARIO, "notas.json")
    return acessar_bd("r", caminho_arquivo).get("registro_notas", {})

def salvar_dados(novos_dados):
    usuario = ler_login()
    if not usuario:
        return
    caminho_arquivo = os.path.join(DATA_PATH,  USUARIO, "notas.json")
    banco = acessar_bd("r", caminho_arquivo)
    banco["registro_notas"] = novos_dados
    acessar_bd("w", caminho_arquivo, banco)

def carregar_materias_registradas():
    """ Carrega a lista de matérias cadastradas. """
    global materias_registradas
    
    caminho_arquivo = os.path.join(DATA_PATH,  USUARIO, "notas.json")
    dados = acessar_bd("r", caminho_arquivo)
    if isinstance(dados, dict):
        materias_registradas = dados.get("dados_academicos", {}).get("materias", {})
    else:
        materias_registradas = {}

    print("materias_registradas: ",materias_registradas)

    opcoes = []
    for id_materia, dados_materia in materias_registradas.items():
        opcoes.append(dados_materia["nome"])  # Agora adiciona o nome da matéria corretamente
        print("Opções: ",opcoes)
    return opcoes
