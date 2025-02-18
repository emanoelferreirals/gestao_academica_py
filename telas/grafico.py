import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from funcs import acessar_bd, ler_login, carregar_lista_materias

def exibir_tela(element_pai):
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

    # Função para criar o gráfico de barras comparando as médias das disciplinas
    def criar_grafico(element_pai, dados_notas):
        if not dados_notas:
            print("Nenhum dado de nota encontrado.")
            return
        
        # Extraindo dados para plotar
        materias = list(set([registro['Matéria'] for registro in dados_notas]))
        medias = []
        for materia in materias:
            medias_materia = [float(registro['Média']) for registro in dados_notas if registro['Matéria'] == materia and is_number(registro['Média'])]
            if medias_materia:
                medias.append(sum(medias_materia) / len(medias_materia))
            else:
                medias.append(0)  # Caso não haja médias válidas, define média como 0

        # Criando a figura do gráfico
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.bar(materias, medias, color='skyblue')

        ax.set_xlabel('Matérias')
        ax.set_ylabel('Médias')
        ax.set_title('Comparação das Médias das Disciplinas')
        
        # Integrando o gráfico na element_pai TkInter
        for widget in frame_grafico.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Função auxiliar para verificar se uma string pode ser convertida para número
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # Função para exibir o gráfico ao clicar no botão
    def exibir_grafico():
        dados_notas = buscar_dados_usuario()
        criar_grafico(frame_grafico, dados_notas)

    # Função para limpar o gráfico
    def limpar_grafico():
        for widget in frame_grafico.winfo_children():
            widget.destroy()

    # Configurando o layout da janela principal
    element_pai.grid_rowconfigure(1, weight=1)
    element_pai.grid_columnconfigure(0, weight=1)

    # Frame para o gráfico
    frame_grafico = tk.Frame(element_pai)
    frame_grafico.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

    # Frame para os botões
    frame_botoes = tk.Frame(element_pai)
    frame_botoes.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

    # Botão para exibir o gráfico
    botao_grafico = ttk.Button(frame_botoes, text='Exibir Gráfico', command=exibir_grafico)
    botao_grafico.pack(side=tk.LEFT, padx=5)

    # Botão para limpar o gráfico
    botao_limpar = ttk.Button(frame_botoes, text='Limpar', command=limpar_grafico)
    botao_limpar.pack(side=tk.LEFT, padx=5)

    # Iniciando o loop da element_pai
    element_pai.mainloop()

