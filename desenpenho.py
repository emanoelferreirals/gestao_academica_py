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
    
    return banco.get("registro_notas", [])

# Função para obter os períodos disponíveis para uma matéria específica
def obter_periodos_disponiveis(materia, dados_notas):
    return sorted(set(str(registro["Período"]) for registro in dados_notas if registro["Matéria"] == materia))

# Função para criar o gráfico de evolução das notas para uma matéria específica
def criar_grafico(janela, dados_notas, materia_selecionada, periodo_selecionado):
    if not dados_notas:
        print("Nenhum dado de nota encontrado.")
        return

    # Filtra os dados pela matéria selecionada
    materia_dados = [registro for registro in dados_notas if registro["Matéria"] == materia_selecionada]

    # Filtra pelo período, a menos que a opção "Todos" tenha sido escolhida
    if periodo_selecionado != "Todos":
        materia_dados = [registro for registro in materia_dados if str(registro["Período"]) == periodo_selecionado]

    if not materia_dados:
        print(f"Nenhum dado encontrado para {materia_selecionada} no período {periodo_selecionado}.")
        return
    
    periodos = [f"Período {registro['Período']}" for registro in materia_dados]
    n1 = [int(registro['n1']) for registro in materia_dados]
    n2 = [int(registro['n2']) for registro in materia_dados]
    n3 = [int(registro['n3']) for registro in materia_dados]
    n4 = [int(registro['n4']) for registro in materia_dados]

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
    
    fig.autofmt_xdate()

    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, pady=10)

# Função para exibir o gráfico ao clicar no botão
def exibir_grafico():
    materia_selecionada = var_materia.get()
    periodo_selecionado = var_periodo.get()
    dados_notas = buscar_dados_usuario()
    criar_grafico(janela, dados_notas, materia_selecionada, periodo_selecionado)

# Função para atualizar os períodos disponíveis ao trocar a matéria
def atualizar_periodos(*args):
    materia_selecionada = var_materia.get()
    periodos_disponiveis = obter_periodos_disponiveis(materia_selecionada, buscar_dados_usuario())

    # Limpa o menu de período e adiciona novas opções
    menu_periodo['menu'].delete(0, 'end')
    periodos_disponiveis.insert(0, "Todos")  # Opção para mostrar todos os períodos
    for periodo in periodos_disponiveis:
        menu_periodo['menu'].add_command(label=periodo, command=tk._setit(var_periodo, periodo))

    var_periodo.set(periodos_disponiveis[0] if periodos_disponiveis else "Todos")

# Criando a janela TkInter
janela = tk.Tk()
janela.title('Gráfico de Evolução das Notas')

# Carregar a lista de matérias
materias = carregar_lista_materias()

var_materia = tk.StringVar(janela)
var_materia.set(materias[0] if materias else '')

var_periodo = tk.StringVar(janela)
var_periodo.set("Todos")

# Menu de seleção de matérias
menu_materias = ttk.OptionMenu(janela, var_materia, materias[0], *materias, command=atualizar_periodos)
menu_materias.grid(row=0, column=0, padx=10, pady=10)

# Menu de seleção de períodos (inicialmente vazio)
menu_periodo = ttk.OptionMenu(janela, var_periodo, "Todos")
menu_periodo.grid(row=0, column=1, padx=10, pady=10)

# Botão para exibir o gráfico
botao_grafico = ttk.Button(janela, text='Ver Desempenho', command=exibir_grafico)
botao_grafico.grid(row=1, column=0, columnspan=2, pady=10)

# Inicializa os períodos corretamente ao iniciar o programa
atualizar_periodos()

# Variável para armazenar o gráfico
canvas = None

janela.mainloop()
