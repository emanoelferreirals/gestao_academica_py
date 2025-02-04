from funcs import carregar_dados, salvar_dados
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.constants import *

# Criando a janela principal
style = Style(theme="minty")
root = style.master
root.title("Gestor de Notas")
root.geometry("900x500")
root.resizable(False, False)

# Criando os frames
frame_botoes = tk.Frame(root, padx=10, pady=10)
frame_botoes.grid(row=0, column=0, padx=20, pady=50, sticky="n")

frame_principal = tk.Frame(root, padx=20, pady=20)
frame_principal.grid(row=0, column=1, padx=20, pady=20)

# Adicionando um título para a tabela
label_titulo = tk.Label(frame_principal, text="Notas Acadêmicas", font=("Arial", 14, "bold"))
label_titulo.grid(row=0, column=0, pady=10)

# Criando um Canvas para a tabela
canvas_tabela = tk.Canvas(frame_principal, width=500, height=350)
canvas_tabela.grid(row=1, column=0)

# Criando a Scrollbar vertical
scrollbar_tabela = tk.Scrollbar(frame_principal, orient="vertical", command=canvas_tabela.yview)
scrollbar_tabela.grid(row=1, column=1, sticky="ns")

# Criando um frame dentro do Canvas para a tabela
frame_conteudo_tabela = tk.Frame(canvas_tabela)
canvas_tabela.create_window((0, 0), window=frame_conteudo_tabela, anchor="nw")

# Configurando o Canvas para funcionar com a Scrollbar
canvas_tabela.configure(yscrollcommand=scrollbar_tabela.set)

# Criando botões laterais
btn_cadastrar_periodo = tk.Button(frame_botoes, text="Cadastrar Período", width=20)
btn_cadastrar_periodo.grid(row=0, column=0, pady=10)

btn_cadastrar_materia = tk.Button(frame_botoes, text="Cadastrar Matéria", width=20)
btn_cadastrar_materia.grid(row=1, column=0, pady=10)

btn_adicionar_linha = tk.Button(frame_botoes, text="Adicionar Linha", width=20, command=lambda: adicionar_linha())
btn_adicionar_linha.grid(row=2, column=0, pady=10)

# Botão para salvar alterações
btn_salvar = tk.Button(frame_botoes, text="Salvar Alterações", width=20, command=lambda: salvar())
btn_salvar.grid(row=3, column=0, pady=10)

# Cabeçalhos da tabela
titulos = ["Matéria", "Período", "N1", "N2", "N3", "N4"]
for col, titulo in enumerate(titulos):
    tk.Label(frame_conteudo_tabela, text=titulo, font=("Arial", 10, "bold"), padx=5, pady=5).grid(row=0, column=col)

# Lista de matérias e períodos disponíveis
materias = ["Português", "Matemática", "Ciências", "História", "Educação Física", "Artes", "Inglês"]
semestres = ["1", "2", "3", "4"]

# Função para adicionar uma linha à tabela
def adicionar_linha():
    row = len(frame_conteudo_tabela.winfo_children()) // len(titulos) + 1

    cmb_materia = tk.StringVar(value=" ")
    cmb_periodo = tk.StringVar(value=" ")

    menu_materia = tk.OptionMenu(frame_conteudo_tabela, cmb_materia, *materias)
    menu_materia.config(width=16)
    menu_materia.grid(row=row, column=0, padx=5, pady=5)

    menu_periodo = tk.OptionMenu(frame_conteudo_tabela, cmb_periodo, *semestres)
    menu_periodo.config(width=5)
    menu_periodo.grid(row=row, column=1, padx=5, pady=5)

    for col in range(2, 6):
        tk.Entry(frame_conteudo_tabela, width=5).grid(row=row, column=col, padx=5, pady=5)

    frame_conteudo_tabela.update_idletasks()
    canvas_tabela.configure(scrollregion=canvas_tabela.bbox("all"))

# Função para salvar os dados no JSON
def salvar():
    novos_dados = []
    
    for row in range(1, len(frame_conteudo_tabela.winfo_children()) // len(titulos) + 1):
        
        linha = []
        for col in range(len(titulos)):
            widget = frame_conteudo_tabela.grid_slaves(row=row, column=col)
            if widget:
                if isinstance(widget[0], tk.OptionMenu):  # Se for um menu suspenso
                    var = widget[0].cget("text")  # Obtém o texto selecionado
                    linha.append(var.strip())  # Remove espaços extras
                elif isinstance(widget[0], tk.Entry):  # Se for uma caixa de entrada
                    linha.append(widget[0].get().strip())  # Obtém o valor digitado
        if linha:
            novos_dados.append(linha)

    salvar_dados(novos_dados)  # Salva os dados no JSON

# Adicionando uma linha inicial
adicionar_linha()

# Rodando a interface
root.mainloop()
