import json
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

# Configurações da Janela
largura_tela, altura_tela = 900, 500
style = Style(theme="minty")
root = style.master
root.title("Notas")
root.geometry(f"{largura_tela}x{altura_tela}")
root.resizable(False, False)

# Função para salvar dados
def salvar_dados():
    dados = []
    for widgets in frame_tabela.grid_slaves():
        if isinstance(widgets, ttk.Entry) or isinstance(widgets, ttk.Combobox):
            row, col = widgets.grid_info()["row"], widgets.grid_info()["column"]
            if row > 0:
                while len(dados) < row:
                    dados.append(["", "", "", "", "", ""])
                dados[row-1][col] = widgets.get()
    dados.sort(key=lambda x: x[1])
    with open("database/alunos/aluno.json", "w") as f:
        json.dump(dados, f, indent=4)

# Função para adicionar linha
def adicionar_linha():
    row = len(frame_tabela.grid_slaves()) // len(titulos) + 1
    cmb_materia = ttk.Combobox(frame_tabela, values=materias, state="readonly", width=15)
    cmb_materia.grid(row=row, column=0, padx=5, pady=5)
    cmb_periodo = ttk.Combobox(frame_tabela, values=semestres, state="readonly", width=10)
    cmb_periodo.grid(row=row, column=1, padx=5, pady=5)
    for col in range(2, 6):
        ttk.Entry(frame_tabela, width=5).grid(row=row, column=col, padx=5, pady=5)
    salvar_dados()

# Frame principal
tela_frame = ttk.Frame(root, padding=20)
tela_frame.grid(row=0, column=1, padx=20, pady=20)

# Botões laterais
frame_botoes = ttk.Frame(root, padding=10)
frame_botoes.grid(row=0, column=0, padx=20, pady=50, sticky="n")

btn_cadastrar_periodo = ttk.Button(frame_botoes, text="Cadastrar Período", bootstyle="secondary")
btn_cadastrar_periodo.grid(row=0, column=0, pady=20, sticky="w")

btn_cadastrar_materia = ttk.Button(frame_botoes, text="Cadastrar Matéria", bootstyle="success")
btn_cadastrar_materia.grid(row=1, column=0, pady=20, sticky="w")

btn_adicionar_linha = ttk.Button(frame_botoes, text="Adicionar Linha", bootstyle="info", command=adicionar_linha)
btn_adicionar_linha.grid(row=2, column=0, pady=20, sticky="w")

# Tabela de Notas
frame_tabela = ttk.Frame(root, padding=10)
frame_tabela.grid(row=0, column=2, padx=20, pady=20, sticky="e")

# Cabeçalho da tabela
titulos = ["Matéria", "Período", "n1", "n2", "n3", "n4"]
for col, titulo in enumerate(titulos):
    ttk.Label(frame_tabela, text=titulo, bootstyle="inverse-light").grid(row=0, column=col, padx=5, pady=5)

# Linhas da tabela
materias = ["Português", "Matemática", "Ciências", "História", "Educação Física", "Artes", "Inglês"]
semestres = ["1", "2", "3", "4"]

for row in range(1, 8):  # Criando 7 linhas para permitir seleção de qualquer matéria
    ttk.Combobox(frame_tabela, values=materias, state="readonly", width=15).grid(row=row, column=0, padx=5, pady=5)
    ttk.Combobox(frame_tabela, values=semestres, state="readonly", width=10).grid(row=row, column=1, padx=5, pady=5)
    for col in range(2, 6):
        ttk.Entry(frame_tabela, width=5).grid(row=row, column=col, padx=5, pady=5)

root.mainloop()