import json
import os
import re
import subprocess

DATABASE_PATH = "database/alunos/"

"""-------------------------FUNÇÕES DE LOGIN / CADASTRO -------------------------"""

# Função para abrir a tela de notas
def abrir_tela_notas(tela_atual,tela):
    tela_atual.destroy()  # Fecha a janela atual
    subprocess.run(["python", tela])  # Executa o outro arquivo

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


"""--------------------------FUNÇÕES DE NOTAS -------------------------------------"""

# Caminho do arquivo JSON
ARQUIVO_DADOS = "database/alunos/aluno.json"

# Função para carregar os dados do arquivo JSON
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):  # Verifica se o arquivo existe
        with open(ARQUIVO_DADOS, "r") as f:  # Abre o arquivo para leitura
            try:
                return json.load(f)  # Retorna os dados carregados
            except json.JSONDecodeError:
                return []  # Se houver erro na leitura, retorna uma lista vazia
    return []  # Se o arquivo não existir, retorna uma lista vazia

# Função para salvar os dados no arquivo JSON
def salvar_dados(novos_dados):
    # Ordena os dados pela segunda coluna (Período), garantindo que seja um número
    # novos_dados.sort(key=lambda x: int(x[1]) if x[1].isdigit() else 0)

    # Escreve os dados no arquivo JSON
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(novos_dados, f, indent=4)  # Salva os dados com indentação para melhor legibilidade
