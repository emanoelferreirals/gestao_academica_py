import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from funcs import acessar_bd, ler_login, carregar_lista_materias

# Função para buscar dados das notas do usuário
def buscar_dados_usuario():
    usuario = ler_login().get("email")
    if not usuario:
        print("Usuário não está logado.")
        return []
    
    caminho_arquivo = f"data/alunos/{usuario}/notas.json"
    banco = acessar_bd("r", caminho_arquivo)
    
    # Supondo que as notas estão armazenadas na estrutura 'registro_notas'
    return banco.get("registro_notas", [])

# Função para criar o gráfico de evolução das notas para uma matéria específica
def criar_grafico(janela, dados_notas, materia_selecionada):
    if not dados_notas:
        print("Nenhum dado de nota encontrado.")
        return
    
    # Filtrando os dados da matéria selecionada
    materia_dados = [registro for registro in dados_notas if registro['Matéria'] == materia_selecionada]
    
    if not materia_dados:
        print(f"Nenhum dado encontrado para a matéria {materia_selecionada}.")
        return
    
    # Extraindo dados para plotar
    periodos = [f"Período {registro['Período']}" for registro in materia_dados]
    n1 = [int(registro['n1']) for registro in materia_dados]
    n2 = [int(registro['n2']) for registro in materia_dados]
    n3 = [int(registro['n3']) for registro in materia_dados]
    n4 = [int(registro['n4']) for registro in materia_dados]

    # Criando a figura do gráfico
    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.plot(periodos, n1, marker='o', label='N1')
    ax.plot(periodos, n2, marker='o', label='N2')
    ax.plot(periodos, n3, marker='o', label='N3')
    ax.plot(periodos, n4, marker='o', label='N4')

    ax.set_xlabel('Períodos')
    ax.set_ylabel('Notas')
    ax.set_title(f'Evolução das Notas - {materia_selecionada}')
    ax.legend()
    
    # Formatando os períodos no eixo x
    fig.autofmt_xdate()

    # Integrando o gráfico na janela TkInter
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Função para exibir o gráfico ao clicar no botão
def exibir_grafico(materia_selecionada):
    dados_notas = buscar_dados_usuario()
    criar_grafico(janela, dados_notas, materia_selecionada)

# Função para atualizar o gráfico quando uma nova matéria é selecionada
def atualizar_grafico(*args):
    materia_selecionada = var_materia.get()
    exibir_grafico(materia_selecionada)

# Criando a janela TkInter
janela = tk.Tk()
janela.title('Gráfico de Evolução das Notas')

# Carregar a lista de matérias
materias = carregar_lista_materias()

# Variável para armazenar a matéria selecionada
var_materia = tk.StringVar(janela)
var_materia.set(materias[0] if materias else '')

# MenuOption para selecionar a matéria
menu_materias = ttk.OptionMenu(janela, var_materia, materias[0], *materias, command=atualizar_grafico)
menu_materias.pack(side=tk.TOP, pady=10)

# Botão para exibir o gráfico
botao_grafico = ttk.Button(janela, text='Exibir Gráfico', command=lambda: exibir_grafico(var_materia.get()))
botao_grafico.pack(side=tk.TOP, pady=10)

# Iniciando o loop da janela
janela.mainloop()