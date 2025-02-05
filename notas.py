# notas.py
from funcs import carregar_dados, salvar_dados, on_close, acessar_lista
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox  # Para mostrar a janela de aviso

largura_tela = 800
altura_tela = 500

# Criando a janela principal
style = Style(theme="minty")
root = style.master
root.title("Gestor de Notas")
root.geometry(f"{largura_tela}x{altura_tela}")
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
titulos = ["Matéria", "Período", "n1", "n2", "n3", "n4"]
for col, titulo in enumerate(titulos):
    tk.Label(frame_conteudo_tabela, text=titulo, font=("Arial", 10, "bold"), padx=5, pady=5).grid(row=0, column=col)

# Lista de matérias e períodos disponíveis
materias = ["Português", "Matemática", "Ciências", "História", "Educação Física", "Artes", "Inglês"]
semestres = ["1", "2", "3", "4"]

"""-----------------------------MOSTRAR E ESCONDER BOTAO-------------------------"""
# Função para mostrar o botão de salvar
def mostrar_botao_salvar():
    btn_salvar.grid(row=3, column=0, pady=10)  # Tornar o botão visível, colocando-o no layout

# Função para esconder o botão de salvar
def esconder_botao_salvar():
    btn_salvar.grid_forget()  # Esconde o botão removendo-o do layout


"""-----------------------------FUNÇÕES SENSORES----------------------------------"""


"""------------------------GERENCIAMENTO DA TABELA-----------------------------------"""

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


def salvar():
    dados = []  # Lista para armazenar múltiplas linhas

    widgets = frame_conteudo_tabela.winfo_children()
    print(widgets)

    # Mapear colunas pelos títulos
    titulos = ["Matéria", "Período", "n1", "n2", "n3", "n4"]  # Ajuste conforme sua tabela

    # Dicionário temporário para armazenar uma linha completa
    dados_por_linha = {}

    linha_atual = -1  # Variável para rastrear mudanças de linha

    for widget in widgets:
        info = widget.grid_info()
        row = info["row"]
        col = info["column"]

        if col >= len(titulos):
            continue

        coluna_nome = titulos[col]  # Nome da coluna com base no índice

        # Se mudamos de linha, salvamos a anterior e iniciamos uma nova
        if row != linha_atual:
            if dados_por_linha:  # Salva a linha anterior (se houver)
                dados.append(dados_por_linha)
            dados_por_linha = {}  # Reseta para uma nova linha
            linha_atual = row  # Atualiza a linha atual

        if isinstance(widget, tk.OptionMenu):
            var_name = widget.cget("textvariable")
            valor = widget.getvar(var_name).strip()

            if valor == "":
                Messagebox.ok("Os campos de matéria e período não podem estar vazios!")
                return

        elif isinstance(widget, tk.Entry):
            valor = widget.get().strip()

        else:
            continue

        # Converter valores numéricos
        if coluna_nome == "Período" or coluna_nome.startswith("N"):
            try:
                valor = valor
            except ValueError:
                valor = 0  # Caso esteja vazio ou inválido

        # Adicionar o valor ao dicionário da linha atual
        dados_por_linha[coluna_nome] = valor

    # Salvar a última linha capturada
    if dados_por_linha:
        dados.append(dados_por_linha)

    print("Dados capturados:", dados)
    salvar_dados(dados)
    preencher_tabela()
    Messagebox.ok("Alterações feitas com sucesso!", "Aviso")



def preencher_tabela():
    dados = carregar_dados()

    # Ordenar os dados pelo valor do período (menor para maior)
    dados_ordenados = sorted(dados, key=lambda x: int(x.get("Período", 0))) 

    # Limpar a tabela existente
    for widget in frame_conteudo_tabela.winfo_children():
        widget.destroy()

    # Recriar os cabeçalhos
    for col, titulo in enumerate(titulos):
        tk.Label(frame_conteudo_tabela, text=titulo, font=("Arial", 10, "bold"), padx=5, pady=5).grid(row=0, column=col)

    # Preencher as linhas com os dados carregados e ordenados
    for row, dado in enumerate(dados_ordenados, start=1):
        cmb_materia = tk.StringVar(value=dado.get("Matéria", ""))
        cmb_periodo = tk.StringVar(value=dado.get("Período", ""))

        menu_materia = tk.OptionMenu(frame_conteudo_tabela, cmb_materia, *materias)
        menu_materia.config(width=16)
        menu_materia.grid(row=row, column=0, padx=5, pady=5)

        menu_periodo = tk.OptionMenu(frame_conteudo_tabela, cmb_periodo, *semestres)
        menu_periodo.config(width=5)
        menu_periodo.grid(row=row, column=1, padx=5, pady=5)

        for col, titulo in enumerate(titulos[2:], start=2):  # Começa a preencher as notas
            tk.Entry(frame_conteudo_tabela, width=5, textvariable=tk.StringVar(value=dado[titulo.lower()])).grid(row=row, column=col, padx=5, pady=5)

    frame_conteudo_tabela.update_idletasks()
    canvas_tabela.configure(scrollregion=canvas_tabela.bbox("all"))


# Esconder botão de salvar alterações
mostrar_botao_salvar()

# Adicionando uma linha inicial
adicionar_linha()

# Carregar os dados e preencher a tabela ao iniciar a interface
preencher_tabela()

# Vinculando a função on_close ao evento de fechar a janela
root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))  # Chamando a função on_close

# Rodando a interface
root.mainloop()
