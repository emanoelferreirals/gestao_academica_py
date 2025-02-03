# Importando as bibliotecas necessárias
import json  # Biblioteca para manipulação de dados no formato JSON
import ttkbootstrap as ttk  # Biblioteca para interfaces gráficas com estilo moderno
from ttkbootstrap import Style  # Para definir o estilo da interface
from ttkbootstrap.constants import *  # Importa as constantes de estilo do ttkbootstrap
import tkinter as tk  # Biblioteca Tkinter para criação de interfaces gráficas
from tkinter import messagebox  # Importa o messagebox para exibição de mensagens de alerta
import os  # Biblioteca para manipulação de caminhos e arquivos no sistema operacional

# Configurações da Janela
largura_tela, altura_tela = 900, 500  # Define a largura e altura da janela da aplicação
style = Style(theme="minty")  # Define o estilo da interface com o tema 'minty'
root = style.master  # Acessa a janela principal com o tema aplicado
root.title("Notas")  # Define o título da janela
root.geometry(f"{largura_tela}x{altura_tela}")  # Define as dimensões da janela de acordo com as variáveis
root.resizable(False, False)  # Impede que a janela seja redimensionada

# Caminho do arquivo de dados (JSON)
arquivo_dados = "database/alunos/aluno.json"  # Define o caminho do arquivo onde os dados dos alunos serão armazenados

# Função para carregar os dados do arquivo JSON
def carregar_dados():
    if os.path.exists(arquivo_dados):  # Verifica se o arquivo existe
        with open(arquivo_dados, "r") as f:  # Abre o arquivo para leitura
            try:
                return json.load(f)  # Tenta carregar os dados no formato JSON
            except json.JSONDecodeError:  # Se ocorrer um erro na leitura do JSON, retorna uma lista vazia
                return []  
    return []  # Se o arquivo não existir, retorna uma lista vazia

dados = carregar_dados()  # Carrega os dados no início da aplicação

# Função para salvar os dados no arquivo JSON
def salvar_dados():
    novos_dados = []  # Cria uma lista vazia para armazenar os novos dados coletados da tabela
    # Percorre as linhas da tabela (começando da linha 1)
    for row in range(1, len(frame_tabela.grid_slaves()) // len(titulos) + 1):
        linha = []  # Lista para armazenar os dados de uma linha
        # Percorre as colunas da tabela
        for col in range(len(titulos)):
            widget = frame_tabela.grid_slaves(row=row, column=col)  # Acessa o widget da célula
            if widget:  # Se o widget existir (campo preenchido)
                linha.append(widget[0].get())  # Adiciona o valor do campo à linha
        if linha:  # Se a linha contiver dados (não vazia)
            novos_dados.append(linha)  # Adiciona a linha à lista de novos dados
    # Ordena os dados pela segunda coluna (presumivelmente um valor numérico)
    novos_dados.sort(key=lambda x: int(x[1]) if x[1].isdigit() else 0)
    # Abre o arquivo para escrita e salva os novos dados no formato JSON
    with open(arquivo_dados, "w") as f:
        json.dump(novos_dados, f, indent=4)  # Salva os dados com indentação de 4 espaços
    atualizar_tabela(novos_dados)  # Atualiza a tabela com os novos dados
    btn_salvar.grid_remove()  # Remove o botão de salvar após a ação

# Função para detectar mudanças na tabela e exibir o botão de salvar
def detectar_mudanca(event):
    btn_salvar.grid(row=3, column=0, pady=10)  # Exibe o botão de salvar ao detectar uma mudança

# Função para adicionar uma nova linha na tabela
def adicionar_linha():
    row = len(frame_tabela.grid_slaves()) // len(titulos) + 1  # Calcula a próxima linha disponível
    criar_linha(row)  # Cria a nova linha
    btn_salvar.grid(row=3, column=0, pady=10)  # Exibe o botão de salvar após adicionar uma linha

# Função para criar uma linha na tabela
def criar_linha(row, valores=None):
    # Cria o campo para selecionar a matéria
    cmb_materia = ttk.Combobox(frame_tabela, values=materias, state="readonly", width=15)
    cmb_materia.grid(row=row, column=0, padx=5, pady=5)  # Posiciona o campo na tabela
    cmb_materia.bind("<<ComboboxSelected>>", detectar_mudanca)  # Detecta mudanças na seleção da matéria
    
    # Cria o campo para selecionar o período
    cmb_periodo = ttk.Combobox(frame_tabela, values=semestres, state="readonly", width=10)
    cmb_periodo.grid(row=row, column=1, padx=5, pady=5)  # Posiciona o campo na tabela
    cmb_periodo.bind("<<ComboboxSelected>>", detectar_mudanca)  # Detecta mudanças na seleção do período
    
    # Se a função foi chamada com valores específicos, define os valores padrões nos campos
    if valores:
        cmb_materia.set(valores[0])  # Define a matéria selecionada
        cmb_periodo.set(valores[1])  # Define o período selecionado
    
    # Cria os campos para as notas (n1, n2, n3, n4)
    for col in range(2, 6):  # Começa a partir da coluna 2 (onde as notas começam)
        entry = ttk.Entry(frame_tabela, width=5)  # Cria um campo de entrada para a nota
        entry.grid(row=row, column=col, padx=5, pady=5)  # Posiciona o campo na tabela
        entry.bind("<KeyRelease>", detectar_mudanca)  # Detecta quando uma tecla for pressionada (alteração)
        if valores:  # Se houver valores passados, insere-os nos campos
            entry.insert(0, valores[col])  # Insere o valor nas caixas de entrada

# Função para atualizar a tabela com novos dados
def atualizar_tabela(novos_dados=None):
    # Remove todos os widgets existentes na tabela
    for widget in frame_tabela.winfo_children():
        widget.destroy()
    # Adiciona os títulos das colunas na tabela
    for col, titulo in enumerate(titulos):
        ttk.Label(frame_tabela, text=titulo, bootstyle="inverse-light").grid(row=0, column=col, padx=5, pady=5)
    global dados  # Torna a variável dados acessível dentro da função
    if novos_dados is not None:  # Se novos dados forem passados, atualiza a variável dados
        dados = novos_dados
    # Preenche a tabela com as linhas de dados
    for row, valores in enumerate(dados, start=1):  # Começa da linha 1 para preencher os dados
        criar_linha(row, valores)  # Cria a linha com os dados

# Criação do Frame principal que conterá todos os elementos da interface
tela_frame = ttk.Frame(root, padding=20)  # Define o frame principal com padding de 20px
tela_frame.grid(row=0, column=1, padx=20, pady=20)  # Posiciona o frame na janela principal

# Frame para os botões laterais
frame_botoes = ttk.Frame(root, padding=10)  # Define o frame dos botões com padding de 10px
frame_botoes.grid(row=0, column=0, padx=20, pady=50, sticky="n")  # Posiciona o frame na janela principal

# Criação dos botões
btn_cadastrar_periodo = ttk.Button(frame_botoes, text="Cadastrar Período", bootstyle="secondary")
btn_cadastrar_periodo.grid(row=0, column=0, pady=20, sticky="w")  # Botão para cadastrar período

btn_cadastrar_materia = ttk.Button(frame_botoes, text="Cadastrar Matéria", bootstyle="success")
btn_cadastrar_materia.grid(row=1, column=0, pady=20, sticky="w")  # Botão para cadastrar matéria

btn_adicionar_linha = ttk.Button(frame_botoes, text="Adicionar Linha", bootstyle="info", command=adicionar_linha)
btn_adicionar_linha.grid(row=2, column=0, pady=20, sticky="w")  # Botão para adicionar uma linha na tabela

btn_salvar = ttk.Button(frame_botoes, text="Salvar Alterações", bootstyle="primary", command=salvar_dados)
btn_salvar.grid(row=3, column=0, pady=10)  # Botão para salvar alterações na tabela
btn_salvar.grid_remove()  # Remove o botão inicialmente, ele só aparece quando há mudanças

# Frame para a tabela de notas
frame_tabela = ttk.Frame(root, padding=10)  # Define o frame para a tabela com padding de 10px
frame_tabela.grid(row=0, column=2, padx=20, pady=20, sticky="e")  # Posiciona o frame da tabela na janela

# Definição das listas de títulos, matérias e semestres
titulos = ["Matéria", "Período", "n1", "n2", "n3", "n4"]  # Títulos das colunas da tabela
materias = ["Português", "Matemática", "Ciências", "História", "Educação Física", "Artes", "Inglês"]  # Matérias disponíveis
semestres = ["1", "2", "3", "4"]  # Semestres disponíveis

# Inicializa a tabela com os dados carregados
atualizar_tabela()

# Inicia o loop principal da interface gráfica
root.mainloop()
