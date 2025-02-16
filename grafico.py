import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para criar o gráfico
def criar_grafico(janela):
    # Suponha que dados_notas seja uma lista de dicionários com 'aluno' e 'nota'
    dados_notas = [
        {'aluno': 'João', 'nota': 85},
        {'aluno': 'Maria', 'nota': 92},
        {'aluno': 'Pedro', 'nota': 78},
        {'aluno': 'Ana', 'nota': 88},
    ]

    # Extraindo os dados para plotar
    alunos = [d['aluno'] for d in dados_notas]
    notas = [d['nota'] for d in dados_notas]

    # Criando a figura do gráfico
    fig = Figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.bar(alunos, notas)
    ax.set_xlabel('Alunos')
    ax.set_ylabel('Notas')
    ax.set_title('Notas dos Alunos')

    # Integrando o gráfico na janela TkInter
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Criando a janela TkInter
janela = tk.Tk()
janela.title('Gráfico de Notas')

# Botão para exibir o gráfico
botao_grafico = ttk.Button(janela, text='Exibir Gráfico', command=lambda: criar_grafico(janela))
botao_grafico.pack(side=tk.TOP, pady=10)

# Iniciando o loop da janela
janela.mainloop()